"""
Message Models
"""

from typing import ClassVar

from pydantic import BaseModel, Field, ConfigDict

from src.models.base import BaseDocument


class Message(BaseDocument):
    """Message model for broadcast messages"""

    content: str = Field(..., description="Message content (text only)")
    is_active: bool = Field(default=True, description="Whether message is active")
    usage_count: int = Field(default=0, description="Times this message was used")

    class Config:
        json_schema_extra: ClassVar = {
            "example": {
                "content": "Hello! This is a broadcast message.",
                "is_active": True,
                "usage_count": 0,
            }
        }


class MessageCreate(BaseModel):
    """Model for creating messages"""

    content: str = Field(..., min_length=1, max_length=4096, description="Message content")


class MessageUpdate(BaseModel):
    """Model for updating messages"""

    content: str | None = Field(default=None, min_length=1, max_length=4096)
    is_active: bool | None = Field(default=None)
