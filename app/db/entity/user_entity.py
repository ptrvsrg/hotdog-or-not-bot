from datetime import datetime

from sqlalchemy import Column, UUID, BOOLEAN, VARCHAR, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.db.entity.base_entity import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    username = Column(VARCHAR(255), nullable=False, unique=True)
    is_enabled = Column(BOOLEAN(), nullable=False, default=True)
    is_admin = Column(BOOLEAN(), nullable=False, default=False)
    statistics = relationship("Statistics", back_populates="user", uselist=False)
    created_at = Column(TIMESTAMP(), nullable=False, default=datetime.now)
    updated_at = Column(
        TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now
    )
