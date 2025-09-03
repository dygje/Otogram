"""
Application Configuration
Enhanced with additional safety settings and validation
"""

from typing import Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Database Configuration
    MONGO_URL: str = Field(default="mongodb://localhost:27017")
    DB_NAME: str = Field(default="telegram_automation")

    # Telegram Credentials (Required)
    TELEGRAM_API_ID: Optional[int] = Field(default=None)
    TELEGRAM_API_HASH: Optional[str] = Field(default=None)
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None)
    TELEGRAM_PHONE_NUMBER: Optional[str] = Field(default=None)

    # System Settings
    LOG_LEVEL: str = Field(default="INFO")
    ENABLE_DEBUG: bool = Field(default=False)

    # Message Timing Settings
    MIN_MESSAGE_DELAY: int = Field(default=5, ge=1, le=60)
    MAX_MESSAGE_DELAY: int = Field(default=10, ge=1, le=60)
    MIN_CYCLE_DELAY_HOURS: float = Field(default=1.1, ge=0.1, le=24.0)
    MAX_CYCLE_DELAY_HOURS: float = Field(default=1.3, ge=0.1, le=24.0)

    # Safety & Limits
    MAX_GROUPS_PER_CYCLE: int = Field(default=50, ge=0, le=500)
    MAX_MESSAGES_PER_DAY: int = Field(default=1000, ge=0, le=10000)
    AUTO_CLEANUP_BLACKLIST: bool = Field(default=True)
    BLACKLIST_CLEANUP_INTERVAL: int = Field(default=24, ge=1, le=168)  # 1-168 hours

    # Directories
    SESSION_DIR: str = Field(default="sessions")
    LOG_DIR: str = Field(default="logs")

    # Development Settings (Optional)
    DEV_MODE: bool = Field(default=False)
    DEBUG_SQL: bool = Field(default=False)
    MOCK_TELEGRAM: bool = Field(default=False)
    TEST_MODE: bool = Field(default=False)

    @validator("TELEGRAM_API_ID", pre=True)
    def parse_api_id(cls, v):
        """Parse API ID from string or int"""
        if isinstance(v, str) and v.strip() == "":
            return None
        try:
            return int(v) if v is not None else None
        except (ValueError, TypeError):
            return None

    @validator("TELEGRAM_API_HASH", "TELEGRAM_BOT_TOKEN", "TELEGRAM_PHONE_NUMBER", pre=True)
    def parse_empty_strings(cls, v):
        """Convert empty strings to None"""
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

    @validator("TELEGRAM_PHONE_NUMBER")
    def validate_phone_number(cls, v):
        """Validate phone number format"""
        if v is not None and not v.startswith("+"):
            raise ValueError("Phone number must start with + (international format)")
        return v

    @validator("MAX_MESSAGE_DELAY")
    def validate_message_delays(cls, v, values):
        """Ensure max delay is greater than min delay"""
        min_delay = values.get("MIN_MESSAGE_DELAY", 5)
        if v <= min_delay:
            raise ValueError("MAX_MESSAGE_DELAY must be greater than MIN_MESSAGE_DELAY")
        return v

    @validator("MAX_CYCLE_DELAY_HOURS")
    def validate_cycle_delays(cls, v, values):
        """Ensure max cycle delay is greater than min cycle delay"""
        min_delay = values.get("MIN_CYCLE_DELAY_HOURS", 1.0)
        if v <= min_delay:
            raise ValueError("MAX_CYCLE_DELAY_HOURS must be greater than MIN_CYCLE_DELAY_HOURS")
        return v

    def is_configured(self) -> bool:
        """Check if all required Telegram credentials are provided"""
        return all(
            [
                self.TELEGRAM_API_ID,
                self.TELEGRAM_API_HASH,
                self.TELEGRAM_BOT_TOKEN,
                self.TELEGRAM_PHONE_NUMBER,
            ]
        )

    def get_credentials_status(self) -> dict:
        """Get status of credential configuration"""
        return {
            "api_id": self.TELEGRAM_API_ID is not None,
            "api_hash": self.TELEGRAM_API_HASH is not None,
            "bot_token": self.TELEGRAM_BOT_TOKEN is not None,
            "phone_number": self.TELEGRAM_PHONE_NUMBER is not None,
            "all_configured": self.is_configured(),
        }

    class Config:
        env_file = ".env"
        case_sensitive = True
        validate_assignment = True


# Global settings instance
settings = Settings()
