import pytest
from api.note.models import NoteModel
from dataclasses import FrozenInstanceError


def test_note_model():
    # Create a model and keyword only test
    note_model = NoteModel(
        id=1,
        title="Sample",
        content="C",
        user_id=1
    )
    deep_copy = note_model.copy()

    # Deep copy test
    assert deep_copy == note_model
    assert deep_copy is not note_model

    # model update test
    update_note_model  = note_model.copy(
        title="t"
    )
    assert deep_copy != update_note_model

    # Forzen test
    with pytest.raises(FrozenInstanceError) as exec:
        update_note_model.title = "T"

    # to str test
    str_repr = f"NoteModel(id={note_model.id}, title={note_model.title!r}, content={note_model.content!r}, user_id={note_model.user_id})"
    assert str(note_model) == str_repr