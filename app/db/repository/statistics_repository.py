from typing import Optional

from sqlalchemy.orm import Session

from app.db.entity import Subscription, Statistics, User


class StatisticsRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> list[Statistics]:
        return self.session.query(Statistics).join(User).all()

    def find_by_username(self, username) -> Optional[Statistics]:
        return self.session.query(Statistics).join(User).filter(User.username == username).first()

    def save(self, statistics: Statistics):
        self.session.add(statistics)
        self.session.commit()

    def save_all(self, statistics: list[Statistics]):
        for s in statistics:
            self.session.add(s)
        self.session.commit()
