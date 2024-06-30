from app.db.repository.statistics_repository import StatisticsRepository
from app.db.repository.user_repository import UserRepository
from app.db.session import Session

user_repository = UserRepository(Session())
statistics_repository = StatisticsRepository(Session())


__all__ = [
    "user_repository",
    "UserRepository",
    "statistics_repository",
    "StatisticsRepository",
]
