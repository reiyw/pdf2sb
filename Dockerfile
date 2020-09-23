FROM python:3.7-slim

COPY . /app

WORKDIR /app

RUN apt-get update && \
    apt-get install poppler-utils -y && \
    pip install poetry && \
    poetry install && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["poetry", "run", "pdf2sb"]