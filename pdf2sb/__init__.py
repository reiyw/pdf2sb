import tempfile
from pathlib import Path
from typing import List

import click
import gyazo
from PIL.Image import Image
from pdf2image import convert_from_path
from tqdm import tqdm

__version__ = "0.2.0"


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
def main(filepath: str, token: str, dpi: int) -> None:
    """Upload PDF file to Gyazo as images then convert Scrapbox format."""
    client = gyazo.Api(access_token=token)
    urls = []
    with tempfile.TemporaryDirectory() as tempdir:
        images: List[Image] = convert_from_path(filepath, dpi=dpi, fmt="png")
        tempdir_p = Path(tempdir)
        for i, img in enumerate(tqdm(images, desc="Uploading")):
            img_path = tempdir_p / f"{i}.png"
            img.save(img_path)
            gyazoimg = client.upload_image(img_path.open("rb"))
            urls.append(gyazoimg.to_dict()["permalink_url"])
    print(*(f"> [{url}]\n" for url in urls), sep="\n")


if __name__ == "__main__":
    main()
