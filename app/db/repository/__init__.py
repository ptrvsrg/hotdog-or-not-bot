from app.db.session import Session
from app.db.repository.user_repository import UserRepository
from app.db.repository.subscription_repository import SubscriptionRepository
from app.db.repository.statistics_repository import StatisticsRepository


user_repository = UserRepository(Session())
subscription_repository = SubscriptionRepository(Session())
statistics_repository = StatisticsRepository(Session())


__all__ = [
    "user_repository",
    "subscription_repository",
    "statistics_repository",
    "UserRepository",
    "SubscriptionRepository",
    "StatisticsRepository",
]