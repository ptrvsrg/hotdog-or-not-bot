import logging
from typing import Optional

from app.db.entity import User, Statistics
from app.db.repository import UserRepository, SubscriptionRepository, StatisticsRepository
from app.service.dto import UserDto
from app.service.exception.user_exceptions import (
    DuplicateUserException,
    UserAlreadyAdminException,
    UserAlreadyBannedException,
    UserNotAdminException,
    UserNotBannedException,
)


class UserService:

    def __init__(
        self,
        owner_username: str,
        user_repository: UserRepository,
        subscription_repository: SubscriptionRepository,
        statistics_repository: StatisticsRepository
    ):
        self.owner_username = owner_username
        self.user_repository = user_repository
        self.subscription_repository = subscription_repository
        self.statistics_repository = statistics_repository
        self.logger = logging.getLogger("UserService")

    def get_user_by_username(self, username: str) -> Optional[UserDto]:
        """
        Asynchronously retrieves a user from the database by their username.
        Args:
            username (str): The username of the user to retrieve.
        Returns:
            Optional[UserDto]: A UserDto object representing the user, or None if the user is not
                found.
        """
        self.logger.info(f"Get user by username: {username}")
        user = self.user_repository.find_by_username(username)
        if user is None:
            return None
        return UserDto.from_orm(user)

    def exists_user_by_username(self, username: str) -> bool:
        """
        Check if a user exists in the database based on their username.
        Args:
            username (str): The username of the user to check.
        Returns:
            bool: True if the user exists, False otherwise.
        """
        self.logger.info(f"Exists user by username: {username}")
        return self.user_repository.exists_by_username(username)

    def create_user(self, username: str, is_enabled: bool = True,
                    is_admin: bool = False) -> UserDto:
        """
        Asynchronously creates a new user in the database.
        Args:
            username (str): The username of the new user.
            is_enabled (bool, optional): Whether the user is enabled. Defaults to True.
            is_admin (bool, optional): Whether the user is an admin. Defaults to False.
        Returns:
            UserDto: A UserDto object representing the created user.
        Raises:
            DuplicateUserException: If the user already exists in the database.
        """
        self.logger.info(f"Create user: {username}")
        if self.exists_user_by_username(username):
            raise DuplicateUserException(username)

        subscription = self.subscription_repository.find_by_name('Free')
        if subscription is None:
            raise Exception('Subscription not found')

        user = User(
            username=username,
            subscription_id=subscription.id,
            is_enabled=is_enabled,
            is_admin=is_admin
        )
        self.user_repository.save(user)

        statistics = Statistics(
            user_id=user.id
        )
        self.statistics_repository.save(statistics)

        return UserDto.from_orm(user)

    def add_admin(self, username: str):
        """
        Asynchronously adds an admin to the database.
        Args:
            username (str): The username of the admin to add.
        Returns:
            None
        Raises:
            UserAlreadyAdminException: If the user is already an admin.
        """
        self.logger.info(f"Add admin: {username}")
        user = self.user_repository.find_by_username(username=username)
        if user is None:
            self.create_user(username, is_admin=True)
            return
        if user.is_admin:
            raise UserAlreadyAdminException(username)
        user.is_admin = True
        self.user_repository.save(user)

    def remove_admin(self, username: str):
        """
        Asynchronously removes an admin from the database.
        Args:
            username (str): The username of the admin to remove.
        Returns:
            None
        Raises:
            UserNotAdminException: If the user is not an admin.
        """
        self.logger.info(f"Remove admin: {username}")
        user = self.user_repository.find_by_username(username=username)
        if user is None:
            self.create_user(username)
            raise UserNotAdminException(username)
        if not user.is_admin:
            raise UserNotAdminException(username)
        user.is_admin = False
        self.user_repository.save(user)

    def get_banned_users(self) -> list[UserDto]:
        """
        Asynchronously retrieves a list of banned users from the database.
        Returns:
            list[User]: A list of User objects representing the banned users.
        """
        self.logger.info("Get banned users")
        users = self.user_repository.find_all_by_is_enabled(is_enabled=False)
        return [UserDto.from_orm(user) for user in users]

    def get_admins(self) -> list[UserDto]:
        """
        Asynchronously retrieves a list of admins from the database.
        Returns:
            list[User]: A list of User objects representing the admins.
        """
        self.logger.info("Get admins")
        users = self.user_repository.find_all_by_is_admin(is_admin=True)
        return [UserDto.from_orm(user) for user in users]

    def ban_user(self, username: str):
        """
        Asynchronously bans a user from the database.
        Args:
            username (str): The username of the user to ban.
        Returns:
            None
        Raises:
            UserAlreadyBannedException: If the user is already banned.
        """
        self.logger.info(f"Ban user: {username}")
        user = self.user_repository.find_by_username(username=username)
        if user is None:
            self.create_user(username, is_enabled=False)
            return
        if not user.is_enabled:
            raise UserAlreadyBannedException(username)
        user.is_enabled = False
        self.user_repository.save(user)

    def unban_user(self, username: str):
        """
        Asynchronously unbans a user from the database.
        Args:
            username (str): The username of the user to unban.
        Returns:
            None
        Raises:
            UserNotBannedException: If the user is not banned.
        """
        self.logger.info(f"Unban user: {username}")
        user = self.user_repository.find_by_username(username=username)
        if user is None:
            self.create_user(username)
            raise UserNotBannedException(username)
        if not user.is_enabled:
            raise UserNotBannedException(username)
        user.is_enabled = True
        self.user_repository.save(user)
