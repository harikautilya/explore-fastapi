from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete, update, select
from api.db.note import Note
from .models import NoteModel


class NoteAdapter(ABC):
    """
    Abstract base class for a note adapter.
    """

    @abstractmethod
    async def create_note(self, note: NoteModel) -> NoteModel | None:
        """
        Create a new note.
        """
        pass

    @abstractmethod
    async def delete_note(self, note_id: int, user_id: int) -> bool:
        """
        Delete a note by its ID.
        """
        pass

    @abstractmethod
    async def update_note(self, note: NoteModel) -> NoteModel | None:
        """
        Update a note.
        """
        pass

    @abstractmethod
    async def get_notes_by_user_id(self, user_id: int) -> list[NoteModel]:
        """
        Get all notes for a given user.
        """
        pass


class NoteDbAdapter(NoteAdapter):
    """
    Database-backed implementation of the NoteAdapter.
    """

    def __init__(self, db: AsyncSession):
        self.db_session = db

    async def create_note(self, note: NoteModel) -> NoteModel | None:
        statement = (
            insert(Note)
            .values(title=note.title, content=note.content, user_id=note.user_id)
            .returning(Note.id)
        )
        execute_result = await self.db_session.execute(statement)
        result = execute_result.scalar_one_or_none()
        if result:
            return NoteModel(
                id=result,
                title=note.title,
                content=note.content,
                user_id=note.user_id,
            )
        return None

    async def delete_note(self, note_id: int, user_id: int) -> bool:
        statement = delete(Note).where(Note.id == note_id, Note.user_id == user_id)
        result = await self.db_session.execute(statement)
        return result.rowcount > 0

    async def update_note(self, note: NoteModel) -> NoteModel | None:
        statement = (
            update(Note)
            .where(Note.id == note.id, Note.user_id == note.user_id)
            .values(title=note.title, content=note.content)
            .returning(Note.id)
        )
        execute_result = await self.db_session.execute(statement)
        result = execute_result.scalar_one_or_none()
        if result:
            return note
        return None

    async def get_notes_by_user_id(self, user_id: int) -> list[NoteModel]:
        statement = select(Note).where(Note.user_id == user_id)
        execute_result = await self.db_session.execute(statement)
        results = execute_result.scalars().all()
        return [
            NoteModel(
                id=note.id,
                title=note.title,
                content=note.content,
                user_id=note.user_id,
            )
            for note in results
        ]
