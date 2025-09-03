"""
Tests for data models
"""
from datetime import datetime

import pytest
from pydantic import ValidationError

from src.models.base import BaseDocument
from src.models.group import Group, GroupBulkCreate, GroupCreate
from src.models.message import Message, MessageCreate, MessageUpdate


class TestBaseDocument:
    """Test BaseDocument class"""

    def test_base_document_creation(self):
        """Test base document creation with default values"""
        doc = BaseDocument()

        assert doc.id is not None
        assert isinstance(doc.id, str)
        assert doc.created_at is not None
        assert doc.updated_at is not None
        assert isinstance(doc.created_at, datetime)
        assert isinstance(doc.updated_at, datetime)

    def test_update_timestamp(self):
        """Test timestamp update"""
        doc = BaseDocument()
        original_updated = doc.updated_at

        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.001)

        doc.update_timestamp()
        assert doc.updated_at > original_updated


class TestMessage:
    """Test Message model"""

    def test_message_creation(self):
        """Test message creation with required fields"""
        message = Message(content="Test message")

        assert message.content == "Test message"
        assert message.is_active is True
        assert message.usage_count == 0
        assert message.id is not None
        assert message.created_at is not None

    def test_message_create_validation(self):
        """Test MessageCreate validation"""
        # Valid message
        msg_create = MessageCreate(content="Valid message")
        assert msg_create.content == "Valid message"

        # Empty content
        with pytest.raises(ValidationError):
            MessageCreate(content="")

        # Too long content (over 4096 chars)
        long_content = "a" * 4097
        with pytest.raises(ValidationError):
            MessageCreate(content=long_content)

    def test_message_update_validation(self):
        """Test MessageUpdate validation"""
        # Valid updates
        msg_update = MessageUpdate(content="Updated content")
        assert msg_update.content == "Updated content"

        msg_update = MessageUpdate(is_active=False)
        assert msg_update.is_active is False

        # All fields None (should be valid)
        msg_update = MessageUpdate()
        assert msg_update.content is None
        assert msg_update.is_active is None


class TestGroup:
    """Test Group model"""

    def test_group_creation(self):
        """Test group creation"""
        group = Group(
            group_id="-1001234567890",
            group_username="@testgroup",
            group_title="Test Group"
        )

        assert group.group_id == "-1001234567890"
        assert group.group_username == "@testgroup"
        assert group.group_title == "Test Group"
        assert group.is_active is True
        assert group.message_count == 0

    def test_username_validation(self):
        """Test username auto-correction"""
        # Username without @
        group = Group(group_username="testgroup")
        assert group.group_username == "@testgroup"

        # Username with @
        group = Group(group_username="@testgroup")
        assert group.group_username == "@testgroup"

        # None username
        group = Group(group_username=None)
        assert group.group_username is None

    def test_group_create_validation(self):
        """Test GroupCreate identifier validation"""
        # Group ID
        group_create = GroupCreate(group_identifier="-1001234567890")
        assert group_create.group_identifier == "-1001234567890"

        # Username with @
        group_create = GroupCreate(group_identifier="@testgroup")
        assert group_create.group_identifier == "@testgroup"

        # Username without @
        group_create = GroupCreate(group_identifier="testgroup")
        assert group_create.group_identifier == "@testgroup"

        # Telegram link
        group_create = GroupCreate(group_identifier="https://t.me/testgroup")
        assert group_create.group_identifier == "https://t.me/testgroup"

    def test_group_bulk_create(self):
        """Test bulk group creation"""
        identifiers_text = """
        -1001234567890
        @testgroup1
        testgroup2
        https://t.me/testgroup3
        
        @testgroup4
        """

        bulk_create = GroupBulkCreate(identifiers=identifiers_text)
        identifiers_list = bulk_create.get_identifiers_list()

        expected = [
            "-1001234567890",
            "@testgroup1",
            "@testgroup2",
            "https://t.me/testgroup3",
            "@testgroup4"
        ]

        assert identifiers_list == expected

    def test_empty_bulk_create(self):
        """Test bulk create with empty/whitespace input"""
        bulk_create = GroupBulkCreate(identifiers="   \n  \n  ")
        identifiers_list = bulk_create.get_identifiers_list()

        assert identifiers_list == []
