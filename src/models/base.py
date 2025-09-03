"""
Base Models
"""

from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class BaseDocument(BaseModel):
    """Base document with common fields"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_timestamp(self):
        """Update the updated_at field"""
        self.updated_at = datetime.utcnow()

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
