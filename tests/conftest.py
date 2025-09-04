"""
Pytest configuration and fixtures
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
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_database() -> AsyncGenerator[Database, None]:
    """Test database fixture"""
    # Use test database
    test_db_name = "telegram_automation_test"
    original_db_name = settings.DB_NAME
    settings.DB_NAME = test_db_name

    # Create test database instance
    db = Database()
    await db.connect()

    yield db

    # Cleanup - drop test database
    await db.client.drop_database(test_db_name)
    await db.disconnect()

    # Restore original database name
    settings.DB_NAME = original_db_name


@pytest.fixture(autouse=True)
def set_test_mode() -> Generator[None, None, None]:
    """Set test mode environment variable"""
    os.environ["TEST_MODE"] = "true"
    yield
    os.environ.pop("TEST_MODE", None)


@pytest.fixture
def mock_telegram_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock Telegram credentials for testing"""
    monkeypatch.setattr(settings, "TELEGRAM_API_ID", 12345678)
    monkeypatch.setattr(settings, "TELEGRAM_API_HASH", "test_api_hash")
    monkeypatch.setattr(settings, "TELEGRAM_BOT_TOKEN", "123456:test_bot_token")
    monkeypatch.setattr(settings, "TELEGRAM_PHONE_NUMBER", "+1234567890")
