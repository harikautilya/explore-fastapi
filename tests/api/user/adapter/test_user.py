import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.user.adapter.user import UserDbAdapter
from api.user.models import CredentailsModel, UserModel
from api.db.user import User


DUMMY_USER_ID = 1


user_store_cases = [
    (UserModel(id=-1, username="bob", name="Bob"), "password123", True),
]

user_creds_cases = [
    (
        UserModel(id=-1, username="alice", name="alice"),
        "secret",
        CredentailsModel(username="alice", password="secret")
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("user_model,password,expected", user_store_cases)
async def test_store_user(
    inmemory_db_session: AsyncSession,
    user_model: UserModel,
    password: str,
    expected: bool,
):
    adapter = UserDbAdapter(db=inmemory_db_session)

    result = await adapter.store_user(user=user_model, password=password)
    assert result is expected

    stmt = select(User).where(User.username == user_model.username)
    res = await inmemory_db_session.execute(stmt)
    db_user = res.scalar_one_or_none()
    assert db_user is not None
    assert db_user.username == user_model.username


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_model, pre_password_plain, creds",
    user_creds_cases,
)
async def test_get_user_by_creds_success(
    inmemory_db_session: AsyncSession,
    user_model: UserModel,
    pre_password_plain: str,
    creds: CredentailsModel,
):
    adapter = UserDbAdapter(db=inmemory_db_session)

    # store a user by inserting directly using the same encrypt function flow as adapter
    # The adapter uses encrpty_string to hash the password; reuse that to produce the same hash
    from api.user.utils.encrpty import encrpty_string

    hashed = await encrpty_string(pre_password_plain)
    result = await adapter.store_user(user=user_model, password=pre_password_plain)

    returned = await adapter.get_user_by_creds(creds=creds)
    assert returned is not None



@pytest.mark.asyncio
async def test_get_user_by_creds_failure(inmemory_db_session: AsyncSession):
    adapter = UserDbAdapter(db=inmemory_db_session)

    creds = CredentailsModel(username="noone", password="bad")
    returned = await adapter.get_user_by_creds(creds=creds)
    assert returned is None


@pytest.mark.asyncio
async def test_get_user_by_id(inmemory_db_session: AsyncSession):
    adapter = UserDbAdapter(db=inmemory_db_session)

    returned = await adapter.get_user_by_id(id=DUMMY_USER_ID)
    assert returned is not None
    assert returned.id == DUMMY_USER_ID
