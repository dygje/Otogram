"""
Tests for Message Models
"""

import pytest
from pydantic import ValidationError

from src.models.message import Message, MessageCreate, MessageUpdate


class TestMessage:
    """Test Message model"""

    def test_message_creation_minimal(self):
        """Test creating message with minimal fields"""
        message = Message(content="Test message")
        
        assert message.content == "Test message"
        assert message.is_active is True
        assert message.usage_count == 0
        
        # Check inherited fields
        assert hasattr(message, 'id')
        assert hasattr(message, 'created_at')
        assert hasattr(message, 'updated_at')

    def test_message_creation_full(self):
        """Test creating message with all fields"""
        message = Message(
            content="Full test message",
            is_active=False,
            usage_count=5
        )
        
        assert message.content == "Full test message"
        assert message.is_active is False
        assert message.usage_count == 5

    def test_message_default_values(self):
        """Test message default values"""
        message = Message(content="Test")
        
        assert message.is_active is True
        assert message.usage_count == 0

    def test_message_content_types(self):
        """Test message with different content types"""
        # Simple text
        msg1 = Message(content="Simple message")
        assert msg1.content == "Simple message"
        
        # Message with emojis
        msg2 = Message(content="Hello! 👋 This is a test message 🎉")
        assert msg2.content == "Hello! 👋 This is a test message 🎉"
        
        # Message with newlines
        msg3 = Message(content="Line 1\nLine 2\nLine 3")
        assert msg3.content == "Line 1\nLine 2\nLine 3"
        
        # Message with special characters
        msg4 = Message(content="Special chars: @#$%^&*()_+-=[]{}|;':\",./<>?`~")
        assert "Special chars:" in msg4.content

    def test_message_long_content(self):
        """Test message with long content"""
        long_content = "A" * 4000  # Close to Telegram's limit
        message = Message(content=long_content)
        assert len(message.content) == 4000

    def test_message_usage_count_operations(self):
        """Test message usage count scenarios"""
        message = Message(content="Test", usage_count=10)
        assert message.usage_count == 10
        
        # Simulate incrementing usage count
        message.usage_count += 1
        assert message.usage_count == 11

    def test_message_active_inactive(self):
        """Test message active/inactive states"""
        # Active message
        active_msg = Message(content="Active", is_active=True)
        assert active_msg.is_active is True
        
        # Inactive message
        inactive_msg = Message(content="Inactive", is_active=False)
        assert inactive_msg.is_active is False

    def test_message_serialization(self):
        """Test message serialization"""
        message = Message(
            content="Serialization test",
            is_active=True,
            usage_count=3
        )
        
        # Test model_dump
        data = message.model_dump()
        assert isinstance(data, dict)
        assert data['content'] == "Serialization test"
        assert data['is_active'] is True
        assert data['usage_count'] == 3
        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data

    def test_message_json_serialization(self):
        """Test message JSON serialization"""
        message = Message(content="JSON test")
        
        json_str = message.model_dump_json()
        assert isinstance(json_str, str)
        assert "JSON test" in json_str

    def test_message_validation(self):
        """Test message field validation"""
        # Content is required
        with pytest.raises(ValidationError):
            Message()
        
        # Content cannot be None
        with pytest.raises(ValidationError):
            Message(content=None)

    def test_message_update_operations(self):
        """Test message update scenarios"""
        message = Message(content="Original content")
        original_updated_at = message.updated_at
        
        # Simulate updating content
        message.content = "Updated content"
        message.update_timestamp()
        
        assert message.content == "Updated content"
        assert message.updated_at > original_updated_at


class TestMessageCreate:
    """Test MessageCreate model"""

    def test_message_create_valid(self):
        """Test creating MessageCreate with valid data"""
        data = MessageCreate(content="Test message content")
        
        assert data.content == "Test message content"

    def test_message_create_validation_empty(self):
        """Test MessageCreate validation with empty content"""
        with pytest.raises(ValidationError):
            MessageCreate(content="")

    def test_message_create_validation_too_long(self):
        """Test MessageCreate validation with content too long"""
        long_content = "A" * 4097  # Over Telegram's limit
        
        with pytest.raises(ValidationError):
            MessageCreate(content=long_content)

    def test_message_create_validation_minimum_length(self):
        """Test MessageCreate minimum length validation"""
        # Single character should be valid
        data = MessageCreate(content="A")
        assert data.content == "A"

    def test_message_create_validation_max_length(self):
        """Test MessageCreate maximum length validation"""
        # Exactly at the limit should be valid
        max_content = "A" * 4096
        data = MessageCreate(content=max_content)
        assert len(data.content) == 4096

    def test_message_create_special_content(self):
        """Test MessageCreate with special content"""
        # Whitespace should be preserved
        data = MessageCreate(content="  Spaced content  ")
        assert data.content == "  Spaced content  "
        
        # Unicode content
        data = MessageCreate(content="Unicode: ñáéíóú 中文 🎉")
        assert "Unicode:" in data.content

    def test_message_create_multiline(self):
        """Test MessageCreate with multiline content"""
        multiline = """Line 1
Line 2
Line 3"""
        data = MessageCreate(content=multiline)
        assert "Line 1" in data.content
        assert "Line 2" in data.content
        assert "Line 3" in data.content

    def test_message_create_required_field(self):
        """Test that content is required"""
        with pytest.raises(ValidationError):
            MessageCreate()


class TestMessageUpdate:
    """Test MessageUpdate model"""

    def test_message_update_content_only(self):
        """Test MessageUpdate with content only"""
        data = MessageUpdate(content="Updated content")
        
        assert data.content == "Updated content"
        assert data.is_active is None

    def test_message_update_is_active_only(self):
        """Test MessageUpdate with is_active only"""
        data = MessageUpdate(is_active=False)
        
        assert data.content is None
        assert data.is_active is False

    def test_message_update_both_fields(self):
        """Test MessageUpdate with both fields"""
        data = MessageUpdate(
            content="Updated content",
            is_active=False
        )
        
        assert data.content == "Updated content"
        assert data.is_active is False

    def test_message_update_all_none(self):
        """Test MessageUpdate with all fields None"""
        data = MessageUpdate()
        
        assert data.content is None
        assert data.is_active is None

    def test_message_update_content_validation(self):
        """Test MessageUpdate content validation"""
        # Empty string should fail
        with pytest.raises(ValidationError):
            MessageUpdate(content="")
        
        # Too long should fail
        with pytest.raises(ValidationError):
            MessageUpdate(content="A" * 4097)

    def test_message_update_valid_lengths(self):
        """Test MessageUpdate with valid content lengths"""
        # Minimum length
        data = MessageUpdate(content="A")
        assert data.content == "A"
        
        # Maximum length
        max_content = "B" * 4096
        data = MessageUpdate(content=max_content)
        assert len(data.content) == 4096

    def test_message_update_active_states(self):
        """Test MessageUpdate with different active states"""
        # True
        data1 = MessageUpdate(is_active=True)
        assert data1.is_active is True
        
        # False
        data2 = MessageUpdate(is_active=False)
        assert data2.is_active is False

    def test_message_update_serialization(self):
        """Test MessageUpdate serialization"""
        data = MessageUpdate(
            content="Update test",
            is_active=True
        )
        
        dict_data = data.model_dump()
        assert dict_data['content'] == "Update test"
        assert dict_data['is_active'] is True

    def test_message_update_partial_serialization(self):
        """Test MessageUpdate serialization with partial data"""
        data = MessageUpdate(content="Partial update")
        
        dict_data = data.model_dump()
        assert dict_data['content'] == "Partial update"
        assert dict_data['is_active'] is None

    def test_message_update_exclude_none(self):
        """Test MessageUpdate excluding None values"""
        data = MessageUpdate(content="Only content")
        
        # Exclude None values
        dict_data = data.model_dump(exclude_none=True)
        assert 'content' in dict_data
        assert 'is_active' not in dict_data
        
        # Include None values (default)
        dict_data_with_none = data.model_dump()
        assert 'content' in dict_data_with_none
        assert 'is_active' in dict_data_with_none
        assert dict_data_with_none['is_active'] is None


class TestMessageModelIntegration:
    """Test integration between Message models"""

    def test_create_to_message_conversion(self):
        """Test converting MessageCreate to Message"""
        create_data = MessageCreate(content="Integration test")
        
        # Create Message from MessageCreate data
        message = Message(content=create_data.content)
        
        assert message.content == create_data.content
        assert message.is_active is True  # Default value
        assert message.usage_count == 0   # Default value

    def test_update_model_usage(self):
        """Test using MessageUpdate model for updates"""
        # Original message
        message = Message(content="Original", is_active=True)
        
        # Update data
        update_data = MessageUpdate(
            content="Updated content",
            is_active=False
        )
        
        # Apply updates (simulated)
        if update_data.content is not None:
            message.content = update_data.content
        if update_data.is_active is not None:
            message.is_active = update_data.is_active
        
        assert message.content == "Updated content"
        assert message.is_active is False

    def test_partial_update_scenario(self):
        """Test partial update scenario"""
        message = Message(
            content="Original content",
            is_active=True,
            usage_count=5
        )
        
        # Partial update - only content
        update_data = MessageUpdate(content="New content")
        
        # Apply partial update
        if update_data.content is not None:
            message.content = update_data.content
        # is_active remains unchanged since it's not in update
        
        assert message.content == "New content"
        assert message.is_active is True  # Unchanged
        assert message.usage_count == 5   # Unchanged

    def test_model_config_example(self):
        """Test that model config example is valid"""
        # The example from Message model config should be valid
        example_data = {
            "content": "Hello! This is a broadcast message.",
            "is_active": True,
            "usage_count": 0,
        }
        
        message = Message(**example_data)
        assert message.content == example_data["content"]
        assert message.is_active == example_data["is_active"]
        assert message.usage_count == example_data["usage_count"]