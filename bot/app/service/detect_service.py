import logging
from typing import List

import numpy as np
from ultralytics import YOLO

from app.utils.image_utils import preprocess_image, postprocess_image


class DetectService:
    def __init__(self, model_file: str) -> None:
        """
        Initializes the DetectService object with the given model file.
        Args:
            model_file (str): The path to the model file.
        Returns:
            None
        Note:
            - The model file is used to initialize the YOLO model.
        """
        self.logger = logging.getLogger("DetectService")

        self.logger.info(f"Loading detect model from {model_file}")
        self.model = YOLO(model_file)

    def detect_all(self, image_bytes: bytes) -> list[bytes]:
        """
        Detects all objects in the given image and returns a list of cropped images of the detected
        objects.
        Parameters:
            image_bytes (np.ndarray): The input image in which objects need to be detected.
        Returns:
            List[np.ndarray]: A list of cropped images of the detected objects.
        Note:
            - The function uses the YOLO model to perform object detection on the input image.
            - The detected objects are cropped from the input image.
            - The function logs the start and end of the detection process.
        """
        self.logger.info(f"Start detection")

        self.logger.debug("Image preprocessing")
        image = preprocess_image(image_bytes)

        results = self.model.predict(
            source=image,
            verbose=False,
        )

        self.logger.debug("Image postprocessing")
        boxes = results[0].boxes.xyxy.tolist()
        cropped_images: list[bytes] = []
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            img = image[int(y1) : int(y2), int(x1) : int(x2)]
            cropped_img = postprocess_image(img)
            cropped_images.append(cropped_img)

        self.logger.info(f"End detection: {len(cropped_images)} objects detected")
        return cropped_images
