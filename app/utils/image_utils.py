import cv2
import numpy as np

MAX_DIMENSION = 65500


def resize_image_if_needed(image: np.ndarray) -> np.ndarray:
    """
    Resizes an image if its height or width exceeds the MAX_DIMENSION.
    Parameters:
        image (numpy.ndarray): The input image to be resized.
    Returns:
        numpy.ndarray or None: The resized image if its height or width exceeds the MAX_DIMENSION.
                              Otherwise, returns the original image.
    """
    height, width = image.shape[:2]
    if height > MAX_DIMENSION or width > MAX_DIMENSION:
        scaling_factor = MAX_DIMENSION / max(height, width)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
        return resized_image
    return image


def preprocess_image(image: bytes) -> np.ndarray:
    """
    Preprocesses an image for inference.
    Parameters:
        image (bytes): The input image to be preprocessed.
    Returns:
        numpy.ndarray: The preprocessed image.
    """
    image = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = resize_image_if_needed(image)
    return image


def postprocess_image(image: np.ndarray) -> bytes:
    """
    Postprocesses an image for inference.
    Parameters:
        image (numpy.ndarray): The input image to be postprocessed.
    Returns:
        bytes: The postprocessed image.
    """
    _, image = cv2.imencode(".jpg", image)
    return image.tobytes()
