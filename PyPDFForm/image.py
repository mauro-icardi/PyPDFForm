# -*- coding: utf-8 -*-
"""Contains helper for rotating images."""

from io import BytesIO
from typing import Union

from PIL import Image

def rotate_image(image_stream: bytes, rotation: Union[float, int]) -> bytes:
    """Rotates an image by a specified rotation angle.

    Args:
        image_stream (bytes): The input image as a byte stream.
        rotation (Union[float, int]): The angle to rotate the image (in degrees).

    Returns:
        bytes: The rotated image as a byte stream.

    Raises:
        ValueError: If the input is not a valid image.
    """
    buff = BytesIO()
    buff.write(image_stream)
    buff.seek(0)

    image = Image.open(buff)

    rotated_buff = BytesIO()
    image.rotate(rotation, expand=True).save(rotated_buff, format=image.format)
    rotated_buff.seek(0)

    result = rotated_buff.read()

    buff.close()
    rotated_buff.close()

    return result
