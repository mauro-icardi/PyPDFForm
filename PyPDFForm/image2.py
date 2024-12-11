from io import BytesIO
from typing import Union

from PIL import Image
def any_image_to_jpg(image_stream: bytes) -> bytes:
    """Converts an image of any type to jpg."""

    buff = BytesIO()
    buff.write(image_stream)
    buff.seek(0)

    image = Image.open(buff)

    if image.format == "JPEG":
        buff.close()
        return image_stream

    rgb_image = Image.new("RGB", image.size, (255, 255, 255))
    rgb_image.paste(image, mask=image.split()[3] if len(image.split()) == 4 else None)

    with BytesIO() as _file:
        rgb_image.save(_file, format="JPEG")
        _file.seek(0)
        result = _file.read()

    buff.close()
    return result