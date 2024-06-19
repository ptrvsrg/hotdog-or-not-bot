import logging
from typing import Optional

from app.db.repository import StatisticsRepository
from app.service.dto import StatisticsDto


class StatisticsService:

    def __init__(self, statistics_repository: StatisticsRepository):
        self.statistics_repository = statistics_repository
        self.logger = logging.getLogger("StatisticsService")

    def get_statistics(self, username: str) -> Optional[StatisticsDto]:
        """
        Retrieves the statistics for a given user.
        Args:
            username (str): The username of the user.
        Returns:
            Optional[StatisticsDto]: The statistics for the user, or None if the user does not exist.
        """
        self.logger.info("Get statistics")
        statistics = self.statistics_repository.find_by_username(username)
        if not statistics:
            return None
        return StatisticsDto.from_orm(statistics)

    def add_hotdog_prediction(self, username: str):
        """
        Add a hotdog prediction for the specified username.
        Args:
            username (str): The username for which the hotdog prediction is being added.
        Returns:
            None
        """
        self.logger.info("Add hotdog prediction")
        statistics = self.statistics_repository.find_by_username(username)
        if not statistics:
            return
        statistics.hotdog_predictions += 1
        statistics.daily_predictions += 1
        statistics.total_predictions += 1
        self.statistics_repository.save(statistics)

    def add_not_hotdog_prediction(self, username: str):
        """
        Add a not hotdog prediction for the specified username.
        Args:
            username (str): The username for which the not hotdog prediction is being added.
        Returns:
            None
        """
        self.logger.info("Add not hotdog prediction")
        statistics = self.statistics_repository.find_by_username(username)
        if not statistics:
            return
        statistics.not_hotdog_predictions += 1
        statistics.daily_predictions += 1
        statistics.total_predictions += 1
        self.statistics_repository.save(statistics)

    def add_successful_prediction(self, username: str):
        """
        Add a successful prediction for the specified username.
        Args:
            username (str): The username for which the successful prediction is being added.
        Returns:
            None
        """
        self.logger.info("Add successful prediction")
        statistics = self.statistics_repository.find_by_username(username)
        if not statistics:
            return
        statistics.successful_predictions += 1
        self.statistics_repository.save(statistics)

    def add_failed_predictions(self, username: str):
        """
        Add a failed prediction for the specified username.
        Args:
            username (str): The username for which the failed prediction is being added.
        Returns:
            None
        """
        self.logger.info("Add failed prediction")
        statistics = self.statistics_repository.find_by_username(username)
        if not statistics:
            return
        statistics.failed_predictions += 1
        self.statistics_repository.save(statistics)

    def clear_daily_predictions(self):
        """
        Clear the daily predictions for all users.
        Args:
            None
        Returns:
            None
        """
        self.logger.info("Clear weekly predictions")
        statistics = self.statistics_repository.find_all()
        for stat in statistics:
            stat.daily_predictions = 0
        self.statistics_repository.save_all(statistics)
