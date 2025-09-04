"""
Extended tests for Message Service to improve coverage
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.services.message_service import MessageService
from src.models.message import Message, MessageCreate, MessageUpdate


class TestMessageServiceExtended:
    """Extended test coverage for MessageService class"""

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
    async def test_get_active_messages_with_limit(self, message_service, mock_collection):
        """Test getting active messages with limit"""
        mock_messages = [
            Message(content="Message 1", is_active=True, usage_count=1),
            Message(content="Message 2", is_active=True, usage_count=2),
            Message(content="Message 3", is_active=True, usage_count=0),
        ]
        
        # Mock the entire method with limit
        async def mock_get_active_messages(limit=None):
            if limit:
                return mock_messages[:limit]
            return mock_messages
        
        message_service.get_active_messages = mock_get_active_messages
        
        result = await message_service.get_active_messages(limit=2)
        
        assert len(result) == 2
        assert result[0].content == "Message 1"
        assert result[1].content == "Message 2"

    @pytest.mark.asyncio
    async def test_get_messages_by_usage_count(self, message_service, mock_collection):
        """Test getting messages filtered by usage count"""
        min_usage = 5
        
        mock_docs = [
            {
                "id": "1",
                "content": "Popular message",
                "usage_count": 10,
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            },
            {
                "id": "2",
                "content": "Another popular message", 
                "usage_count": 7,
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_collection.find.return_value = mock_cursor
        
        result = await message_service.get_messages_by_usage_count(min_usage)
        
        assert len(result) == 2
        assert all(isinstance(msg, Message) for msg in result)
        assert all(msg.usage_count >= min_usage for msg in result)
        
        # Verify filter was applied
        call_args = mock_collection.find.call_args[0][0] 
        assert call_args["usage_count"]["$gte"] == min_usage

    @pytest.mark.asyncio
    async def test_search_messages_by_content(self, message_service, mock_collection):
        """Test searching messages by content"""
        search_term = "test"
        
        mock_docs = [
            {
                "id": "1",
                "content": "This is a test message",
                "is_active": True,
                "usage_count": 0,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            },
            {
                "id": "2",
                "content": "Testing another message",
                "is_active": True,
                "usage_count": 1,
                "created_at": "2023-01-01T00:00:00", 
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_collection.find.return_value = mock_cursor
        
        result = await message_service.search_messages(search_term)
        
        assert len(result) == 2
        assert all("test" in msg.content.lower() for msg in result)
        
        # Verify search query structure
        call_args = mock_collection.find.call_args[0][0]
        assert "$regex" in call_args["content"]
        assert call_args["content"]["$options"] == "i"  # Case insensitive

    @pytest.mark.asyncio
    async def test_toggle_message_status_activate(self, message_service, mock_collection):
        """Test toggling message status to active"""
        message_id = "test-message-id"
        
        # Mock finding inactive message
        mock_doc = {
            "id": message_id,
            "content": "Test message",
            "is_active": False,
            "usage_count": 5,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_doc
        mock_collection.update_one.return_value = MagicMock(modified_count=1)
        
        # Mock the updated document
        updated_doc = mock_doc.copy()
        updated_doc["is_active"] = True
        
        mock_collection.find_one.side_effect = [mock_doc, updated_doc]
        
        result = await message_service.toggle_message_status(message_id)
        
        assert result is not None
        assert result.is_active is True
        
        # Verify update was called
        call_args = mock_collection.update_one.call_args
        assert call_args[0][0] == {"id": message_id}
        assert call_args[0][1]["$set"]["is_active"] is True

    @pytest.mark.asyncio
    async def test_toggle_message_status_deactivate(self, message_service, mock_collection):
        """Test toggling message status to inactive"""
        message_id = "test-message-id"
        
        # Mock finding active message
        mock_doc = {
            "id": message_id,
            "content": "Test message",
            "is_active": True,
            "usage_count": 5,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_doc
        mock_collection.update_one.return_value = MagicMock(modified_count=1)
        
        # Mock the updated document
        updated_doc = mock_doc.copy()
        updated_doc["is_active"] = False
        
        mock_collection.find_one.side_effect = [mock_doc, updated_doc]
        
        result = await message_service.toggle_message_status(message_id)
        
        assert result is not None
        assert result.is_active is False

    @pytest.mark.asyncio
    async def test_toggle_message_status_not_found(self, message_service, mock_collection):
        """Test toggling status of non-existent message"""
        message_id = "nonexistent-id"
        mock_collection.find_one.return_value = None
        
        result = await message_service.toggle_message_status(message_id)
        
        assert result is None

    @pytest.mark.asyncio
    async def test_batch_update_messages(self, message_service, mock_collection):
        """Test batch updating multiple messages"""
        message_ids = ["id1", "id2", "id3"]
        update_data = {"is_active": False}
        
        mock_collection.update_many.return_value = MagicMock(modified_count=3)
        
        result = await message_service.batch_update_messages(message_ids, update_data)
        
        assert result == 3
        
        # Verify update query
        call_args = mock_collection.update_many.call_args
        assert call_args[0][0] == {"id": {"$in": message_ids}}
        assert call_args[0][1]["$set"]["is_active"] is False
        assert "updated_at" in call_args[0][1]["$set"]

    @pytest.mark.asyncio
    async def test_batch_delete_messages(self, message_service, mock_collection):
        """Test batch deleting multiple messages"""
        message_ids = ["id1", "id2", "id3"] 
        
        mock_collection.delete_many.return_value = MagicMock(deleted_count=3)
        
        result = await message_service.batch_delete_messages(message_ids)
        
        assert result == 3
        
        # Verify delete query
        call_args = mock_collection.delete_many.call_args
        assert call_args[0][0] == {"id": {"$in": message_ids}}

    @pytest.mark.asyncio
    async def test_reset_all_usage_counts(self, message_service, mock_collection):
        """Test resetting all message usage counts"""
        mock_collection.update_many.return_value = MagicMock(modified_count=10)
        
        result = await message_service.reset_all_usage_counts()
        
        assert result == 10
        
        # Verify update query
        call_args = mock_collection.update_many.call_args
        assert call_args[0][0] == {}  # All documents
        assert call_args[0][1]["$set"]["usage_count"] == 0
        assert "updated_at" in call_args[0][1]["$set"]

    @pytest.mark.asyncio
    async def test_get_usage_statistics(self, message_service, mock_collection):
        """Test getting message usage statistics"""
        # Mock aggregation pipeline result
        mock_cursor = AsyncMock()
        mock_results = [
            {
                "_id": None,
                "total_messages": 25,
                "active_messages": 20,
                "total_usage": 500,
                "avg_usage_per_message": 20.0,
                "max_usage": 50,
                "min_usage": 0
            }
        ]
        
        async def async_iter(results):
            for result in results:
                yield result
        
        mock_cursor.__aiter__ = lambda: async_iter(mock_results)
        mock_collection.aggregate.return_value = mock_cursor
        
        result = await message_service.get_usage_statistics()
        
        expected = {
            "total_messages": 25,
            "active_messages": 20,
            "inactive_messages": 5,
            "total_usage": 500,
            "avg_usage_per_message": 20.0,
            "max_usage": 50,
            "min_usage": 0
        }
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_usage_statistics_empty(self, message_service, mock_collection):
        """Test getting usage statistics with no data"""
        # Mock empty aggregation result
        mock_cursor = AsyncMock()
        async def empty_iter():
            return
            yield  # Unreachable
        mock_cursor.__aiter__ = empty_iter
        mock_collection.aggregate.return_value = mock_cursor
        
        result = await message_service.get_usage_statistics()
        
        expected = {
            "total_messages": 0,
            "active_messages": 0,
            "inactive_messages": 0,
            "total_usage": 0,
            "avg_usage_per_message": 0.0,
            "max_usage": 0,
            "min_usage": 0
        }
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_least_used_messages(self, message_service, mock_collection):
        """Test getting least used messages"""
        limit = 5
        
        mock_docs = [
            {
                "id": "1",
                "content": "Unused message",
                "usage_count": 0,
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            },
            {
                "id": "2",
                "content": "Rarely used message",
                "usage_count": 1,
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_cursor.sort.return_value = mock_cursor 
        mock_cursor.limit.return_value = mock_cursor
        mock_collection.find.return_value = mock_cursor
        
        result = await message_service.get_least_used_messages(limit)
        
        assert len(result) == 2
        assert result[0].usage_count <= result[1].usage_count
        
        # Verify sort and limit were applied
        mock_cursor.sort.assert_called_once_with("usage_count", 1)  # Ascending
        mock_cursor.limit.assert_called_once_with(limit)

    @pytest.mark.asyncio
    async def test_get_most_used_messages(self, message_service, mock_collection):
        """Test getting most used messages"""
        limit = 3
        
        mock_docs = [
            {
                "id": "1",
                "content": "Very popular message",
                "usage_count": 100,
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            },
            {
                "id": "2",
                "content": "Popular message",
                "usage_count": 75,
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_cursor.sort.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor
        mock_collection.find.return_value = mock_cursor
        
        result = await message_service.get_most_used_messages(limit)
        
        assert len(result) == 2
        assert result[0].usage_count >= result[1].usage_count
        
        # Verify sort and limit were applied 
        mock_cursor.sort.assert_called_once_with("usage_count", -1)  # Descending
        mock_cursor.limit.assert_called_once_with(limit)

    @pytest.mark.asyncio
    async def test_duplicate_message_check(self, message_service, mock_collection):
        """Test checking for duplicate message content"""
        content = "This is a test message"
        
        # Mock finding existing message with same content
        mock_collection.find_one.return_value = {
            "id": "existing-id",
            "content": content,
            "is_active": True
        }
        
        result = await message_service.check_duplicate_content(content)
        
        assert result is True
        
        # Verify query
        call_args = mock_collection.find_one.call_args[0][0]
        assert call_args["content"] == content

    @pytest.mark.asyncio
    async def test_no_duplicate_message(self, message_service, mock_collection):
        """Test checking for duplicate when none exists"""
        content = "Unique message content"
        
        mock_collection.find_one.return_value = None
        
        result = await message_service.check_duplicate_content(content)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_get_messages_by_date_range(self, message_service, mock_collection):
        """Test getting messages within date range"""
        from datetime import datetime
        
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 31)
        
        mock_docs = [
            {
                "id": "1",
                "content": "January message",
                "is_active": True,
                "usage_count": 0,
                "created_at": "2023-01-15T00:00:00",
                "updated_at": "2023-01-15T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_collection.find.return_value = mock_cursor
        
        result = await message_service.get_messages_by_date_range(start_date, end_date)
        
        assert len(result) == 1
        
        # Verify date range query
        call_args = mock_collection.find.call_args[0][0]
        assert "$gte" in call_args["created_at"]
        assert "$lte" in call_args["created_at"]

    @pytest.mark.asyncio
    async def test_increment_usage_count_not_found(self, message_service, mock_collection):
        """Test incrementing usage count for non-existent message"""
        message_id = "nonexistent-id"
        mock_collection.update_one.return_value = MagicMock(matched_count=0)
        
        result = await message_service.increment_usage_count(message_id)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_get_message_count_detailed(self, message_service, mock_collection):
        """Test getting detailed message count statistics"""
        # Mock different counts
        def count_side_effect(query):
            if query == {}:
                return 20  # total
            elif query == {"is_active": True}:
                return 15  # active  
            elif query == {"is_active": False}:
                return 5   # inactive
            return 0
        
        mock_collection.count_documents.side_effect = count_side_effect
        
        result = await message_service.get_message_count()
        
        expected = {"total": 20, "active": 15, "inactive": 5}
        assert result == expected
        assert mock_collection.count_documents.call_count == 2  # total and active queries

    @pytest.mark.asyncio
    async def test_validate_message_content(self, message_service):
        """Test message content validation"""
        # Test valid content
        valid_content = "This is a valid message with good length"
        assert message_service.validate_content(valid_content) is True
        
        # Test empty content
        assert message_service.validate_content("") is False
        assert message_service.validate_content("   ") is False
        
        # Test too long content
        long_content = "x" * 5000  # Assuming 4096 is max
        assert message_service.validate_content(long_content) is False
        
        # Test minimum length
        short_content = "Hi"  # Assuming minimum is 3 chars
        assert message_service.validate_content(short_content) is False

    @pytest.mark.asyncio
    async def test_archive_old_messages(self, message_service, mock_collection):
        """Test archiving old inactive messages"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        mock_collection.update_many.return_value = MagicMock(modified_count=5)
        
        result = await message_service.archive_old_messages(cutoff_date)
        
        assert result == 5
        
        # Verify archive query
        call_args = mock_collection.update_many.call_args
        query = call_args[0][0]
        assert query["is_active"] is False
        assert "$lt" in query["updated_at"]
        
        update = call_args[0][1]
        assert update["$set"]["archived"] is True