"""
Configuration Models
"""

from typing import Union, Optional
from pydantic import BaseModel, Field
from src.models.base import BaseDocument


class Configuration(BaseDocument):
    """Configuration model"""

    key: str = Field(..., description="Configuration key")
    value: Union[str, int, float, bool] = Field(..., description="Configuration value")
    value_type: str = Field(..., description="Type of value")
    description: Optional[str] = Field(None, description="Description")
    category: str = Field(default="general", description="Category")
    is_editable: bool = Field(default=True, description="Can be edited")

    def get_typed_value(self):
        """Get value with proper type"""
        if self.value_type == "int":
            return int(self.value)
        elif self.value_type == "float":
            return float(self.value)
        elif self.value_type == "bool":
            return str(self.value).lower() in ("true", "1", "yes")
        return str(self.value)


class ConfigUpdate(BaseModel):
    """Model for updating configuration"""

    value: Union[str, int, float, bool] = Field(..., description="New value")


# Default configurations
DEFAULT_CONFIGS = [
    {
        "key": "min_message_delay",
        "value": 5,
        "value_type": "int",
        "description": "Minimum delay between messages (seconds)",
        "category": "messaging",
    },
    {
        "key": "max_message_delay",
        "value": 10,
        "value_type": "int",
        "description": "Maximum delay between messages (seconds)",
        "category": "messaging",
    },
    {
        "key": "min_cycle_delay_hours",
        "value": 1.1,
        "value_type": "float",
        "description": "Minimum delay between cycles (hours)",
        "category": "messaging",
    },
    {
        "key": "max_cycle_delay_hours",
        "value": 1.3,
        "value_type": "float",
        "description": "Maximum delay between cycles (hours)",
        "category": "messaging",
    },
    {
        "key": "auto_cleanup_blacklist",
        "value": True,
        "value_type": "bool",
        "description": "Auto cleanup expired blacklist entries",
        "category": "system",
    },
]
