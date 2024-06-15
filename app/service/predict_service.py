import logging

from ultralytics import YOLO

from app.utils.image_utils import preprocess_image


class PredictService:
    def __init__(self, model_file: str) -> None:
        """
        Initializes the PredictService class with a given model file.
        Args:
            model_file (str): The path to the model file.
        Returns:
            None
        Note:
            - The model file is used to initialize the trained YOLO classifier.
        """
        self.logger = logging.getLogger("PredictService")

        self.logger.info(f"Loading predict model from {model_file}")
        self.model = YOLO(model_file)

    def predict(self, image_bytes: bytes) -> float:
        """
        Predicts the probability of an image being a hotdog or not.
        Args:
            image_bytes (bytes): The input image to be predicted.
        Returns:
            float: The probability of the image being a hotdog.
        Note:
            - The image is passed as a numpy array.
            - The prediction is obtained by running the image through a pre-trained model.
            - The prediction is returned as a float between 0 and 1.
        """
        self.logger.info("Start predicting image")

        self.logger.info("Image preprocessing")
        image = preprocess_image(image_bytes)

        results = self.model.predict(
            source=image,
            verbose=False,
        )
        prob = results[0].probs.data.cpu().numpy()[0]
        self.logger.info(f"End prediction: Probability {prob * 100}%")
        return prob
