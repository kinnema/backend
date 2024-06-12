FROM python:latest

RUN pip install poetry

WORKDIR /code

COPY . /code

RUN poetry install
