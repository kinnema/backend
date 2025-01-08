FROM ultrafunk/undetected-chromedriver:latest

RUN apt update -y && apt install google-chrome-stable -y

RUN pip install poetry

WORKDIR /code

COPY . /code

RUN poetry install

RUN poetry run alembic upgrade head