from abc import ABC, abstractmethod
from app1.api.db.note import Note
from .models import NoteModel
from app1.api.db.session import AsyncSessionManagedDB


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

    def __init__(self, db: AsyncSessionManagedDB):
        self.db_session = db

    async def create_note(self, note: NoteModel) -> NoteModel | None:
        note_db = Note(title=note.title, content=note.content, user_id=note.user_id)
        result = await self.db_session.insert(note_db)
        if result:
            return NoteModel(
                id=result,
                title=note.title,
                content=note.content,
                user_id=note.user_id,
            )
        return None

    async def delete_note(self, note_id: int, user_id: int) -> bool:
        return await self.db_session.delete(id=note_id, user_id=user_id)


    async def update_note(self, note: NoteModel) -> NoteModel | None:
        return  await self.db_session.update(note)


    async def get_notes_by_user_id(self, user_id: int) -> list[NoteModel]:
        results = await self.db_session.filter(user_id=user_id)
        return [
            NoteModel(
                id=note.id,
                title=note.title,
                content=note.content,
                user_id=note.user_id,
            )
            for note in results
        ]
