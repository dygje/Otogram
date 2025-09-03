"""
Base Models
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseDocument(BaseModel):
    """Base document with common fields"""

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_timestamp(self):
        """Update the updated_at field"""
        self.updated_at = datetime.utcnow()
