from app.config import config
from app.db.repository import (
    user_repository,
    statistics_repository,
)
from app.service.detect_service import DetectService
from app.service.exception.user_exceptions import (
    UserNotFoundException,
    DuplicateUserException,
    UserAlreadyAdminException,
    UserAlreadyBannedException,
    UserNotBannedException,
    UserNotAdminException,
)
from app.service.predict_service import PredictService
from app.service.statistics_service import StatisticsService
from app.service.user_service import UserService
from app.service.yandex_disk_service import YandexDiskService

detect_service = DetectService(
    config.detect_model.path,
)
predict_service = PredictService(
    config.predict_model.path,
)
statistics_service = StatisticsService(statistics_repository)
user_service = UserService(
    config.bot.owner_username,
    user_repository,
    statistics_repository,
)
yandex_disk_service = YandexDiskService(
    config.yandex_disk.api_key.get_secret_value(), config.yandex_disk.base_dir
)

__all__ = [
    "detect_service",
    "DetectService",
    "predict_service",
    "PredictService",
    "statistics_service",
    "StatisticsService",
    "user_service",
    "UserService",
    "UserNotFoundException",
    "DuplicateUserException",
    "UserAlreadyAdminException",
    "UserAlreadyBannedException",
    "UserNotBannedException",
    "UserNotAdminException",
    "yandex_disk_service",
    "YandexDiskService",
]
