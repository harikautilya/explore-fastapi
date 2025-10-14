from dataclasses import dataclass
from api.core.model import CoreModel

@dataclass(repr=True, frozen=True,kw_only=True, eq=True)
class CredentailsModel(CoreModel):
    username : str
    password : str

@dataclass(repr=True, frozen=True,kw_only=True, eq=True)
class UserModel(CoreModel):
    id: int
    username : str
    name : str

@dataclass(repr=True, frozen=True,kw_only=True, eq=True)
class TokenModel(CoreModel):
    token : str
    user : UserModel | None