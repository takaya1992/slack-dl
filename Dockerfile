FROM python:3.7 AS base

RUN apt-get update -y \
    && apt-get install -y python3.7-dev \
    && apt-get clean autoclean \
    && apt-get autoremove -y

RUN pip install virtualenv pipenv

ENV PIPENV_VENV_IN_PROJECT=true

WORKDIR /app
