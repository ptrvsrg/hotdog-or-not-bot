from sqlalchemy import create_engine

from app.config import config

engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    config.postgres.user,
    config.postgres.password.get_secret_value(),
    config.postgres.host,
    config.postgres.port,
    config.postgres.db
), pool_size=5, max_overflow=10, echo=True)
