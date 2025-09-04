"""
Message Service - Handles message CRUD operations
"""

from datetime import datetime
from typing import Any

from loguru import logger

from src.core.database import database
from src.models.message import Message, MessageCreate, MessageUpdate


class MessageService:
    """Service for managing messages"""

    def __init__(self) -> None:
        self.collection: Any = database.get_collection("messages")

    async def create_message(self, message_data: MessageCreate) -> Message:
        """Create a new message"""
        message = Message(content=message_data.content)

        await self.collection.insert_one(message.model_dump())
        logger.info(f"Created message: {message.id}")

        return message

    async def get_all_messages(self) -> list[Message]:
        """Get all messages"""
        cursor = self.collection.find()
        messages = []

        async for doc in cursor:
            messages.append(Message(**doc))

        return messages

    async def get_active_messages(self, limit: int | None = None) -> list[Message]:
        """Get only active messages"""
        cursor = self.collection.find({"is_active": True})

        if limit:
            cursor = cursor.limit(limit)

        messages = []
        async for doc in cursor:
            messages.append(Message(**doc))

        return messages

    async def get_messages_by_usage_count(
        self, min_count: int = 0, max_count: int | None = None
    ) -> list[Message]:
        """Get messages filtered by usage count"""
        query = {"usage_count": {"$gte": min_count}}

        if max_count is not None:
            query["usage_count"]["$lte"] = max_count

        cursor = self.collection.find(query)
        messages = []

        async for doc in cursor:
            messages.append(Message(**doc))

        return messages

    async def search_messages(self, search_term: str) -> list[Message]:
        """Search messages by content"""
        query = {"content": {"$regex": search_term, "$options": "i"}}

        cursor = self.collection.find(query)
        messages = []

        async for doc in cursor:
            messages.append(Message(**doc))

        return messages

    async def toggle_message_status(self, message_id: str) -> Message | None:
        """Toggle message active status"""
        message = await self.get_message_by_id(message_id)
        if not message:
            return None

        new_status = not message.is_active
        update_data = MessageUpdate(is_active=new_status)

        updated = await self.update_message(message_id, update_data)

        if updated:
            status_text = "activated" if new_status else "deactivated"
            logger.info(f"Message {message_id} {status_text}")

        return updated

    async def batch_update_messages(
        self, message_ids: list[str], update_data: MessageUpdate
    ) -> dict[str, bool]:
        """Batch update multiple messages"""
        results = {}

        for message_id in message_ids:
            try:
                updated = await self.update_message(message_id, update_data)
                results[message_id] = updated is not None
            except Exception as e:
                logger.error(f"Failed to update message {message_id}: {e}")
                results[message_id] = False

        return results

    async def batch_delete_messages(self, message_ids: list[str]) -> dict[str, bool]:
        """Batch delete multiple messages"""
        results = {}

        for message_id in message_ids:
            try:
                success = await self.delete_message(message_id)
                results[message_id] = success
            except Exception as e:
                logger.error(f"Failed to delete message {message_id}: {e}")
                results[message_id] = False

        return results

    async def reset_all_usage_counts(self) -> int:
        """Reset usage count for all messages"""
        result = await self.collection.update_many(
            {}, {"$set": {"usage_count": 0, "updated_at": datetime.utcnow()}}
        )

        logger.info(f"Reset usage count for {result.modified_count} messages")
        return result.modified_count

    async def get_usage_statistics(self) -> dict[str, Any]:
        """Get message usage statistics"""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_messages": {"$sum": 1},
                    "active_messages": {"$sum": {"$cond": ["$is_active", 1, 0]}},
                    "total_usage": {"$sum": "$usage_count"},
                    "avg_usage": {"$avg": "$usage_count"},
                    "max_usage": {"$max": "$usage_count"},
                    "min_usage": {"$min": "$usage_count"},
                }
            }
        ]

        cursor = self.collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)

        if result:
            stats = result[0]
            stats.pop("_id", None)  # Remove _id field
            stats["inactive_messages"] = stats["total_messages"] - stats["active_messages"]
            return stats

        return {
            "total_messages": 0,
            "active_messages": 0,
            "inactive_messages": 0,
            "total_usage": 0,
            "avg_usage": 0,
            "max_usage": 0,
            "min_usage": 0,
        }

    async def get_least_used_messages(self, limit: int = 10) -> list[Message]:
        """Get messages with lowest usage count"""
        cursor = self.collection.find({"is_active": True}).sort("usage_count", 1).limit(limit)
        messages = []

        async for doc in cursor:
            messages.append(Message(**doc))

        return messages

    async def get_most_used_messages(self, limit: int = 10) -> list[Message]:
        """Get messages with highest usage count"""
        cursor = self.collection.find({"is_active": True}).sort("usage_count", -1).limit(limit)
        messages = []

        async for doc in cursor:
            messages.append(Message(**doc))

        return messages

    async def check_duplicate_content(self, content: str) -> bool:
        """Check if message content already exists"""
        existing = await self.collection.find_one({"content": content})
        return existing is not None

    async def get_messages_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> list[Message]:
        """Get messages created within date range"""
        query = {"created_at": {"$gte": start_date, "$lte": end_date}}

        cursor = self.collection.find(query)
        messages = []

        async for doc in cursor:
            messages.append(Message(**doc))

        return messages

    def validate_content(self, content: str) -> bool:
        """Validate message content"""
        if not content or not content.strip():
            return False

        # Check length limits (from Telegram limits)
        if len(content) > 4096:
            return False

        return True

    async def archive_old_messages(self, cutoff_date: datetime) -> int:
        """Archive messages older than cutoff date"""
        result = await self.collection.update_many(
            {"created_at": {"$lt": cutoff_date}, "is_active": True},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}},
        )

        logger.info(f"Archived {result.modified_count} old messages")
        return result.modified_count

    async def get_message_by_id(self, message_id: str) -> Message | None:
        """Get message by ID"""
        doc = await self.collection.find_one({"id": message_id})

        if doc:
            return Message(**doc)
        return None

    async def update_message(self, message_id: str, update_data: MessageUpdate) -> Message | None:
        """Update a message"""
        update_dict: dict[str, Any] = {
            k: v for k, v in update_data.model_dump().items() if v is not None
        }

        if not update_dict:
            return await self.get_message_by_id(message_id)

        update_dict["updated_at"] = datetime.utcnow()

        result = await self.collection.update_one({"id": message_id}, {"$set": update_dict})

        if result.modified_count > 0:
            logger.info(f"Updated message: {message_id}")
            return await self.get_message_by_id(message_id)

        return None

    async def delete_message(self, message_id: str) -> bool:
        """Delete a message"""
        result = await self.collection.delete_one({"id": message_id})

        if result.deleted_count > 0:
            logger.info(f"Deleted message: {message_id}")
            return True

        return False

    async def increment_usage_count(self, message_id: str) -> bool:
        """Increment usage count for a message"""
        result = await self.collection.update_one(
            {"id": message_id},
            {"$inc": {"usage_count": 1}, "$set": {"updated_at": datetime.utcnow()}},
        )
        return result.matched_count > 0

    async def get_active_message_count(self) -> int:
        """Get active message count"""
        return await self.collection.count_documents({"is_active": True})

    async def get_message_count(self) -> dict[str, int]:
        """Get message statistics"""
        total = await self.collection.count_documents({})
        active = await self.collection.count_documents({"is_active": True})

        return {"total": total, "active": active, "inactive": total - active}
