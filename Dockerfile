FROM python:3.12
LABEL authors="BigBlackBob"

WORKDIR /src
COPY ./poetry.lock ./pyproject.toml ./

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get upgrade -y

RUN pip3 install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root --no-directory --no-cache

COPY . .