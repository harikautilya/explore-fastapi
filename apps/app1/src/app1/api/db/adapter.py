from .base import SessionLocal
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import  async_sessionmaker, AsyncSession
from sqlalchemy import insert as insert_sql
from sqlalchemy import delete as delete_sql
from sqlalchemy import update as update_sql
from sqlalchemy import select as select_sql
from .base import Base

T = TypeVar("T", bound=Base)
K = TypeVar("K")


class DBOperations(ABC, Generic[T, K]):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def insert(self, model: T):
        pass

    @abstractmethod
    def update(self, model: T, **kwargs):
        pass

    @abstractmethod
    def delete(self, model: T):
        pass

    @abstractmethod
    def get(self, id: K) -> Optional[T]:
        pass

    @abstractmethod
    def filter(self, **kwargs) -> List[T]:
        pass


class SessionManagedDB(DBOperations[T, K]):

    def __init__(
        self,
        session_manager: sessionmaker[Session],
        model_class: Type[T],
    ) -> None:
        super().__init__()
        self.model_class = model_class
        self.session_manager = session_manager

    def insert(self, model: T):
        values = {
            c.key: getattr(model, c.key)
            for c in model.__table__.columns
            if getattr(model, c.key) is not None
        }
        statement = insert_sql(self.model_class).values(**values)
        with self.session_manager() as session:
            session.execute(statement=statement)
            session.commit()
        return model

    def update(self, model: T, **kwargs):
        with self.session_manager() as session:
            # Use the ID from the model instance to target the row
            stmt = (
                update_sql(self.model_class)
                .where(getattr(self.model_class, "id") == getattr(model, "id"))
                .values(**kwargs)
            )
            session.execute(stmt)
            session.commit()

    def delete(self, model: T):
        with self.session_manager() as session:
            stmt = delete_sql(self.model_class).where(
                getattr(self.model_class, "id") == getattr(model, "id")
            )
            session.execute(stmt)
            session.commit()

    def get(self, id: K) -> Optional[T]:
        with self.session_manager() as session:
            # select(T) returns rows, we use scalars() to get the object
            stmt = select_sql(self.model_class).where(
                getattr(self.model_class, "id") == id
            )
            result = session.execute(stmt)
            return result.scalar_one_or_none()
        raise Exception("Something went wrong")

    def filter(self, **kwargs) -> List[T]:
        with self.session_manager() as session:
            stmt = select_sql(self.model_class).filter_by(**kwargs)
            result = session.execute(stmt)
            return list(result.scalars().all())


class AsyncSessionManagedDB(DBOperations[T, K]):

    def __init__(
        self,
        session_manager: async_sessionmaker[AsyncSession],
        model_class: Type[T],
    ) -> None:
        super().__init__()
        self.model_class = model_class
        self.session_manager = session_manager

    async def insert(self, model: T):
        values = {
            c.key: getattr(model, c.key)
            for c in model.__table__.columns
            if getattr(model, c.key) is not None
        }
        statement = insert_sql(self.model_class).values(**values)
        async with self.session_manager() as session:
            await session.execute(statement=statement)
            await session.commit()
        return model

    async def update(self, model: T, **kwargs):
        async with self.session_manager() as session:
            # Use the ID from the model instance to target the row
            stmt = (
                update_sql(self.model_class)
                .where(getattr(self.model_class, "id") == getattr(model, "id"))
                .values(**kwargs)
            )
            await session.execute(stmt)
            await session.commit()

    async def delete(self, model: T):
        async with self.session_manager() as session:
            stmt = delete_sql(self.model_class).where(
                getattr(self.model_class, "id") == getattr(model, "id")
            )
            await session.execute(stmt)
            await session.commit()

    async def get(self, id: K) -> Optional[T]:
        async with self.session_manager() as session:
            # select(T) returns rows, we use scalars() to get the object
            stmt = select_sql(self.model_class).where(
                getattr(self.model_class, "id") == id
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        raise Exception("Something went wrong")

    async def filter(self, **kwargs) -> List[T]:
        async with self.session_manager() as session:
            stmt = select_sql(self.model_class).filter_by(**kwargs)
            result = await session.execute(stmt)
            return list(result.scalars().all())
