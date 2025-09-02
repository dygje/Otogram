"""
Userbot - Handles mass messaging using MTProto
"""
import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Optional
from pyrogram import Client
from pyrogram.errors import (
    FloodWait, SlowmodeWait, ChatForbidden, ChatIdInvalid,
    UserBlocked, PeerIdInvalid, ChannelInvalid, UserBannedInChannel,
    ChatWriteForbidden, ChatRestricted
)
from loguru import logger

from src.core.config import settings
from src.services.message_service import MessageService
from src.services.group_service import GroupService
from src.services.blacklist_service import BlacklistService
from src.services.config_service import ConfigService
from src.models.blacklist import BlacklistCreate, BlacklistType, BlacklistReason


class UserBot:
    """Telegram userbot for mass messaging"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.message_service = MessageService()
        self.group_service = GroupService()
        self.blacklist_service = BlacklistService()
        self.config_service = ConfigService()
        self.is_running = False
        self.current_cycle_task = None
    
    async def start(self):
        """Start the userbot"""
        if not settings.TELEGRAM_API_ID or not settings.TELEGRAM_API_HASH:
            raise ValueError("TELEGRAM_API_ID and TELEGRAM_API_HASH must be set")
        
        if not settings.TELEGRAM_PHONE_NUMBER:
            raise ValueError("TELEGRAM_PHONE_NUMBER must be set")
        
        # Initialize Pyrogram client
        self.client = Client(
            "userbot_session",
            api_id=settings.TELEGRAM_API_ID,
            api_hash=settings.TELEGRAM_API_HASH,
            phone_number=settings.TELEGRAM_PHONE_NUMBER,
            workdir="sessions"
        )
        
        try:
            await self.client.start()
            logger.info("🔄 Userbot connected successfully")
            
            # Start the broadcasting cycle
            self.is_running = True
            self.current_cycle_task = asyncio.create_task(self._broadcasting_loop())
            
        except Exception as e:
            logger.error(f"Failed to start userbot: {e}")
            raise
    
    async def stop(self):
        """Stop the userbot"""
        self.is_running = False
        
        if self.current_cycle_task:
            self.current_cycle_task.cancel()
            try:
                await self.current_cycle_task
            except asyncio.CancelledError:
                pass
        
        if self.client:
            await self.client.stop()
            logger.info("🛑 Userbot stopped")
    
    async def _broadcasting_loop(self):
        """Main broadcasting loop"""
        logger.info("🔄 Broadcasting loop started")
        
        while self.is_running:
            try:
                # Clean up expired blacklist entries at the start of each cycle
                cleaned_count = await self.blacklist_service.cleanup_expired()
                if cleaned_count > 0:
                    logger.info(f"🧹 Cleaned up {cleaned_count} expired blacklist entries")
                else:
                    logger.debug("🧹 No expired blacklist entries to clean")
                
                # Get active messages and groups
                messages = await self.message_service.get_active_messages()
                groups = await self.group_service.get_active_groups()
                
                if not messages:
                    logger.warning("⚠️ No active messages found, skipping cycle")
                elif not groups:
                    logger.warning("⚠️ No active groups found, skipping cycle")
                else:
                    # Start broadcasting cycle
                    await self._broadcast_cycle(messages, groups)
                
                # Wait for next cycle
                await self._wait_for_next_cycle()
                
            except Exception as e:
                logger.error(f"Error in broadcasting loop: {e}")
                # Wait a bit before retrying
                await asyncio.sleep(300)  # 5 minutes
    
    async def _broadcast_cycle(self, messages: List, groups: List):
        """Execute a single broadcasting cycle"""
        logger.info(f"🚀 Starting broadcast cycle: {len(groups)} groups, {len(messages)} messages")
        
        sent_count = 0
        failed_count = 0
        skipped_count = 0
        start_time = datetime.utcnow()
        
        # Shuffle groups for randomness
        random.shuffle(groups)
        
        for group in groups:
            if not self.is_running:
                break
            
            # Check if group is blacklisted
            if await self.blacklist_service.is_blacklisted(group.group_id or str(group.id)):
                skipped_count += 1
                logger.debug(f"⏭️ Skipping blacklisted group: {group.group_id or group.group_username}")
                continue
            
            # Select random message
            message = random.choice(messages)
            
            # Send message
            success = await self._send_message_to_group(group, message.content)
            
            if success:
                sent_count += 1
                await self.message_service.increment_usage_count(message.id)
                await self.group_service.increment_message_count(group.group_id or str(group.id))
            else:
                failed_count += 1
            
            # Random delay between messages (only if not the last group)
            if group != groups[-1]:  # Don't delay after last group
                delay = await self._get_message_delay()
                logger.debug(f"⏱️ Waiting {delay} seconds before next message")
                await asyncio.sleep(delay)
        
        # Log cycle completion
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds() / 60  # in minutes
        
        logger.info(
            f"✅ Broadcast cycle completed: "
            f"{sent_count} sent, {failed_count} failed, {skipped_count} skipped (blacklisted), "
            f"{duration:.1f}m duration"
        )
    
    async def _send_message_to_group(self, group, message_content: str) -> bool:
        """Send message to a specific group"""
        try:
            # Determine the chat identifier
            chat_id = None
            
            if group.group_id:
                chat_id = int(group.group_id)
            elif group.group_username:
                chat_id = group.group_username
            else:
                logger.warning(f"No valid identifier for group: {group.id}")
                return False
            
            # Send the message
            await self.client.send_message(chat_id, message_content)
            
            logger.info(f"✅ Message sent to {chat_id}")
            return True
            
        except (FloodWait, SlowmodeWait) as e:
            # Temporary errors - add to temporary blacklist and skip immediately
            duration = getattr(e, 'value', 3600)  # Get duration from Telegram error
            
            error_type = "FloodWait" if isinstance(e, FloodWait) else "SlowModeWait"
            reason = BlacklistReason.FLOOD_WAIT if isinstance(e, FloodWait) else BlacklistReason.SLOW_MODE_WAIT
            
            await self._add_to_blacklist(
                group,
                BlacklistType.TEMPORARY,
                reason,
                duration,
                str(e)
            )
            
            # Log detailed information about the skip
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
            
            logger.warning(f"⏰ {error_type} detected for {chat_id}: {duration}s ({time_str}) - SKIPPING and adding to temporary blacklist")
            return False
            
        except (ChatForbidden, ChatIdInvalid, UserBlocked, PeerIdInvalid, 
                ChannelInvalid, UserBannedInChannel, ChatWriteForbidden, ChatRestricted) as e:
            # Permanent errors - add to permanent blacklist
            
            reason_mapping = {
                ChatForbidden: BlacklistReason.CHAT_FORBIDDEN,
                ChatIdInvalid: BlacklistReason.CHAT_ID_INVALID,
                UserBlocked: BlacklistReason.USER_BLOCKED,
                PeerIdInvalid: BlacklistReason.PEER_ID_INVALID,
                ChannelInvalid: BlacklistReason.CHANNEL_INVALID,
                UserBannedInChannel: BlacklistReason.USER_BANNED_IN_CHANNEL,
                ChatWriteForbidden: BlacklistReason.CHAT_WRITE_FORBIDDEN,
                ChatRestricted: BlacklistReason.CHAT_RESTRICTED,
            }
            
            reason = reason_mapping.get(type(e), BlacklistReason.CHAT_FORBIDDEN)
            
            await self._add_to_blacklist(
                group,
                BlacklistType.PERMANENT,
                reason,
                None,
                str(e)
            )
            
            logger.error(f"❌ Permanent error for {chat_id}: {e}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Unexpected error sending to {chat_id}: {e}")
            return False
    
    async def _add_to_blacklist(self, group, blacklist_type: BlacklistType, 
                               reason: BlacklistReason, duration_seconds: Optional[int], 
                               error_message: str):
        """Add group to blacklist"""
        
        group_identifier = group.group_username or group.group_link
        
        blacklist_data = BlacklistCreate(
            group_id=group.group_id or str(group.id),
            group_identifier=group_identifier,
            blacklist_type=blacklist_type,
            reason=reason,
            duration_seconds=duration_seconds,
            error_message=error_message
        )
        
        await self.blacklist_service.add_to_blacklist(blacklist_data)
    
    async def _get_message_delay(self) -> int:
        """Get random delay between messages"""
        min_delay = await self.config_service.get_config_value("min_message_delay", 5)
        max_delay = await self.config_service.get_config_value("max_message_delay", 10)
        
        return random.randint(min_delay, max_delay)
    
    async def _wait_for_next_cycle(self):
        """Wait for the next broadcasting cycle"""
        min_hours = await self.config_service.get_config_value("min_cycle_delay_hours", 1.1)
        max_hours = await self.config_service.get_config_value("max_cycle_delay_hours", 1.3)
        
        # Random delay between cycles
        delay_hours = random.uniform(min_hours, max_hours)
        delay_seconds = delay_hours * 3600
        
        logger.info(f"⏰ Next cycle in {delay_hours:.1f} hours")
        
        # Sleep in chunks to allow for graceful shutdown
        slept = 0
        chunk_size = 60  # 1 minute chunks
        
        while slept < delay_seconds and self.is_running:
            sleep_time = min(chunk_size, delay_seconds - slept)
            await asyncio.sleep(sleep_time)
            slept += sleep_time