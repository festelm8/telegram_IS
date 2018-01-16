import datetime
from flask import g
from flask_restful import Resource
from webargs.flaskparser import use_args

from src.db import db
from src.db.models import User, Stream, Listeners
from src.lib.access import user_only, validate_uuid
from src.schemas.statistic import statistic_get


class StatisticAPI(Resource):
    @user_only()
    @use_args(statistic_get)
    def get(self, data, stream_id):
        if not stream_id or not validate_uuid(stream_id):
            return {
                "message": "stream not selected"
            }, 422

        stream = Stream.query.filter_by(id=str(stream_id)).first()
        if not stream:
            return {
                       "message": "no such stream"
                   }, 404

        # if time range not selected, show listeners for current day
        date_from = datetime.datetime.now()
        if data.get('when'):
            date_from = datetime.datetime.fromtimestamp(int(data.get('when')))

        date_to = date_from + datetime.timedelta(days=1)


        listeners = stream.listeners.filter(Listeners.created_at.between(date_from.date(), date_to.date())).order_by(Listeners.created_at).all()

        if not listeners:
            return {
                "message": "couldn't find statistic for this day"
            }, 404

        return {
            'stream_name': stream.name,
            'selected_date': date_from.strftime('%Y-%m-%d'),
            'checkpoints': [
                {
                    'song': checkpoint.song,
                    'connections': checkpoint.connections,
                    'created_at': checkpoint.created_at.isoformat() if checkpoint.created_at else None
                }
                for checkpoint in listeners]
        }





