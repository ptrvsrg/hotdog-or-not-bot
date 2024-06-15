from typing import Optional

from sqlalchemy.orm import Session

from app.db.entity import Subscription


class SubscriptionRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_all_order_by_name_asc(self) -> list[Subscription]:
        return self.session.query(Subscription).order_by(Subscription.name.asc()).all()

    def find_by_name(self, name) -> Optional[Subscription]:
        return self.session.query(Subscription).filter(Subscription.name == name).first()
