import requests
import html
import re
import time
from datetime import datetime
from flask import current_app

from src.db import db, rq
from src.db.models import Stream, Listeners, Cdn


@rq.job
def streams_list_checker():
    cdns = Cdn.query.filter_by(is_active=True).all()
    if not cdns:
        print('* Cdns not finded')
        return False

    for cdn in cdns:
        certain_cdn_check(cdn)


def certain_cdn_check(cdn):
    statistic_url = 'http://api.cdnvideo.ru:8888/0/streams?id={access_id}'.format(**dict(
        access_id=cdn.access_id
    ))
    statistic = requests.get(statistic_url)
    if not statistic.ok:
        print('* (FAIL) Cant recieve source statistic for cdn "{cdn}"'.format(**dict(
            cdn=cdn.name
        )))
        return False

    if not cdn.streams.count():
        print('* (FAIL) Streams not finded for cdn "{cdn}"'.format(**dict(
            cdn=cdn.name
        )))
        return False

    for stream in cdn.streams:
        certain_stream_check(statistic.json()['streams'], stream)


def certain_stream_check(statistic, stream):
    connections = count_source_connections(statistic, stream.source_list)

    main_source = stream.main_source
    source_meta_url = '{sources_domain}{source_name}'.format(**dict(
        sources_domain=stream.cdn.sources_domain,
        source_name=main_source.name
    ))
    song_name = get_song_name(source_meta_url, tries=current_app.config['GET_SONG_TRIES'], ttl=current_app.config['TTL_IF_NO_SONG'])

    if not connections:
        print('* (FAIL) Cant recieve source statistic for "{stream}"'.format(**dict(
            stream=stream.name
        )))
        return False

    stream.listeners.append(
        Listeners(
            song=song_name,
            connections=connections
        )
    )
    db.session.commit()

    print('* (SUCCESS) Make checkpoint for "{stream}" at {datetime}'.format(**dict(
        stream=stream.name,
        datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )))


def get_song_name(source_meta_url, tries, ttl):
    result = None
    while not result and tries > 0:
        tries -= 1
        try:
            source_meta = requests.get(
                source_meta_url,
                stream=True,
                headers={'Icy-MetaData': '1'})
        except requests.exceptions.ConnectionError:
            print('(!) Cant connect to source stream data, will try again after '+str(ttl)+' seconds')
            time.sleep(ttl)
            continue

        if not source_meta.ok:
            print('(!) Client error on recieve source stream data')
            break

        icy_metaint_header = source_meta.headers.get('icy-metaint')
        if icy_metaint_header is None:
            print('(!) Not found meta-data in source')
            break

        metaint = int(icy_metaint_header)
        read_buffer = metaint + 1024
        content = source_meta.iter_content(read_buffer).__next__()
        result = html.unescape(str(content[metaint:].split(b"'")[1], 'utf-8'))
        # Срезаем из потока метки времени типа [0:08],
        result = re.sub(r'\[\d{1,2}:\d{1,2}\]', '', result)
        # строку + JINGLE, и боковые пробелы
        result = result.replace('+ JINGLE', '').strip()
        if not result:
            # print('(!) No music playing at now, will try again after '+str(ttl)+' seconds')
            time.sleep(ttl)

    if not result:
        result = current_app.config['NO_SONG_NAME']
        # print('(!) Cant recieve information about song')
    return result


def count_source_connections(statistic, sources):
    connections = 0
    for source in sources:
        if source in statistic:
            connections += statistic[source]['sessionsTotal']

    return connections






