from ..adapter.user import UserAdapter
from ..models import UserModel
from ..exceptions import InvalidUserDetails


class UserService:
    """
    User service to handle user related operations
    """

    @staticmethod
    def get_instance(user_adapter: UserAdapter):
        return UserService(user_adapter=user_adapter)

    def __init__(
        self,
        user_adapter: UserAdapter,
    ):
        self.user_adapter = user_adapter

    async def create_user(
        self,
        username: str,
        password: str,
        name: str,
    ):
        """
        Create user
        """
        user_model: UserModel = UserModel(name=name, username=username, id=-1)
        is_success = await self.user_adapter.store_user(
            user=user_model, password=password
        )
        if not is_success:
            ## This is idealy the correct place but i am just exploring how exception handling works
            ## Just created a dummy exception case to understand
            raise InvalidUserDetails("Invalid user details")

    async def get_user_by_id(self, id: int) -> UserModel:
        return await self.user_adapter.get_user_by_id(id=id)
