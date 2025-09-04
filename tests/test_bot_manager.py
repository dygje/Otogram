"""
Tests for Bot Manager
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.telegram.bot_manager import BotManager


class TestBotManager:
    """Test BotManager class"""

    @pytest.fixture
    def bot_manager(self):
        """BotManager fixture"""
        return BotManager()

    @pytest.mark.asyncio
    async def test_init(self, bot_manager):
        """Test BotManager initialization"""
        assert bot_manager.management_bot is None
        assert bot_manager.userbot is None
        assert bot_manager.config_service is not None
        assert bot_manager.running is False

    @pytest.mark.asyncio
    async def test_start_success(self, bot_manager):
        """Test successful bot manager start"""
        # Mock the config service
        mock_config_service = AsyncMock()
        bot_manager.config_service = mock_config_service

        # Mock the management bot
        mock_management_bot = AsyncMock()
        
        with patch('src.telegram.bot_manager.ManagementBot') as mock_bot_class:
            mock_bot_class.return_value = mock_management_bot
            
            await bot_manager.start()
            
            # Verify initialization calls
            mock_config_service.initialize_default_configs.assert_called_once()
            mock_management_bot.start.assert_called_once()
            
            # Verify state
            assert bot_manager.running is True
            assert bot_manager.management_bot == mock_management_bot

    @pytest.mark.asyncio
    async def test_start_with_config_failure(self, bot_manager):
        """Test bot manager start with config service failure"""
        # Mock the config service to raise an exception
        mock_config_service = AsyncMock()
        mock_config_service.initialize_default_configs.side_effect = Exception("Config error")
        bot_manager.config_service = mock_config_service

        with pytest.raises(Exception, match="Config error"):
            with patch.object(bot_manager, 'stop') as mock_stop:
                await bot_manager.start()
                # Verify stop was called on failure
                mock_stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_with_management_bot_failure(self, bot_manager):
        """Test bot manager start with management bot failure"""
        # Mock the config service to succeed
        mock_config_service = AsyncMock()
        bot_manager.config_service = mock_config_service

        # Mock the management bot to fail
        mock_management_bot = AsyncMock()
        mock_management_bot.start.side_effect = Exception("Bot start error")
        
        with patch('src.telegram.bot_manager.ManagementBot') as mock_bot_class:
            mock_bot_class.return_value = mock_management_bot
            
            with pytest.raises(Exception, match="Bot start error"):
                with patch.object(bot_manager, 'stop') as mock_stop:
                    await bot_manager.start()
                    # Verify stop was called on failure
                    mock_stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_with_both_bots(self, bot_manager):
        """Test stopping with both bots active"""
        # Setup mock bots
        mock_management_bot = AsyncMock()
        mock_userbot = AsyncMock()
        
        bot_manager.management_bot = mock_management_bot
        bot_manager.userbot = mock_userbot
        bot_manager.running = True

        await bot_manager.stop()

        # Verify stop calls
        mock_userbot.stop.assert_called_once()
        mock_management_bot.stop.assert_called_once()
        assert bot_manager.running is False

    @pytest.mark.asyncio
    async def test_stop_with_only_management_bot(self, bot_manager):
        """Test stopping with only management bot"""
        # Setup mock management bot only
        mock_management_bot = AsyncMock()
        bot_manager.management_bot = mock_management_bot
        bot_manager.userbot = None
        bot_manager.running = True

        await bot_manager.stop()

        # Verify only management bot stop is called
        mock_management_bot.stop.assert_called_once()
        assert bot_manager.running is False

    @pytest.mark.asyncio
    async def test_stop_with_no_bots(self, bot_manager):
        """Test stopping with no bots initialized"""
        bot_manager.management_bot = None
        bot_manager.userbot = None
        bot_manager.running = True

        # Should not raise any exceptions
        await bot_manager.stop()
        assert bot_manager.running is False

    def test_is_running_true(self, bot_manager):
        """Test is_running returns True when running"""
        bot_manager.running = True
        assert bot_manager.is_running() is True

    def test_is_running_false(self, bot_manager):
        """Test is_running returns False when not running"""
        bot_manager.running = False
        assert bot_manager.is_running() is False

    @pytest.mark.asyncio
    async def test_start_stop_integration(self, bot_manager):
        """Test integration of start and stop methods"""
        # Mock dependencies
        mock_config_service = AsyncMock()
        bot_manager.config_service = mock_config_service
        
        mock_management_bot = AsyncMock()
        
        with patch('src.telegram.bot_manager.ManagementBot') as mock_bot_class:
            mock_bot_class.return_value = mock_management_bot
            
            # Start bot manager
            await bot_manager.start()
            assert bot_manager.is_running() is True
            
            # Stop bot manager
            await bot_manager.stop()
            assert bot_manager.is_running() is False
            
            # Verify stop calls
            mock_management_bot.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_double_stop_no_error(self, bot_manager):
        """Test that calling stop twice doesn't cause errors"""
        mock_management_bot = AsyncMock()
        bot_manager.management_bot = mock_management_bot
        bot_manager.running = True

        # First stop
        await bot_manager.stop()
        assert bot_manager.running is False
        
        # Second stop - should not raise error
        await bot_manager.stop()
        assert bot_manager.running is False
        
        # Stop should be called twice
        assert mock_management_bot.stop.call_count == 2