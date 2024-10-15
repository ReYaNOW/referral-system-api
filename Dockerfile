FROM python:3.12-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.2.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

WORKDIR /usr/local/src/referral_system


RUN useradd -m noroot
RUN chown -R noroot:noroot /usr/local/src/referral_system

RUN apt-get update && apt-get install -y make
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY . .
USER noroot
