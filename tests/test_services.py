"""
Business logic tests - Core functionality only
"""

from src.models.blacklist import BlacklistCreate, BlacklistReason, BlacklistType
from src.models.group import GroupCreate
from src.models.message import MessageCreate
from src.services.blacklist_service import BlacklistService
from src.services.group_service import GroupService
from src.services.message_service import MessageService


class TestMessageService:
    """Test message service basics"""

    async def test_create_message(self, test_database) -> None:
        """Test message creation service"""
        service = MessageService(test_database)

        message_data = MessageCreate(content="Test content")
        message = await service.create_message(message_data)
        assert message.content == "Test content"
        assert message.is_active is True

    async def test_get_active_messages(self, test_database) -> None:
        """Test getting active messages"""
        service = MessageService(test_database)

        # Create test message
        message_data = MessageCreate(content="Active message")
        await service.create_message(message_data)

        messages = await service.get_active_messages()
        assert len(messages) >= 1
        assert all(msg.is_active for msg in messages)


class TestGroupService:
    """Test group service basics"""

    async def test_create_group(self, test_database) -> None:
        """Test group creation service"""
        service = GroupService(test_database)

        group_data = GroupCreate(group_identifier="-1001234567890")
        group = await service.create_group(group_data)
        assert group.group_id == "-1001234567890"
        assert group.is_active is True

    async def test_get_active_groups(self, test_database) -> None:
        """Test getting active groups"""
        service = GroupService(test_database)

        # Create test group
        group_data = GroupCreate(group_identifier="-1001234567890")
        await service.create_group(group_data)

        groups = await service.get_active_groups()
        assert len(groups) >= 1
        assert all(group.is_active for group in groups)


class TestBlacklistService:
    """Test blacklist service basics"""

    async def test_create_blacklist(self, test_database) -> None:
        """Test blacklist creation"""
        service = BlacklistService(test_database)

        blacklist_data = BlacklistCreate(
            group_id="-1001234567890",
            group_identifier="test_group",
            blacklist_type=BlacklistType.PERMANENT,
            reason=BlacklistReason.USER_BLOCKED,
            duration_seconds=None,
            error_message="Test error"
        )
        blacklist = await service.add_to_blacklist(blacklist_data)
        assert blacklist.group_id == "-1001234567890"
        assert blacklist.blacklist_type == BlacklistType.PERMANENT

    async def test_is_blacklisted(self, test_database) -> None:
        """Test blacklist checking"""
        service = BlacklistService(test_database)

        # Add to blacklist
        blacklist_data = BlacklistCreate(
            group_id="-1001234567890",
            group_identifier="test_group",
            blacklist_type=BlacklistType.PERMANENT,
            reason=BlacklistReason.USER_BLOCKED,
            duration_seconds=None,
            error_message="Test error"
        )
        await service.add_to_blacklist(blacklist_data)

        # Check if blacklisted
        is_blacklisted = await service.is_blacklisted("-1001234567890")
        assert is_blacklisted is True

    async def test_cleanup_expired(self, test_database) -> None:
        """Test cleanup of expired blacklists"""
        service = BlacklistService(test_database)

        # This should not raise errors
        cleaned = await service.cleanup_expired()
        assert isinstance(cleaned, int)
