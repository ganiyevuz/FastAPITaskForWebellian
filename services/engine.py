from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from services.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=30
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True)  # noqa: type checking

AsyncScopedSession = async_scoped_session(async_session, scopefunc=current_task)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# Generic async context manager for sessions
@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()
