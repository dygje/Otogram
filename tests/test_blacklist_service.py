"""
Tests for Blacklist Service
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from src.services.blacklist_service import BlacklistService
from src.models.blacklist import (
    Blacklist,
    BlacklistCreate,
    BlacklistType,
    BlacklistReason,
)


class TestBlacklistService:
    """Test BlacklistService class"""

    @pytest.fixture
    def mock_collection(self):
        """Mock collection fixture"""
        return AsyncMock()

    @pytest.fixture
    def blacklist_service(self, mock_collection):
        """BlacklistService fixture with mocked collection"""
        with patch('src.services.blacklist_service.database') as mock_database:
            mock_database.get_collection.return_value = mock_collection
            service = BlacklistService()
            return service

    @pytest.mark.asyncio
    async def test_add_to_blacklist_permanent(self, blacklist_service, mock_collection):
        """Test adding permanent blacklist"""
        blacklist_data = BlacklistCreate(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.PERMANENT,
            reason=BlacklistReason.CHAT_FORBIDDEN,
        )
        
        mock_collection.delete_many.return_value = AsyncMock()
        mock_collection.insert_one.return_value = AsyncMock()
        
        result = await blacklist_service.add_to_blacklist(blacklist_data)
        
        assert isinstance(result, Blacklist)
        assert result.group_id == "-1001234567890"
        assert result.blacklist_type == BlacklistType.PERMANENT
        assert result.reason == BlacklistReason.CHAT_FORBIDDEN
        assert result.expires_at is None
        
        # Verify database operations
        mock_collection.delete_many.assert_called_once_with({"group_id": "-1001234567890"})
        mock_collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_to_blacklist_temporary(self, blacklist_service, mock_collection):
        """Test adding temporary blacklist"""
        blacklist_data = BlacklistCreate(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.TEMPORARY,
            reason=BlacklistReason.FLOOD_WAIT,
            duration_seconds=3600,
        )
        
        mock_collection.delete_many.return_value = AsyncMock()
        mock_collection.insert_one.return_value = AsyncMock()
        
        result = await blacklist_service.add_to_blacklist(blacklist_data)
        
        assert isinstance(result, Blacklist)
        assert result.group_id == "-1001234567890"
        assert result.blacklist_type == BlacklistType.TEMPORARY
        assert result.reason == BlacklistReason.FLOOD_WAIT
        assert result.duration_seconds == 3600
        assert result.expires_at is not None
        
        # Check that expires_at is set correctly (approximately 1 hour from now)
        expected_expires = datetime.utcnow() + timedelta(seconds=3600)
        time_diff = abs((result.expires_at - expected_expires).total_seconds())
        assert time_diff < 10  # Allow 10 seconds tolerance

    @pytest.mark.asyncio
    async def test_add_to_blacklist_with_identifier(self, blacklist_service, mock_collection):
        """Test adding blacklist with group identifier"""
        blacklist_data = BlacklistCreate(
            group_id="-1001234567890",
            group_identifier="@testgroup",
            blacklist_type=BlacklistType.PERMANENT,
            reason=BlacklistReason.CHAT_FORBIDDEN,
        )
        
        mock_collection.delete_many.return_value = AsyncMock()
        mock_collection.insert_one.return_value = AsyncMock()
        
        result = await blacklist_service.add_to_blacklist(blacklist_data)
        
        assert result.group_identifier == "@testgroup"

    @pytest.mark.asyncio
    async def test_add_from_error_permanent(self, blacklist_service, mock_collection):
        """Test adding blacklist from error message (permanent)"""
        group_id = "-1001234567890"
        error_msg = "ChatForbidden: User is banned from this chat"
        
        mock_collection.delete_many.return_value = AsyncMock()
        mock_collection.insert_one.return_value = AsyncMock()
        
        result = await blacklist_service.add_from_error(group_id, error_msg)
        
        assert isinstance(result, Blacklist)
        assert result.group_id == group_id
        assert result.blacklist_type == BlacklistType.PERMANENT
        assert result.reason == BlacklistReason.CHAT_FORBIDDEN
        assert result.error_message == error_msg

    @pytest.mark.asyncio
    async def test_add_from_error_temporary_with_duration(self, blacklist_service, mock_collection):
        """Test adding blacklist from error message (temporary with duration)"""
        group_id = "-1001234567890"
        error_msg = "FloodWait: wait 3600 seconds"
        
        mock_collection.delete_many.return_value = AsyncMock()
        mock_collection.insert_one.return_value = AsyncMock()
        
        result = await blacklist_service.add_from_error(group_id, error_msg)
        
        assert isinstance(result, Blacklist)
        assert result.group_id == group_id
        assert result.blacklist_type == BlacklistType.TEMPORARY
        assert result.reason == BlacklistReason.FLOOD_WAIT
        assert result.duration_seconds == 3600
        assert result.error_message == error_msg

    def test_extract_duration_from_error_flood_wait(self, blacklist_service):
        """Test extracting duration from FloodWait error"""
        error_msg = "FloodWait: wait 3600 seconds"
        duration = blacklist_service._extract_duration_from_error(error_msg)
        assert duration == 3600

    def test_extract_duration_from_error_slow_mode(self, blacklist_service):
        """Test extracting duration from SlowModeWait error"""
        error_msg = "SlowModeWait 30"
        duration = blacklist_service._extract_duration_from_error(error_msg)
        assert duration == 30

    def test_extract_duration_from_error_generic_seconds(self, blacklist_service):
        """Test extracting duration from generic seconds pattern"""
        error_msg = "Please wait 120 seconds before retrying"
        duration = blacklist_service._extract_duration_from_error(error_msg)
        assert duration == 120

    def test_extract_duration_from_error_no_match(self, blacklist_service):
        """Test extracting duration when no pattern matches"""
        with patch('src.services.blacklist_service.DEFAULT_FLOOD_DURATION', 300):
            error_msg = "Some flood error without duration"
            duration = blacklist_service._extract_duration_from_error(error_msg)
            assert duration == 300

    def test_extract_duration_from_error_slowmode_default(self, blacklist_service):
        """Test extracting duration for slowmode with default"""
        with patch('src.services.blacklist_service.DEFAULT_SLOWMODE_DURATION', 60):
            error_msg = "SlowMode restriction is active"
            duration = blacklist_service._extract_duration_from_error(error_msg)
            assert duration == 60

    @pytest.mark.asyncio
    async def test_is_blacklisted_true(self, blacklist_service, mock_collection):
        """Test is_blacklisted returns True when group is blacklisted"""
        group_id = "-1001234567890"
        
        # Mock cleanup_expired and find_one
        mock_collection.delete_many.return_value = MagicMock(deleted_count=0)
        mock_collection.find_one.return_value = {"group_id": group_id, "blacklist_type": "permanent"}
        
        result = await blacklist_service.is_blacklisted(group_id)
        
        assert result is True
        mock_collection.find_one.assert_called_with({"group_id": group_id})

    @pytest.mark.asyncio
    async def test_is_blacklisted_false(self, blacklist_service, mock_collection):
        """Test is_blacklisted returns False when group is not blacklisted"""
        group_id = "-1001234567890"
        
        # Mock cleanup_expired and find_one
        mock_collection.delete_many.return_value = MagicMock(deleted_count=0)
        mock_collection.find_one.return_value = None
        
        result = await blacklist_service.is_blacklisted(group_id)
        
        assert result is False
        mock_collection.find_one.assert_called_with({"group_id": group_id})

    @pytest.mark.asyncio
    async def test_get_blacklist_entry_found(self, blacklist_service, mock_collection):
        """Test getting blacklist entry when found"""
        group_id = "-1001234567890"
        mock_doc = {
            "id": "blacklist-id",
            "group_id": group_id,
            "blacklist_type": "permanent",
            "reason": "ChatForbidden",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }
        
        mock_collection.find_one.return_value = mock_doc
        
        result = await blacklist_service.get_blacklist_entry(group_id)
        
        assert result is not None
        assert isinstance(result, Blacklist)
        assert result.group_id == group_id
        mock_collection.find_one.assert_called_once_with({"group_id": group_id})

    @pytest.mark.asyncio
    async def test_get_blacklist_entry_not_found(self, blacklist_service, mock_collection):
        """Test getting blacklist entry when not found"""
        group_id = "-1001234567890"
        mock_collection.find_one.return_value = None
        
        result = await blacklist_service.get_blacklist_entry(group_id)
        
        assert result is None
        mock_collection.find_one.assert_called_once_with({"group_id": group_id})

    @pytest.mark.asyncio
    async def test_remove_from_blacklist_success(self, blacklist_service, mock_collection):
        """Test removing from blacklist successfully"""
        group_id = "-1001234567890"
        mock_collection.delete_one.return_value = MagicMock(deleted_count=1)
        
        result = await blacklist_service.remove_from_blacklist(group_id)
        
        assert result is True
        mock_collection.delete_one.assert_called_once_with({"group_id": group_id})

    @pytest.mark.asyncio
    async def test_remove_from_blacklist_not_found(self, blacklist_service, mock_collection):
        """Test removing from blacklist when not found"""
        group_id = "-1001234567890"
        mock_collection.delete_one.return_value = MagicMock(deleted_count=0)
        
        result = await blacklist_service.remove_from_blacklist(group_id)
        
        assert result is False
        mock_collection.delete_one.assert_called_once_with({"group_id": group_id})

    @pytest.mark.asyncio
    async def test_cleanup_expired(self, blacklist_service, mock_collection):
        """Test cleaning up expired blacklist entries"""
        mock_collection.delete_many.return_value = MagicMock(deleted_count=3)
        
        result = await blacklist_service.cleanup_expired()
        
        assert result == 3
        # Verify the correct query was used
        call_args = mock_collection.delete_many.call_args[0][0]
        assert call_args["blacklist_type"] == BlacklistType.TEMPORARY
        assert "$lte" in call_args["expires_at"]

    @pytest.mark.asyncio
    async def test_cleanup_expired_none(self, blacklist_service, mock_collection):
        """Test cleanup when no expired entries"""
        mock_collection.delete_many.return_value = MagicMock(deleted_count=0)
        
        result = await blacklist_service.cleanup_expired()
        
        assert result == 0

    @pytest.mark.asyncio
    async def test_get_all_blacklists(self, blacklist_service, mock_collection):
        """Test getting all blacklist entries"""
        mock_docs = [
            {
                "id": "blacklist-1",
                "group_id": "-1001111111",
                "blacklist_type": "permanent",
                "reason": "ChatForbidden",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
            },
            {
                "id": "blacklist-2",
                "group_id": "-1002222222",
                "blacklist_type": "temporary",
                "reason": "FloodWait",
                "expires_at": "2023-01-01T01:00:00",
                "duration_seconds": 3600,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
            }
        ]
        
        # Mock the async cursor properly
        async def mock_cursor():
            for doc in mock_docs:
                yield doc
        
        mock_collection.find.return_value = mock_cursor()
        
        result = await blacklist_service.get_all_blacklists()
        
        assert len(result) == 2
        assert all(isinstance(bl, Blacklist) for bl in result)
        assert result[0].group_id == "-1001111111"
        assert result[1].group_id == "-1002222222"

    @pytest.mark.asyncio
    async def test_get_blacklist_stats(self, blacklist_service, mock_collection):
        """Test getting blacklist statistics"""
        # Mock different counts
        def count_side_effect(query):
            if query == {}:
                return 10  # total
            elif query == {"blacklist_type": BlacklistType.PERMANENT}:
                return 6  # permanent
            elif query == {"blacklist_type": BlacklistType.TEMPORARY}:
                return 4  # temporary
            elif "expires_at" in query and "$lte" in query["expires_at"]:
                return 2  # expired
            return 0
        
        mock_collection.count_documents.side_effect = count_side_effect
        
        result = await blacklist_service.get_blacklist_stats()
        
        expected = {"total": 10, "permanent": 6, "temporary": 4, "expired": 2}
        assert result == expected
        assert mock_collection.count_documents.call_count == 4

    @pytest.mark.asyncio
    async def test_get_blacklist_entry_by_id_found(self, blacklist_service, mock_collection):
        """Test getting blacklist entry by ID when found"""
        blacklist_id = "blacklist-123"
        mock_doc = {
            "id": blacklist_id,
            "group_id": "-1001234567890",
            "blacklist_type": "permanent",
            "reason": "ChatForbidden",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }
        
        mock_collection.find_one.return_value = mock_doc
        
        result = await blacklist_service.get_blacklist_entry_by_id(blacklist_id)
        
        assert result is not None
        assert isinstance(result, Blacklist)
        assert result.id == blacklist_id
        mock_collection.find_one.assert_called_once_with({"id": blacklist_id})

    @pytest.mark.asyncio
    async def test_get_blacklist_entry_by_id_not_found(self, blacklist_service, mock_collection):
        """Test getting blacklist entry by ID when not found"""
        blacklist_id = "nonexistent-id"
        mock_collection.find_one.return_value = None
        
        result = await blacklist_service.get_blacklist_entry_by_id(blacklist_id)
        
        assert result is None
        mock_collection.find_one.assert_called_once_with({"id": blacklist_id})