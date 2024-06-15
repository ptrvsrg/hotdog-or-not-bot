import logging
from typing import Optional

from sqlalchemy import Connection

from app.db.db import engine
from app.db.entity import Base

logger = logging.getLogger("database")
conn: Optional[Connection] = None


def connect_db():
    logger.info("Connect to database")
    conn = engine.connect()

    logger.info("Create schema")
    Base.metadata.create_all(engine)


def disconnect_db():
    logger.info("Disconnect from database")
    if conn is not None:
        conn.close()
