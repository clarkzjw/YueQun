FROM python:3
LABEL MAINTAINER=clarkzjw<hello@jinwei.me>

ENV TZ Asia/Shanghai

ADD requirements.txt /yqbot/requirements.txt

WORKDIR /yqbot

RUN pip install -r requirements.txt

ADD . /yqbot
