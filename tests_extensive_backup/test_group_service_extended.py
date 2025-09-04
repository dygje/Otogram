"""
Extended tests for Group Service to improve coverage
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.services.group_service import GroupService
from src.models.group import Group, GroupCreate, GroupBulkCreate


class TestGroupServiceExtended:
    """Extended test coverage for GroupService class"""

    @pytest.fixture
    def mock_collection(self):
        """Mock collection fixture"""
        return AsyncMock()

    @pytest.fixture
    def group_service(self, mock_collection):
        """GroupService fixture with mocked collection"""
        with patch('src.services.group_service.database') as mock_database:
            mock_database.get_collection.return_value = mock_collection
            service = GroupService()
            return service

    @pytest.mark.asyncio
    async def test_create_bulk_groups_empty_list(self, group_service):
        """Test creating bulk groups with empty list"""
        bulk_data = GroupBulkCreate(identifiers="")
        
        result = await group_service.create_bulk_groups(bulk_data)
        
        assert result == []

    @pytest.mark.asyncio
    async def test_create_bulk_groups_single_identifier(self, group_service, mock_collection):
        """Test creating bulk groups with single identifier"""
        bulk_data = GroupBulkCreate(identifiers="-1001234567890")
        mock_collection.insert_many.return_value = AsyncMock()
        
        result = await group_service.create_bulk_groups(bulk_data)
        
        assert len(result) == 1
        assert result[0].group_id == "-1001234567890"
        mock_collection.insert_many.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_bulk_groups_multiple_identifiers(self, group_service, mock_collection):
        """Test creating bulk groups with multiple identifiers"""
        identifiers = "-1001234567890\n@testgroup\nhttps://t.me/testgroup2"
        bulk_data = GroupBulkCreate(identifiers=identifiers)
        mock_collection.insert_many.return_value = AsyncMock()
        
        result = await group_service.create_bulk_groups(bulk_data)
        
        assert len(result) == 3
        assert result[0].group_id == "-1001234567890"
        assert result[1].group_username == "testgroup"
        assert result[2].group_link == "https://t.me/testgroup2"
        mock_collection.insert_many.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_group_stats(self, group_service, mock_collection):
        """Test getting group statistics"""
        # Mock different counts
        def count_side_effect(query):
            if query == {}:
                return 15  # total
            elif query == {"is_active": True}:
                return 12  # active
            return 0
        
        mock_collection.count_documents.side_effect = count_side_effect
        
        result = await group_service.get_group_stats()
        
        expected = {"total": 15, "active": 12, "inactive": 3}
        assert result == expected
        assert mock_collection.count_documents.call_count == 2

    @pytest.mark.asyncio
    async def test_toggle_group_status_activate(self, group_service, mock_collection):
        """Test toggling group status to active"""
        group_id = "test-group-id"
        
        # Mock finding inactive group
        mock_doc = {
            "id": group_id,
            "group_id": "-1001234567890",
            "is_active": False,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_doc
        mock_collection.update_one.return_value = MagicMock(modified_count=1)
        
        # Mock the updated document for return value
        updated_doc = mock_doc.copy()
        updated_doc["is_active"] = True
        
        # Setup find_one to return updated doc on second call
        mock_collection.find_one.side_effect = [mock_doc, updated_doc]
        
        result = await group_service.toggle_group_status(group_id)
        
        assert result is not None
        assert result.is_active is True
        
        # Verify update was called with correct parameters
        call_args = mock_collection.update_one.call_args
        assert call_args[0][0] == {"id": group_id}
        assert call_args[0][1]["$set"]["is_active"] is True

    @pytest.mark.asyncio
    async def test_toggle_group_status_deactivate(self, group_service, mock_collection):
        """Test toggling group status to inactive"""
        group_id = "test-group-id"
        
        # Mock finding active group
        mock_doc = {
            "id": group_id,
            "group_id": "-1001234567890",
            "is_active": True,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_doc
        mock_collection.update_one.return_value = MagicMock(modified_count=1)
        
        # Mock the updated document for return value
        updated_doc = mock_doc.copy()
        updated_doc["is_active"] = False
        
        # Setup find_one to return updated doc on second call
        mock_collection.find_one.side_effect = [mock_doc, updated_doc]
        
        result = await group_service.toggle_group_status(group_id)
        
        assert result is not None
        assert result.is_active is False

    @pytest.mark.asyncio
    async def test_toggle_group_status_not_found(self, group_service, mock_collection):
        """Test toggling status of non-existent group"""
        group_id = "nonexistent-id"
        mock_collection.find_one.return_value = None
        
        result = await group_service.toggle_group_status(group_id)
        
        assert result is None

    @pytest.mark.asyncio
    async def test_search_groups_by_username(self, group_service, mock_collection):
        """Test searching groups by username"""
        search_term = "test"
        
        # Mock cursor for find operation
        mock_cursor = AsyncMock()
        mock_docs = [
            {
                "id": "1",
                "group_username": "testgroup",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            },
            {
                "id": "2", 
                "group_username": "test_channel",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_collection.find.return_value = mock_cursor
        
        result = await group_service.search_groups(search_term)
        
        assert len(result) == 2
        assert all(isinstance(group, Group) for group in result)
        assert result[0].group_username == "testgroup"
        assert result[1].group_username == "test_channel"
        
        # Verify search query
        call_args = mock_collection.find.call_args[0][0]
        assert "$or" in call_args
        assert any("$regex" in condition.get("group_username", {}) for condition in call_args["$or"])

    @pytest.mark.asyncio
    async def test_search_groups_no_results(self, group_service, mock_collection):
        """Test searching groups with no results"""
        search_term = "nonexistent"
        
        # Mock empty cursor
        mock_cursor = AsyncMock()
        async def empty_iter():
            return
            yield  # Unreachable, but needed for async generator
        mock_cursor.__aiter__ = empty_iter
        mock_collection.find.return_value = mock_cursor
        
        result = await group_service.search_groups(search_term)
        
        assert result == []

    @pytest.mark.asyncio
    async def test_get_groups_by_status_active(self, group_service, mock_collection):
        """Test getting groups filtered by active status"""
        # Mock cursor for active groups
        mock_cursor = AsyncMock()
        mock_docs = [
            {
                "id": "1",
                "group_id": "-1001111111",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_collection.find.return_value = mock_cursor
        
        result = await group_service.get_groups_by_status(is_active=True)
        
        assert len(result) == 1
        assert result[0].is_active is True
        
        # Verify filter was applied
        call_args = mock_collection.find.call_args[0][0]
        assert call_args["is_active"] is True

    @pytest.mark.asyncio
    async def test_get_groups_by_status_inactive(self, group_service, mock_collection):
        """Test getting groups filtered by inactive status"""
        # Mock cursor for inactive groups
        mock_cursor = AsyncMock()
        mock_docs = [
            {
                "id": "1",
                "group_id": "-1001111111",
                "is_active": False,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_collection.find.return_value = mock_cursor
        
        result = await group_service.get_groups_by_status(is_active=False)
        
        assert len(result) == 1
        assert result[0].is_active is False

    @pytest.mark.asyncio
    async def test_batch_update_groups_success(self, group_service, mock_collection):
        """Test batch updating multiple groups"""
        group_ids = ["id1", "id2", "id3"]
        update_data = {"is_active": False}
        
        mock_collection.update_many.return_value = MagicMock(modified_count=3)
        
        result = await group_service.batch_update_groups(group_ids, update_data)
        
        assert result == 3
        
        # Verify update query
        call_args = mock_collection.update_many.call_args
        assert call_args[0][0] == {"id": {"$in": group_ids}}
        assert call_args[0][1]["$set"]["is_active"] is False
        assert "updated_at" in call_args[0][1]["$set"]

    @pytest.mark.asyncio
    async def test_batch_update_groups_partial_success(self, group_service, mock_collection):
        """Test batch updating with partial success"""
        group_ids = ["id1", "id2", "id3"]
        update_data = {"is_active": True}
        
        mock_collection.update_many.return_value = MagicMock(modified_count=2)  # Only 2 updated
        
        result = await group_service.batch_update_groups(group_ids, update_data)
        
        assert result == 2

    @pytest.mark.asyncio
    async def test_batch_delete_groups_success(self, group_service, mock_collection):
        """Test batch deleting multiple groups"""
        group_ids = ["id1", "id2", "id3"]
        
        mock_collection.delete_many.return_value = MagicMock(deleted_count=3)
        
        result = await group_service.batch_delete_groups(group_ids)
        
        assert result == 3
        
        # Verify delete query
        call_args = mock_collection.delete_many.call_args
        assert call_args[0][0] == {"id": {"$in": group_ids}}

    @pytest.mark.asyncio
    async def test_batch_delete_groups_no_matches(self, group_service, mock_collection):
        """Test batch deleting with no matches"""
        group_ids = ["nonexistent1", "nonexistent2"]
        
        mock_collection.delete_many.return_value = MagicMock(deleted_count=0)
        
        result = await group_service.batch_delete_groups(group_ids)
        
        assert result == 0

    @pytest.mark.asyncio
    async def test_get_groups_with_message_count_filter(self, group_service, mock_collection):
        """Test getting groups filtered by message count"""
        min_count = 5
        
        # Mock cursor
        mock_cursor = AsyncMock()
        mock_docs = [
            {
                "id": "1",
                "group_id": "-1001111111",
                "message_count": 10,
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_collection.find.return_value = mock_cursor
        
        result = await group_service.get_groups_with_message_count_filter(min_count)
        
        assert len(result) == 1
        assert result[0].message_count >= min_count
        
        # Verify filter was applied
        call_args = mock_collection.find.call_args[0][0]
        assert call_args["message_count"]["$gte"] == min_count

    @pytest.mark.asyncio
    async def test_reset_all_message_counts(self, group_service, mock_collection):
        """Test resetting all group message counts"""
        mock_collection.update_many.return_value = MagicMock(modified_count=10)
        
        result = await group_service.reset_all_message_counts()
        
        assert result == 10
        
        # Verify update query
        call_args = mock_collection.update_many.call_args
        assert call_args[0][0] == {}  # All documents
        assert call_args[0][1]["$set"]["message_count"] == 0
        assert "updated_at" in call_args[0][1]["$set"]

    @pytest.mark.asyncio
    async def test_get_group_activity_summary(self, group_service, mock_collection):
        """Test getting group activity summary"""
        # Mock aggregation pipeline result
        mock_cursor = AsyncMock()
        mock_results = [
            {
                "_id": None,
                "total_groups": 20,
                "active_groups": 15,
                "total_messages": 500,
                "avg_messages_per_group": 25.0
            }
        ]
        
        async def async_iter(results):
            for result in results:
                yield result
        
        mock_cursor.__aiter__ = lambda: async_iter(mock_results)
        mock_collection.aggregate.return_value = mock_cursor
        
        result = await group_service.get_group_activity_summary()
        
        expected = {
            "total_groups": 20,
            "active_groups": 15,
            "inactive_groups": 5,
            "total_messages": 500,
            "avg_messages_per_group": 25.0
        }
        assert result == expected
        
        # Verify aggregation was called
        mock_collection.aggregate.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_group_activity_summary_empty(self, group_service, mock_collection):
        """Test getting group activity summary with no data"""
        # Mock empty aggregation result
        mock_cursor = AsyncMock()
        async def empty_iter():
            return
            yield  # Unreachable
        mock_cursor.__aiter__ = empty_iter
        mock_collection.aggregate.return_value = mock_cursor
        
        result = await group_service.get_group_activity_summary()
        
        expected = {
            "total_groups": 0,
            "active_groups": 0,
            "inactive_groups": 0,
            "total_messages": 0,
            "avg_messages_per_group": 0.0
        }
        assert result == expected