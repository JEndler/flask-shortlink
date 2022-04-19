FROM python:3

RUN mkdir /app

WORKDIR /app

ADD . /app

RUN pip install poetry

RUN poetry install

EXPOSE 8019

CMD poetry run gunicorn -w 2 -b 127.0.0.1:8019 wsgi:app