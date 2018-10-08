FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1


RUN mkdir /project
WORKDIR /project
COPY ./ .

RUN apk --update --upgrade add --no-cache --virtual .build-dep \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    && pip install poetry && poetry install --no-dev

ENV FLASK_APP=coffee_shop/app.py
ENV FLASK_ENV=production

CMD poetry run flask run

