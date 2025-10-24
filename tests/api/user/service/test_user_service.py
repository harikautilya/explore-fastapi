import asyncio
from unittest.mock import MagicMock, AsyncMock
import pytest

from api.user.service.user import UserService
from api.user.models import UserModel
from api.user.exceptions import InvalidUserDetails


@pytest.fixture
def adapter_mock():
    m = MagicMock()
    m.store_user = AsyncMock()
    m.get_user_by_id = AsyncMock()
    m.get_user_by_creds = AsyncMock()
    return m

@pytest.mark.asyncio
async def test_user_service_create_user_success(adapter_mock):
    service = UserService.get_instance(user_adapter=adapter_mock)

    adapter_mock.store_user.return_value = True

    result = await service.create_user(username="bob", password="p", name="Bob")

    adapter_mock.store_user.assert_awaited_once()
    assert result is None

@pytest.mark.asyncio
async def test_user_service_create_user_failure(adapter_mock):
    service = UserService.get_instance(user_adapter=adapter_mock)

    adapter_mock.store_user.return_value = False

    with pytest.raises(InvalidUserDetails):
        await service.create_user(username="bad", password="p", name="B")

@pytest.mark.asyncio
async def test_get_user_by_id(adapter_mock):
    service = UserService.get_instance(user_adapter=adapter_mock)

    adapter_mock.get_user_by_id.return_value = UserModel(id=1, username="u", name="n")

    result = await service.get_user_by_id(id=1)

    adapter_mock.get_user_by_id.assert_awaited_once_with(id=1)
    assert result.id == 1
