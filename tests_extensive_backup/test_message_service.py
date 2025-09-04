"""
Tests for Message Service
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.services.message_service import MessageService
from src.models.message import Message, MessageCreate, MessageUpdate


class TestMessageService:
    """Test MessageService class"""

    @pytest.fixture
    def mock_collection(self):
        """Mock collection fixture"""
        return AsyncMock()

    @pytest.fixture
    def message_service(self, mock_collection):
        """MessageService fixture with mocked collection"""
        with patch('src.services.message_service.database') as mock_database:
            mock_database.get_collection.return_value = mock_collection
            service = MessageService()
            return service

    @pytest.mark.asyncio
    async def test_create_message(self, message_service, mock_collection):
        """Test message creation"""
        message_data = MessageCreate(content="Test message")
        mock_collection.insert_one.return_value = AsyncMock()
        
        result = await message_service.create_message(message_data)
        
        assert isinstance(result, Message)
        assert result.content == "Test message"
        assert result.is_active is True
        assert result.usage_count == 0
        mock_collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_messages(self, message_service, mock_collection):
        """Test getting all messages"""
        mock_messages = [
            Message(content="Message 1", is_active=True, usage_count=0),
            Message(content="Message 2", is_active=False, usage_count=5),
        ]
        
        # Mock the entire method
        message_service.get_all_messages = AsyncMock(return_value=mock_messages)
        
        result = await message_service.get_all_messages()
        
        assert len(result) == 2
        assert all(isinstance(msg, Message) for msg in result)
        assert result[0].content == "Message 1" 
        assert result[1].content == "Message 2"

    @pytest.mark.asyncio
    async def test_get_active_messages(self, message_service, mock_collection):
        """Test getting active messages"""
        mock_messages = [
            Message(content="Active message", is_active=True, usage_count=0),
        ]
        
        # Mock the entire method
        message_service.get_active_messages = AsyncMock(return_value=mock_messages)
        
        result = await message_service.get_active_messages()
        
        assert len(result) == 1
        assert result[0].is_active is True

    @pytest.mark.asyncio
    async def test_get_message_by_id(self, message_service, mock_collection):
        """Test getting message by ID"""
        message_id = "test-id"
        mock_doc = {
            "id": message_id,
            "content": "Test message",
            "is_active": True,
            "usage_count": 0,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_doc
        
        result = await message_service.get_message_by_id(message_id)
        
        assert result is not None
        assert isinstance(result, Message)
        assert result.id == message_id
        mock_collection.find_one.assert_called_once_with({"id": message_id})

    @pytest.mark.asyncio
    async def test_get_message_by_id_not_found(self, message_service, mock_collection):
        """Test getting message by ID when not found"""
        message_id = "nonexistent-id"
        mock_collection.find_one.return_value = None
        
        result = await message_service.get_message_by_id(message_id)
        
        assert result is None
        mock_collection.find_one.assert_called_once_with({"id": message_id})

    @pytest.mark.asyncio
    async def test_update_message(self, message_service, mock_collection):
        """Test updating message"""
        message_id = "test-id"
        update_data = MessageUpdate(content="Updated content", is_active=False)
        mock_result = MagicMock()
        mock_result.modified_count = 1
        mock_collection.update_one.return_value = mock_result
        
        # Mock the get_message_by_id call for the return value
        mock_updated_doc = {
            "id": message_id,
            "content": "Updated content",
            "is_active": False,
            "usage_count": 0,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_updated_doc
        
        result = await message_service.update_message(message_id, update_data)
        
        assert result is not None
        assert isinstance(result, Message)
        assert result.content == "Updated content"
        assert result.is_active is False
        mock_collection.update_one.assert_called_once()
        # Check that the update includes both fields and updated_at
        call_args = mock_collection.update_one.call_args
        assert call_args[0][0] == {"id": message_id}  # filter
        update_doc = call_args[0][1]["$set"]
        assert update_doc["content"] == "Updated content"
        assert update_doc["is_active"] is False
        assert "updated_at" in update_doc

    @pytest.mark.asyncio
    async def test_update_message_not_found(self, message_service, mock_collection):
        """Test updating message when not found"""
        message_id = "nonexistent-id"
        update_data = MessageUpdate(content="Updated content")
        mock_result = MagicMock()
        mock_result.modified_count = 0
        mock_collection.update_one.return_value = mock_result
        
        result = await message_service.update_message(message_id, update_data)
        
        assert result is None
        mock_collection.update_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_message(self, message_service, mock_collection):
        """Test deleting message"""
        message_id = "test-id"
        mock_collection.delete_one.return_value = MagicMock(deleted_count=1)
        
        result = await message_service.delete_message(message_id)
        
        assert result is True
        mock_collection.delete_one.assert_called_once_with({"id": message_id})

    @pytest.mark.asyncio
    async def test_delete_message_not_found(self, message_service, mock_collection):
        """Test deleting message when not found"""
        message_id = "nonexistent-id"
        mock_collection.delete_one.return_value = MagicMock(deleted_count=0)
        
        result = await message_service.delete_message(message_id)
        
        assert result is False
        mock_collection.delete_one.assert_called_once_with({"id": message_id})

    @pytest.mark.asyncio
    async def test_increment_usage_count(self, message_service, mock_collection):
        """Test incrementing message usage count"""
        message_id = "test-id"
        mock_collection.update_one.return_value = MagicMock(matched_count=1)
        
        result = await message_service.increment_usage_count(message_id)
        
        assert result is True
        mock_collection.update_one.assert_called_once()
        call_args = mock_collection.update_one.call_args
        assert call_args[0][0] == {"id": message_id}
        assert "$inc" in call_args[0][1]
        assert call_args[0][1]["$inc"]["usage_count"] == 1
        assert "$set" in call_args[0][1]
        assert "updated_at" in call_args[0][1]["$set"]

    @pytest.mark.asyncio
    async def test_get_message_count(self, message_service, mock_collection):
        """Test getting total message count"""
        # Mock different counts for total and active
        def count_side_effect(query):
            if query == {}:
                return 5  # total
            elif query == {"is_active": True}:
                return 5  # active
            return 0
        
        mock_collection.count_documents.side_effect = count_side_effect
        
        result = await message_service.get_message_count()
        
        assert result == {"total": 5, "active": 5, "inactive": 0}
        assert mock_collection.count_documents.call_count == 2

    @pytest.mark.asyncio
    async def test_get_active_message_count(self, message_service, mock_collection):
        """Test getting active message count"""
        mock_collection.count_documents.return_value = 3
        
        result = await message_service.get_active_message_count()
        
        assert result == 3
        mock_collection.count_documents.assert_called_once_with({"is_active": True})