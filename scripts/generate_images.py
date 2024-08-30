import os
from pathlib import Path

from PIL import Image

PREVIEW_SIZE = 1000, 310
COVER_SIZE = 300, 1000

INPUT_DIR = "images_input"
OUTPUT_DIR = "images_generated"


def generate(base_dir: Path):
    input_dir = base_dir / INPUT_DIR
    output_dir = base_dir / OUTPUT_DIR

    input_images = os.listdir(input_dir)

    for image_name in input_images:

        out_name = lambda suffix: os.path.splitext(image_name)[0] + suffix + ".webp"

        out_preview = output_dir / out_name("_preview")
        out_cover = output_dir / out_name("_cover")
        image_name = input_dir / image_name

        try:
            im = Image.open(image_name)
            im.convert("RGBA")
            preview_image = im.copy()
            cover_image = im.copy()

            preview_image.thumbnail(PREVIEW_SIZE, Image.Resampling.LANCZOS)
            cover_image.thumbnail(COVER_SIZE, Image.Resampling.LANCZOS)
            preview_image.save(out_preview, "WEBP", quality=95)
            cover_image.save(out_cover, "WEBP", quality=95)
        except IOError:
            print("cannot create thumbnail for '%s'" % image_name)


if __name__ == "__main__":

    base_dir = Path(__file__).resolve()
    generate(base_dir)
