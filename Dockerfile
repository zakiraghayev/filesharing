FROM python:3.7-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0


RUN python -m pip install --upgrade pip

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps
# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# collect static files
RUN python manage.py collectstatic --noinput

# add and run as non-root user
# RUN adduser -D myuser
# USER myuser

WORKDIR /django
ADD . /django

COPY . .