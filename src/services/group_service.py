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

    def __init__(self, db_instance: Any = None) -> None:
        self._db = db_instance or database
        self._collection: Any = None

    @property
    def collection(self) -> Any:
        """Lazy-load collection"""
        if self._collection is None:
            self._collection = self._db.get_collection("groups")
        return self._collection

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

        await self.collection.insert_one(group.model_dump())
        logger.info(f"Created group: {identifier}")

        return group

    async def create_bulk_groups(self, bulk_data: GroupBulkCreate) -> list[Group]:
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

    async def create_groups_bulk(self, bulk_data: GroupBulkCreate) -> list[Group]:
        """Create multiple groups - alias for backward compatibility"""
        return await self.create_bulk_groups(bulk_data)

    async def get_all_groups(self) -> list[Group]:
        """Get all groups"""
        cursor = self.collection.find()
        groups = []

        async for doc in cursor:
            groups.append(Group(**doc))

        return groups

    async def get_active_groups(self) -> list[Group]:
        """Get only active groups"""
        cursor = self.collection.find({"is_active": True})
        groups = []

        async for doc in cursor:
            groups.append(Group(**doc))

        return groups

    async def get_group_by_id(self, group_id: str) -> Group | None:
        """Get group by ID"""
        doc = await self.collection.find_one({"id": group_id})

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

        doc = await self.collection.find_one(query)

        if doc:
            return Group(**doc)
        return None

    async def update_group(self, group_id: str, update_data: dict[str, Any]) -> bool:
        """Update group"""
        if not update_data:
            return False

        update_data["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one({"id": group_id}, {"$set": update_data})

        return result.matched_count > 0

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

        result = await self.collection.update_one({"id": group_id}, {"$set": update_dict})

        if result.modified_count > 0:
            logger.info(f"Updated group: {group_id}")
            return await self.get_group_by_id(group_id)

        return None

    async def toggle_group_status(self, group_id: str) -> Group | None:
        """Toggle group active status"""
        group = await self.get_group_by_id(group_id)
        if not group:
            return None

        new_status = not group.is_active
        updated = await self.update_group_info(group_id, is_active=new_status)

        if updated:
            status_text = "activated" if new_status else "deactivated"
            logger.info(f"Group {group_id} {status_text}")

        return updated

    async def search_groups(self, search_term: str) -> list[Group]:
        """Search groups by username, title, or ID"""
        query = {
            "$or": [
                {"group_username": {"$regex": search_term, "$options": "i"}},
                {"group_title": {"$regex": search_term, "$options": "i"}},
                {"group_id": {"$regex": search_term, "$options": "i"}},
            ]
        }

        cursor = self.collection.find(query)
        groups = []

        async for doc in cursor:
            groups.append(Group(**doc))

        return groups

    async def get_groups_by_status(self, is_active: bool) -> list[Group]:
        """Get groups by active status"""
        cursor = self.collection.find({"is_active": is_active})
        groups = []

        async for doc in cursor:
            groups.append(Group(**doc))

        return groups

    async def batch_update_groups(
        self, group_ids: list[str], update_data: dict[str, Any]
    ) -> dict[str, bool]:
        """Batch update multiple groups"""
        results = {}

        for group_id in group_ids:
            try:
                success = await self.update_group(group_id, update_data.copy())
                results[group_id] = success
            except Exception as e:
                logger.error(f"Failed to update group {group_id}: {e}")
                results[group_id] = False

        return results

    async def batch_delete_groups(self, group_ids: list[str]) -> dict[str, bool]:
        """Batch delete multiple groups"""
        results = {}

        for group_id in group_ids:
            try:
                success = await self.delete_group(group_id)
                results[group_id] = success
            except Exception as e:
                logger.error(f"Failed to delete group {group_id}: {e}")
                results[group_id] = False

        return results

    async def get_groups_with_message_count_filter(
        self, min_count: int = 0, max_count: int | None = None
    ) -> list[Group]:
        """Get groups filtered by message count"""
        query = {"message_count": {"$gte": min_count}}

        if max_count is not None:
            query["message_count"]["$lte"] = max_count

        cursor = self.collection.find(query)
        groups = []

        async for doc in cursor:
            groups.append(Group(**doc))

        return groups

    async def reset_all_message_counts(self) -> int:
        """Reset message count for all groups"""
        result = await self.collection.update_many(
            {}, {"$set": {"message_count": 0, "updated_at": datetime.utcnow()}}
        )

        logger.info(f"Reset message count for {result.modified_count} groups")
        return result.modified_count

    async def get_group_activity_summary(self) -> dict[str, Any]:
        """Get group activity summary with statistics"""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_groups": {"$sum": 1},
                    "active_groups": {"$sum": {"$cond": ["$is_active", 1, 0]}},
                    "total_messages": {"$sum": "$message_count"},
                    "avg_messages": {"$avg": "$message_count"},
                    "max_messages": {"$max": "$message_count"},
                    "min_messages": {"$min": "$message_count"},
                }
            }
        ]

        cursor = self.collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)

        if result:
            summary = result[0]
            summary.pop("_id", None)  # Remove _id field
            summary["inactive_groups"] = summary["total_groups"] - summary["active_groups"]
            return summary

        return {
            "total_groups": 0,
            "active_groups": 0,
            "inactive_groups": 0,
            "total_messages": 0,
            "avg_messages": 0,
            "max_messages": 0,
            "min_messages": 0,
        }

    async def delete_group(self, group_id: str) -> bool:
        """Delete a group"""
        result = await self.collection.delete_one({"id": group_id})

        if result.deleted_count > 0:
            logger.info(f"Deleted group: {group_id}")
            return True

        return False

    async def increment_message_count(self, group_id: str) -> bool:
        """Increment message count for a group"""
        result = await self.collection.update_one({"id": group_id}, {"$inc": {"message_count": 1}})
        return result.matched_count > 0

    async def get_group_count(self) -> int:
        """Get total group count"""
        return await self.collection.count_documents({})

    async def get_active_group_count(self) -> int:
        """Get active group count"""
        return await self.collection.count_documents({"is_active": True})

    async def get_group_stats(self) -> dict[str, int]:
        """Get group statistics"""
        total = await self.collection.count_documents({})
        active = await self.collection.count_documents({"is_active": True})

        return {"total": total, "active": active, "inactive": total - active}
