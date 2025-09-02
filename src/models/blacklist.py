"""
Blacklist Models
"""
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from src.models.base import BaseDocument


class BlacklistType(str, Enum):
    """Blacklist types"""
    PERMANENT = "permanent"
    TEMPORARY = "temporary"


class BlacklistReason(str, Enum):
    """Blacklist reasons"""
    
    # Permanent errors
    CHAT_FORBIDDEN = "ChatForbidden"
    CHAT_ID_INVALID = "ChatIdInvalid"
    USER_BLOCKED = "UserBlocked"
    PEER_ID_INVALID = "PeerIdInvalid"
    CHANNEL_INVALID = "ChannelInvalid"
    USER_BANNED_IN_CHANNEL = "UserBannedInChannel"
    CHAT_WRITE_FORBIDDEN = "ChatWriteForbidden"
    CHAT_RESTRICTED = "ChatRestricted"
    
    # Temporary errors
    SLOW_MODE_WAIT = "SlowModeWait"
    FLOOD_WAIT = "FloodWait"
    
    # Manual
    MANUAL = "Manual"


class Blacklist(BaseDocument):
    """Blacklist entry model"""
    
    group_id: str = Field(..., description="Group ID")
    group_identifier: Optional[str] = Field(None, description="Group username/link")
    blacklist_type: BlacklistType = Field(..., description="Blacklist type")
    reason: BlacklistReason = Field(..., description="Reason for blacklisting")
    expires_at: Optional[datetime] = Field(
        None, description="Expiration time (temporary only)"
    )
    duration_seconds: Optional[int] = Field(None, description="Duration in seconds")
    error_message: Optional[str] = Field(None, description="Original error message")
    
    @property
    def is_expired(self) -> bool:
        """Check if temporary blacklist expired"""
        if self.blacklist_type == BlacklistType.PERMANENT:
            return False
        
        if not self.expires_at:
            return True
        
        return datetime.utcnow() >= self.expires_at
    
    @property
    def time_remaining(self) -> Optional[timedelta]:
        """Get remaining time for temporary blacklist"""
        if self.blacklist_type == BlacklistType.PERMANENT or not self.expires_at:
            return None
        
        now = datetime.utcnow()
        if now >= self.expires_at:
            return None
            
        return self.expires_at - now
    
    class Config:
        json_schema_extra = {
            "example": {
                "group_id": "-1001234567890",
                "blacklist_type": "temporary",
                "reason": "FloodWait",
                "duration_seconds": 3600
            }
        }


class BlacklistCreate(BaseModel):
    """Model for creating blacklist entries"""
    
    group_id: str = Field(..., description="Group ID")
    group_identifier: Optional[str] = Field(None)
    blacklist_type: BlacklistType = Field(..., description="Blacklist type")
    reason: BlacklistReason = Field(..., description="Reason")
    duration_seconds: Optional[int] = Field(None, description="Duration for temporary")
    error_message: Optional[str] = Field(None)


def determine_blacklist_from_error(
    error_msg: str
) -> tuple[BlacklistType, BlacklistReason]:
    """Determine blacklist type and reason from error message"""
    
    error_lower = error_msg.lower()
    
    # Permanent errors
    permanent_mapping = {
        'chatforbidden': BlacklistReason.CHAT_FORBIDDEN,
        'chatidinvalid': BlacklistReason.CHAT_ID_INVALID,
        'userblocked': BlacklistReason.USER_BLOCKED,
        'peeridinvalid': BlacklistReason.PEER_ID_INVALID,
        'channelinvalid': BlacklistReason.CHANNEL_INVALID,
        'userbannedin': BlacklistReason.USER_BANNED_IN_CHANNEL,
        'chatwriteforbidden': BlacklistReason.CHAT_WRITE_FORBIDDEN,
        'chatrestricted': BlacklistReason.CHAT_RESTRICTED,
    }
    
    for error_key, reason in permanent_mapping.items():
        if error_key in error_lower:
            return BlacklistType.PERMANENT, reason
    
    # Temporary errors
    if 'slowmode' in error_lower or 'slow mode' in error_lower:
        return BlacklistType.TEMPORARY, BlacklistReason.SLOW_MODE_WAIT
    
    if 'flood' in error_lower:
        return BlacklistType.TEMPORARY, BlacklistReason.FLOOD_WAIT
    
    # Default to permanent
    return BlacklistType.PERMANENT, BlacklistReason.CHAT_FORBIDDEN