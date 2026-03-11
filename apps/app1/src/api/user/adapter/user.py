from abc import ABC, abstractmethod
from ..models import CredentailsModel, UserModel, TokenModel
from api.db.user import User, Token
from ..utils.encrpty import encrpty_string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update


class UserAdapter(ABC):
    """
    A Sample user adapter for the purpose to reading and writing data to
    to the source
    """

    def __init__(self):
        pass

    @abstractmethod
    async def get_user_by_creds(self, creds: CredentailsModel) -> UserModel | None:
        """
        Get user based on creds
        """
        pass

    @abstractmethod
    async def get_user_by_id(self, id: int) -> UserModel | None:
        """
        Get user by id
        """
        pass

    @abstractmethod
    async def store_user(self, user: UserModel, password: str) -> bool:
        """
        Store user details. Password is declared as additonal argument to ensure that it is propageted only
        to this method and not other methods where is not required.
        """
        pass


class UserDbAdapter(UserAdapter):
    """
    User Adapter based on db as source
    """

    def __init__(self, db: AsyncSession):
        self.db_session = db

    async def get_user_by_creds(self, creds: CredentailsModel) -> UserModel | None:
        input_password_encrpty = await encrpty_string(creds.password)
        statment = (
            select(User.id, User.name, User.username)
            .filter(User.username == creds.username)
            .filter(User.password == input_password_encrpty)
        )

        # Ideally we would also search if the size is more than 1 but i am omitting here
        excute_statment = await self.db_session.execute(statement=statment)
        result = excute_statment.first()
        if result is None:
            return None
        return UserModel(id=result[0], username=result[2], name=result[1])

    async def get_user_by_id(self, id: int) -> UserModel:
        statement = select(User.id, User.name).filter(User.id == id)
        execute_result = await self.db_session.execute(statement=statement)
        result = execute_result.first()
        return UserModel(id=id, name=result[1], username="")

    async def store_user(self, user: UserModel, password: str) -> bool:
        input_password_encrpty = await encrpty_string(password)
        statement = insert(User).values(
            username=user.username,
            password=input_password_encrpty,
            name=user.name,
        )
        result = await self.db_session.execute(statement=statement)
        return True
