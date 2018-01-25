FROM ubuntu:16.04
MAINTAINER Sergey Nikulin "s.nikulin@pr-solition"
ADD . /srv/telegram_is
WORKDIR /srv/telegram_is
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential libpq-dev iputils-ping
RUN pip3 install -r requirements.txt
ENV TZ=Europe/Moscow
ENV LANG C.UTF-8
#CMD ./manage.py run
