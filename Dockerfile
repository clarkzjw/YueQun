FROM python:3
LABEL MAINTAINER=clarkzjw<hello@jinwei.me>

RUN pip install --upgrade pipenv

ADD Pipfile.lock /app/Pipfile.lock

ADD Pipfile /app/Pipfile

WORKDIR /app

RUN pipenv sync

ADD . /app

