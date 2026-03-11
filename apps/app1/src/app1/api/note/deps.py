from typing import Annotated, Any
from fastapi import Depends

from .service import NoteService
from .adapter import NoteAdapter, NoteDbAdapter
from app1.api.db.base import SessionLocal
from app1.api.db.session import AsyncSessionManagedDB
from app1.api.db.note import Note


def get_note_adapter() -> NoteAdapter:
    """
    Returns a database-backed implementation of the NoteAdapter.
    """
    session  = AsyncSessionManagedDB[Note, int](session_manager=SessionLocal, model_class=Note)
    return NoteDbAdapter(db=session)


async def get_note_service(
    note_adapter: Annotated[NoteAdapter, Depends(get_note_adapter)],
) -> NoteService:
    """
    Returns an instance of the NoteService.
    """
    return NoteService.get_instance(
        note_adapter=note_adapter,
    )
