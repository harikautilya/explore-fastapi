from typing import List 
from dataclasses import dataclass
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import Base



@dataclass(repr=True)
class Note(Base):
    """
    The model class for the notes
    """

    __tablename__ = "tbl_note"

    id : Mapped[int] = mapped_column(primary_key=True, name="id")
    title : Mapped[str] = mapped_column(name="title")
    content : Mapped[str] = mapped_column(name="content")
    user_id: Mapped[int] = mapped_column(ForeignKey("tbl_user.id"))

    # relation ships
    user: Mapped["User"] = relationship(back_populates="notes")
    histories : Mapped[List["NoteHistory"]]  = relationship(back_populates="note")


@dataclass(repr=True)
class NoteHistory(Base):
    """
    The model class for the history of note changes
    """
    __tablename__ = "tbl_note_history"

    note_id : Mapped[int] = mapped_column(ForeignKey("tbl_note.id"), primary_key=True)
    update_at : Mapped[datetime] = mapped_column(primary_key=True)


    # relation ships
    note : Mapped["Note"] = relationship(back_populates="histories")



