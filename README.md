# pdf2sb

Upload PDF file to Gyazo as images then convert Scrapbox format.

## Usage

Download slides (e.g. https://speakerdeck.com/reiyw/effective-modern-python-2018).
Run:

```sh
pdf2sb ~/Downloads/presentation.pdf | pbcopy
```

Paste copied text to a Scrapbox page:

[![Image from Gyazo](https://i.gyazo.com/0417c51246c401de8725393d7c78f715.png)](https://gyazo.com/0417c51246c401de8725393d7c78f715)

## Installation

- Install pdf2sb:

```sh
pip install pdf2sb
```

- Get Gyazo access token from [here](https://gyazo.com/oauth/applications).
    - Follow the instructions in [this article (in Japanese)](https://blog.naichilab.com/entry/gyazo-access-token).
- Set `$GYAZO_ACCESS_TOKEN`:

```sh
export GYAZO_ACCESS_TOKEN=<access token>
```

## Running via Docker

You can run pdf2sb also via Docker:

```sh
FILE=<your pdf file>; docker run --env GYAZO_ACCESS_TOKEN=$GYAZO_ACCESS_TOKEN -v $(readlink -f $FILE):/app/${FILE##*/} reiyw/pdf2sb ${FILE##*/}
# or
docker run --env GYAZO_ACCESS_TOKEN=$GYAZO_ACCESS_TOKEN reiyw/pdf2sb <URL>
```
