from ..models import CredentailsModel, UserModel, TokenModel
from ..adapter import UserAdapter, TokenAdapter
from ..exceptions import InvalidCredentialsException
from ..utils.string import generate_random_string


class TokenService:
    """
    Service class to handle authetication and token generation
    """

    @staticmethod
    def get_instance(
        user_adapter: UserAdapter,
        token_adapter: TokenAdapter,
    ):
        """
        Generate instance of the Token service
        """
        return TokenService(
            user_adapter=user_adapter,
            token_adapter=token_adapter,
        )

    def __init__(
        self,
        user_adapter: UserAdapter,
        token_adapter: TokenAdapter,
    ):
        self.user_adapter = user_adapter
        self.token_adapter = token_adapter

    async def generate_token(self, username: str, password: str) -> str:
        creds: CredentailsModel = CredentailsModel(username=username, password=password)
        user = await self._verify_user_creds(creds=creds)
        token = await self._generate_token_from_creds(creds=creds, user=user)
        return token

    async def _verify_user_creds(self, creds: CredentailsModel) -> UserModel:
        user = await self.user_adapter.get_user_by_creds(creds=creds)
        if not user:
            raise InvalidCredentialsException("User not found")
        return user

    async def _generate_token_from_creds(
        self,
        creds: CredentailsModel,
        user: UserModel,
    ) -> str:
        token_model : TokenModel = TokenModel(
            user=user,
            token=generate_random_string()
        )
        is_stored = await self.token_adapter.store_token(
            token=token_model
        )
        if is_stored:
            return token_model.token
        raise Exception("Something went wrong")
