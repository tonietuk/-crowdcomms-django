FROM python:3.9-buster

WORKDIR /opt/app

RUN apt-get -y update && apt-get -y upgrade

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --with=dev

COPY . /opt/app/