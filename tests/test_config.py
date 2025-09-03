"""
Tests for configuration module
"""

import pytest
from pydantic import ValidationError

from src.core.config import Settings
from src.core.constants import (
    DEFAULT_MIN_MESSAGE_DELAY,
    DEFAULT_MAX_MESSAGE_DELAY,
    DEFAULT_MAX_GROUPS_PER_CYCLE,
    TEST_API_ID,
    DEFAULT_MIN_CYCLE_DELAY_HOURS,
    DEFAULT_MAX_CYCLE_DELAY_HOURS,
)


class TestSettings:
    """Test Settings class"""

    def test_default_settings(self):
        """Test default settings initialization"""
        settings = Settings()

        assert settings.MONGO_URL == "mongodb://localhost:27017"
        assert settings.DB_NAME == "otogram"
        assert settings.LOG_LEVEL == "INFO"
        assert settings.MIN_MESSAGE_DELAY == DEFAULT_MIN_MESSAGE_DELAY
        assert settings.MAX_MESSAGE_DELAY == DEFAULT_MAX_MESSAGE_DELAY
        assert settings.MAX_GROUPS_PER_CYCLE == DEFAULT_MAX_GROUPS_PER_CYCLE

    def test_api_id_parsing(self):
        """Test API ID parsing from different formats"""
        # String number
        settings = Settings(TELEGRAM_API_ID=str(TEST_API_ID))
        assert settings.TELEGRAM_API_ID == TEST_API_ID

        # Integer
        settings = Settings(TELEGRAM_API_ID=TEST_API_ID)
        assert settings.TELEGRAM_API_ID == TEST_API_ID

        # Empty string
        settings = Settings(TELEGRAM_API_ID="")
        assert settings.TELEGRAM_API_ID is None

        # None
        settings = Settings(TELEGRAM_API_ID=None)
        assert settings.TELEGRAM_API_ID is None

    def test_phone_number_validation(self):
        """Test phone number validation"""
        # Valid international format
        settings = Settings(TELEGRAM_PHONE_NUMBER="+1234567890")
        assert settings.TELEGRAM_PHONE_NUMBER == "+1234567890"

        # Invalid format (without +)
        with pytest.raises(ValidationError) as exc_info:
            Settings(TELEGRAM_PHONE_NUMBER="1234567890")

        assert "Phone number must start with +" in str(exc_info.value)

    def test_delay_validation(self):
        """Test message delay validation"""
        # Valid delays
        settings = Settings(MIN_MESSAGE_DELAY=DEFAULT_MIN_MESSAGE_DELAY, MAX_MESSAGE_DELAY=DEFAULT_MAX_MESSAGE_DELAY)
        assert settings.MIN_MESSAGE_DELAY == DEFAULT_MIN_MESSAGE_DELAY
        assert settings.MAX_MESSAGE_DELAY == DEFAULT_MAX_MESSAGE_DELAY

        # Invalid delays (max < min)
        with pytest.raises(ValidationError) as exc_info:
            Settings(MIN_MESSAGE_DELAY=10, MAX_MESSAGE_DELAY=5)

        assert "MAX_MESSAGE_DELAY must be greater than MIN_MESSAGE_DELAY" in str(exc_info.value)

    def test_cycle_delay_validation(self):
        """Test cycle delay validation"""
        # Valid cycle delays
        settings = Settings(MIN_CYCLE_DELAY_HOURS=1.0, MAX_CYCLE_DELAY_HOURS=2.0)
        assert settings.MIN_CYCLE_DELAY_HOURS == 1.0
        assert settings.MAX_CYCLE_DELAY_HOURS == 2.0

        # Invalid cycle delays
        with pytest.raises(ValidationError) as exc_info:
            Settings(MIN_CYCLE_DELAY_HOURS=2.0, MAX_CYCLE_DELAY_HOURS=1.0)

        assert "MAX_CYCLE_DELAY_HOURS must be greater than MIN_CYCLE_DELAY_HOURS" in str(
            exc_info.value
        )

    def test_is_configured(self, mock_telegram_credentials):
        """Test configuration status check"""
        settings = Settings()

        # Mock complete configuration
        settings.TELEGRAM_API_ID = 12345678
        settings.TELEGRAM_API_HASH = "test_hash"
        settings.TELEGRAM_BOT_TOKEN = "123456:test_token"
        settings.TELEGRAM_PHONE_NUMBER = "+1234567890"

        assert settings.is_configured() is True

        # Incomplete configuration
        settings.TELEGRAM_API_ID = None
        assert settings.is_configured() is False

    def test_get_credentials_status(self):
        """Test credentials status report"""
        # Test with no credentials
        settings = Settings(
            TELEGRAM_API_ID=None,
            TELEGRAM_API_HASH=None,
            TELEGRAM_BOT_TOKEN=None,
            TELEGRAM_PHONE_NUMBER=None,
            _env_file=None,  # Don't load from .env file
        )

        status = settings.get_credentials_status()
        assert status["all_configured"] is False
        assert status["api_id"] is False
        assert status["api_hash"] is False
        assert status["bot_token"] is False
        assert status["phone_number"] is False

        # Test with all credentials
        settings = Settings(
            TELEGRAM_API_ID=12345678,
            TELEGRAM_API_HASH="test_hash",
            TELEGRAM_BOT_TOKEN="123456789:ABC-DEF...",
            TELEGRAM_PHONE_NUMBER="+1234567890",
            _env_file=None,
        )

        status = settings.get_credentials_status()
        assert status["api_id"] is True
        assert status["api_hash"] is True
        assert status["bot_token"] is False
        assert status["phone_number"] is False
        assert status["all_configured"] is False
