FROM python:3.11.9-slim

WORKDIR /app

ADD requirements.txt /app

RUN pip install -r requirements.txt

ADD src /app
