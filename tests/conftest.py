import sys
from pathlib import Path
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import Generator, Any


# Ensure project root is on sys.path so tests can import the `api` package
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DUMMY_TEST_TOKEN = "testtoken"


@pytest.fixture
def inmemory_db_session() -> Generator[Session, Any, Any]:
    from api.db.base import Base
    """Create a reusable in-memory SQLite SQLAlchemy Session for tests.

    Yields a SQLAlchemy Session that has created metadata for the project's
    models. The caller is responsible for committing/rolling back any
    changes in the test.
    """

    engine = create_engine("sqlite:///:memory:")

    # Event listener to enable foreign keys for each new connection
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    session = SessionLocal()
    try:
        setup_dummy_user(session)
        setup_token(session)
        yield session
    finally:
        session.close()



def setup_dummy_user(session):
    # Create a dummy user
    from api.db.user import User

    dummy_user = User(username="testuser", name="test", password="password")
    session.add(dummy_user)
    session.commit()


def setup_token(inmemory_db_session):
    """Create a token row for the dummy user and return the token string.

    Tests can use this token value when they need a valid authentication token
    stored in the database. The dummy user created by `setup_dummy_user`
    has id 1 in these tests.
    """
    from api.db.user import Token

    token_value = DUMMY_TEST_TOKEN
    token_row = Token(user_id=1, token=token_value, last_used="now")
    inmemory_db_session.add(token_row)
    inmemory_db_session.commit()
    return token_value
