"""
Data models tests - Key validation only
"""

import pytest
from pydantic import ValidationError

from src.models.blacklist import Blacklist, BlacklistType, BlacklistReason
from src.models.group import Group
from src.models.message import Message, MessageCreate


class TestMessage:
    """Test message model basics"""

    def test_message_creation(self) -> None:
        """Test message creation works"""
        message = Message(content="Test message")
        assert message.content == "Test message"
        assert message.is_active is True
        assert message.usage_count == 0

    def test_message_validation(self) -> None:
        """Test message validation"""
        # Valid
        msg = MessageCreate(content="Valid message")
        assert msg.content == "Valid message"

        # Empty content should fail
        with pytest.raises(ValidationError):
            MessageCreate(content="")

        # Too long should fail
        with pytest.raises(ValidationError):
            MessageCreate(content="x" * 5000)


class TestGroup:
    """Test group model basics"""

    def test_group_creation(self) -> None:
        """Test group creation works"""
        group = Group(
            group_id="-1001234567890", group_username="@testgroup", group_title="Test Group"
        )
        assert group.group_id == "-1001234567890"
        assert group.group_username == "@testgroup"
        assert group.is_active is True

    def test_username_formatting(self) -> None:
        """Test username auto-formatting"""
        # Without @
        group = Group(group_username="testgroup")
        assert group.group_username == "@testgroup"

        # With @
        group = Group(group_username="@testgroup")
        assert group.group_username == "@testgroup"


class TestBlacklist:
    """Test blacklist model basics"""

    def test_blacklist_creation(self) -> None:
        """Test blacklist creation works"""
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.PERMANENT,
            reason="UserDeactivated",
        )
        assert blacklist.group_id == "-1001234567890"
        assert blacklist.blacklist_type == BlacklistType.PERMANENT
        assert blacklist.reason == "UserDeactivated"

    def test_temporary_blacklist(self) -> None:
        """Test temporary blacklist with expiration"""
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.TEMPORARY,
            reason="FloodWait",
            duration_seconds=3600,
        )
        assert blacklist.expires_at is not None
        assert not blacklist.is_expired()
