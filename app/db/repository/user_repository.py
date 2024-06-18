from typing import Optional, List

from sqlalchemy.orm import Session

from app.db.entity import User, Subscription, Statistics


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_username(self, username) -> Optional[User]:
        """
        Find a user by their username.
        This method queries the database to find a user by their username. It joins the
        Subscription and Statistics tables to retrieve additional information about the user.
        The username is used as a filter to find the user.
        Args:
            username (str): The username of the user to find.
        Returns:
            Optional[User]: The user object if found, None otherwise.
        """
        return (
            self.session.query(User)
            .join(Subscription)
            .join(Statistics)
            .filter(User.username == username)
            .first()
        )

    def find_all_by_is_enabled(self, is_enabled) -> list[User]:
        """
        Find all users by their is_enabled flag.
        This method queries the database to find all users by their is_enabled flag. It joins
        the Subscription and Statistics tables to retrieve additional information about the
        user. The is_enabled flag is used as a filter to find the users.
        Args:
            is_enabled (bool): The is_enabled flag of the users to find.
        Returns:
            List[User]: A list of user objects.
        """
        return (
            self.session.query(User)
            .join(Subscription)
            .join(Statistics)
            .filter(User.is_enabled == is_enabled)
            .all()
        )

    def find_all_by_is_admin(self, is_admin) -> list[User]:
        """
        Find all users by their is_admin flag.
        This method queries the database to find all users by their is_admin flag. It joins
        the Subscription and Statistics tables to retrieve additional information about the
        user. The is_admin flag is used as a filter to find the users.
        Args:
            is_admin (bool): The is_admin flag of the users to find.
        Returns:
            List[User]: A list of user objects.
        """
        return (
            self.session.query(User)
            .join(Subscription)
            .join(Statistics)
            .filter(User.is_admin == is_admin)
            .all()
        )

    def find_all(self) -> List[User]:
        """
        Find all users.
        This method queries the database to find all users. It joins the Subscription and
        Statistics tables to retrieve additional information about the user.
        Returns:
            List[User]: A list of user objects.
        """
        return self.session.query(User).join(Subscription).join(Statistics).all()

    def exists_by_username(self, username) -> bool:
        """
        Check if a user exists by their username.
        This method queries the database to check if a user exists by their username. It
        joins the Subscription and Statistics tables to retrieve additional information
        about the user. The username is used as a filter to check if the user exists.
        Args:
            username (str): The username of the user to check.
        Returns:
            bool: True if the user exists, False otherwise.
        """
        return (
            self.session.query(User).filter(User.username == username).first()
            is not None
        )

    def save(self, user: User):
        """
        Save a user in the database.
        This method adds a user to the database. It joins the Subscription and Statistics
        tables to retrieve additional information about the user. The user is added to the
        database using the session.
        Args:
            user (User): The user to add to the database.
        Returns:
            None
        """
        self.session.add(user)
        self.session.commit()

    def delete(self, user: User):
        """
        Delete a user from the database.
        This method removes a user from the database. It joins the Subscription and
        Statistics tables to retrieve additional information about the user. The user is
        removed from the database using the session.
        Args:
            user (User): The user to remove from the database.
        Returns:
            None
        """
        self.session.delete(user)
        self.session.commit()
