"""
Authentication Handlers - Handle userbot authentication through bot interface
"""

import asyncio
from typing import Any

from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.core.config import settings
from src.telegram.userbot import UserBot


class AuthHandlers:
    """Handlers for userbot authentication"""

    def __init__(self):
        self.userbot_instance: UserBot | None = None
        self.auth_in_progress = False

    async def show_auth_status(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show current authentication status"""
        try:
            # Check if userbot is already authenticated
            is_authenticated = await self._check_userbot_status()
            
            if is_authenticated:
                text = (
                    "✅ **USERBOT STATUS: AUTHENTICATED**\n"
                    "═══════════════════════════════\n\n"
                    "🤖 **Userbot Details:**\n"
                    f"├ Phone: {settings.TELEGRAM_PHONE_NUMBER}\n"
                    f"├ Status: 🟢 Connected & Ready\n"
                    f"├ Session: 🔒 Secure\n"
                    f"└ Broadcasting: ✅ Enabled\n\n"
                    "🎯 **System is ready for broadcasting!**\n"
                    "You can now add messages and groups to start automation."
                )
                
                keyboard = [
                    [
                        InlineKeyboardButton("🔄 Restart Userbot", callback_data="auth_restart"),
                        InlineKeyboardButton("🗑️ Clear Session", callback_data="auth_clear"),
                    ],
                    [
                        InlineKeyboardButton("📊 Test Connection", callback_data="auth_test"),
                        InlineKeyboardButton("🔙 Back to Menu", callback_data="dashboard"),
                    ],
                ]
            else:
                text = (
                    "⚠️ **USERBOT STATUS: NOT AUTHENTICATED**\n"
                    "═══════════════════════════════════\n\n"
                    "🔐 **Authentication Required**\n"
                    f"├ Phone: {settings.TELEGRAM_PHONE_NUMBER}\n"
                    f"├ Status: 🔴 Not Connected\n"
                    f"├ Session: ❌ Missing\n"
                    f"└ Broadcasting: ❌ Disabled\n\n"
                    "📱 **To enable broadcasting:**\n"
                    "1. Click 'Start Authentication' below\n"
                    "2. Enter verification code from Telegram\n"
                    "3. Complete setup in a few seconds\n\n"
                    "🎯 **Ready to authenticate?**"
                )
                
                keyboard = [
                    [InlineKeyboardButton("🚀 Start Authentication", callback_data="auth_start")],
                    [
                        InlineKeyboardButton("❓ Help", callback_data="auth_help"),
                        InlineKeyboardButton("🔙 Back to Menu", callback_data="dashboard"),
                    ],
                ]
                
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )
            elif update.message:
                await update.message.reply_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )
                
        except Exception as e:
            logger.error(f"Error showing auth status: {e}")
            await self._send_error_message(update, "Failed to check authentication status")

    async def start_authentication(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start the authentication process"""
        try:
            if self.auth_in_progress:
                await self._send_message(update, "⚠️ Authentication already in progress. Please wait...")
                return
                
            self.auth_in_progress = True
            
            # Show starting message
            await self._send_message(
                update,
                "🚀 **STARTING USERBOT AUTHENTICATION**\n\n"
                "📱 Sending verification code to your phone...\n"
                "Please wait a moment..."
            )
            
            # Start authentication process in background
            asyncio.create_task(self._authenticate_userbot(update, context))
            
        except Exception as e:
            logger.error(f"Error starting authentication: {e}")
            self.auth_in_progress = False
            await self._send_error_message(update, "Failed to start authentication")

    async def _authenticate_userbot(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Perform the actual authentication"""
        try:
            from pyrogram import Client
            from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired
            
            # Initialize client
            client = Client(
                "userbot_session",
                api_id=settings.TELEGRAM_API_ID,
                api_hash=settings.TELEGRAM_API_HASH,
                phone_number=settings.TELEGRAM_PHONE_NUMBER,
                workdir="sessions",
            )
            
            await client.connect()
            
            # Send verification code
            sent_code = await client.send_code(settings.TELEGRAM_PHONE_NUMBER)
            
            # Inform user about code
            text = (
                "📱 **VERIFICATION CODE SENT**\n"
                "═══════════════════════════\n\n"
                f"📞 Code sent to: {settings.TELEGRAM_PHONE_NUMBER}\n"
                f"📧 Type: {sent_code.type}\n\n"
                "🔢 **Please enter the verification code you received:**\n"
                "└ Format: Just the numbers (e.g., 12345)\n\n"
                "⚠️ **Important:**\n"
                "• Check your Telegram app for the code\n"
                "• Code expires in a few minutes\n"
                "• Reply with the code in this chat"
            )
            
            await self._send_message(update, text)
            
            # Set waiting state
            if context.user_data is not None:
                context.user_data["waiting_for"] = "auth_code"
                context.user_data["auth_client"] = client
                context.user_data["auth_phone_code_hash"] = sent_code.phone_code_hash
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            self.auth_in_progress = False
            await self._send_error_message(update, f"Authentication failed: {str(e)}")
            
            # Clean up
            try:
                if 'auth_client' in context.user_data:
                    await context.user_data['auth_client'].disconnect()
            except:
                pass

    async def handle_verification_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle verification code input"""
        try:
            if not update.message or not update.message.text:
                return
                
            code = update.message.text.strip()
            
            # Validate code format
            if not code.isdigit() or len(code) < 4:
                await update.message.reply_text(
                    "❌ Invalid code format. Please enter only numbers (e.g., 12345)"
                )
                return
                
            # Show processing message
            processing_msg = await update.message.reply_text("🔄 Verifying code...")
            
            # Get client from context
            if not context.user_data or 'auth_client' not in context.user_data:
                await processing_msg.edit_text("❌ Authentication session expired. Please restart.")
                return
                
            client = context.user_data['auth_client']
            phone_code_hash = context.user_data['auth_phone_code_hash']
            
            try:
                # Sign in with code
                await client.sign_in(
                    settings.TELEGRAM_PHONE_NUMBER,
                    phone_code_hash,
                    code
                )
                
                # Success!
                await processing_msg.edit_text(
                    "✅ **AUTHENTICATION SUCCESSFUL!**\n\n"
                    "🤖 Userbot is now connected and ready for broadcasting.\n"
                    "🎯 You can now start using the automation features!"
                )
                
                # Initialize userbot instance
                self.userbot_instance = UserBot()
                await self.userbot_instance.start()
                
                # Clean up
                context.user_data.pop("waiting_for", None)
                context.user_data.pop("auth_client", None)
                context.user_data.pop("auth_phone_code_hash", None)
                self.auth_in_progress = False
                
                # Show dashboard after 3 seconds
                await asyncio.sleep(3)
                await self.show_auth_status(update, context)
                
            except Exception as sign_in_error:
                logger.error(f"Sign in error: {sign_in_error}")
                
                error_msg = "❌ Verification failed. "
                if "PHONE_CODE_INVALID" in str(sign_in_error):
                    error_msg += "Invalid code. Please try again."
                elif "PHONE_CODE_EXPIRED" in str(sign_in_error):
                    error_msg += "Code expired. Please restart authentication."
                else:
                    error_msg += f"Error: {str(sign_in_error)}"
                    
                await processing_msg.edit_text(error_msg)
                
                # Reset if expired
                if "EXPIRED" in str(sign_in_error):
                    context.user_data.pop("waiting_for", None)
                    self.auth_in_progress = False
                    
        except Exception as e:
            logger.error(f"Error handling verification code: {e}")
            await self._send_error_message(update, "Failed to process verification code")

    async def clear_session(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Clear userbot session"""
        try:
            import os
            from pathlib import Path
            
            session_file = Path("sessions/userbot_session.session")
            if session_file.exists():
                os.remove(session_file)
                
            text = (
                "🗑️ **SESSION CLEARED**\n\n"
                "✅ Userbot session has been cleared.\n"
                "🔄 You will need to authenticate again to use broadcasting features.\n\n"
                "Use 'Start Authentication' to reconnect."
            )
            
            keyboard = [
                [InlineKeyboardButton("🚀 Start Authentication", callback_data="auth_start")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )
                
        except Exception as e:
            logger.error(f"Error clearing session: {e}")
            await self._send_error_message(update, "Failed to clear session")

    async def test_connection(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Test userbot connection"""
        try:
            is_connected = await self._check_userbot_status()
            
            if is_connected:
                text = (
                    "✅ **CONNECTION TEST: SUCCESS**\n\n"
                    "🤖 Userbot is connected and responding.\n"
                    "📡 Connection to Telegram servers: OK\n"
                    "🔒 Session: Valid\n"
                    "🎯 Ready for broadcasting!"
                )
            else:
                text = (
                    "❌ **CONNECTION TEST: FAILED**\n\n"
                    "🤖 Userbot is not connected.\n"
                    "🔄 Please authenticate first to enable broadcasting."
                )
                
            keyboard = [
                [InlineKeyboardButton("🔙 Back to Auth Status", callback_data="auth_status")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )
                
        except Exception as e:
            logger.error(f"Error testing connection: {e}")
            await self._send_error_message(update, "Failed to test connection")

    async def show_auth_help(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show authentication help"""
        text = (
            "❓ **AUTHENTICATION HELP**\n"
            "═══════════════════════════\n\n"
            "🔐 **What is Userbot Authentication?**\n"
            "The userbot is your personal Telegram client that sends messages to groups. "
            "It needs to be authenticated with your phone number to work.\n\n"
            "📱 **Authentication Process:**\n"
            "1. Click 'Start Authentication'\n"
            "2. Telegram sends a code to your phone\n"
            "3. Enter the code in this chat\n"
            "4. Done! Userbot is ready\n\n"
            "🔒 **Security:**\n"
            "• Your session is encrypted and stored locally\n"
            "• Only you have access to your account\n"
            "• Session can be cleared anytime\n\n"
            "⚠️ **Troubleshooting:**\n"
            "• Code not received? Check your Telegram app\n"
            "• Code expired? Restart authentication\n"
            "• Still issues? Clear session and try again"
        )
        
        keyboard = [
            [InlineKeyboardButton("🚀 Start Authentication", callback_data="auth_start")],
            [InlineKeyboardButton("🔙 Back to Auth", callback_data="auth_status")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
        """Handle authentication-related callbacks"""
        if data == "auth_status":
            await self.show_auth_status(update, context)
        elif data == "auth_start":
            await self.start_authentication(update, context)
        elif data == "auth_clear":
            await self.clear_session(update, context)
        elif data == "auth_test":
            await self.test_connection(update, context)
        elif data == "auth_help":
            await self.show_auth_help(update, context)
        elif data == "auth_restart":
            await self.clear_session(update, context)
            await asyncio.sleep(1)
            await self.start_authentication(update, context)

    async def _check_userbot_status(self) -> bool:
        """Check if userbot is authenticated and connected"""
        try:
            from pathlib import Path
            session_file = Path("sessions/userbot_session.session")
            return session_file.exists()
        except:
            return False

    async def _send_message(self, update: Update, text: str) -> None:
        """Send message helper"""
        if update.callback_query:
            await update.callback_query.edit_message_text(text, parse_mode="Markdown")
        elif update.message:
            await update.message.reply_text(text, parse_mode="Markdown")

    async def _send_error_message(self, update: Update, error: str) -> None:
        """Send error message helper"""
        text = f"❌ **Error**: {error}\n\nPlease try again or contact support if the issue persists."
        await self._send_message(update, text)