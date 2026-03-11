import asyncio
from unittest.mock import MagicMock, AsyncMock
import pytest

from api.note.service import NoteService
from api.note.models import NoteModel


DUMMY_USER_ID = 1


@pytest.fixture
def adapter_mock():
    m = MagicMock()
    # make async methods
    m.create_note = AsyncMock()
    m.update_note = AsyncMock()
    m.delete_note = AsyncMock()
    m.get_notes_by_user_id = AsyncMock()
    return m


def test_note_service_create_note(adapter_mock):
    note_service = NoteService.get_instance(note_adapter=adapter_mock)

    adapter_mock.create_note.return_value = NoteModel(
        id=1, title="t", content="C", user_id=DUMMY_USER_ID
    )

    result = asyncio.run(
        note_service.create_note(title="t", content="C", user_id=DUMMY_USER_ID)
    )

    adapter_mock.create_note.assert_awaited_once()
    assert isinstance(result, NoteModel)
    assert result.title == "t"


def test_note_service_update_note(adapter_mock):
    note_service = NoteService.get_instance(note_adapter=adapter_mock)

    adapter_mock.update_note.return_value = NoteModel(
        id=1, title="t2", content="C2", user_id=DUMMY_USER_ID
    )

    result = asyncio.run(
        note_service.update_note(
            note_id=1, title="t2", content="C2", user_id=DUMMY_USER_ID
        )
    )

    adapter_mock.update_note.assert_awaited_once()
    assert result.title == "t2"


def test_note_service_delete_note(adapter_mock):
    note_service = NoteService.get_instance(note_adapter=adapter_mock)

    adapter_mock.delete_note.return_value = True

    result = asyncio.run(note_service.delete_note(note_id=1, user_id=DUMMY_USER_ID))

    adapter_mock.delete_note.assert_awaited_once_with(note_id=1, user_id=DUMMY_USER_ID)
    assert result is True


def test_note_service_get_notes(adapter_mock):
    note_service = NoteService.get_instance(note_adapter=adapter_mock)

    adapter_mock.get_notes_by_user_id.return_value = [
        NoteModel(id=1, title="t", content="C", user_id=DUMMY_USER_ID)
    ]

    result = asyncio.run(note_service.get_notes(user_id=DUMMY_USER_ID))

    adapter_mock.get_notes_by_user_id.assert_awaited_once_with(user_id=DUMMY_USER_ID)
    assert isinstance(result, list)
    assert result[0].user_id == DUMMY_USER_ID
