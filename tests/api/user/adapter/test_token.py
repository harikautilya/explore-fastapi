import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.user.adapter.token import TokenDbAdpater
from api.user.models import TokenModel, UserModel
from api.db.user import Token


DUMMY_USER_ID = 1


token_create_cases = [
    (
        TokenModel(
            token="abc123", user=UserModel(id=DUMMY_USER_ID, username="u", name="n")
        ),
        "abc123",
    ),
]

token_get_existing = [
    (
        TokenModel(
            token="tok-1", user=UserModel(id=DUMMY_USER_ID, username="", name="")
        ),
        DUMMY_USER_ID,
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("token_model, expected_token_value", token_create_cases)
async def test_store_token(
    inmemory_db_session: AsyncSession,
    token_model: TokenModel,
    expected_token_value: str,
):
    adapter = TokenDbAdpater(db=inmemory_db_session)
    result = await adapter.store_token(token=token_model)
    assert result is True

    stmt = select(Token).where(
        Token.user_id == token_model.user.id,
        Token.token == token_model.token,
    )
    res = await inmemory_db_session.execute(stmt)
    db_token = res.scalar_one_or_none()
    assert db_token is not None
    assert db_token.token == expected_token_value


@pytest.mark.asyncio
@pytest.mark.parametrize(" query_token_model, expected_user_id", token_get_existing)
async def test_get_user_returns_user(
    inmemory_db_session: AsyncSession,
    query_token_model: TokenModel,
    expected_user_id: int,
):
    adapter = TokenDbAdpater(db=inmemory_db_session)

    # insert token row directly with the expected user id
    await adapter.store_token(query_token_model)

    returned = await adapter.get_user(token=query_token_model)

    assert returned is not None
    assert isinstance(returned.user, UserModel)
    assert returned.user.id == expected_user_id


@pytest.mark.asyncio
@pytest.mark.parametrize("missing_token", ["nonexistent"])
async def test_get_user_returns_none_for_missing_token(
    inmemory_db_session: AsyncSession, missing_token: str
):
    adapter = TokenDbAdpater(db=inmemory_db_session)
    token = TokenModel(token=missing_token, user=None)
    returned = await adapter.get_user(token=token)
    assert returned is None
