# pdf2sb

![PyPI](https://img.shields.io/pypi/v/pdf2sb.svg) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pdf2sb.svg) ![PyPI - License](https://img.shields.io/pypi/l/pdf2sb.svg)

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

- [poppler](https://poppler.freedesktop.org/) is required to generate images from a PDF file. Install poppler via Homebrew:

```sh
brew install poppler
```

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
FILE=<your pdf file>; docker run --env GYAZO_ACCESS_TOKEN=$GYAZO_ACCESS_TOKEN -v $(readlink -f $FILE):/app/${FILE##*/} ghcr.io/reiyw/pdf2sb ${FILE##*/}
# or
docker run --env GYAZO_ACCESS_TOKEN=$GYAZO_ACCESS_TOKEN ghcr.io/reiyw/pdf2sb <URL>
```
