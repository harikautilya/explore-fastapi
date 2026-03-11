from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from contextlib import asynccontextmanager

SQL_URL = "sqlite+aiosqlite:///sample.db"

# Create async engine
engine = create_async_engine(SQL_URL, echo=True)

# Create async sessionmaker
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Dependency for FastAPI
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
        await session.commit()

# Base class for models
class Base(DeclarativeBase):
    pass
