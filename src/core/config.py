"""
Application Configuration
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    MONGO_URL: str = Field(default="mongodb://localhost:27017")
    DB_NAME: str = Field(default="telegram_automation")
    
    # Telegram Credentials
    TELEGRAM_API_ID: Optional[int] = Field(default=None)
    TELEGRAM_API_HASH: Optional[str] = Field(default=None)
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None)
    TELEGRAM_PHONE_NUMBER: Optional[str] = Field(default=None)
    
    # System Settings
    LOG_LEVEL: str = Field(default="INFO")
    ENABLE_DEBUG: bool = Field(default=False)
    
    # Message Settings
    MIN_MESSAGE_DELAY: int = Field(default=5)
    MAX_MESSAGE_DELAY: int = Field(default=10)
    MIN_CYCLE_DELAY_HOURS: float = Field(default=1.1)
    MAX_CYCLE_DELAY_HOURS: float = Field(default=1.3)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()