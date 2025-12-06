FROM python:3.12-slim AS base

ENV PYTHONDOWNTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIF /app

RUN apt-get update && apt-get install -y --no-install-recomends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

RUN useradd -m appuser
USER appuser

EXPOSE 5000

ARG APP_VERSION=0.0.0
ARG GIT_COMMIT=unknown
ENV APP_VERSION=${APP_VERSION}
ENV GIT_COMMIT=${GIT_COMMIT}

WORKDIR /app/app

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
