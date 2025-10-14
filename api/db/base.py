from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from contextlib import asynccontextmanager
SQL_URL = "sqlite:///sample.db"

engine = create_engine(SQL_URL)

Session = sessionmaker(engine)


async def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.commit()
        session.close()

class Base(DeclarativeBase):
    pass