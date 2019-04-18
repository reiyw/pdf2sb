import tempfile
from itertools import chain
from pathlib import Path
from typing import List, Iterator, Optional

import click
import gyazo
from PIL.Image import Image
from pdf2image import convert_from_path

__version__ = "0.3.3"


def parse_range(expr: str) -> Iterator[int]:
    """Yield start and end integer pairs from a complex range string like "1-9,12, 15-20,23".

    >>> list(parse_range("1-9,12, 15-20,23"))
    [(1, 9), (12, 12), (15, 20), (23, 23)]

    >>> list(parse_range("1-9,12, 15-20,2-3-4"))
    Traceback (most recent call last):
        ...
    ValueError: format error in 2-3-4
    """
    for x in expr.split(","):
        elem = x.split("-")
        if len(elem) == 1:  # a number
            yield int(elem[0]), int(elem[0])
        elif len(elem) == 2:  # a range inclusive
            yield int(elem[0]), int(elem[1])
        else:  # more than one hyphen
            raise ValueError(f"format error in {x}")


def pdf2sb(
    pdf_file: str,
    gyazo_access_token: str,
    dpi: int = 100,
    n_spaces: int = 1,
    expand: bool = False,
    pages: Optional[str] = None,
) -> str:
    """Upload PDF file to Gyazo as images then convert to Scrapbox format."""
    client = gyazo.Api(access_token=gyazo_access_token)
    urls = []
    with tempfile.TemporaryDirectory() as tempdir:
        if pages is None:
            images: List[Image] = convert_from_path(pdf_file, dpi=dpi, fmt="png")
        else:
            images: List[Image] = list(
                chain.from_iterable(
                    convert_from_path(
                        pdf_file, dpi=dpi, fmt="png", first_page=first, last_page=last
                    )
                    for first, last in parse_range(pages)
                )
            )
        tempdir_p = Path(tempdir)
        with click.progressbar(images, label="Uploading") as bar:
            for i, img in enumerate(bar):
                img_path = tempdir_p / f"{i}.png"
                img.save(img_path)
                gyazoimg = client.upload_image(img_path.open("rb"))
                urls.append(gyazoimg.to_dict()["permalink_url"])
    if expand:
        return "".join(f"> [[{url}]]\n" + "\n" * n_spaces for url in urls)
    else:
        return "".join(f"> [{url}]\n" + "\n" * n_spaces for url in urls)


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option(
    "-t",
    "--token",
    envvar="GYAZO_ACCESS_TOKEN",
    help="Access token for Gyazo. If not specified, use $GYAZO_ACCESS_TOKEN.",
)
@click.option(
    "-d", "--dpi", default=100, show_default=True, help="DPI of generating images."
)
@click.option(
    "-s",
    "--spaces",
    default=1,
    show_default=True,
    help="Number of spaces after images.",
)
@click.option("-p", "--pages", help="PDF pages to upload.")
@click.option("-e", "--expand", is_flag=True)
def main(
    filepath: str, token: str, dpi: int, spaces: int, pages: Optional[str], expand: bool
) -> None:
    click.echo(
        pdf2sb(
            pdf_file=filepath,
            gyazo_access_token=token,
            dpi=dpi,
            n_spaces=spaces,
            expand=expand,
            pages=pages,
        ),
        nl=False,
    )


if __name__ == "__main__":
    main()
