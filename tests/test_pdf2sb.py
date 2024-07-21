import re
from pathlib import Path
from typing import IO
from unittest import mock
import uuid

import gyazo
import pytest
from pytest_httpserver import HTTPServer
from pytest_mock import MockerFixture

from pdf2sb import __version__, parse_range, pdf2sb, download_pdf


def test_version() -> None:
    assert __version__ == "0.3.11"


def test_parse_range() -> None:
    assert list(parse_range("1-9,12, 15-20,23")) == [
        (1, 9),
        (12, 12),
        (15, 20),
        (23, 23),
    ]
    with pytest.raises(ValueError):
        list(parse_range("1-9,12, 15-20,2-3-4"))


def test_download_pdf(httpserver: HTTPServer) -> None:
    with open(Path(__file__).parent / "slides.pdf", "rb") as f:
        pdf_bytes = f.read()

    httpserver.expect_request("/").respond_with_data(pdf_bytes)

    downloaded_path = download_pdf(httpserver.url_for("/"))
    with open(downloaded_path, "rb") as f:
        assert f.read() == pdf_bytes


def _make_dummy_upload_image_response(_file: IO[bytes]) -> gyazo.Image:
    image_id = str(uuid.uuid4()).replace("-", "")
    permalink_url = f"https://gyazo.com/{image_id}"
    return gyazo.Image(
        permalink_url=permalink_url, created_at=None, thumb_url=None, type=None
    )


def test_pdf2sb(mocker: MockerFixture) -> None:
    pdf_file = str(Path(__file__).resolve().parent / "slides.pdf")

    mock_api = mocker.patch("gyazo.Api")
    mock_client = mock.Mock()
    mock_client.upload_image.side_effect = _make_dummy_upload_image_response
    mock_api.return_value = mock_client

    sb_repr = pdf2sb(
        url_or_filepath=pdf_file,
        gyazo_access_token="dummy-token",
        dpi=50,
        n_spaces=1,
    )
    mock_api.assert_called_with(access_token="dummy-token")
    assert (
        re.match(
            r"> \[[^\]]+\]\n{2}> \[[^\]]+\]\n{2}> \[[^\]]+\]\n{2}> \[[^\]]+\]\n{2}",
            sb_repr,
        )
        is not None
    )

    sb_repr = pdf2sb(
        url_or_filepath=pdf_file,
        gyazo_access_token="dummy-token",
        dpi=50,
        n_spaces=4,
    )
    assert (
        re.match(
            r"> \[[^\]]+\]\n{5}> \[[^\]]+\]\n{5}> \[[^\]]+\]\n{5}> \[[^\]]+\]\n{5}",
            sb_repr,
        )
        is not None
    )
