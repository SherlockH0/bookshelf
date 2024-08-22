import os

from PIL import Image

PREVIEW_SIZE = 1000, 310
COVER_SIZE = 300, 1000

INPUT_DIR = "images_input"
OUTPUT_DIR = "images_generated"

input_images = os.listdir(INPUT_DIR)


for image_name in input_images:
    out_name = (
        lambda suffix: os.path.splitext(image_name)[0]
        + suffix
        + os.path.splitext(image_name)[1]
    )
    out_preview = os.path.join(OUTPUT_DIR, out_name("_preview"))
    out_cover = os.path.join(OUTPUT_DIR, out_name("_cover"))
    image_name = os.path.join(INPUT_DIR, image_name)
    try:
        im = Image.open(image_name)
        im.convert("RGBA")
        preview_image = im.copy()
        cover_image = im.copy()

        preview_image.thumbnail(PREVIEW_SIZE, Image.Resampling.LANCZOS)
        cover_image.thumbnail(COVER_SIZE, Image.Resampling.LANCZOS)
        preview_image.save(out_preview, "JPEG", quality=95)
        cover_image.save(out_cover, "JPEG", quality=95)
    except IOError:
        print("cannot create thumbnail for '%s'" % image_name)
