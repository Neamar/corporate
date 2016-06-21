from io import BytesIO
from PIL import Image, ImageDraw, ImageOps

from django.core.files.base import ContentFile

from stdimage.utils import render_variations


def preprocess(file_name, variations, storage):
    with storage.open(file_name) as f:
        with Image.open(f) as image:
            file_format = 'PNG'

            # resize to a maximum of 1000x1000 keeping aspect ratio
            image.thumbnail((1000, 1000), resample=Image.ANTIALIAS)

            # Create a disk as mask
            mindimension = min(1000, image.size[1], image.size[0])
            bigsize = (mindimension * 3, mindimension * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize((mindimension, mindimension), Image.ANTIALIAS)

            # only keep the image that fit in the mask
            output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)

            with BytesIO() as file_buffer:
                output.save(file_buffer, file_format)
                f = ContentFile(file_buffer.getvalue())
                # delete the original big image
                storage.delete(file_name)
                # save the resized version with the same filename and format
                storage.save(file_name, f)

    # render stdimage variations
    render_variations(file_name, variations, replace=True, storage=storage)

    return False  # prevent default rendering
