FROM python:3.11-slim

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install uv==0.7.11 \
    && uv pip sync requirements.lock

ENTRYPOINT ["pdf2sb"]
