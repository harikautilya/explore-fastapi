from typing import Annotated, Any
from fastapi import Depends

from .service import TokenService, UserService
from .adapter import UserAdapter, TokenAdapter

from app1.api.db.base import SessionLocal
from app1.api.db.session import AsyncSessionManagedDB
from app1.api.db.user import User, Token
from app1.api.db.base import get_db_session


def get_user_adapter(
    db_session: Annotated[Any, Depends(get_db_session)],
) -> UserAdapter:
    from .adapter.user import UserDbAdapter

    return UserDbAdapter(db=db_session)


def get_token_adapter() -> TokenAdapter:
    from .adapter.token import TokenDbAdpater

    session = AsyncSessionManagedDB[Token, int](
        session_manager=SessionLocal,
        model_class=Token,
    )
    return TokenDbAdpater(db=session)


async def get_token_service(
    user_adapter: Annotated[UserAdapter, Depends(get_user_adapter)],
    token_adapter: Annotated[TokenAdapter, Depends(get_token_adapter)],
):
    service = TokenService.get_instance(
        user_adapter=user_adapter,
        token_adapter=token_adapter,
    )
    return service


async def get_user_service(
    user_adapter: Annotated[UserAdapter, Depends(get_user_adapter)],
):
    service = UserService.get_instance(user_adapter=user_adapter)
    return service
