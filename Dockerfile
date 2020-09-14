FROM python:3.7

ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

COPY . .

RUN apt-get update && \
    apt-get install poppler-utils -y && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    poetry install && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["poetry", "run", "pdf2sb"]