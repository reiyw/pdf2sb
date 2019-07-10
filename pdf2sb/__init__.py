import tempfile
from itertools import chain
from pathlib import Path
from typing import List, Iterator, Optional

import PyPDF2
import click
import gyazo
from PIL.Image import Image
from pdf2image import convert_from_path

__version__ = "0.3.5"


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


def extract_links_from_pdf(
    pdf_file: str, pages: Optional[List[int]] = None
) -> Iterator[List[str]]:
    # Mostly from https://stackoverflow.com/a/56299671
    pdf = PyPDF2.PdfFileReader(open(pdf_file, "rb"))
    annots = "/Annots"
    uri = "/URI"
    ank = "/A"
    for page in range(pdf.getNumPages()):
        if pages is not None and page not in pages:
            continue

        links = []
        pageobj = pdf.getPage(page).getObject()
        if annots in pageobj.keys():
            ann = pageobj[annots]
            for a in ann:
                u = a.getObject()
                if uri in u[ank].keys():
                    links.append(u[ank][uri])
        yield links


def build_scrapbox_repr(
    gyazo_urls: List[str],
    expand: bool,
    n_spaces: int,
    links: Optional[List[List[str]]] = None,
) -> str:
    if links is None:
        links = [[]] * len(gyazo_urls)

    blocks = []
    for gyazo_url, links_per_page in zip(gyazo_urls, links):
        block = []
        if expand:
            block.append(f"> [[{gyazo_url}]]\n")
        else:
            block.append(f"> [{gyazo_url}]\n")
        for link in links_per_page:
            block.append(f" {link}\n")
        block.append("\n" * n_spaces)
        blocks.append("".join(block))

    return "".join(blocks)


def pdf2sb(
    pdf_file: str,
    gyazo_access_token: str,
    dpi: int = 100,
    n_spaces: int = 1,
    expand: bool = False,
    pages: Optional[str] = None,
    extract_links: bool = False,
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

    if pages is not None:
        # "1-4,6" --> [1, 2, 3, 4, 6]
        pages = list(
            chain.from_iterable(
                range(start, end + 1) for start, end in parse_range(pages)
            )
        )

    links = extract_links_from_pdf(pdf_file, pages) if extract_links else None

    sb_repr = build_scrapbox_repr(
        gyazo_urls=urls, expand=expand, n_spaces=n_spaces, links=links
    )
    return sb_repr


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
@click.option("--extract-links/--no-extract-links", "-l/-L", default=True)
def main(
    filepath: str,
    token: str,
    dpi: int,
    spaces: int,
    pages: Optional[str],
    expand: bool,
    extract_links: bool,
) -> None:
    click.echo(
        pdf2sb(
            pdf_file=filepath,
            gyazo_access_token=token,
            dpi=dpi,
            n_spaces=spaces,
            expand=expand,
            pages=pages,
            extract_links=extract_links,
        ),
        nl=False,
    )


if __name__ == "__main__":
    main()
