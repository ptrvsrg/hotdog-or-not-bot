from typing import Optional, List

from sqlalchemy.orm import Session

from app.db.entity import User, Subscription, Statistics


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_username(self, username) -> Optional[User]:
        return self.session.query(User).join(Subscription).join(Statistics).filter(
            User.username == username).first()

    def find_all_by_is_enabled(self, is_enabled) -> list[User]:
        return self.session.query(User).join(Subscription).join(Statistics).filter(
            User.is_enabled == is_enabled).all()

    def find_all_by_is_admin(self, is_admin) -> list[User]:
        return self.session.query(User).join(Subscription).join(Statistics).filter(
            User.is_admin == is_admin).all()

    def find_all(self) -> List[User]:
        return self.session.query(User).join(Subscription).join(Statistics).all()

    def exists_by_username(self, username) -> bool:
        return self.session.query(User).filter(User.username == username).first() is not None

    def save(self, user: User):
        self.session.add(user)
        self.session.commit()

    def delete(self, user: User):
        self.session.delete(user)
        self.session.commit()
