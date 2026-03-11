from typing import List
from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .note import Note

@dataclass(repr=True)
class User(Base):
    """
    This is the model class for the user table.
    """

    __tablename__ = "tbl_user"

    id: Mapped[int] = mapped_column(primary_key=True, name="id")
    username: Mapped[str] = mapped_column(name="username")
    password: Mapped[str] = mapped_column(name="password")
    name: Mapped[str] = mapped_column(name="name")

    # Relationships
    tokens: Mapped[List["Token"]] = relationship(back_populates="user")
    notes: Mapped[List["Note"]] = relationship(back_populates="user")


@dataclass(repr=True)
class Token(Base):
    """
    This is the model class to maintain token provided to the user.
    """

    __tablename__ = "tbl_user_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, name="id")
    user_id: Mapped[int] = mapped_column(ForeignKey("tbl_user.id"))
    token: Mapped[str] = mapped_column(name="token")
    last_used: Mapped[str] = mapped_column(name="last_used")

    # Relationships
    user: Mapped["User"] = relationship(back_populates="tokens")


