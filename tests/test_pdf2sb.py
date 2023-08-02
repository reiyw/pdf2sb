import re
from pathlib import Path
from unittest import mock
import uuid

import gyazo
import pytest

from pdf2sb import __version__, parse_range, pdf2sb


def test_version() -> None:
    assert __version__ == "0.3.9"


def test_parse_range() -> None:
    assert list(parse_range("1-9,12, 15-20,23")) == [
        (1, 9),
        (12, 12),
        (15, 20),
        (23, 23),
    ]
    with pytest.raises(ValueError):
        list(parse_range("1-9,12, 15-20,2-3-4"))


def _make_dummy_upload_image_response(_file):
    image_id = str(uuid.uuid4()).replace("-", "")
    permalink_url = f"https://gyazo.com/{image_id}"
    return gyazo.Image(
        permalink_url=permalink_url, created_at=None, thumb_url=None, type=None
    )


def test_pdf2sb(mocker) -> None:
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
