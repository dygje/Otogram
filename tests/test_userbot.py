"""
Tests for UserBot
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from pyrogram.errors import FloodWait, SlowmodeWait, ChatForbidden, ChatIdInvalid

from src.telegram.userbot import UserBot
from src.models.blacklist import BlacklistType, BlacklistReason
from src.models.message import Message
from src.models.group import Group


class TestUserBot:
    """Test UserBot class"""

    @pytest.fixture
    def userbot(self):
        """UserBot fixture"""
        with patch('src.services.config_service.database'), \
             patch('src.services.message_service.database'), \
             patch('src.services.group_service.database'), \
             patch('src.services.blacklist_service.database'):
            return UserBot()

    @pytest.fixture
    def mock_telegram_credentials(self, monkeypatch):
        """Mock Telegram credentials"""
        monkeypatch.setattr("src.core.config.settings.TELEGRAM_API_ID", 123456)
        monkeypatch.setattr("src.core.config.settings.TELEGRAM_API_HASH", "test_hash")
        monkeypatch.setattr("src.core.config.settings.TELEGRAM_PHONE_NUMBER", "+1234567890")

    @pytest.mark.asyncio
    async def test_init(self, userbot):
        """Test UserBot initialization"""
        assert userbot.client is None
        assert userbot.message_service is not None
        assert userbot.group_service is not None
        assert userbot.blacklist_service is not None
        assert userbot.config_service is not None
        assert userbot.is_running is False
        assert userbot.current_cycle_task is None

    @pytest.mark.asyncio
    async def test_start_success(self, userbot, mock_telegram_credentials):
        """Test successful userbot start"""
        mock_client = AsyncMock()
        
        with patch('src.telegram.userbot.Client') as mock_client_class:
            mock_client_class.return_value = mock_client
            with patch.object(userbot, '_broadcasting_loop') as mock_loop:
                mock_loop_task = AsyncMock()
                with patch('asyncio.create_task', return_value=mock_loop_task):
                    
                    await userbot.start()
                    
                    # Verify client creation and start
                    mock_client_class.assert_called_once()
                    mock_client.start.assert_called_once()
                    
                    # Verify state
                    assert userbot.client == mock_client
                    assert userbot.is_running is True
                    assert userbot.current_cycle_task == mock_loop_task

    @pytest.mark.asyncio
    async def test_start_no_api_credentials(self, userbot):
        """Test userbot start without API credentials"""
        with patch('src.core.config.settings.TELEGRAM_API_ID', None):
            with pytest.raises(ValueError, match="TELEGRAM_API_ID and TELEGRAM_API_HASH must be set"):
                await userbot.start()

    @pytest.mark.asyncio
    async def test_start_no_phone_number(self, userbot, monkeypatch):
        """Test userbot start without phone number"""
        monkeypatch.setattr("src.core.config.settings.TELEGRAM_API_ID", 123456)
        monkeypatch.setattr("src.core.config.settings.TELEGRAM_API_HASH", "test_hash")
        monkeypatch.setattr("src.core.config.settings.TELEGRAM_PHONE_NUMBER", None)
        
        with pytest.raises(ValueError, match="TELEGRAM_PHONE_NUMBER must be set"):
            await userbot.start()

    @pytest.mark.asyncio
    async def test_start_client_failure(self, userbot, mock_telegram_credentials):
        """Test userbot start with client failure"""
        mock_client = AsyncMock()
        mock_client.start.side_effect = Exception("Connection failed")
        
        with patch('src.telegram.userbot.Client') as mock_client_class:
            mock_client_class.return_value = mock_client
            
            with pytest.raises(Exception, match="Connection failed"):
                await userbot.start()

    @pytest.mark.asyncio
    async def test_stop_with_task(self, userbot):
        """Test stopping userbot with active task"""
        mock_client = AsyncMock()
        
        # Create a proper mock task that can be awaited
        mock_task = AsyncMock()
        mock_task_coroutine = AsyncMock()
        mock_task.__await__ = lambda: mock_task_coroutine.__await__()
        
        userbot.client = mock_client
        userbot.current_cycle_task = mock_task
        userbot.is_running = True

        await userbot.stop()

        # Verify stop sequence
        assert userbot.is_running is False
        mock_task.cancel.assert_called_once()
        mock_client.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_without_task(self, userbot):
        """Test stopping userbot without active task"""
        mock_client = AsyncMock()
        userbot.client = mock_client
        userbot.current_cycle_task = None
        userbot.is_running = True

        await userbot.stop()

        # Verify client stop
        assert userbot.is_running is False
        mock_client.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_cancelled_task(self, userbot):
        """Test stopping userbot with cancelled task"""
        mock_client = AsyncMock()
        
        # Create a proper mock task that raises CancelledError when awaited
        mock_task = AsyncMock()
        async def cancelled_coro():
            raise asyncio.CancelledError()
        mock_task.__await__ = lambda: cancelled_coro().__await__()
        
        userbot.client = mock_client
        userbot.current_cycle_task = mock_task
        userbot.is_running = True

        await userbot.stop()

        # Should handle CancelledError gracefully
        assert userbot.is_running is False
        mock_task.cancel.assert_called_once()
        mock_client.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_broadcasting_loop_no_messages(self, userbot):
        """Test broadcasting loop with no active messages"""
        userbot.is_running = True
        
        # Mock services
        userbot.blacklist_service.cleanup_expired = AsyncMock(return_value=0)
        userbot.message_service.get_active_messages = AsyncMock(return_value=[])
        userbot.group_service.get_active_groups = AsyncMock(return_value=[Group(group_id="-100123")])
        
        # Mock wait method to stop after first iteration
        original_wait = userbot._wait_for_next_cycle
        call_count = 0
        async def mock_wait():
            nonlocal call_count
            call_count += 1
            userbot.is_running = False  # Stop after first iteration
            
        userbot._wait_for_next_cycle = mock_wait

        await userbot._broadcasting_loop()

        # Verify no broadcast cycle was called
        userbot.blacklist_service.cleanup_expired.assert_called()
        userbot.message_service.get_active_messages.assert_called()
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_broadcasting_loop_no_groups(self, userbot):
        """Test broadcasting loop with no active groups"""
        userbot.is_running = True
        
        # Create mock message
        mock_message = Message(content="Test message")
        
        # Mock services
        userbot.blacklist_service.cleanup_expired = AsyncMock(return_value=0)
        userbot.message_service.get_active_messages = AsyncMock(return_value=[mock_message])
        userbot.group_service.get_active_groups = AsyncMock(return_value=[])
        
        # Mock wait method to stop after first iteration
        call_count = 0
        async def mock_wait():
            nonlocal call_count
            call_count += 1
            userbot.is_running = False
            
        userbot._wait_for_next_cycle = mock_wait

        await userbot._broadcasting_loop()

        # Verify services were called but no broadcast
        userbot.message_service.get_active_messages.assert_called()
        userbot.group_service.get_active_groups.assert_called()
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_broadcasting_loop_with_cleanup(self, userbot):
        """Test broadcasting loop with expired blacklist cleanup"""
        userbot.is_running = True
        
        # Mock services - cleanup returns 5 cleaned entries
        userbot.blacklist_service.cleanup_expired = AsyncMock(return_value=5)
        userbot.message_service.get_active_messages = AsyncMock(return_value=[])
        userbot.group_service.get_active_groups = AsyncMock(return_value=[])
        
        # Mock wait method to stop after first iteration
        async def mock_wait():
            userbot.is_running = False
            
        userbot._wait_for_next_cycle = mock_wait

        await userbot._broadcasting_loop()

        # Verify cleanup was called and logged
        userbot.blacklist_service.cleanup_expired.assert_called()

    @pytest.mark.asyncio
    async def test_broadcasting_loop_error_handling(self, userbot):
        """Test broadcasting loop error handling"""
        userbot.is_running = True
        iteration_count = 0
        
        # Mock services to raise error on first call, succeed on second
        async def cleanup_side_effect():
            nonlocal iteration_count
            iteration_count += 1
            if iteration_count == 1:
                raise Exception("Database error")
            else:
                userbot.is_running = False  # Stop after second iteration
                return 0
                
        userbot.blacklist_service.cleanup_expired = AsyncMock(side_effect=cleanup_side_effect)
        
        # Mock asyncio.sleep to avoid actual delays
        with patch('asyncio.sleep', new_callable=AsyncMock):
            await userbot._broadcasting_loop()

        # Verify error was handled and loop continued
        assert userbot.blacklist_service.cleanup_expired.call_count == 2

    @pytest.mark.asyncio
    async def test_broadcast_cycle_success(self, userbot):
        """Test successful broadcast cycle"""
        # Setup test data
        mock_message = Message(id="msg1", content="Test message")
        mock_group = Group(id="grp1", group_id="-100123456", group_username="testgroup")
        
        messages = [mock_message]
        groups = [mock_group]
        
        # Ensure userbot is running
        userbot.is_running = True
        
        # Mock services
        userbot.blacklist_service.is_blacklisted = AsyncMock(return_value=False)
        userbot._send_message_to_group = AsyncMock(return_value=True)
        userbot.message_service.increment_usage_count = AsyncMock()
        userbot.group_service.increment_message_count = AsyncMock()
        userbot._get_message_delay = AsyncMock(return_value=5)
        
        # Mock SecureRandom
        with patch('src.telegram.userbot.SecureRandom') as mock_random:
            mock_random.shuffle.return_value = None  # In-place shuffle
            mock_random.choice.return_value = mock_message
            
            # Mock asyncio.sleep
            with patch('asyncio.sleep', new_callable=AsyncMock):
                await userbot._broadcast_cycle(messages, groups)

        # Verify message was sent and stats updated
        userbot._send_message_to_group.assert_called_once_with(mock_group, "Test message")
        userbot.message_service.increment_usage_count.assert_called_once_with("msg1")
        userbot.group_service.increment_message_count.assert_called_once_with("-100123456")

    @pytest.mark.asyncio
    async def test_broadcast_cycle_blacklisted_group(self, userbot):
        """Test broadcast cycle with blacklisted group"""
        mock_message = Message(content="Test message")
        mock_group = Group(group_id="-100123456")
        
        # Mock blacklist check to return True
        userbot.blacklist_service.is_blacklisted = AsyncMock(return_value=True)
        userbot._send_message_to_group = AsyncMock()
        
        with patch('src.telegram.userbot.SecureRandom') as mock_random:
            mock_random.shuffle.return_value = None
            mock_random.choice.return_value = mock_message
            
            await userbot._broadcast_cycle([mock_message], [mock_group])

        # Verify message was not sent to blacklisted group
        userbot._send_message_to_group.assert_not_called()

    @pytest.mark.asyncio
    async def test_send_message_to_group_success(self, userbot):
        """Test successful message sending to group"""
        mock_client = AsyncMock()
        userbot.client = mock_client
        
        mock_group = Group(group_id="-100123456")
        message_content = "Test message"
        
        result = await userbot._send_message_to_group(mock_group, message_content)
        
        assert result is True
        mock_client.send_message.assert_called_once_with(-100123456, message_content)

    @pytest.mark.asyncio
    async def test_send_message_to_group_with_username(self, userbot):
        """Test message sending to group using username"""
        mock_client = AsyncMock()
        userbot.client = mock_client
        
        mock_group = Group(group_username="testgroup")
        message_content = "Test message"
        
        result = await userbot._send_message_to_group(mock_group, message_content)
        
        assert result is True
        # Note: userbot adds '@' prefix to usernames automatically
        mock_client.send_message.assert_called_once_with("@testgroup", message_content)

    @pytest.mark.asyncio
    async def test_send_message_to_group_no_identifier(self, userbot):
        """Test message sending to group with no valid identifier"""
        mock_client = AsyncMock()
        userbot.client = mock_client
        
        mock_group = Group(id="123")  # No group_id or group_username
        message_content = "Test message"
        
        result = await userbot._send_message_to_group(mock_group, message_content)
        
        assert result is False
        mock_client.send_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_send_message_to_group_no_client(self, userbot):
        """Test message sending with no client initialized"""
        userbot.client = None
        
        mock_group = Group(group_id="-100123456")
        message_content = "Test message"
        
        result = await userbot._send_message_to_group(mock_group, message_content)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_send_message_flood_wait_error(self, userbot):
        """Test message sending with FloodWait error"""
        mock_client = AsyncMock()
        userbot.client = mock_client
        
        # Mock FloodWait exception
        flood_error = FloodWait(3600)  # 1 hour wait
        mock_client.send_message.side_effect = flood_error
        
        mock_group = Group(group_id="-100123456")
        userbot._add_to_blacklist = AsyncMock()
        
        result = await userbot._send_message_to_group(mock_group, "Test message")
        
        assert result is False
        # Verify blacklist was called with correct parameters
        userbot._add_to_blacklist.assert_called_once()
        call_args = userbot._add_to_blacklist.call_args[0]
        assert call_args[1] == BlacklistType.TEMPORARY
        assert call_args[2] == BlacklistReason.FLOOD_WAIT
        assert call_args[3] == 3600

    @pytest.mark.asyncio
    async def test_send_message_slowmode_wait_error(self, userbot):
        """Test message sending with SlowmodeWait error"""
        mock_client = AsyncMock()
        userbot.client = mock_client
        
        # Mock SlowmodeWait exception
        slowmode_error = SlowmodeWait(30)  # 30 seconds wait
        mock_client.send_message.side_effect = slowmode_error
        
        mock_group = Group(group_id="-100123456")
        userbot._add_to_blacklist = AsyncMock()
        
        result = await userbot._send_message_to_group(mock_group, "Test message")
        
        assert result is False
        # Verify blacklist was called with correct parameters
        userbot._add_to_blacklist.assert_called_once()
        call_args = userbot._add_to_blacklist.call_args[0]
        assert call_args[1] == BlacklistType.TEMPORARY
        assert call_args[2] == BlacklistReason.SLOW_MODE_WAIT
        assert call_args[3] == 30

    @pytest.mark.asyncio
    async def test_send_message_permanent_error(self, userbot):
        """Test message sending with permanent error"""
        mock_client = AsyncMock()
        userbot.client = mock_client
        
        # Mock permanent error
        mock_client.send_message.side_effect = ChatForbidden()
        
        mock_group = Group(group_id="-100123456")
        userbot._add_to_blacklist = AsyncMock()
        
        result = await userbot._send_message_to_group(mock_group, "Test message")
        
        assert result is False
        # Verify permanent blacklist was called
        userbot._add_to_blacklist.assert_called_once()
        call_args = userbot._add_to_blacklist.call_args[0]
        assert call_args[1] == BlacklistType.PERMANENT
        assert call_args[2] == BlacklistReason.CHAT_FORBIDDEN

    @pytest.mark.asyncio
    async def test_send_message_unexpected_error(self, userbot):
        """Test message sending with unexpected error"""
        mock_client = AsyncMock()
        userbot.client = mock_client
        
        # Mock unexpected error
        mock_client.send_message.side_effect = Exception("Unexpected error")
        
        mock_group = Group(group_id="-100123456")
        
        result = await userbot._send_message_to_group(mock_group, "Test message")
        
        assert result is False

    @pytest.mark.asyncio
    async def test_add_to_blacklist(self, userbot):
        """Test adding group to blacklist"""
        mock_group = Group(
            id="123",
            group_id="-100123456",
            group_username="testgroup",
            group_link="https://t.me/testgroup"
        )
        
        userbot.blacklist_service.add_to_blacklist = AsyncMock()
        
        await userbot._add_to_blacklist(
            mock_group,
            BlacklistType.PERMANENT,
            BlacklistReason.CHAT_FORBIDDEN,
            None,
            "Chat forbidden error"
        )
        
        # Verify blacklist service was called
        userbot.blacklist_service.add_to_blacklist.assert_called_once()
        call_args = userbot.blacklist_service.add_to_blacklist.call_args[0][0]
        assert call_args.group_id == "-100123456"
        assert call_args.group_identifier == "@testgroup"  # Note: userbot adds '@' prefix
        assert call_args.blacklist_type == BlacklistType.PERMANENT
        assert call_args.reason == BlacklistReason.CHAT_FORBIDDEN

    @pytest.mark.asyncio
    async def test_get_message_delay(self, userbot):
        """Test getting message delay"""
        userbot.config_service.get_config_value = AsyncMock()
        userbot.config_service.get_config_value.side_effect = lambda key, default: {
            "min_message_delay": 5,
            "max_message_delay": 10
        }.get(key.replace("min_", "").replace("max_", ""), default)
        
        with patch('src.telegram.userbot.SecureRandom.randint', return_value=7):
            delay = await userbot._get_message_delay()
            
        assert delay == 7

    @pytest.mark.asyncio
    async def test_wait_for_next_cycle(self, userbot):
        """Test waiting for next cycle"""
        userbot.config_service.get_config_value = AsyncMock()
        userbot.config_service.get_config_value.side_effect = lambda key, default: {
            "min_cycle_delay_hours": 1.1,
            "max_cycle_delay_hours": 1.3
        }.get(key.replace("min_", "").replace("max_", ""), default)
        
        userbot.is_running = True
        
        # Mock SecureRandom.uniform to return 1.2 hours
        with patch('src.telegram.userbot.SecureRandom.uniform', return_value=1.2):
            # Mock asyncio.sleep and track calls
            sleep_calls = []
            
            async def mock_sleep(duration):
                sleep_calls.append(duration)
                # Stop after first sleep call
                userbot.is_running = False
                
            with patch('asyncio.sleep', side_effect=mock_sleep):
                await userbot._wait_for_next_cycle()
        
        # Verify sleep was called (should be broken into chunks)
        assert len(sleep_calls) == 1
        # First sleep should be <= SLEEP_CHUNK_SIZE (60 seconds)
        assert sleep_calls[0] <= 60

    @pytest.mark.asyncio 
    async def test_wait_for_next_cycle_stop_early(self, userbot):
        """Test waiting for next cycle with early stop"""
        userbot.config_service.get_config_value = AsyncMock()
        userbot.config_service.get_config_value.side_effect = lambda key, default: {
            "min_cycle_delay_hours": 1.1,
            "max_cycle_delay_hours": 1.3
        }.get(key.replace("min_", "").replace("max_", ""), default)
        
        userbot.is_running = False  # Already stopped
        
        with patch('src.telegram.userbot.SecureRandom.uniform', return_value=1.2):
            with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                await userbot._wait_for_next_cycle()
                
        # Should not sleep if not running
        mock_sleep.assert_not_called()