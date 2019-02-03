import os
import sys
import tempfile
from pathlib import Path
from typing import List

import gyazo
from PIL.Image import Image
from pdf2image import convert_from_path

__version__ = "0.1.0"


def main() -> None:
    client = gyazo.Api(access_token=os.getenv("GYAZO_ACCESS_TOKEN"))
    urls = []
    with tempfile.TemporaryDirectory() as tempdir:
        images: List[Image] = convert_from_path(sys.argv[1], dpi=100, fmt="png")
        tempdir_p = Path(tempdir)
        for i, img in enumerate(images):
            img_path = tempdir_p / f"{i}.png"
            img.save(img_path)
            gyazoimg = client.upload_image(img_path.open("rb"))
            urls.append(gyazoimg.to_dict()["permalink_url"])
    print(*(f"[{url}]" for url in urls), sep="\n")


if __name__ == "__main__":
    main()
