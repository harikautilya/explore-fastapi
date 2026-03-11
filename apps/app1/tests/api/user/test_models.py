import pytest
from dataclasses import FrozenInstanceError

from api.user.models import UserModel, CredentailsModel, TokenModel


def test_user_model():
    # Create a model and keyword only test
    user = UserModel(id=1, username="bob", name="Bob")
    deep_copy = user.copy()

    # Deep copy test
    assert deep_copy == user
    assert deep_copy is not user

    # model update test
    updated = user.copy(username="bobby")
    assert deep_copy != updated

    # Forzen test
    with pytest.raises(FrozenInstanceError):
        updated.username = "x"

    # to str test
    str_repr = f"UserModel(id={user.id}, username={user.username!r}, name={user.name!r})"
    assert str(user) == str_repr


def test_credentials_model():
    # Create a model and keyword only test
    creds = CredentailsModel(username="u", password="p")
    copy = creds.copy()

    # Deep copy test
    assert copy == creds

    # Forzen test
    with pytest.raises(FrozenInstanceError):
        copy.password = "x"


def test_token_model():
    # Create a model and keyword only test
    user = UserModel(id=2, username="a", name="A")
    token = TokenModel(token="t", user=user)
    copy = token.copy()

    # Deep copy test
    assert copy == token
    assert copy is not token

    # model update test
    updated = token.copy(token="t2")
    assert copy != updated

    # Forzen test
    with pytest.raises(FrozenInstanceError):
        updated.token = "x"

    # to str test
    str_repr = f"TokenModel(token={token.token!r}, user={token.user!r})"
    assert str(token) == str_repr
