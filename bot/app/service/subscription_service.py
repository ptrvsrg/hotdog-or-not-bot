import logging
from typing import Optional

from app.db.repository import SubscriptionRepository
from app.service.dto import SubscriptionDto


class SubscriptionService:

    def __init__(self, subscription_repository: SubscriptionRepository):
        self.logger = logging.getLogger("SubscriptionService")
        self.subscription_repository = subscription_repository

    def get_all(self) -> list[SubscriptionDto]:
        """
        Retrieves all subscriptions from the database and sorts them by name in ascending order.
        Returns:
            list[SubscriptionDto]: A list of SubscriptionDto objects.
        """
        self.logger.info("Get all subscriptions")
        subscriptions = self.subscription_repository.find_all_order_by_name_asc()
        return [
            SubscriptionDto.from_orm(subscription) for subscription in subscriptions
        ]

    def get_by_name(self, name: str) -> Optional[SubscriptionDto]:
        """
        Retrieves a Subscription object from the database based on the provided name.
        Args:
            name (str): The name of the Subscription to retrieve.
        Returns:
            SubscriptionDto: A SubscriptionDto object representing the retrieved Subscription, or
                None if not found.
        """
        self.logger.info(f"Get subscription by name: {name}")
        subscription = self.subscription_repository.find_by_name(name)
        if subscription is None:
            return None
        return SubscriptionDto.from_orm(subscription)
