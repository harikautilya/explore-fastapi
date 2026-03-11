from .models import NoteModel
from .adapter import NoteAdapter


class NoteService:
    """
    Service class to handle note-related business logic.
    """

    @staticmethod
    def get_instance(note_adapter: NoteAdapter):
        """
        Get an instance of the NoteService.
        """
        return NoteService(note_adapter=note_adapter)

    def __init__(self, note_adapter: NoteAdapter):
        self.note_adapter = note_adapter

    async def create_note(
        self,
        title: str,
        content: str,
        user_id: int,
    ) -> NoteModel | None:
        """
        Create a new note.
        """
        note_to_create = NoteModel(id=0, title=title, content=content, user_id=user_id)
        return await self.note_adapter.create_note(note=note_to_create)

    async def delete_note(self, note_id: int, user_id: int) -> bool:
        """
        Delete a note.
        """
        return await self.note_adapter.delete_note(note_id=note_id, user_id=user_id)

    async def update_note(
        self,
        note_id: int,
        title: str,
        content: str,
        user_id: int,
    ) -> NoteModel | None:
        """
        Update an existing note.
        """
        note_to_update = NoteModel(
            id=note_id, title=title, content=content, user_id=user_id
        )
        return await self.note_adapter.update_note(note=note_to_update)

    async def get_notes(self, user_id: int) -> list[NoteModel]:
        """
        Get all notes for a user.
        """
        return await self.note_adapter.get_notes_by_user_id(user_id=user_id)
