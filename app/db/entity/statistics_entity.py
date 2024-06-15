from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, Integer, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.entity.base_entity import Base


class Statistics(Base):
    __tablename__ = "statistics"
        
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    total_predictions = Column(Integer(), nullable=False, default=0)
    daily_predictions = Column(Integer(), nullable=False, default=0)
    successful_predictions = Column(Integer(), nullable=False, default=0)
    failed_predictions = Column(Integer(), nullable=False, default=0)
    hotdog_predictions = Column(Integer, nullable=False, default=0)
    not_hotdog_predictions = Column(Integer(), nullable=False, default=0)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="statistics", uselist=False)
    created_at = Column(TIMESTAMP(), nullable=False, default=datetime.now)
    updated_at = Column(TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now)
