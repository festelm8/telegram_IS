FROM ubuntu:16.04
MAINTAINER Sergey Nikulin "s.nikulin@pr-solition"
ADD . /srv/rr-logs
WORKDIR /srv/rr-logs
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential libpq-dev iputils-ping
RUN pip3 install -r requirements.txt
ENV TZ=Europe/Moscow
ENV LANG C.UTF-8
#CMD ./manage.py run
