import logging
import os

from pydantic import ValidationError

from app.config.model_config import ConfigModel

logger = logging.getLogger("config")


def load_config() -> ConfigModel:
    # Load config
    config_data: dict = {
        "application": {
            "major_version": os.getenv("MAJOR_VERSION", 0),
            "minor_version": os.getenv("MINOR_VERSION", 0),
            "patch_version": os.getenv("PATCH_VERSION", 0),
            "locale_dir": os.getenv("LOCALE_DIR", "i18n"),
        },
        "detect_model": {
            "path": os.getenv("DETECT_MODEL_PATH"),
        },
        "predict_model": {
            "path": os.getenv("PREDICT_MODEL_PATH"),
        },
        "bot": {
            "telegram_token": os.getenv("TELEGRAM_TOKEN"),
            "owner_username": os.getenv("OWNER_USERNAME"),
            "webhook_url": os.getenv("WEBHOOK_URL"),
            "daily_limit": int(os.getenv("DAILY_LIMIT", 100)),
        },
        "postgres": {
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "db": os.getenv("POSTGRES_DB"),
        },
        "redis": {
            "host": os.getenv("REDIS_HOST"),
            "port": os.getenv("REDIS_PORT"),
            "user": os.getenv("REDIS_USER"),
            "password": os.getenv("REDIS_PASSWORD"),
            "db": (
                int(os.getenv("REDIS_DB"))
                if os.getenv("REDIS_DB") is not None
                else None
            ),
        },
        "yandex_disk": {
            "api_key": os.getenv("YANDEX_DISK_API_KEY"),
            "base_dir": os.getenv("YANDEX_DISK_BASE_DIR", "hotdog_or_not"),
        },
        "server": {
            "debug": os.getenv("DEBUG", False),
            "port": int(os.getenv("PORT", 8080)),
        },
    }

    # Validate config
    try:
        config = ConfigModel(**config_data)
    except ValidationError as e:
        logger.exception(e)
        exit(1)

    logger.info("Config loaded")
    return config
