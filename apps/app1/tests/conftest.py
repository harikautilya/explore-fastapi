import sys
from pathlib import Path
import pytest_asyncio
import pytest
from typing import Generator, Any, Dict, AsyncGenerator
from fastapi import FastAPI
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.engine import Engine

from api import note, user
from api.db.base import get_db_session, Base



DUMMY_TEST_TOKEN = "testtoken"
DUMMY_TEST_TOKEN2 = "testtoken2"

DUMMY_USER_ID = 1
DUMMY_USER_ID2 = 1


@pytest_asyncio.fixture
async def inmemory_db_session() -> AsyncGenerator[AsyncSession, Any]:

    async def setup_dummy_user(session: AsyncSession):
        # Create a dummy user
        from api.db.user import User
        from api.user.utils.encrpty import encrpty_string
        psww = await encrpty_string("password")
        dummy_user = User(username="testuser", name="test", password=psww)
        session.add(dummy_user)

        psww = await encrpty_string("password2")
        dummy_user2 = User(username="testuser2", name="test2", password=psww)
        session.add(dummy_user2)

        await session.commit()

    async def setup_token(inmemory_db_session: AsyncSession):
        """Create token rows for the dummy users and commit them."""
        from api.db.user import Token

        token_value = DUMMY_TEST_TOKEN
        token_row = Token(user_id=1, token=token_value, last_used="now")
        inmemory_db_session.add(token_row)

        token_value2 = DUMMY_TEST_TOKEN2
        token_row2 = Token(user_id=2, token=token_value2, last_used="now")
        inmemory_db_session.add(token_row2)

        await inmemory_db_session.commit()
        return token_value

    """Create a reusable in-memory SQLite SQLAlchemy AsyncSession for tests.

    Yields a SQLAlchemy AsyncSession that has created metadata for the project's
    models. The caller is responsible for committing/rolling back any
    changes in the test.
    """

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    # Event listener to enable foreign keys for each new connection
    @event.listens_for(engine.sync_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(bind=engine)

    session = SessionLocal()
    try:
        await setup_dummy_user(session)
        await setup_token(session)
        yield session
    finally:
        await session.close()


@pytest.fixture
def test_request() -> Dict[str, dict]:
    return {"headers": {"Authorization": f"Bearer {DUMMY_TEST_TOKEN}"}}


@pytest.fixture
def test_request_two() -> Dict[str, dict]:
    return {"headers": {"Authorization": f"Bearer {DUMMY_TEST_TOKEN2}"}}


@pytest.fixture
def test_app(inmemory_db_session) -> FastAPI:
    from api.user.middleware import Authentication
    app = FastAPI()
    note.register_router(app=app)
    user.register_router(app=app)
    user.setup_excepttion_handling(app=app)
   

    async def get_modified_db():
        yield inmemory_db_session

    app.dependency_overrides[get_db_session] = get_modified_db
    # Modified middleware
    app.add_middleware(Authentication, db_session=get_modified_db)
    main_app = FastAPI()
    main_app.mount("/api", app)
    return main_app
