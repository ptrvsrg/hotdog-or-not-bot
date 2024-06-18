from datetime import datetime

from sqlalchemy import Column, UUID, VARCHAR, TIMESTAMP, func, INTEGER
from sqlalchemy.orm import relationship

from app.db.entity.base_entity import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name = Column(VARCHAR(255), nullable=False, unique=True)
    total_daily_predictions = Column(INTEGER(), nullable=False, default=-1)
    users = relationship("User", back_populates="subscription")
    created_at = Column(TIMESTAMP(), nullable=False, default=datetime.now)
    updated_at = Column(
        TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now
    )
