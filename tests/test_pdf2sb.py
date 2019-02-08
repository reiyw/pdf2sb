import pytest

from pdf2sb import __version__, parse_range


def test_version() -> None:
    assert __version__ == "0.3.0"


def test_parse_range() -> None:
    assert list(parse_range("1-9,12, 15-20,23")) == [
        (1, 9),
        (12, 12),
        (15, 20),
        (23, 23),
    ]
    with pytest.raises(ValueError):
        list(parse_range("1-9,12, 15-20,2-3-4"))
