import sqlalchemy
import pytest


from api.db.note import Note, NoteHistory


note_data = [
    (
        {
            "id": 1,
            "title": "First",
            "content": "Hello world",
            "user_id": 1,
        },
        Note(id=1, title="First", content="Hello world", user_id=1),
    ),
    (
        {
            "id": 2,
            "title": "Second",
            "content": "Another note",
            "user_id": 2,
        },
        Note(id=2, title="Second", content="Another note", user_id=2),
    ),
]


history_data = [
    (
        {
            "note_id": 1,
            "update_at": None,  # allow None for simple equality check (dataclass will accept it)
        },
        NoteHistory(note_id=1, update_at=None),
    ),
]


@pytest.mark.parametrize("model_data, expected", note_data)
def test_note_create(model_data: dict, expected: Note):
    created = Note(**model_data)
    assert created.id == expected.id
    assert created.title == expected.title
    assert created.content == expected.content
    assert created.user_id == expected.user_id


@pytest.mark.parametrize("model_data, expected", history_data)
def test_note_history_create(model_data: dict, expected: NoteHistory):
    created = NoteHistory(**model_data)
    assert created.note_id == expected.note_id
    assert created.update_at == expected.update_at


def test_note_relationship_fields_exist():
    n = Note(id=3, title="t", content="c", user_id=3)
    assert hasattr(n, "user")
    assert hasattr(n, "histories")
    n.histories = []
    assert isinstance(n.histories, list)
