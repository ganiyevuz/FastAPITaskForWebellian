import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from main import app
from services.engine import get_session


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    return engine


@pytest_asyncio.fixture(scope="function")
async def db_session(engine):
    async_session = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_session] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
