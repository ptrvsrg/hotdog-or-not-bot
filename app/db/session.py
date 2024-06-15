from sqlalchemy.orm import sessionmaker

from app.db.db import engine

Session = sessionmaker(bind=engine)
