import logging
import os

from envyaml import EnvYAML
from pydantic import ValidationError

from app.config.model_config import ConfigModel

DEFAULT_CONFIG_PATH: str = "config/config.yaml"
logger = logging.getLogger("config")


def load_config() -> ConfigModel:
    # Load config
    config_path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)
    try:
        config_data = EnvYAML(config_path)
    except ValueError as e:
        logger.exception(e)
        exit(1)

    # Validate config
    try:
        config = ConfigModel(**config_data.export())
    except ValidationError as e:
        logger.exception(e)
        exit(1)

    logger.info("Config loaded")
    return config
