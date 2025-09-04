"""
Tests for Telegram Handlers
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from telegram import Update, CallbackQuery, Message as TelegramMessage
from telegram.ext import ContextTypes

from src.telegram.handlers.message_handlers import MessageHandlers
from src.telegram.handlers.group_handlers import GroupHandlers
from src.telegram.handlers.config_handlers import ConfigHandlers
from src.telegram.handlers.blacklist_handlers import BlacklistHandlers


class TestMessageHandlers:
    """Test MessageHandlers class"""

    @pytest.fixture
    def message_handlers(self):
        """MessageHandlers fixture"""
        with patch('src.services.message_service.database'):
            return MessageHandlers()

    @pytest.mark.asyncio
    async def test_init(self, message_handlers):
        """Test MessageHandlers initialization"""
        assert message_handlers.message_service is not None
        # Note: user_states might not be a class attribute in actual implementation

    @pytest.mark.asyncio
    async def test_list_messages_empty(self, message_handlers):
        """Test listing messages when none exist"""
        # Mock empty message list
        message_handlers.message_service.get_all_messages = AsyncMock(return_value=[])
        message_handlers.message_service.get_message_count = AsyncMock(
            return_value={"total": 0, "active": 0, "inactive": 0}
        )
        
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()

        await message_handlers.list_messages(mock_update, mock_context)

        # Verify response was sent
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args[0][0]
        assert "No messages found" in call_args or "Tidak ada pesan" in call_args

    @pytest.mark.asyncio
    async def test_list_messages_with_data(self, message_handlers):
        """Test listing messages with data"""
        from src.models.message import Message
        
        mock_messages = [
            Message(content="Test message 1", is_active=True, usage_count=5),
            Message(content="Test message 2", is_active=False, usage_count=0),
        ]
        
        message_handlers.message_service.get_all_messages = AsyncMock(return_value=mock_messages)
        message_handlers.message_service.get_message_count = AsyncMock(
            return_value={"total": 2, "active": 1, "inactive": 1}
        )
        
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()

        await message_handlers.list_messages(mock_update, mock_context)

        # Verify response contains message data
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args
        assert call_args[1]["parse_mode"] == "Markdown"
        assert call_args[1]["reply_markup"] is not None

    @pytest.mark.asyncio
    async def test_add_message_command(self, message_handlers):
        """Test add message command"""
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()
        mock_context.user_data = {}

        await message_handlers.add_message_command(mock_update, mock_context)

        # Verify user state was set and prompt sent
        assert mock_context.user_data["waiting_for"] == "message_content"
        mock_message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_message_input_valid(self, message_handlers):
        """Test handling valid message input"""
        from src.models.message import Message
        
        # Mock successful message creation
        new_message = Message(content="New test message", is_active=True, usage_count=0)
        message_handlers.message_service.create_message = AsyncMock(return_value=new_message)
        
        mock_message = AsyncMock()
        mock_message.text = "New test message"
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()
        mock_context.user_data = {"waiting_for": "message_content"}

        await message_handlers.handle_message_input(mock_update, mock_context)

        # Verify message was created and user state cleared
        message_handlers.message_service.create_message.assert_called_once()
        assert "waiting_for" not in mock_context.user_data
        mock_message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_message_input_invalid(self, message_handlers):
        """Test handling invalid message input"""
        mock_message = AsyncMock()
        mock_message.text = ""  # Empty message
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()
        mock_context.user_data = {"waiting_for": "message_content"}

        await message_handlers.handle_message_input(mock_update, mock_context)

        # Verify error response and user state maintained
        assert mock_context.user_data["waiting_for"] == "message_content"
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args[0][0]
        assert "invalid" in call_args.lower() or "tidak valid" in call_args.lower()

    @pytest.mark.asyncio
    async def test_handle_callback_toggle_message(self, message_handlers):
        """Test handling callback to toggle message status"""
        from src.models.message import Message
        
        # Mock message toggle
        toggled_message = Message(content="Test message", is_active=False, usage_count=3)
        message_handlers.message_service.toggle_message_status = AsyncMock(return_value=toggled_message)
        
        mock_callback_query = AsyncMock()
        mock_update = MagicMock()
        mock_update.callback_query = mock_callback_query
        mock_context = MagicMock()

        await message_handlers.handle_callback(mock_update, mock_context, "messages_toggle_msg123")

        # Verify toggle was called and response sent
        message_handlers.message_service.toggle_message_status.assert_called_once_with("msg123")
        mock_callback_query.edit_message_text.assert_called_once()


class TestGroupHandlers:
    """Test GroupHandlers class"""

    @pytest.fixture
    def group_handlers(self):
        """GroupHandlers fixture"""
        with patch('src.services.group_service.database'):
            return GroupHandlers()

    @pytest.mark.asyncio
    async def test_init(self, group_handlers):
        """Test GroupHandlers initialization"""
        assert group_handlers.group_service is not None
        assert hasattr(group_handlers, 'user_states')

    @pytest.mark.asyncio
    async def test_list_groups_empty(self, group_handlers):
        """Test listing groups when none exist"""
        # Mock empty group list
        group_handlers.group_service.get_all_groups = AsyncMock(return_value=[])
        group_handlers.group_service.get_group_stats = AsyncMock(
            return_value={"total": 0, "active": 0, "inactive": 0}
        )
        
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()

        await group_handlers.list_groups(mock_update, mock_context)

        # Verify response was sent
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args[0][0]
        assert "No groups" in call_args or "Tidak ada grup" in call_args

    @pytest.mark.asyncio
    async def test_add_group_command(self, group_handlers):
        """Test add group command"""
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()
        mock_context.user_data = {}

        await group_handlers.add_group_command(mock_update, mock_context)

        # Verify user state was set
        assert mock_context.user_data["waiting_for"] == "group_identifier"
        mock_message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_groups_bulk_command(self, group_handlers):
        """Test add groups bulk command"""
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()
        mock_context.user_data = {}

        await group_handlers.add_groups_bulk_command(mock_update, mock_context)

        # Verify user state was set for bulk input
        assert mock_context.user_data["waiting_for"] == "groups_bulk"
        mock_message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_group_input_valid(self, group_handlers):
        """Test handling valid group input"""
        from src.models.group import Group
        
        # Mock successful group creation
        new_group = Group(group_id="-1001234567890", is_active=True)
        group_handlers.group_service.create_group = AsyncMock(return_value=new_group)
        
        mock_message = AsyncMock()
        mock_message.text = "-1001234567890"
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()
        mock_context.user_data = {"waiting_for": "group_identifier"}

        await group_handlers.handle_group_input(mock_update, mock_context)

        # Verify group was created
        group_handlers.group_service.create_group.assert_called_once()
        assert "waiting_for" not in mock_context.user_data
        mock_message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_bulk_input_valid(self, group_handlers):
        """Test handling valid bulk group input"""
        from src.models.group import Group
        
        # Mock successful bulk creation
        new_groups = [
            Group(group_id="-1001111111", is_active=True),
            Group(group_username="testgroup", is_active=True),
        ]
        group_handlers.group_service.create_bulk_groups = AsyncMock(return_value=new_groups)
        
        mock_message = AsyncMock()
        mock_message.text = "-1001111111\n@testgroup"
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()
        mock_context.user_data = {"waiting_for": "groups_bulk"}

        await group_handlers.handle_bulk_input(mock_update, mock_context)

        # Verify groups were created
        group_handlers.group_service.create_bulk_groups.assert_called_once()
        assert "waiting_for" not in mock_context.user_data
        mock_message.reply_text.assert_called_once()


class TestConfigHandlers:
    """Test ConfigHandlers class"""

    @pytest.fixture
    def config_handlers(self):
        """ConfigHandlers fixture"""
        with patch('src.services.config_service.database'):
            return ConfigHandlers()

    @pytest.mark.asyncio
    async def test_init(self, config_handlers):
        """Test ConfigHandlers initialization"""
        assert config_handlers.config_service is not None

    @pytest.mark.asyncio
    async def test_show_config(self, config_handlers):
        """Test showing configuration"""
        from src.models.config import Configuration
        
        # Mock config data
        mock_configs = [
            Configuration(key="min_delay", value="5", description="Min delay"),
            Configuration(key="max_delay", value="10", description="Max delay"),
        ]
        
        config_handlers.config_service.get_all_configs = AsyncMock(return_value=mock_configs)
        
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()

        await config_handlers.show_config(mock_update, mock_context)

        # Verify response was sent
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args
        assert call_args[1]["parse_mode"] == "Markdown"
        assert call_args[1]["reply_markup"] is not None

    @pytest.mark.asyncio
    async def test_handle_callback_edit_config(self, config_handlers):
        """Test handling callback to edit config"""
        from src.models.config import Configuration
        
        # Mock config retrieval
        mock_config = Configuration(key="test_setting", value="current_value", description="Test setting")
        config_handlers.config_service.get_config = AsyncMock(return_value=mock_config)
        
        mock_callback_query = AsyncMock()
        mock_update = MagicMock()
        mock_update.callback_query = mock_callback_query
        mock_context = MagicMock()
        mock_context.user_data = {}

        await config_handlers.handle_callback(mock_update, mock_context, "config_edit_test_setting")

        # Verify config was retrieved and user state set
        config_handlers.config_service.get_config.assert_called_once_with("test_setting")
        assert mock_context.user_data["waiting_for"] == "config_test_setting"
        mock_callback_query.edit_message_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_config_input_valid(self, config_handlers):
        """Test handling valid config input"""
        from src.models.config import Configuration
        
        # Mock config update
        updated_config = Configuration(key="test_setting", value="new_value", description="Test setting")
        config_handlers.config_service.set_config = AsyncMock(return_value=updated_config)
        
        mock_message = AsyncMock()
        mock_message.text = "new_value"
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()
        mock_context.user_data = {"waiting_for": "config_test_setting"}

        await config_handlers.handle_config_input(mock_update, mock_context)

        # Verify config was updated
        config_handlers.config_service.set_config.assert_called_once_with("test_setting", "new_value")
        assert "waiting_for" not in mock_context.user_data
        mock_message.reply_text.assert_called_once()


class TestBlacklistHandlers:
    """Test BlacklistHandlers class"""

    @pytest.fixture
    def blacklist_handlers(self):
        """BlacklistHandlers fixture"""
        with patch('src.services.blacklist_service.database'):
            return BlacklistHandlers()

    @pytest.mark.asyncio
    async def test_init(self, blacklist_handlers):
        """Test BlacklistHandlers initialization"""
        assert blacklist_handlers.blacklist_service is not None

    @pytest.mark.asyncio
    async def test_show_blacklist_empty(self, blacklist_handlers):
        """Test showing blacklist when empty"""
        # Mock empty blacklist
        blacklist_handlers.blacklist_service.get_all_blacklists = AsyncMock(return_value=[])
        blacklist_handlers.blacklist_service.get_blacklist_stats = AsyncMock(
            return_value={"total": 0, "permanent": 0, "temporary": 0, "expired": 0}
        )
        
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()

        await blacklist_handlers.show_blacklist(mock_update, mock_context)

        # Verify response was sent
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args[0][0]
        assert "No blacklisted" in call_args or "Tidak ada yang diblokir" in call_args

    @pytest.mark.asyncio
    async def test_show_blacklist_with_data(self, blacklist_handlers):
        """Test showing blacklist with data"""
        from src.models.blacklist import Blacklist, BlacklistType, BlacklistReason
        
        mock_blacklists = [
            Blacklist(
                group_id="-1001111111",
                blacklist_type=BlacklistType.PERMANENT,
                reason=BlacklistReason.CHAT_FORBIDDEN
            ),
            Blacklist(
                group_id="-1002222222",
                blacklist_type=BlacklistType.TEMPORARY,
                reason=BlacklistReason.FLOOD_WAIT,
                duration_seconds=3600
            ),
        ]
        
        blacklist_handlers.blacklist_service.get_all_blacklists = AsyncMock(return_value=mock_blacklists)
        blacklist_handlers.blacklist_service.get_blacklist_stats = AsyncMock(
            return_value={"total": 2, "permanent": 1, "temporary": 1, "expired": 0}
        )
        
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()

        await blacklist_handlers.show_blacklist(mock_update, mock_context)

        # Verify response contains blacklist data
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args
        assert call_args[1]["parse_mode"] == "Markdown"
        assert call_args[1]["reply_markup"] is not None

    @pytest.mark.asyncio
    async def test_handle_callback_remove_blacklist(self, blacklist_handlers):
        """Test handling callback to remove blacklist entry"""
        # Mock successful removal
        blacklist_handlers.blacklist_service.remove_from_blacklist = AsyncMock(return_value=True)
        
        mock_callback_query = AsyncMock()
        mock_update = MagicMock()
        mock_update.callback_query = mock_callback_query
        mock_context = MagicMock()

        await blacklist_handlers.handle_callback(mock_update, mock_context, "blacklist_remove_-1001234567890")

        # Verify removal was called
        blacklist_handlers.blacklist_service.remove_from_blacklist.assert_called_once_with("-1001234567890")
        mock_callback_query.edit_message_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_callback_cleanup_expired(self, blacklist_handlers):
        """Test handling callback to cleanup expired entries"""
        # Mock cleanup result
        blacklist_handlers.blacklist_service.cleanup_expired = AsyncMock(return_value=5)
        
        mock_callback_query = AsyncMock()
        mock_update = MagicMock()
        mock_update.callback_query = mock_callback_query
        mock_context = MagicMock()

        await blacklist_handlers.handle_callback(mock_update, mock_context, "blacklist_cleanup")

        # Verify cleanup was called
        blacklist_handlers.blacklist_service.cleanup_expired.assert_called_once()
        mock_callback_query.edit_message_text.assert_called_once()