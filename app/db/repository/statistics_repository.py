from typing import Optional

from sqlalchemy.orm import Session

from app.db.entity import Statistics, User


class StatisticsRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> list[Statistics]:
        """
        Retrieves all the statistics from the database.
        Returns:
            list[Statistics]: A list of Statistics objects representing the statistics.
        """
        return self.session.query(Statistics).join(User).all()

    def find_by_username(self, username) -> Optional[Statistics]:
        """
        Retrieves the statistics for a given user.
        Args:
            username (str): The username of the user.
        Returns:
            Optional[Statistics]: The statistics for the user, or None if the user does not exist.
        """
        return (
            self.session.query(Statistics)
            .join(User)
            .filter(User.username == username)
            .first()
        )

    def save(self, statistics: Statistics):
        """
        Adds a new statistics to the database.
        Args:
            statistics (Statistics): The statistics to be added.
        Returns:
            None
        """
        self.session.add(statistics)
        self.session.commit()

    def save_all(self, statistics: list[Statistics]):
        """
        Adds a list of statistics to the database.
        Args:
            statistics (list[Statistics]): The statistics to be added.
        Returns:
            None
        """
        for s in statistics:
            self.session.add(s)
        self.session.commit()
