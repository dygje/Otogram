"""
Tests for configuration module
"""

import pytest
from pydantic import ValidationError

from src.core.config import Settings
from src.core.constants import (
    DEFAULT_MAX_GROUPS_PER_CYCLE,
    DEFAULT_MAX_MESSAGE_DELAY,
    DEFAULT_MIN_MESSAGE_DELAY,
    TEST_API_ID,
    TEST_CYCLE_DELAY_MAX,
    TEST_CYCLE_DELAY_MIN,
)


class TestSettings:
    """Test Settings class"""

    def test_default_settings(self) -> None:
        """Test default settings initialization"""
        settings = Settings()

        assert settings.MONGO_URL == "mongodb://localhost:27017"
        assert settings.DB_NAME == "otogram"
        assert settings.LOG_LEVEL == "INFO"
        assert settings.MIN_MESSAGE_DELAY == DEFAULT_MIN_MESSAGE_DELAY
        assert settings.MAX_MESSAGE_DELAY == DEFAULT_MAX_MESSAGE_DELAY
        assert settings.MAX_GROUPS_PER_CYCLE == DEFAULT_MAX_GROUPS_PER_CYCLE

    def test_api_id_parsing(self) -> None:
        """Test API ID parsing from different formats"""
        # String number
        settings = Settings(TELEGRAM_API_ID=str(TEST_API_ID))  # type: ignore[arg-type]
        assert settings.TELEGRAM_API_ID == TEST_API_ID

        # Integer
        settings = Settings(TELEGRAM_API_ID=TEST_API_ID)
        assert settings.TELEGRAM_API_ID == TEST_API_ID

        # Empty string
        settings = Settings(TELEGRAM_API_ID="")  # type: ignore[arg-type]
        assert settings.TELEGRAM_API_ID is None

        # None
        settings = Settings(TELEGRAM_API_ID=None)
        assert settings.TELEGRAM_API_ID is None

    def test_phone_number_validation(self) -> None:
        """Test phone number validation"""
        # Valid international format
        settings = Settings(TELEGRAM_PHONE_NUMBER="+1234567890")
        assert settings.TELEGRAM_PHONE_NUMBER == "+1234567890"

        # Invalid format (without +)
        with pytest.raises(ValidationError) as exc_info:
            Settings(TELEGRAM_PHONE_NUMBER="1234567890")

        assert "Phone number must start with +" in str(exc_info.value)

    def test_delay_validation(self) -> None:
        """Test message delay validation"""
        # Valid delays
        settings = Settings(
            MIN_MESSAGE_DELAY=DEFAULT_MIN_MESSAGE_DELAY, MAX_MESSAGE_DELAY=DEFAULT_MAX_MESSAGE_DELAY
        )
        assert settings.MIN_MESSAGE_DELAY == DEFAULT_MIN_MESSAGE_DELAY
        assert settings.MAX_MESSAGE_DELAY == DEFAULT_MAX_MESSAGE_DELAY

        # Invalid delays (max < min)
        with pytest.raises(ValidationError) as exc_info:
            Settings(MIN_MESSAGE_DELAY=10, MAX_MESSAGE_DELAY=5)

        assert "MAX_MESSAGE_DELAY must be greater than MIN_MESSAGE_DELAY" in str(exc_info.value)

    def test_cycle_delay_validation(self) -> None:
        """Test cycle delay validation"""
        # Valid cycle delays
        settings = Settings(
            MIN_CYCLE_DELAY_HOURS=TEST_CYCLE_DELAY_MIN, MAX_CYCLE_DELAY_HOURS=TEST_CYCLE_DELAY_MAX
        )
        assert settings.MIN_CYCLE_DELAY_HOURS == TEST_CYCLE_DELAY_MIN
        assert settings.MAX_CYCLE_DELAY_HOURS == TEST_CYCLE_DELAY_MAX

        # Invalid cycle delays
        with pytest.raises(ValidationError) as exc_info:
            Settings(
                MIN_CYCLE_DELAY_HOURS=TEST_CYCLE_DELAY_MAX,
                MAX_CYCLE_DELAY_HOURS=TEST_CYCLE_DELAY_MIN,
            )

        assert "MAX_CYCLE_DELAY_HOURS must be greater than MIN_CYCLE_DELAY_HOURS" in str(
            exc_info.value
        )

    def test_is_configured(self, mock_telegram_credentials: None) -> None:
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

    def test_get_credentials_status(self) -> None:
        """Test credentials status report"""
        # Test with no credentials
        settings = Settings(
            TELEGRAM_API_ID=None,
            TELEGRAM_API_HASH=None,
            TELEGRAM_BOT_TOKEN=None,
            TELEGRAM_PHONE_NUMBER=None,
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
        )

        status = settings.get_credentials_status()
        assert status["api_id"] is True
        assert status["api_hash"] is True
        assert status["bot_token"] is True
        assert status["phone_number"] is True
        assert status["all_configured"] is True
