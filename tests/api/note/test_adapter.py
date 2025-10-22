import asyncio
import pytest
from api.db.note import Note
from api.note.models import NoteModel
from api.note.adapter import NoteDbAdapter
from sqlalchemy.orm import Session
from sqlalchemy import select
import asyncio

DUMMY_USER_ID = 1

note_create = [
    (
        NoteModel(id=-1, title="t", content="C", user_id=DUMMY_USER_ID),
        Note(title="t", content="C", user_id=DUMMY_USER_ID),
    )
]

note_update = [
    (
        NoteModel(id=-1, title="t", content="C", user_id=DUMMY_USER_ID),
        NoteModel(id=1, title="t2", content="C2", user_id=DUMMY_USER_ID),
        Note(id=1, title="t2", content="C2", user_id=DUMMY_USER_ID),
    )
]

note_delete = [
    NoteModel(id=-1, title="t", content="C", user_id=DUMMY_USER_ID),
]


@pytest.mark.parametrize("note_model, note", note_create)
def test_create_note(inmemory_db_session: Session, note_model: NoteModel, note: Note):
    # Use the provided in-memory session; insert a note and verify adapter
    adapter = NoteDbAdapter(db=inmemory_db_session)

    returned_result = asyncio.run(adapter.create_note(note=note_model))

    assert returned_result.content == note.content
    assert returned_result.title == note.title
    assert returned_result.user_id == note.user_id


@pytest.mark.parametrize("note_model, update_note, note", note_update)
def test_update_note(
    inmemory_db_session: Session,
    note_model: NoteModel,
    update_note: NoteModel,
    note: Note,
):
    # Use the provided in-memory session; insert a note and verify adapter
    adapter = NoteDbAdapter(db=inmemory_db_session)

    asyncio.run(adapter.create_note(note=note_model))

    returned_result = asyncio.run(adapter.update_note(update_note))

    assert returned_result.content == note.content
    assert returned_result.title == note.title
    assert returned_result.user_id == note.user_id


@pytest.mark.parametrize("note_model", note_delete)
def test_delete_note(inmemory_db_session: Session, note_model: NoteModel):
    adapter = NoteDbAdapter(db=inmemory_db_session)

    created = asyncio.run(adapter.create_note(note=note_model))

    statement = select(Note).where(Note.id == created.id)
    result = inmemory_db_session.execute(statement).scalar_one_or_none()
    assert result is not None

    # delete the created note and verify it's removed from the session
    asyncio.run(adapter.delete_note(note_id=created.id, user_id=DUMMY_USER_ID))

    result = inmemory_db_session.execute(statement).scalar_one_or_none()
    assert result is None
