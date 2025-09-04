"""
Tests for Management Bot
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from telegram import Update, CallbackQuery, Message as TelegramMessage
from telegram.ext import ContextTypes

from src.telegram.management_bot import ManagementBot


class TestManagementBot:
    """Test ManagementBot class"""

    @pytest.fixture
    def management_bot(self):
        """ManagementBot fixture"""
        with patch('src.services.config_service.database'), \
             patch('src.services.message_service.database'), \
             patch('src.services.group_service.database'), \
             patch('src.services.blacklist_service.database'):
            return ManagementBot()

    @pytest.fixture
    def mock_telegram_credentials(self, monkeypatch):
        """Mock Telegram credentials"""
        monkeypatch.setattr("src.core.config.settings.TELEGRAM_BOT_TOKEN", "123456:test_token")

    @pytest.mark.asyncio
    async def test_init(self, management_bot):
        """Test ManagementBot initialization"""
        assert management_bot.app is None
        assert management_bot.message_handlers is not None
        assert management_bot.group_handlers is not None
        assert management_bot.config_handlers is not None
        assert management_bot.blacklist_handlers is not None

    @pytest.mark.asyncio
    async def test_start_success(self, management_bot, mock_telegram_credentials):
        """Test successful bot start"""
        # Mock Application and its methods
        mock_app = AsyncMock()
        mock_updater = AsyncMock()
        mock_app.updater = mock_updater
        
        with patch('src.telegram.management_bot.Application') as mock_app_class:
            mock_builder = MagicMock()
            mock_builder.token.return_value = mock_builder
            mock_builder.build.return_value = mock_app
            mock_app_class.builder.return_value = mock_builder
            
            await management_bot.start()
            
            # Verify Application was created correctly
            mock_app_class.builder.assert_called_once()
            mock_builder.token.assert_called_once_with("123456:test_token")
            mock_builder.build.assert_called_once()
            
            # Verify bot lifecycle calls
            mock_app.initialize.assert_called_once()
            mock_app.start.assert_called_once()
            mock_updater.start_polling.assert_called_once()
            
            # Verify app is set
            assert management_bot.app == mock_app

    @pytest.mark.asyncio
    async def test_start_no_token(self, management_bot):
        """Test bot start without token"""
        with patch('src.core.config.settings.TELEGRAM_BOT_TOKEN', None):
            with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN not set"):
                await management_bot.start()

    @pytest.mark.asyncio
    async def test_start_no_updater(self, management_bot, mock_telegram_credentials):
        """Test bot start when updater is not available"""
        mock_app = AsyncMock()
        mock_app.updater = None
        
        with patch('src.telegram.management_bot.Application') as mock_app_class:
            mock_builder = MagicMock()
            mock_builder.token.return_value = mock_builder
            mock_builder.build.return_value = mock_app
            mock_app_class.builder.return_value = mock_builder
            
            with pytest.raises(RuntimeError, match="Updater not available"):
                await management_bot.start()

    @pytest.mark.asyncio
    async def test_stop_with_app(self, management_bot):
        """Test stopping bot with app initialized"""
        mock_app = AsyncMock()
        mock_updater = AsyncMock()
        mock_app.updater = mock_updater
        management_bot.app = mock_app

        await management_bot.stop()

        # Verify stop sequence
        mock_updater.stop.assert_called_once()
        mock_app.stop.assert_called_once()
        mock_app.shutdown.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_without_app(self, management_bot):
        """Test stopping bot without app initialized"""
        management_bot.app = None
        
        # Should not raise any exceptions
        await management_bot.stop()

    @pytest.mark.asyncio
    async def test_stop_without_updater(self, management_bot):
        """Test stopping bot without updater"""
        mock_app = AsyncMock()
        mock_app.updater = None
        management_bot.app = mock_app

        await management_bot.stop()

        # Should still call stop and shutdown
        mock_app.stop.assert_called_once()
        mock_app.shutdown.assert_called_once()

    def test_add_handlers_no_app(self, management_bot):
        """Test adding handlers without app initialized"""
        management_bot.app = None
        
        with pytest.raises(RuntimeError, match="Application not initialized"):
            management_bot._add_handlers()

    def test_add_handlers_success(self, management_bot):
        """Test successful handler addition"""
        mock_app = MagicMock()
        management_bot.app = mock_app
        
        management_bot._add_handlers()
        
        # Verify handlers were added (check that add_handler was called multiple times)
        assert mock_app.add_handler.call_count > 10  # Multiple handlers should be added

    @pytest.mark.asyncio
    async def test_start_command(self, management_bot):
        """Test /start command handler"""
        # Mock Update and Message
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()

        await management_bot.start_command(mock_update, mock_context)

        # Verify reply was sent
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args
        assert "Telegram Automation System" in call_args[0][0]
        assert call_args[1]["parse_mode"] == "Markdown"
        assert call_args[1]["reply_markup"] is not None

    @pytest.mark.asyncio
    async def test_start_command_no_message(self, management_bot):
        """Test /start command with no message in update"""
        mock_update = MagicMock()
        mock_update.message = None
        mock_context = MagicMock()

        # Should not raise exception
        await management_bot.start_command(mock_update, mock_context)

    @pytest.mark.asyncio
    async def test_help_command(self, management_bot):
        """Test /help command handler"""
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()

        await management_bot.help_command(mock_update, mock_context)

        # Verify help text was sent
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args
        assert "OTOGRAM AUTOMATION SYSTEM" in call_args[0][0]
        assert "/start" in call_args[0][0]
        assert "/help" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_status_command(self, management_bot):
        """Test /status command handler"""
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()

        await management_bot.status_command(mock_update, mock_context)

        # Verify status was sent
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args
        assert "Status Sistem" in call_args[0][0]
        assert "Management Bot" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_main_menu_with_message(self, management_bot):
        """Test main menu with message update"""
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_update.callback_query = None
        mock_context = MagicMock()

        # Mock the stats method
        management_bot._get_system_stats = AsyncMock(return_value="Mock stats")

        await management_bot.main_menu(mock_update, mock_context)

        # Verify message was sent
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args
        assert "SYSTEM DASHBOARD" in call_args[0][0]
        assert call_args[1]["parse_mode"] == "Markdown"
        assert call_args[1]["reply_markup"] is not None

    @pytest.mark.asyncio
    async def test_main_menu_with_callback_query(self, management_bot):
        """Test main menu with callback query"""
        mock_callback_query = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = None
        mock_update.callback_query = mock_callback_query
        mock_context = MagicMock()

        # Mock the stats method
        management_bot._get_system_stats = AsyncMock(return_value="Mock stats")

        await management_bot.main_menu(mock_update, mock_context)

        # Verify callback query was edited
        mock_callback_query.edit_message_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_system_stats_success(self, management_bot):
        """Test getting system stats successfully"""
        # Mock all handlers and their services
        mock_message_service = AsyncMock()
        mock_message_service.get_message_count.return_value = {"total": 5, "active": 3, "inactive": 2}
        management_bot.message_handlers.message_service = mock_message_service
        
        mock_group_service = AsyncMock()
        mock_group_service.get_group_stats.return_value = {"total": 10, "active": 8, "inactive": 2}
        management_bot.group_handlers.group_service = mock_group_service
        
        mock_blacklist_service = AsyncMock()
        mock_blacklist_service.get_blacklist_stats.return_value = {"total": 2, "permanent": 1, "temporary": 1, "expired": 0}
        management_bot.blacklist_handlers.blacklist_service = mock_blacklist_service

        result = await management_bot._get_system_stats()

        assert "Messages:" in result
        assert "Groups:" in result
        assert "Blacklist:" in result  
        assert "System:" in result
        assert "3/5" in result  # active/total messages
        assert "8/10" in result  # active/total groups

    @pytest.mark.asyncio
    async def test_get_system_stats_error(self, management_bot):
        """Test getting system stats with error"""
        # Mock service to raise exception
        mock_message_service = AsyncMock()
        mock_message_service.get_message_count.side_effect = Exception("DB Error")
        management_bot.message_handlers.message_service = mock_message_service

        result = await management_bot._get_system_stats()

        assert "Loading stats..." in result

    @pytest.mark.asyncio
    async def test_handle_callback_dashboard(self, management_bot):
        """Test callback handler for dashboard"""
        mock_callback_query = AsyncMock()
        mock_callback_query.data = "dashboard"
        mock_update = MagicMock()
        mock_update.callback_query = mock_callback_query
        mock_context = MagicMock()

        # Mock main_menu method
        management_bot.main_menu = AsyncMock()

        await management_bot.handle_callback(mock_update, mock_context)

        # Verify callback was answered and main_menu was called
        mock_callback_query.answer.assert_called_once()
        management_bot.main_menu.assert_called_once_with(mock_update, mock_context)

    @pytest.mark.asyncio
    async def test_handle_callback_no_query(self, management_bot):
        """Test callback handler with no query"""
        mock_update = MagicMock()
        mock_update.callback_query = None
        mock_context = MagicMock()

        # Should return early without error
        result = await management_bot.handle_callback(mock_update, mock_context)
        assert result is None

    @pytest.mark.asyncio
    async def test_handle_callback_no_data(self, management_bot):
        """Test callback handler with no data"""
        mock_callback_query = AsyncMock()
        mock_callback_query.data = None
        mock_update = MagicMock()
        mock_update.callback_query = mock_callback_query
        mock_context = MagicMock()

        # Should return after answering query
        result = await management_bot.handle_callback(mock_update, mock_context)
        mock_callback_query.answer.assert_called_once()
        assert result is None

    @pytest.mark.asyncio
    async def test_handle_callback_messages_prefix(self, management_bot):
        """Test callback handler for messages_ prefix"""
        mock_callback_query = AsyncMock()
        mock_callback_query.data = "messages_list"
        mock_update = MagicMock()
        mock_update.callback_query = mock_callback_query
        mock_context = MagicMock()

        # Mock message handlers
        management_bot.message_handlers.handle_callback = AsyncMock()

        await management_bot.handle_callback(mock_update, mock_context)

        # Verify message handler was called
        mock_callback_query.answer.assert_called_once()
        management_bot.message_handlers.handle_callback.assert_called_once_with(
            mock_update, mock_context, "messages_list"
        )

    @pytest.mark.asyncio
    async def test_handle_text_input_waiting_for_message(self, management_bot):
        """Test text input handler when waiting for message content"""
        mock_update = MagicMock()
        mock_context = MagicMock()
        mock_context.user_data = {"waiting_for": "message_content"}
        
        # Mock message handlers
        management_bot.message_handlers.handle_message_input = AsyncMock()

        await management_bot.handle_text_input(mock_update, mock_context)

        # Verify message handler was called
        management_bot.message_handlers.handle_message_input.assert_called_once_with(mock_update, mock_context)

    @pytest.mark.asyncio
    async def test_handle_text_input_no_waiting_state(self, management_bot):
        """Test text input handler with no waiting state"""
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()
        mock_context.user_data = {}

        await management_bot.handle_text_input(mock_update, mock_context)

        # Verify default response was sent
        mock_message.reply_text.assert_called_once()
        call_args = mock_message.reply_text.call_args[0][0]
        assert "Saya tidak mengerti" in call_args

    @pytest.mark.asyncio
    async def test_handle_text_input_unknown_waiting_state(self, management_bot):
        """Test text input handler with unknown waiting state"""
        mock_message = AsyncMock()
        mock_update = MagicMock()
        mock_update.message = mock_message
        mock_context = MagicMock()
        mock_context.user_data = {"waiting_for": "unknown_state"}

        await management_bot.handle_text_input(mock_update, mock_context)

        # Verify waiting state was cleared and error message sent
        assert "waiting_for" not in mock_context.user_data
        mock_message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_show_quick_setup(self, management_bot):
        """Test quick setup display"""
        mock_callback_query = AsyncMock()
        mock_update = MagicMock()
        mock_update.callback_query = mock_callback_query
        mock_context = MagicMock()

        await management_bot._show_quick_setup(mock_update, mock_context)

        # Verify setup wizard was displayed
        mock_callback_query.edit_message_text.assert_called_once()
        call_args = mock_callback_query.edit_message_text.call_args
        assert "QUICK SETUP WIZARD" in call_args[0][0]
        assert call_args[1]["parse_mode"] == "Markdown"
        assert call_args[1]["reply_markup"] is not None