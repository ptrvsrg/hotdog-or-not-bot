from typing import Optional

from sqlalchemy.orm import Session

from app.db.entity import Subscription


class SubscriptionRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_all_order_by_name_asc(self) -> list[Subscription]:
        """
        Retrieves all subscriptions from the database and sorts them by name in ascending order.
        Returns:
            list[Subscription]: A list of Subscription objects sorted by name in ascending order.
        """
        return self.session.query(Subscription).order_by(Subscription.name.asc()).all()

    def find_by_name(self, name) -> Optional[Subscription]:
        """
        Retrieves a Subscription object from the database based on the provided name.
        Args:
            name (str): The name of the Subscription to retrieve.
        Returns:
            Optional[Subscription]: A Subscription object representing the retrieved Subscription,
                or None if not found.
        """
        return (
            self.session.query(Subscription).filter(Subscription.name == name).first()
        )
