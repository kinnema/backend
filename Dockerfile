FROM ultrafunk/undetected-chromedriver:latest

RUN pip install poetry

WORKDIR /code

COPY . /code

RUN poetry install
