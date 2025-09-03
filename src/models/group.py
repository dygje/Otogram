"""
Group Models
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.models.base import BaseDocument


class Group(BaseDocument):
    """Group model for target groups"""

    group_id: Optional[str] = Field(None, description="Telegram group ID")
    group_username: Optional[str] = Field(None, description="Group username")
    group_link: Optional[str] = Field(None, description="Group link")
    group_title: Optional[str] = Field(None, description="Group title")
    is_active: bool = Field(default=True, description="Whether group is active")
    message_count: int = Field(default=0, description="Messages sent to this group")

    @field_validator("group_username")
    @classmethod
    def validate_username(cls, v):
        if v and not v.startswith("@"):
            return f"@{v}"
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_id": "-1001234567890",
                "group_username": "@example_group",
                "group_title": "Example Group",
                "is_active": True,
            }
        }
    )


class GroupCreate(BaseModel):
    """Model for creating groups"""

    group_identifier: str = Field(..., description="Group ID, username, or link")

    @field_validator("group_identifier")
    @classmethod
    def validate_identifier(cls, v):
        v = v.strip()

        # Group ID (negative number)
        if v.startswith("-") and v[1:].isdigit():
            return v

        # Username
        if v.startswith("@"):
            return v

        # Link
        if "t.me/" in v:
            return v

        # Assume username without @
        return f"@{v}"


class GroupBulkCreate(BaseModel):
    """Model for bulk creating groups"""

    identifiers: str = Field(..., description="Group identifiers (one per line)")

    def get_identifiers_list(self) -> list:
        """Parse identifiers into list"""
        result = []
        for line in self.identifiers.strip().split("\n"):
            line = line.strip()
            if line:
                # Process each identifier
                if line.startswith("-") and line[1:].isdigit():
                    result.append(line)
                elif line.startswith("@"):
                    result.append(line)
                elif "t.me/" in line:
                    result.append(line)
                else:
                    result.append(f"@{line}")
        return result
