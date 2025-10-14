from typing import Annotated
from fastapi import Depends

from .service import NoteService
from .adapter import NoteAdapter, NoteDbAdapter

from api.db.base import get_db_session


def get_note_adapter(
    db_session: Annotated[any, Depends(get_db_session)],
) -> NoteAdapter:
    """
    Returns a database-backed implementation of the NoteAdapter.
    """
    return NoteDbAdapter(db=db_session)


async def get_note_service(
    note_adapter: Annotated[NoteAdapter, Depends(get_note_adapter)],
) -> NoteService:
    """
    Returns an instance of the NoteService.
    """
    return NoteService.get_instance(
        note_adapter=note_adapter,
    )
