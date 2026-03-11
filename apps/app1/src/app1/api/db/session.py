from .base import SessionLocal
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import insert as insert_sql
from sqlalchemy import delete as delete_sql
from sqlalchemy import update as update_sql
from sqlalchemy import select as select_sql
from sqlalchemy import inspect
from sqlalchemy.orm import selectinload
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
    def delete(self, model: T) -> bool:
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

    def delete(self, model: T) -> bool:
        with self.session_manager() as session:
            stmt = delete_sql(self.model_class).where(
                getattr(self.model_class, "id") == getattr(model, "id")
            )
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0

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

        self._eager_loads = [
            getattr(self.model_class, r.key)
            for r in inspect(self.model_class).relationships
        ]

    async def insert(self, model: T):
        id = -1
        values = {
            c.key: getattr(model, c.key)
            for c in model.__table__.columns
            if getattr(model, c.key) is not None
        }
        pk_column = getattr(self.model_class, "id")
        statement = insert_sql(self.model_class).values(**values).returning(pk_column)
        async with self.session_manager() as session:
            result = await session.execute(statement=statement)
            id = result.scalar()
            await session.commit()
        return id

    async def update(self, model: T):
        async with self.session_manager() as session:
            # Use the ID from the model instance to target the row
            update_data = {
                c.key: getattr(model, c.key)
                for c in self.model_class.__table__.columns
                if c.key != "id"
            }
            stmt = (
                update_sql(self.model_class)
                .where(getattr(self.model_class, "id") == getattr(model, "id"))
                .values(**update_data)
            )
            result = await session.execute(stmt)
            await session.commit()

            if result.rowcount == 0:
                raise Exception("Updated operation failed")
        return model
        

    async def delete(self, **kwargs) -> bool:
        async with self.session_manager() as session:
                stmt = delete_sql(self.model_class)
                
                # Convert dictionary to SQL expressions
                for key, value in kwargs.items():
                    column = getattr(self.model_class, key)
                    stmt = stmt.where(column == value)

                result = await session.execute(stmt)
                await session.commit()
                return result.rowcount > 0

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

    # def _apply_eager_loading(self, stmt):
    #     """Automatically attaches selectinload for all relationships."""
    #     print("Here ==========>", [r.key for r in inspect(self.model_class).relationships])
    #     if self._eager_loads:
    #         return stmt.options(*[selectinload(prop) for prop in self._eager_loads])
    #     return stmt
