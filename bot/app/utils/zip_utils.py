import io
import zipfile
from typing import List

import numpy as np


def zip_cropped_images(images: List[np.ndarray]) -> io.BytesIO:
    """
    Compresses a list of cropped images into a zip file.
    Args:
        images (List[np.ndarray]): A list of cropped images represented as numpy arrays.
    Returns:
        io.BytesIO: A BytesIO object containing the compressed zip file.
    Raises:
        None
    """
    zip_file = io.BytesIO()
    with zipfile.ZipFile(zip_file, "w") as zf:
        for i, image in enumerate(images):
            zf.writestr(f"object_{i}.jpg", image.tobytes())
    zip_file.seek(0)

    return zip_file
