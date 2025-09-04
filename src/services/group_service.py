"""
Group Service - Handles group CRUD operations
"""

from datetime import datetime
from typing import Any

from loguru import logger

from src.core.database import database
from src.models.group import Group, GroupBulkCreate, GroupCreate


class GroupService:
    """Service for managing groups"""

    def __init__(self) -> None:
        self.collection: Any = database.get_collection("groups")

    async def create_group(self, group_data: GroupCreate) -> Group:
        """Create a new group"""
        identifier = group_data.group_identifier

        # Parse identifier and build group data
        group_kwargs: dict[str, Any] = {
            "group_id": None,
            "group_username": None,
            "group_link": None,
            "group_title": None,
            "is_active": True,
            "message_count": 0,
        }

        if identifier.startswith("-") and identifier[1:].isdigit():
            group_kwargs["group_id"] = identifier
        elif identifier.startswith("@"):
            group_kwargs["group_username"] = identifier
        elif "t.me/" in identifier:
            group_kwargs["group_link"] = identifier
            # Extract username from link
            if "/" in identifier:
                username = identifier.split("/")[-1]
                if not username.startswith("@"):
                    username = f"@{username}"
                group_kwargs["group_username"] = username

        group = Group(**group_kwargs)

        # Check if group already exists
        existing = await self.get_group_by_identifier(identifier)
        if existing:
            logger.warning(f"Group already exists: {identifier}")
            return existing

        await self.collection.insert_one(group.dict())  # type: ignore
        logger.info(f"Created group: {identifier}")

        return group

    async def create_groups_bulk(self, bulk_data: GroupBulkCreate) -> list[Group]:
        """Create multiple groups"""
        identifiers = bulk_data.get_identifiers_list()
        created_groups = []

        for identifier in identifiers:
            try:
                group_data = GroupCreate(group_identifier=identifier)
                group = await self.create_group(group_data)
                created_groups.append(group)
            except Exception as e:
                logger.error(f"Failed to create group {identifier}: {e}")

        return created_groups

    async def get_all_groups(self) -> list[Group]:
        """Get all groups"""
        cursor = self.collection.find()  # type: ignore
        groups = []

        async for doc in cursor:
            groups.append(Group(**doc))

        return groups

    async def get_active_groups(self) -> list[Group]:
        """Get only active groups"""
        cursor = self.collection.find({"is_active": True})  # type: ignore
        groups = []

        async for doc in cursor:
            groups.append(Group(**doc))

        return groups

    async def get_group_by_id(self, group_id: str) -> Group | None:
        """Get group by ID"""
        doc = await self.collection.find_one({"id": group_id})  # type: ignore

        if doc:
            return Group(**doc)
        return None

    async def get_group_by_identifier(self, identifier: str) -> Group | None:
        """Get group by telegram identifier"""
        # Try different fields
        query = {
            "$or": [
                {"group_id": identifier},
                {"group_username": identifier},
                {"group_link": {"$regex": identifier}},
            ]
        }

        doc = await self.collection.find_one(query)  # type: ignore

        if doc:
            return Group(**doc)
        return None

    async def update_group_info(
        self, group_id: str, title: str | None = None, is_active: bool | None = None
    ) -> Group | None:
        """Update group information"""
        update_dict: dict[str, Any] = {}

        if title is not None:
            update_dict["group_title"] = title

        if is_active is not None:
            update_dict["is_active"] = is_active

        if not update_dict:
            return await self.get_group_by_id(group_id)

        update_dict["updated_at"] = datetime.utcnow()

        result = await self.collection.update_one({"id": group_id}, {"$set": update_dict})  # type: ignore

        if result.modified_count > 0:
            logger.info(f"Updated group: {group_id}")
            return await self.get_group_by_id(group_id)

        return None

    async def delete_group(self, group_id: str) -> bool:
        """Delete a group"""
        result = await self.collection.delete_one({"id": group_id})  # type: ignore

        if result.deleted_count > 0:
            logger.info(f"Deleted group: {group_id}")
            return True

        return False

    async def increment_message_count(self, group_telegram_id: str) -> None:
        """Increment message count for a group"""
        await self.collection.update_one(  # type: ignore
            {"group_id": group_telegram_id}, {"$inc": {"message_count": 1}}
        )

    async def get_group_stats(self) -> dict[str, int]:
        """Get group statistics"""
        total = await self.collection.count_documents({})  # type: ignore
        active = await self.collection.count_documents({"is_active": True})  # type: ignore

        return {"total": total, "active": active, "inactive": total - active}