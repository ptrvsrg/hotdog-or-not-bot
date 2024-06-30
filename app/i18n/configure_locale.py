import logging

from i18next import config as locale_config

from app.config import config

logger = logging.getLogger("i18n")


def configure_locale():
    locale_config.fallback_lang = "ru"
    locale_config.locale_path = config.application.locale_dir
    locale_config.strict = False
    logger.info("Locale configured")
