"""
Business logic tests - Core functionality only
"""

import pytest

from src.services.message_service import MessageService
from src.services.group_service import GroupService
from src.services.blacklist_service import BlacklistService
from src.models.message import Message
from src.models.group import Group
from src.models.blacklist import BlacklistType


class TestMessageService:
    """Test message service basics"""

    async def test_create_message(self, test_database) -> None:
        """Test message creation service"""
        service = MessageService()
        
        message = await service.create_message("Test content")
        assert message.content == "Test content"
        assert message.is_active is True

    async def test_get_active_messages(self, test_database) -> None:
        """Test getting active messages"""
        service = MessageService()
        
        # Create test message
        await service.create_message("Active message")
        
        messages = await service.get_active_messages()
        assert len(messages) >= 1
        assert all(msg.is_active for msg in messages)


class TestGroupService:
    """Test group service basics"""

    async def test_create_group(self, test_database) -> None:
        """Test group creation service"""
        service = GroupService()
        
        group = await service.create_group("-1001234567890", "@testgroup")
        assert group.group_id == "-1001234567890"
        assert group.group_username == "@testgroup"
        assert group.is_active is True

    async def test_get_active_groups(self, test_database) -> None:
        """Test getting active groups"""
        service = GroupService()
        
        # Create test group
        await service.create_group("-1001234567890", "@testgroup")
        
        groups = await service.get_active_groups()
        assert len(groups) >= 1
        assert all(group.is_active for group in groups)


class TestBlacklistService:
    """Test blacklist service basics"""

    async def test_create_blacklist(self, test_database) -> None:
        """Test blacklist creation"""
        service = BlacklistService()
        
        blacklist = await service.add_to_blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.PERMANENT,
            reason="UserDeactivated"
        )
        assert blacklist.group_id == "-1001234567890"
        assert blacklist.blacklist_type == BlacklistType.PERMANENT

    async def test_is_blacklisted(self, test_database) -> None:
        """Test blacklist checking"""
        service = BlacklistService()
        
        # Add to blacklist
        await service.add_to_blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.PERMANENT,
            reason="Test"
        )
        
        # Check if blacklisted
        is_blacklisted, _ = await service.is_blacklisted("-1001234567890")
        assert is_blacklisted is True

    async def test_cleanup_expired(self, test_database) -> None:
        """Test cleanup of expired blacklists"""
        service = BlacklistService()
        
        # This should not raise errors
        cleaned = await service.cleanup_expired_blacklists()
        assert isinstance(cleaned, int)