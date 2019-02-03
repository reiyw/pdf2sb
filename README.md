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

```sh
pip install pdf2sb
```

Get Gyazo access token from [here](https://gyazo.com/oauth/applications).

Set `$GYAZO_ACCESS_TOKEN`:

```sh
export GYAZO_ACCESS_TOKEN=<access token>
```
