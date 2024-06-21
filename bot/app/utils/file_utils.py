import imghdr
import os
from typing import BinaryIO


def is_image(file: BinaryIO) -> bool:
    """
    Check if the given file is an image file.
    Args:
        file (BinaryIO): The file object to check.
    Returns:
        bool: True if the file is a JPEG or JPG image, False otherwise.
    """
    file_type = imghdr.what(file)
    return file_type in ["jpeg", "jpg"]


def get_size(file: BinaryIO):
    """
    Get the size of a file.
    Args:
        file (BinaryIO): The file object to get the size of.
    Returns:
        int: The size of the file in bytes.
    This function takes a file object as input and returns the size of the file in bytes. It does
    this by seeking to the end of the file, getting the current position (which represents the size
    of the file), and then seeking back to the beginning of the file.
    """
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0, 0)
    return file_size
