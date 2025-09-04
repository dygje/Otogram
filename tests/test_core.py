"""
Core system tests - Essential functionality only
"""

import pytest
from pydantic import ValidationError

from src.core.config import Settings
from src.core.database import Database


class TestConfig:
    """Test core configuration"""

    def test_default_settings(self) -> None:
        """Test basic settings work"""
        settings = Settings()
        assert settings.MONGO_URL == "mongodb://localhost:27017"
        assert settings.DB_NAME == "otogram"
        assert settings.LOG_LEVEL == "INFO"

    def test_phone_validation(self) -> None:
        """Test phone number validation"""
        # Valid
        settings = Settings(TELEGRAM_PHONE_NUMBER="+1234567890")
        assert settings.TELEGRAM_PHONE_NUMBER == "+1234567890"

        # Invalid
        with pytest.raises(ValidationError):
            Settings(TELEGRAM_PHONE_NUMBER="1234567890")

    def test_config_status(self) -> None:
        """Test configuration status check"""
        settings = Settings(
            TELEGRAM_API_ID=12345,
            TELEGRAM_API_HASH="hash",
            TELEGRAM_BOT_TOKEN="token",
            TELEGRAM_PHONE_NUMBER="+123456789",
        )
        assert settings.is_configured() is True


class TestDatabase:
    """Test database connectivity"""

    async def test_database_connection(self, test_database: Database) -> None:
        """Test database connects successfully"""
        assert test_database.client is not None
        assert test_database.db is not None

    async def test_health_check(self, test_database: Database) -> None:
        """Test database health check"""
        health = await test_database.health_check()
        assert health is True
