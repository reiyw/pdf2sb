import os
import re
from pathlib import Path

import pytest

from pdf2sb import __version__, parse_range, pdf2sb


def test_version() -> None:
    assert __version__ == "0.3.4"


def test_parse_range() -> None:
    assert list(parse_range("1-9,12, 15-20,23")) == [
        (1, 9),
        (12, 12),
        (15, 20),
        (23, 23),
    ]
    with pytest.raises(ValueError):
        list(parse_range("1-9,12, 15-20,2-3-4"))


def test_pdf2sb() -> None:
    pdf_file = str(Path(__file__).resolve().parent / "slides.pdf")
    gyazo_access_token = os.getenv("GYAZO_ACCESS_TOKEN")

    sb_repr = pdf2sb(
        pdf_file=pdf_file, gyazo_access_token=gyazo_access_token, dpi=50, n_spaces=1
    )
    assert (
        re.match(
            r"> \[[^\]]+\]\n{2}> \[[^\]]+\]\n{2}> \[[^\]]+\]\n{2}> \[[^\]]+\]\n{2}",
            sb_repr,
        )
        is not None
    )

    sb_repr = pdf2sb(
        pdf_file=pdf_file, gyazo_access_token=gyazo_access_token, dpi=50, n_spaces=4
    )
    assert (
        re.match(
            r"> \[[^\]]+\]\n{5}> \[[^\]]+\]\n{5}> \[[^\]]+\]\n{5}> \[[^\]]+\]\n{5}",
            sb_repr,
        )
        is not None
    )
