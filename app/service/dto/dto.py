from dataclasses import dataclass

from app.config import config
from app.db.entity import User, Statistics


@dataclass
class StatisticsDto:
    total_predictions: int
    daily_predictions: int
    successful_predictions: int
    failed_predictions: int
    hotdog_predictions: int
    not_hotdog_predictions: int

    @classmethod
    def from_orm(cls, statistics: Statistics):
        return cls(
            total_predictions=statistics.total_predictions,
            daily_predictions=statistics.daily_predictions,
            successful_predictions=statistics.successful_predictions,
            failed_predictions=statistics.failed_predictions,
            hotdog_predictions=statistics.hotdog_predictions,
            not_hotdog_predictions=statistics.not_hotdog_predictions,
        )


@dataclass
class UserDto:

    username: str
    is_banned: bool
    is_admin: bool
    is_owner: bool
    statistics: StatisticsDto

    @classmethod
    def from_orm(cls, user: User):
        return cls(
            username=user.username,
            is_banned=not user.is_enabled,
            is_admin=user.is_admin,
            is_owner=user.username == config.bot.owner_username,
            statistics=StatisticsDto.from_orm(user.statistics),
        )
