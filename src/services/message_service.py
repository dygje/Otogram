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

        await self.collection.insert_one(message.dict())
        logger.info(f"Created message: {message.id}")

        return message

    async def get_all_messages(self) -> list[Message]:
        """Get all messages"""
        cursor = self.collection.find()
        messages = []

        async for doc in cursor:
            messages.append(Message(**doc))

        return messages

    async def get_active_messages(self) -> list[Message]:
        """Get only active messages"""
        cursor = self.collection.find({"is_active": True})
        messages = []

        async for doc in cursor:
            messages.append(Message(**doc))

        return messages

    async def get_message_by_id(self, message_id: str) -> Message | None:
        """Get message by ID"""
        doc = await self.collection.find_one({"id": message_id})

        if doc:
            return Message(**doc)
        return None

    async def update_message(self, message_id: str, update_data: MessageUpdate) -> Message | None:
        """Update a message"""
        update_dict: dict[str, Any] = {k: v for k, v in update_data.dict().items() if v is not None}

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

    async def increment_usage_count(self, message_id: str) -> None:
        """Increment usage count for a message"""
        await self.collection.update_one({"id": message_id}, {"$inc": {"usage_count": 1}})

    async def get_message_count(self) -> dict[str, int]:
        """Get message statistics"""
        total = await self.collection.count_documents({})
        active = await self.collection.count_documents({"is_active": True})

        return {"total": total, "active": active, "inactive": total - active}
