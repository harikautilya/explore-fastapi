
import pytest
from api.db.user import User, Token


user_data = [
	(
		{
			"id": 1,
			"username": "alice",
			"password": "secret",
			"name": "Alice",
		},
		User(id=1, username="alice", password="secret", name="Alice"),
	),
	(
		{
			"id": 2,
			"username": "bob",
			"password": "p@55",
			"name": "Bob",
		},
		User(id=2, username="bob", password="p@55", name="Bob"),
	),
]


token_data = [
	(
		{
			"id": 1,
			"user_id": 1,
			"token": "tok-123",
			"last_used": "2025-10-22T00:00:00Z",
		},
		Token(id=1, user_id=1, token="tok-123", last_used="2025-10-22T00:00:00Z"),
	),
]


@pytest.mark.parametrize("model_data, expected", user_data)
def test_user_create(model_data: dict, expected: User):
	created = User(**model_data)
	assert created.id == expected.id
	assert created.username == expected.username
	assert created.password == expected.password
	assert created.name == expected.name


@pytest.mark.parametrize("model_data, expected", token_data)
def test_token_create(model_data: dict, expected: Token):
	created = Token(**model_data)
	assert created.id == expected.id
	assert created.user_id == expected.user_id
	assert created.token == expected.token
	assert created.last_used == expected.last_used


def test_user_token_relationship_fields_exist():
	# Ensure dataclass fields exist and can be assigned lists (relationships are defined on ORM side)
	u = User(id=3, username="carol", password="pw", name="Carol")
	# tokens and notes are relationships; they should exist as attributes (SQLAlchemy will manage them at runtime)
	assert hasattr(u, "tokens")
	assert hasattr(u, "notes")
	# Assign simple list to tokens to mimic relationship behavior in-memory
	u.tokens = []
	u.notes = []
	assert isinstance(u.tokens, list)
	assert isinstance(u.notes, list)

