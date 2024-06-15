from app.config import config
from app.db.repository import user_repository, subscription_repository, statistics_repository
from app.service.detect_service import DetectService
from app.service.exception.user_exceptions import UserNotFoundException, DuplicateUserException, \
    UserAlreadyAdminException, UserAlreadyBannedException, UserNotBannedException, \
    UserNotAdminException
from app.service.predict_service import PredictService
from app.service.statistics_service import StatisticsService
from app.service.subscription_service import SubscriptionService
from app.service.user_service import UserService

detect_service = DetectService(
    config.detect_model.path,
)
predict_service = PredictService(
    config.predict_model.path,
)
statistics_service = StatisticsService(statistics_repository)
subscription_service = SubscriptionService(subscription_repository)
user_service = UserService(
    config.bot.owner_username,
    user_repository,
    subscription_repository,
    statistics_repository
)

__all__ = [
    "detect_service",

    "predict_service",

    "statistics_service",

    "subscription_service",

    "user_service",
    "UserNotFoundException",
    "DuplicateUserException",
    "UserAlreadyAdminException",
    "UserAlreadyBannedException",
    "UserNotBannedException",
    "UserNotAdminException",
]
