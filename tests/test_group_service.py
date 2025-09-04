"""
Tests for Group Service
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.services.group_service import GroupService
from src.models.group import Group, GroupCreate, GroupBulkCreate


class TestGroupService:
    """Test GroupService class"""

    @pytest.fixture
    def mock_collection(self):
        """Mock collection fixture"""
        return AsyncMock()

    @pytest.fixture
    def group_service(self, mock_collection):
        """GroupService fixture with mocked collection"""
        service = GroupService()
        service.collection = mock_collection
        return service

    @pytest.mark.asyncio
    async def test_create_group_with_id(self, group_service, mock_collection):
        """Test group creation with group ID"""
        group_data = GroupCreate(group_identifier="-1001234567890")
        mock_collection.insert_one.return_value = AsyncMock()
        
        result = await group_service.create_group(group_data)
        
        assert isinstance(result, Group)
        assert result.group_id == "-1001234567890"
        assert result.group_username is None
        assert result.group_link is None
        assert result.is_active is True
        mock_collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_group_with_username(self, group_service, mock_collection):
        """Test group creation with username"""
        group_data = GroupCreate(group_identifier="@testgroup")
        mock_collection.insert_one.return_value = AsyncMock()
        
        result = await group_service.create_group(group_data)
        
        assert isinstance(result, Group)
        assert result.group_username == "@testgroup"
        assert result.group_id is None
        assert result.group_link is None
        assert result.is_active is True
        mock_collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_group_with_link(self, group_service, mock_collection):
        """Test group creation with t.me link"""
        group_data = GroupCreate(group_identifier="https://t.me/testgroup")
        mock_collection.insert_one.return_value = AsyncMock()
        
        result = await group_service.create_group(group_data)
        
        assert isinstance(result, Group)
        assert result.group_link == "https://t.me/testgroup"
        assert result.group_id is None
        assert result.group_username is None 
        assert result.is_active is True
        mock_collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_bulk_groups(self, group_service, mock_collection):
        """Test bulk group creation"""
        bulk_data = GroupBulkCreate(identifiers="-1001234567890\n@testgroup\nhttps://t.me/testgroup2")
        mock_collection.insert_many.return_value = AsyncMock()
        
        result = await group_service.create_bulk_groups(bulk_data)
        
        assert len(result) == 3
        assert all(isinstance(group, Group) for group in result)
        # Check first group (ID)
        assert result[0].group_id == "-1001234567890"
        # Check second group (username)
        assert result[1].group_username == "@testgroup"
        # Check third group (link)
        assert result[2].group_link == "https://t.me/testgroup2"
        mock_collection.insert_many.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_groups(self, group_service, mock_collection):
        """Test getting all groups"""
        mock_docs = [
            {
                "id": "test-id-1",
                "group_id": "-1001234567890",
                "group_username": None,
                "group_link": None,
                "group_title": "Test Group 1",
                "is_active": True,
                "message_count": 0,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        mock_collection.find.return_value.to_list.return_value = mock_docs
        
        result = await group_service.get_all_groups()
        
        assert len(result) == 1
        assert isinstance(result[0], Group)
        assert result[0].group_id == "-1001234567890"
        mock_collection.find.assert_called_once_with({})

    @pytest.mark.asyncio
    async def test_get_active_groups(self, group_service, mock_collection):
        """Test getting active groups"""
        mock_docs = [
            {
                "id": "test-id-1",
                "group_id": "-1001234567890",
                "group_username": None,
                "group_link": None,
                "group_title": "Active Group",
                "is_active": True,
                "message_count": 0,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        mock_collection.find.return_value.to_list.return_value = mock_docs
        
        result = await group_service.get_active_groups()
        
        assert len(result) == 1
        assert result[0].is_active is True
        mock_collection.find.assert_called_once_with({"is_active": True})

    @pytest.mark.asyncio
    async def test_get_group_by_id(self, group_service, mock_collection):
        """Test getting group by ID"""
        group_id = "test-id"
        mock_doc = {
            "id": group_id,
            "group_id": "-1001234567890",
            "group_username": None,
            "group_link": None,
            "group_title": "Test Group",
            "is_active": True,
            "message_count": 0,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_doc
        
        result = await group_service.get_group_by_id(group_id)
        
        assert result is not None
        assert isinstance(result, Group)
        assert result.id == group_id
        mock_collection.find_one.assert_called_once_with({"id": group_id})

    @pytest.mark.asyncio
    async def test_get_group_by_id_not_found(self, group_service, mock_collection):
        """Test getting group by ID when not found"""
        group_id = "nonexistent-id"
        mock_collection.find_one.return_value = None
        
        result = await group_service.get_group_by_id(group_id)
        
        assert result is None
        mock_collection.find_one.assert_called_once_with({"id": group_id})

    @pytest.mark.asyncio
    async def test_update_group(self, group_service, mock_collection):
        """Test updating group"""
        group_id = "test-id"
        update_data = {"group_title": "Updated Title", "is_active": False}
        mock_collection.update_one.return_value = MagicMock(matched_count=1)
        
        result = await group_service.update_group(group_id, update_data)
        
        assert result is True
        mock_collection.update_one.assert_called_once()
        call_args = mock_collection.update_one.call_args
        assert call_args[0][0] == {"id": group_id}
        update_doc = call_args[0][1]["$set"]
        assert update_doc["group_title"] == "Updated Title"
        assert update_doc["is_active"] is False
        assert "updated_at" in update_doc

    @pytest.mark.asyncio
    async def test_delete_group(self, group_service, mock_collection):
        """Test deleting group"""
        group_id = "test-id"
        mock_collection.delete_one.return_value = MagicMock(deleted_count=1)
        
        result = await group_service.delete_group(group_id)
        
        assert result is True
        mock_collection.delete_one.assert_called_once_with({"id": group_id})

    @pytest.mark.asyncio
    async def test_increment_message_count(self, group_service, mock_collection):
        """Test incrementing group message count"""
        group_id = "test-id"
        mock_collection.update_one.return_value = MagicMock(matched_count=1)
        
        result = await group_service.increment_message_count(group_id)
        
        assert result is True
        mock_collection.update_one.assert_called_once()
        call_args = mock_collection.update_one.call_args
        assert call_args[0][0] == {"id": group_id}
        assert "$inc" in call_args[0][1]
        assert call_args[0][1]["$inc"]["message_count"] == 1

    @pytest.mark.asyncio
    async def test_get_group_count(self, group_service, mock_collection):
        """Test getting total group count"""
        mock_collection.count_documents.return_value = 10
        
        result = await group_service.get_group_count()
        
        assert result == 10
        mock_collection.count_documents.assert_called_once_with({})

    @pytest.mark.asyncio
    async def test_get_active_group_count(self, group_service, mock_collection):
        """Test getting active group count"""
        mock_collection.count_documents.return_value = 7
        
        result = await group_service.get_active_group_count()
        
        assert result == 7
        mock_collection.count_documents.assert_called_once_with({"is_active": True})