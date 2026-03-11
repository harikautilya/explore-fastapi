from abc import ABC, abstractmethod
from ..models import TokenModel, UserModel
from api.db.user import Token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from datetime import datetime


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

    def __init__(self, db: AsyncSession):
        self.db = db

    async def store_token(self, token: TokenModel) -> bool:
        statement = insert(Token).values(
            user_id=token.user.id,
            token=token.token,
            last_used=datetime.now(),
        )
        result = await self.db.execute(statement=statement)
        return True

    async def get_user(self, token: TokenModel) -> TokenModel:
        statement = select(Token.user_id).filter(Token.token==token.token)
        execute_result  = await self.db.execute(statement=statement)
        result= execute_result.first()
        if not result:
            return None
        token_updated_with_user = token.copy(
            user=UserModel(id=result[0], username="", name=""),
        )
        return token_updated_with_user
