from abc import ABC, abstractmethod
from ..models import TokenModel, UserModel
from app1.api.db.user import Token
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app1.api.db.session import AsyncSessionManagedDB
from sqlalchemy.orm import joinedload

class TokenAdapter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    async def store_token(self, token: TokenModel) -> bool:
        """
        Store token
        """
        pass

    @abstractmethod
    async def get_user(self, token: TokenModel) -> UserModel:
        """
        Get token
        """
        pass


class TokenDbAdpater(TokenAdapter):

    def __init__(self, db: AsyncSessionManagedDB[Token, int]):
        self.db = db

    async def store_token(self, token: TokenModel) -> bool:
        if token.user is not None:
            token_db = Token(user_id=token.user.id,
                            token=token.token,
                            last_used=str(datetime.now()))
        else:
            raise Exception("User id is missing for token")
        result = await self.db.insert(token_db)
        return True

    async def get_user(self, token: TokenModel) -> TokenModel:
        result  = await self.db.filter(token=token.token)
        if not result:
            raise Exception("Token not assocated with any user")
        token_updated_with_user = token.copy(
            user=UserModel(id=result[0].user_id, username="", name=""),
        )
        return token_updated_with_user
