"""
Log Models
"""

from enum import Enum
from typing import Any, ClassVar

from pydantic import BaseModel, Field, ConfigDict

from src.models.base import BaseDocument


class LogType(str, Enum):
    """Log types"""

    SYSTEM = "system"
    MESSAGE_SENT = "message_sent"
    MESSAGE_FAILED = "message_failed"
    BLACKLIST_ADDED = "blacklist_added"
    CYCLE_STARTED = "cycle_started"
    CYCLE_COMPLETED = "cycle_completed"
    USER_ACTION = "user_action"


class LogLevel(str, Enum):
    """Log levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class Log(BaseDocument):
    """Log entry model"""

    log_type: LogType = Field(..., description="Log type")
    level: LogLevel = Field(default=LogLevel.INFO, description="Log level")
    message: str = Field(..., description="Log message")
    details: dict[str, Any] | None = Field(None, description="Additional details")
    group_id: str | None = Field(None, description="Related group ID")
    user_id: str | None = Field(None, description="Related user ID")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "log_type": "message_sent",
                "level": "info",
                "message": "Message sent successfully",
                "group_id": "-1001234567890",
            }
        }
    )


class LogCreate(BaseModel):
    """Model for creating logs"""

    log_type: LogType = Field(..., description="Log type")
    level: LogLevel = Field(default=LogLevel.INFO)
    message: str = Field(..., description="Log message")
    details: dict[str, Any] | None = Field(None)
    group_id: str | None = Field(None)
    user_id: str | None = Field(None)
