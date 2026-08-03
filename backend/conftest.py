"""Pytest fixtures for CondoCombat backend tests."""

import os

os.environ.setdefault(
    "SECRET_KEY",
    "test-secret-key-for-tests-32chars-min!"
)

import pytest
import pytest_asyncio

from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy.pool import StaticPool

from app.database import Base


# Banco SQLite temporário para testes
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


engine_test = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)


AsyncSessionTest = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="function")
async def async_session():
    """
    Sessão real de banco para testes de models.
    """

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionTest() as session:
        yield session

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



@pytest.fixture
def mock_session():
    """
    Mock de AsyncSession para testes unitários de repository.

    Retorna AsyncMock para métodos async (commit, flush, etc.)
    e MagicMock para o Result de execute().
    """

    session = AsyncMock(spec=AsyncSession)

    result = MagicMock()

    result.scalar_one_or_none = MagicMock(
        return_value=None
    )

    scalars_mock = MagicMock()
    scalars_mock.all = MagicMock(
        return_value=[]
    )

    result.scalars = MagicMock(
        return_value=scalars_mock
    )

    session.execute = AsyncMock(
        return_value=result
    )

    session.add = MagicMock()
    session.add_all = MagicMock()

    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session.close = AsyncMock()
    session.flush = AsyncMock()

    return session