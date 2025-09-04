"""
Blacklist Service - Handles blacklist management
"""

from datetime import datetime, timedelta
from typing import Any

from loguru import logger

from src.core.constants import DEFAULT_FLOOD_DURATION, DEFAULT_SLOWMODE_DURATION
from src.core.database import database
from src.models.blacklist import (
    Blacklist,
    BlacklistCreate,
    BlacklistType,
    determine_blacklist_from_error,
)


class BlacklistService:
    """Service for managing blacklists"""

    def __init__(self) -> None:
        self.collection: Any = database.get_collection("blacklists")

    async def add_to_blacklist(self, blacklist_data: BlacklistCreate) -> Blacklist:
        """Add group to blacklist"""

        # Set expiration time for temporary blacklist
        expires_at = None
        if (
            blacklist_data.blacklist_type == BlacklistType.TEMPORARY
            and blacklist_data.duration_seconds
        ):
            expires_at = datetime.utcnow() + timedelta(seconds=blacklist_data.duration_seconds)

        blacklist = Blacklist(
            group_id=blacklist_data.group_id,
            group_identifier=blacklist_data.group_identifier,
            blacklist_type=blacklist_data.blacklist_type,
            reason=blacklist_data.reason,
            expires_at=expires_at,
            duration_seconds=blacklist_data.duration_seconds,
            error_message=blacklist_data.error_message,
        )

        # Remove existing blacklist for this group
        await self.collection.delete_many({"group_id": blacklist_data.group_id})

        # Insert new blacklist entry
        await self.collection.insert_one(blacklist.dict())

        logger.info(
            f"Added to {blacklist_data.blacklist_type} blacklist: {blacklist_data.group_id} - {blacklist_data.reason}"
        )

        return blacklist

    async def add_from_error(
        self, group_id: str, error_msg: str, group_identifier: str | None = None
    ) -> Blacklist:
        """Add to blacklist based on error message"""

        blacklist_type, reason = determine_blacklist_from_error(error_msg)

        # Extract duration from error message for temporary errors
        duration_seconds = None
        if blacklist_type == BlacklistType.TEMPORARY:
            duration_seconds = self._extract_duration_from_error(error_msg)

        blacklist_data = BlacklistCreate(
            group_id=group_id,
            group_identifier=group_identifier,
            blacklist_type=blacklist_type,
            reason=reason,
            duration_seconds=duration_seconds,
            error_message=error_msg,
        )

        return await self.add_to_blacklist(blacklist_data)

    def _extract_duration_from_error(self, error_msg: str) -> int | None:
        """Extract duration from error message"""
        import re

        # Look for patterns like "wait 3600 seconds" or "SlowModeWait 30"
        patterns = [
            r"wait (\d+) seconds?",
            r"SlowModeWait.*?(\d+)",
            r"FloodWait.*?(\d+)",
            r"(\d+) seconds?",
        ]

        for pattern in patterns:
            match = re.search(pattern, error_msg, re.IGNORECASE)
            if match:
                return int(match.group(1))

        # Default durations
        if "slowmode" in error_msg.lower():
            return DEFAULT_SLOWMODE_DURATION
        elif "flood" in error_msg.lower():
            return DEFAULT_FLOOD_DURATION

        return None

    async def is_blacklisted(self, group_id: str) -> bool:
        """Check if group is blacklisted"""

        # Clean up expired entries first
        await self.cleanup_expired()

        doc = await self.collection.find_one({"group_id": group_id})
        return doc is not None

    async def get_blacklist_entry(self, group_id: str) -> Blacklist | None:
        """Get blacklist entry for group"""
        doc = await self.collection.find_one({"group_id": group_id})

        if doc:
            return Blacklist(**doc)
        return None

    async def remove_from_blacklist(self, group_id: str) -> bool:
        """Remove group from blacklist"""
        result = await self.collection.delete_one({"group_id": group_id})

        if result.deleted_count > 0:
            logger.info(f"Removed from blacklist: {group_id}")
            return True

        return False

    async def cleanup_expired(self) -> int:
        """Clean up expired temporary blacklist entries"""
        now = datetime.utcnow()

        result = await self.collection.delete_many(
            {"blacklist_type": BlacklistType.TEMPORARY, "expires_at": {"$lte": now}}
        )

        if result.deleted_count > 0:
            logger.info(f"Cleaned up {result.deleted_count} expired blacklist entries")

        return int(result.deleted_count)

    async def get_all_blacklists(self) -> list[Blacklist]:
        """Get all blacklist entries"""
        cursor = self.collection.find()
        blacklists = []

        async for doc in cursor:
            blacklists.append(Blacklist(**doc))

        return blacklists

    async def get_blacklist_stats(self) -> dict[str, int]:
        """Get blacklist statistics"""
        total = await self.collection.count_documents({})
        permanent = await self.collection.count_documents(
            {"blacklist_type": BlacklistType.PERMANENT}
        )
        temporary = await self.collection.count_documents(
            {"blacklist_type": BlacklistType.TEMPORARY}
        )

        # Count expired temporary entries
        now = datetime.utcnow()
        expired = await self.collection.count_documents(
            {"blacklist_type": BlacklistType.TEMPORARY, "expires_at": {"$lte": now}}
        )

        return {"total": total, "permanent": permanent, "temporary": temporary, "expired": expired}

    async def get_blacklist_entry_by_id(self, blacklist_id: str) -> Blacklist | None:
        """Get blacklist entry by ID"""
        doc = await self.collection.find_one({"id": blacklist_id})

        if doc:
            return Blacklist(**doc)
        return None
