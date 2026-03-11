import asyncio
from unittest.mock import MagicMock, AsyncMock
import pytest

from api.user.service.token import TokenService
from api.user.models import UserModel
from api.user.exceptions import InvalidCredentialsException


@pytest.fixture
def adapters_mock():
    ua = MagicMock()
    ta = MagicMock()
    ua.get_user_by_creds = AsyncMock()
    ta.store_token = AsyncMock()
    return ua, ta

@pytest.mark.asyncio
async def test_generate_token_success(adapters_mock):
    user_adapter, token_adapter = adapters_mock
    user_adapter.get_user_by_creds.return_value = UserModel(id=1, username="u", name="n")
    token_adapter.store_token.return_value = True

    service = TokenService.get_instance(user_adapter=user_adapter, token_adapter=token_adapter)

    token = await service.generate_token(username="u", password="p")

    user_adapter.get_user_by_creds.assert_awaited_once()
    token_adapter.store_token.assert_awaited_once()
    assert isinstance(token, str)

@pytest.mark.asyncio
async def test_generate_token_invalid_creds(adapters_mock):
    user_adapter, token_adapter = adapters_mock
    user_adapter.get_user_by_creds.return_value = None


    service = TokenService.get_instance(user_adapter=user_adapter, token_adapter=token_adapter)

    with pytest.raises(InvalidCredentialsException):
        await service.generate_token(username="u", password="p")
