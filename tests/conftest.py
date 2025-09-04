"""
Simplified pytest configuration for personal project
"""

import asyncio
import os
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio

from src.core.config import settings
from src.core.database import Database


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_database() -> AsyncGenerator[Database, None]:
    """Test database fixture"""
    test_db_name = "otogram_test"
    original_db_name = settings.DB_NAME
    settings.DB_NAME = test_db_name

    db = Database()
    await db.connect()

    yield db

    # Cleanup
    await db.client.drop_database(test_db_name)
    await db.disconnect()
    settings.DB_NAME = original_db_name


@pytest.fixture(autouse=True)
def set_test_mode() -> Generator[None, None, None]:
    """Set test environment"""
    os.environ["TEST_MODE"] = "true"
    yield
    os.environ.pop("TEST_MODE", None)


@pytest.fixture
def mock_telegram_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock Telegram credentials"""
    monkeypatch.setattr(settings, "TELEGRAM_API_ID", 12345678)
    monkeypatch.setattr(settings, "TELEGRAM_API_HASH", "test_hash")
    monkeypatch.setattr(settings, "TELEGRAM_BOT_TOKEN", "123456:test_token")
    monkeypatch.setattr(settings, "TELEGRAM_PHONE_NUMBER", "+1234567890")