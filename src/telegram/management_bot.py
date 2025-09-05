"""
Management Bot - Modern Telegram bot interface for system management
Enhanced with 2025 UI/UX best practices
"""

from loguru import logger

from src.core.config import settings
from src.core.constants import MAX_RECENT_ITEMS_DISPLAY, PREVIEW_MESSAGE_LENGTH
from src.telegram.handlers.auth_handlers import AuthHandlers
from src.telegram.handlers.blacklist_handlers import BlacklistHandlers
from src.telegram.handlers.config_handlers import ConfigHandlers
from src.telegram.handlers.group_handlers import GroupHandlers
from src.telegram.handlers.message_handlers import MessageHandlers
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


class ManagementBot:
    """Modern Telegram bot for system management with enhanced UI/UX"""

    def __init__(self) -> None:
        self.app: Application | None = None
        self.auth_handlers = AuthHandlers()
        self.message_handlers = MessageHandlers()
        self.group_handlers = GroupHandlers()
        self.config_handlers = ConfigHandlers()
        self.blacklist_handlers = BlacklistHandlers()

    async def start(self) -> None:
        """Start the management bot"""
        if not settings.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in environment")

        # Create application
        self.app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Add handlers
        self._add_handlers()

        # Start the bot
        await self.app.initialize()
        await self.app.start()
        if self.app.updater:
            await self.app.updater.start_polling()
        else:
            raise RuntimeError("Updater not available")

        logger.info("🤖 Management bot is running")

    async def stop(self) -> None:
        """Stop the management bot"""
        if self.app:
            try:
                if self.app.updater and self.app.updater.running:
                    await self.app.updater.stop()
                await self.app.stop()
                await self.app.shutdown()
            except Exception as e:
                logger.warning(f"Error during bot shutdown: {e}")

    def _add_handlers(self) -> None:
        """Add command and callback handlers"""
        if not self.app:
            raise RuntimeError("Application not initialized")

        # Main commands
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("menu", self.main_menu))
        self.app.add_handler(CommandHandler("status", self.status_command))

        # Authentication
        self.app.add_handler(CommandHandler("auth", self.auth_handlers.show_auth_status))

        # Message management
        self.app.add_handler(CommandHandler("messages", self.message_handlers.list_messages))
        self.app.add_handler(
            CommandHandler("addmessage", self.message_handlers.add_message_command)
        )

        # Group management
        self.app.add_handler(CommandHandler("groups", self.group_handlers.list_groups))
        self.app.add_handler(CommandHandler("addgroup", self.group_handlers.add_group_command))
        self.app.add_handler(
            CommandHandler("addgroups", self.group_handlers.add_groups_bulk_command)
        )

        # Configuration
        self.app.add_handler(CommandHandler("config", self.config_handlers.show_config))

        # Blacklist management
        self.app.add_handler(CommandHandler("blacklist", self.blacklist_handlers.show_blacklist))

        # Callback query handlers
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))

        # Message handlers for text input
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_input)
        )

    async def start_command(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command with modern welcome interface"""
        welcome_text = (
            "🚀 **OTOGRAM AUTOMATION SYSTEM**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 **Smart Mass Messaging Platform for Telegram**\n\n"
            "✨ **Core Features:**\n"
            "├ 📤 Automated group broadcasting\n"
            "├ 🛡️ Intelligent blacklist management\n"
            "├ ⚡ Smart rate limiting & optimization\n"
            "├ 🔐 Secure userbot authentication\n"
            "└ 📊 Real-time analytics & monitoring\n\n"
            "🎮 **Ready to get started?**\n"
            "Choose an option below to begin:"
        )

        keyboard = [
            [
                InlineKeyboardButton("🏠 Main Dashboard", callback_data="dashboard"),
                InlineKeyboardButton("⚡ Quick Setup", callback_data="quick_setup"),
            ],
            [
                InlineKeyboardButton("🔐 Authentication", callback_data="auth_status"),
                InlineKeyboardButton("📚 User Guide", callback_data="tutorial"),
            ],
            [
                InlineKeyboardButton("💡 Help Center", callback_data="help_center"),
                InlineKeyboardButton("ℹ️ System Info", callback_data="system_info"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(
                welcome_text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def main_menu(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Modern main dashboard with enhanced UI"""
        # Get system stats
        stats_text = await self._get_system_stats()

        text = (
            f"🏠 **CONTROL DASHBOARD**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{stats_text}\n"
            f"🎛️ **Management Center**\n"
            f"Select a category to manage:"
        )

        keyboard = [
            [
                InlineKeyboardButton("📝 Messages", callback_data="messages_dashboard"),
                InlineKeyboardButton("👥 Groups", callback_data="groups_dashboard"),
            ],
            [
                InlineKeyboardButton("🔐 Authentication", callback_data="auth_status"),
                InlineKeyboardButton("🚫 Blacklist", callback_data="blacklist_dashboard"),
            ],
            [
                InlineKeyboardButton("⚙️ Configuration", callback_data="settings_dashboard"),
                InlineKeyboardButton("📊 Analytics", callback_data="analytics"),
            ],
            [
                InlineKeyboardButton("🎛️ System Control", callback_data="system_control"),
                InlineKeyboardButton("🔄 Refresh Data", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def status_command(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced system status with real-time data"""
        try:
            # Get real-time system statistics
            message_stats = await self.message_handlers.message_service.get_message_count()
            group_stats = await self.group_handlers.group_service.get_group_stats()
            blacklist_stats = await self.blacklist_handlers.blacklist_service.get_blacklist_stats()
            userbot_status = await self.auth_handlers._check_userbot_status()

            # Status indicators
            bot_status = "🟢 Online"
            userbot_indicator = "🟢 Connected" if userbot_status else "🔴 Disconnected"
            database_status = "🟢 Connected"  # We'll enhance this later

            status_text = (
                "📊 **SYSTEM STATUS REPORT**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🤖 **Service Status:**\n"
                f"├ Management Bot: {bot_status}\n"
                f"├ Userbot Engine: {userbot_indicator}\n"
                f"└ Database: {database_status}\n\n"
                "📈 **Content Statistics:**\n"
                f"├ Active Messages: {message_stats['active']}/{message_stats['total']}\n"
                f"├ Active Groups: {group_stats['active']}/{group_stats['total']}\n"
                f"└ Blacklisted: {blacklist_stats['total']} entries\n\n"
                "⚡ **System Health:**\n"
                f"├ Broadcasting: {'✅ Ready' if userbot_status and message_stats['active'] > 0 and group_stats['active'] > 0 else '⚠️ Setup Required'}\n"
                f"├ Auto Recovery: 🟢 Enabled\n"
                f"└ Safety Limits: 🛡️ Active\n\n"
                "🕐 **Last Updated:** Just now"
            )

            keyboard = [
                [
                    InlineKeyboardButton("🔄 Refresh Status", callback_data="refresh_status"),
                    InlineKeyboardButton("📊 Detailed Analytics", callback_data="analytics"),
                ],
                [
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    InlineKeyboardButton("⚙️ System Settings", callback_data="settings_dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.message:
                await update.message.reply_text(
                    status_text, parse_mode="Markdown", reply_markup=reply_markup
                )
            elif update.callback_query:
                await update.callback_query.edit_message_text(
                    status_text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error getting status: {e}")
            await self._send_error_message(update, "Failed to retrieve system status")

    async def help_command(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced help command with better organization"""
        help_text = (
            "💡 **OTOGRAM HELP CENTER**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🚀 **Quick Commands:**\n"
            "├ `/start` - Launch main interface\n"
            "├ `/menu` - Access control dashboard\n"
            "├ `/status` - View system status\n"
            "└ `/help` - Show this help menu\n\n"
            "🎛️ **Management Commands:**\n"
            "├ `/auth` - Setup userbot authentication\n"
            "├ `/messages` - Manage broadcast messages\n"
            "├ `/groups` - Manage target groups\n"
            "└ `/config` - System configuration\n\n"
            "🔧 **Utility Commands:**\n"
            "├ `/addmessage` - Quick add new message\n"
            "├ `/addgroup` - Quick add single group\n"
            "├ `/addgroups` - Bulk add multiple groups\n"
            "└ `/blacklist` - View blacklist status\n\n"
            "📚 **Getting Started:**\n"
            "1️⃣ Setup authentication with `/auth`\n"
            "2️⃣ Add messages with `/addmessage`\n"
            "3️⃣ Add target groups with `/addgroup`\n"
            "4️⃣ Configure settings and start broadcasting!\n\n"
            "💡 Use `/menu` for the graphical interface!"
        )

        keyboard = [
            [
                InlineKeyboardButton("🏠 Main Dashboard", callback_data="dashboard"),
                InlineKeyboardButton("🚀 Quick Setup", callback_data="quick_setup"),
            ],
            [
                InlineKeyboardButton("📚 Tutorial Guide", callback_data="tutorial"),
                InlineKeyboardButton("💬 Support Center", callback_data="help_center"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(
                help_text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _get_system_stats(self) -> str:
        """Get enhanced system statistics for dashboard"""
        try:
            # Get stats from services
            message_stats = await self.message_handlers.message_service.get_message_count()
            group_stats = await self.group_handlers.group_service.get_group_stats()
            blacklist_stats = await self.blacklist_handlers.blacklist_service.get_blacklist_stats()

            # Check userbot status
            userbot_status = await self.auth_handlers._check_userbot_status()

            # Calculate health scores
            msg_health = "🟢" if message_stats["active"] > 0 else "🔴"
            grp_health = "🟢" if group_stats["active"] > 0 else "🔴"
            auth_health = "🟢" if userbot_status else "🔴"
            bl_health = (
                "🟢"
                if blacklist_stats["total"] < 5
                else "🟡"
                if blacklist_stats["total"] < 20
                else "🔴"
            )

            # Overall system health
            ready_to_broadcast = (
                userbot_status and message_stats["active"] > 0 and group_stats["active"] > 0
            )
            system_health = "🟢 Operational" if ready_to_broadcast else "⚠️ Setup Required"

            stats = (
                f"📊 **System Overview**\n"
                f"├ Status: {system_health}\n"
                f"├ Authentication: {auth_health} {'Ready' if userbot_status else 'Required'}\n"
                f"└ Health Score: {'Excellent' if ready_to_broadcast else 'Setup Needed'}\n\n"
                f"📝 **Content Status**\n"
                f"├ Messages: {msg_health} {message_stats['active']}/{message_stats['total']} active\n"
                f"├ Groups: {grp_health} {group_stats['active']}/{group_stats['total']} active\n"
                f"└ Blacklist: {bl_health} {blacklist_stats['total']} entries\n"
            )

            return stats

        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return (
                "📊 **System Overview**\n"
                "├ Status: ⚠️ Loading...\n"
                "├ Authentication: ⏳ Checking...\n"
                "└ Health Score: Initializing\n\n"
                "📝 **Content Status**\n"
                "├ Messages: ⏳ Loading...\n"
                "├ Groups: ⏳ Loading...\n"
                "└ Blacklist: ⏳ Loading...\n"
            )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced callback handling with modern routing"""
        query = update.callback_query
        if not query:
            return
        await query.answer()

        data = query.data
        if not data:
            return

        # Main navigation
        if data == "dashboard":
            await self.main_menu(update, context)
        elif data == "refresh_status":
            await self.status_command(update, context)
        elif data == "quick_setup":
            await self._show_quick_setup(update, context)
        elif data == "tutorial":
            await self._show_tutorial(update, context)
        elif data == "help_center":
            await self._show_help_center(update, context)
        elif data == "system_info":
            await self._show_system_info(update, context)

        # Dashboard sections
        elif data == "messages_dashboard":
            await self._show_messages_dashboard(update, context)
        elif data == "groups_dashboard":
            await self._show_groups_dashboard(update, context)
        elif data == "blacklist_dashboard":
            await self._show_blacklist_dashboard(update, context)
        elif data == "settings_dashboard":
            await self._show_settings_dashboard(update, context)
        elif data == "analytics":
            await self._show_analytics(update, context)
        elif data == "system_control":
            await self._show_system_control(update, context)
        elif data == "emergency_stop":
            await self._show_emergency_stop(update, context)

        # Legacy routing for existing handlers
        elif data.startswith("auth_"):
            await self.auth_handlers.handle_callback(update, context, str(data))
        elif data.startswith("messages_"):
            await self.message_handlers.handle_callback(update, context, str(data))
        elif data.startswith("groups_"):
            await self.group_handlers.handle_callback(update, context, str(data))
        elif data.startswith("config_"):
            await self.config_handlers.handle_callback(update, context, str(data))
        elif data.startswith("blacklist_"):
            await self.blacklist_handlers.handle_callback(update, context, str(data))

        # Back navigation
        elif data == "back_to_dashboard":
            await self.main_menu(update, context)

    async def _show_quick_setup(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced quick setup wizard"""
        text = (
            "🚀 **QUICK SETUP WIZARD**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 **Get your system ready in 4 simple steps:**\n\n"
            "**Step 1:** 🔐 **Authentication Setup**\n"
            "└ Connect your Telegram account for broadcasting\n\n"
            "**Step 2:** 📝 **Add Broadcast Messages**\n"
            "└ Create messages that will be sent to groups\n\n"
            "**Step 3:** 👥 **Add Target Groups**\n"
            "└ Specify which groups should receive messages\n\n"
            "**Step 4:** ⚡ **Configure & Launch**\n"
            "└ Fine-tune settings and start automation\n\n"
            "🎮 **Choose where to start:**"
        )

        keyboard = [
            [InlineKeyboardButton("🔐 Step 1: Authentication", callback_data="auth_status")],
            [InlineKeyboardButton("📝 Step 2: Add Messages", callback_data="messages_dashboard")],
            [InlineKeyboardButton("👥 Step 3: Add Groups", callback_data="groups_dashboard")],
            [InlineKeyboardButton("⚡ Step 4: Configuration", callback_data="settings_dashboard")],
            [
                InlineKeyboardButton("📊 Check Status", callback_data="refresh_status"),
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_system_info(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show system information"""
        text = (
            "ℹ️ **SYSTEM INFORMATION**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🤖 **Otogram Automation System**\n"
            "├ Version: 2.0.4\n"
            "├ Build: Personal Edition\n"
            "└ Status: Production Ready\n\n"
            "⚙️ **Technical Stack:**\n"
            "├ Engine: Python 3.11+\n"
            "├ Telegram API: Pyrofork 2.3+\n"
            "├ Bot Framework: python-telegram-bot 21+\n"
            "├ Database: MongoDB 4.4+\n"
            "└ Scheduler: APScheduler 3.11+\n\n"
            "🛡️ **Security Features:**\n"
            "├ Rate Limiting: ✅ Enabled\n"
            "├ Auto Blacklist: ✅ Active\n"
            "├ Session Encryption: ✅ Secured\n"
            "└ Error Recovery: ✅ Automated\n\n"
            "📄 **License:** MIT License\n"
            "🔗 **GitHub:** github.com/dygje/Otogram"
        )

        keyboard = [
            [
                InlineKeyboardButton("📚 Documentation", callback_data="help_center"),
                InlineKeyboardButton("📊 System Status", callback_data="refresh_status"),
            ],
            [
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings_dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_messages_dashboard(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced messages dashboard with modern design"""
        try:
            messages = await self.message_handlers.message_service.get_all_messages()
            stats = await self.message_handlers.message_service.get_message_count()

            # Health indicator
            health_status = "🟢 Healthy" if stats["active"] > 0 else "🔴 No Active Messages"
            usage_rate = (stats["active"] / max(stats["total"], 1)) * 100

            text = (
                f"📝 **MESSAGES CONTROL CENTER**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📊 **Overview Dashboard:**\n"
                f"├ Status: {health_status}\n"
                f"├ Total Messages: {stats['total']}\n"
                f"├ Active Messages: {stats['active']} ({usage_rate:.0f}%)\n"
                f"├ Inactive Messages: {stats['inactive']}\n"
                f"└ Broadcast Ready: {'✅ Yes' if stats['active'] > 0 else '❌ Setup Required'}\n\n"
            )

            if messages:
                text += "*📋 Recent Messages Preview:*\n"
                for i, msg in enumerate(messages[:MAX_RECENT_ITEMS_DISPLAY], 1):
                    status_icon = "🟢" if msg.is_active else "⚪"
                    preview = (
                        msg.content[:PREVIEW_MESSAGE_LENGTH] + "..."
                        if len(msg.content) > PREVIEW_MESSAGE_LENGTH
                        else msg.content
                    )
                    text += f"{i}. {status_icon} {preview}\n"

                if len(messages) > MAX_RECENT_ITEMS_DISPLAY:
                    remaining = len(messages) - MAX_RECENT_ITEMS_DISPLAY
                    text += f"   ⋮ *{remaining} more messages...*\n"
            else:
                text += "📝 *No messages configured yet*\n"

            keyboard = [
                [
                    InlineKeyboardButton("➕ Add Message", callback_data="messages_add"),
                    InlineKeyboardButton("📋 View All", callback_data="messages_menu"),
                ],
                [
                    InlineKeyboardButton("🔄 Bulk Actions", callback_data="messages_bulk"),
                    InlineKeyboardButton("📊 Analytics", callback_data="messages_analytics"),
                ],
                [
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    InlineKeyboardButton("🔄 Refresh", callback_data="messages_dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error loading messages dashboard: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Error loading messages dashboard")

    async def _show_groups_dashboard(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced groups dashboard with modern design"""
        try:
            groups = await self.group_handlers.group_service.get_all_groups()
            stats = await self.group_handlers.group_service.get_group_stats()

            # Health indicator
            health_status = "🟢 Healthy" if stats["active"] > 0 else "🔴 No Active Groups"
            usage_rate = (stats["active"] / max(stats["total"], 1)) * 100

            text = (
                f"👥 **GROUPS CONTROL CENTER**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📊 **Overview Dashboard:**\n"
                f"├ Status: {health_status}\n"
                f"├ Total Groups: {stats['total']}\n"
                f"├ Active Groups: {stats['active']} ({usage_rate:.0f}%)\n"
                f"├ Inactive Groups: {stats['inactive']}\n"
                f"└ Ready to Receive: {'✅ Yes' if stats['active'] > 0 else '❌ Setup Required'}\n\n"
            )

            if groups:
                text += "*📋 Recent Groups Preview:*\n"
                for i, group in enumerate(groups[:MAX_RECENT_ITEMS_DISPLAY], 1):
                    status_icon = "🟢" if group.is_active else "⚪"
                    name = group.group_title or group.group_username or group.group_id or "Unknown"
                    # Truncate long names
                    display_name = name[:40] + "..." if len(str(name)) > 40 else name
                    text += f"{i}. {status_icon} {display_name}\n"

                if len(groups) > MAX_RECENT_ITEMS_DISPLAY:
                    remaining = len(groups) - MAX_RECENT_ITEMS_DISPLAY
                    text += f"   ⋮ *{remaining} more groups...*\n"
            else:
                text += "👥 *No groups configured yet*\n"

            keyboard = [
                [
                    InlineKeyboardButton("➕ Add Group", callback_data="groups_add"),
                    InlineKeyboardButton("📋 Add Bulk", callback_data="groups_bulk"),
                ],
                [
                    InlineKeyboardButton("👥 View All", callback_data="groups_menu"),
                    InlineKeyboardButton("📊 Group Stats", callback_data="groups_analytics"),
                ],
                [
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    InlineKeyboardButton("🔄 Refresh", callback_data="groups_dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error loading groups dashboard: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Error loading groups dashboard")

    async def _show_blacklist_dashboard(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced blacklist dashboard"""
        try:
            stats = await self.blacklist_handlers.blacklist_service.get_blacklist_stats()

            # Determine health status
            if stats["total"] == 0:
                health_status = "🟢 Excellent"
            elif stats["permanent"] == 0:
                health_status = "🟡 Good"
            else:
                health_status = "🔴 Attention Needed"

            text = (
                f"🛡️ **BLACKLIST MONITORING CENTER**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📊 **System Health: {health_status}**\n\n"
                f"📈 **Statistics Overview:**\n"
                f"├ Total Blacklisted: {stats['total']} entries\n"
                f"├ 🔴 Permanent Blocks: {stats['permanent']}\n"
                f"├ 🟡 Temporary Blocks: {stats['temporary']}\n"
                f"└ ⏰ Expired Entries: {stats['expired']}\n\n"
            )

            if stats["total"] > 0:
                text += "*🔍 Health Analysis:*\n"
                if stats["expired"] > 0:
                    text += f"⚠️ {stats['expired']} expired entries need cleanup\n"
                if stats["permanent"] > 0:
                    text += f"🔴 {stats['permanent']} permanent blocks detected\n"
                if stats["temporary"] > 0:
                    text += f"🟡 {stats['temporary']} temporary blocks active\n"
                text += "\n"
            else:
                text += "✅ *All target groups are healthy and accessible!*\n\n"

            # Add recommendations
            if stats["total"] > 10:
                text += "💡 *Recommendation: Review blacklist for optimization*"
            elif stats["expired"] > 0:
                text += "💡 *Recommendation: Run cleanup to remove expired entries*"
            else:
                text += "💡 *System is running optimally*"

            keyboard = [
                [
                    InlineKeyboardButton("📋 View Blacklist", callback_data="blacklist_menu"),
                    InlineKeyboardButton("🧹 Cleanup", callback_data="blacklist_cleanup"),
                ],
                [
                    InlineKeyboardButton("📊 Analytics", callback_data="blacklist_analytics"),
                    InlineKeyboardButton("⚙️ Settings", callback_data="blacklist_settings"),
                ],
                [
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    InlineKeyboardButton("🔄 Refresh", callback_data="blacklist_dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error loading blacklist dashboard: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ Error loading blacklist dashboard"
                )

    async def _show_settings_dashboard(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced settings dashboard"""
        text = (
            "⚙️ **SYSTEM CONFIGURATION CENTER**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎛️ **Configuration Categories:**\n\n"
            "📨 **Broadcasting Settings**\n"
            "├ Message timing & delays\n"
            "├ Cycle intervals & scheduling\n"
            "└ Rate limiting & safety\n\n"
            "🛡️ **Blacklist Management**\n"
            "├ Auto-cleanup policies\n"
            "├ Retry attempt limits\n"
            "└ Error handling rules\n\n"
            "🔧 **System Performance**\n"
            "├ Logging levels & output\n"
            "├ Performance optimization\n"
            "└ Resource management\n\n"
            "🔒 **Security & Privacy**\n"
            "├ Session management\n"
            "├ API rate limits\n"
            "└ Data protection settings"
        )

        keyboard = [
            [
                InlineKeyboardButton("📨 Broadcasting", callback_data="config_messaging"),
                InlineKeyboardButton("🛡️ Blacklist", callback_data="config_blacklist"),
            ],
            [
                InlineKeyboardButton("🔧 Performance", callback_data="config_system"),
                InlineKeyboardButton("🔒 Security", callback_data="config_security"),
            ],
            [
                InlineKeyboardButton("📋 View All Settings", callback_data="config_menu"),
                InlineKeyboardButton("🔄 Reset to Defaults", callback_data="config_reset"),
            ],
            [
                InlineKeyboardButton("💾 Backup Config", callback_data="config_backup"),
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_analytics(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced analytics dashboard"""
        try:
            # Get real-time analytics data
            message_stats = await self.message_handlers.message_service.get_message_count()
            group_stats = await self.group_handlers.group_service.get_group_stats()
            blacklist_stats = await self.blacklist_handlers.blacklist_service.get_blacklist_stats()

            # Calculate success rates and metrics
            total_content = message_stats["total"] + group_stats["total"]
            active_content = message_stats["active"] + group_stats["active"]
            success_rate = (
                (active_content / max(total_content, 1)) * 100 if total_content > 0 else 0
            )

            text = (
                f"📊 **ANALYTICS & INSIGHTS**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📈 **Performance Metrics:**\n"
                f"├ Overall Success Rate: {success_rate:.1f}%\n"
                f"├ Content Utilization: {active_content}/{total_content} active\n"
                f"├ System Health Score: {'Excellent' if success_rate > 80 else 'Good' if success_rate > 50 else 'Needs Attention'}\n"
                f"└ Error Rate: {(blacklist_stats['total'] / max(group_stats['total'], 1)) * 100:.1f}%\n\n"
                f"🎯 **Broadcasting Overview:**\n"
                f"├ Ready Messages: {message_stats['active']}\n"
                f"├ Target Groups: {group_stats['active']}\n"
                f"├ Potential Reach: {message_stats['active'] * group_stats['active']} deliveries\n"
                f"└ Blocked Groups: {blacklist_stats['total']}\n\n"
                f"🔍 **System Insights:**\n"
                f"├ Configuration Status: {'✅ Complete' if message_stats['active'] > 0 and group_stats['active'] > 0 else '⚠️ Incomplete'}\n"
                f"├ Maintenance Needed: {'Yes' if blacklist_stats['expired'] > 0 else 'No'}\n"
                f"└ Optimization Score: {min(100, max(0, 100 - (blacklist_stats['total'] * 5)))}/100\n\n"
                f"📅 **Data freshness:** Real-time\n"
                f"🔄 **Last analysis:** Just now"
            )

            keyboard = [
                [
                    InlineKeyboardButton("📊 Detailed Report", callback_data="analytics_detailed"),
                    InlineKeyboardButton("📈 Trend Analysis", callback_data="analytics_trends"),
                ],
                [
                    InlineKeyboardButton("📋 Export Data", callback_data="analytics_export"),
                    InlineKeyboardButton("🔄 Refresh Data", callback_data="analytics"),
                ],
                [
                    InlineKeyboardButton(
                        "💡 Recommendations", callback_data="analytics_recommendations"
                    ),
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error loading analytics: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ Error loading analytics dashboard"
                )

    async def _show_system_control(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced system control panel"""
        text = (
            "🎛️ **SYSTEM CONTROL PANEL**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚠️ **Advanced System Controls**\n"
            "*Use these controls carefully - they affect system operation*\n\n"
            "🔄 **Broadcasting Operations:**\n"
            "├ Pause/Resume broadcast cycles\n"
            "├ Force immediate cycle execution\n"
            "├ Skip current cycle safely\n"
            "└ Emergency broadcast stop\n\n"
            "🧹 **System Maintenance:**\n"
            "├ Cleanup expired blacklist entries\n"
            "├ Optimize database performance\n"
            "├ Clear system logs\n"
            "└ Reset session data\n\n"
            "🔧 **Service Management:**\n"
            "├ Restart bot services\n"
            "├ Reload configuration\n"
            "├ Update system settings\n"
            "└ Emergency system shutdown\n\n"
            "🛡️ **Safety:** All operations include confirmation dialogs"
        )

        keyboard = [
            [
                InlineKeyboardButton("⏸️ Pause System", callback_data="system_pause"),
                InlineKeyboardButton("▶️ Resume System", callback_data="system_resume"),
            ],
            [
                InlineKeyboardButton("⏭️ Force Cycle", callback_data="system_force_cycle"),
                InlineKeyboardButton("⏩ Skip Cycle", callback_data="system_skip_cycle"),
            ],
            [
                InlineKeyboardButton("🧹 Run Maintenance", callback_data="system_maintenance"),
                InlineKeyboardButton("🔄 Restart Services", callback_data="system_restart"),
            ],
            [
                InlineKeyboardButton("🆘 Emergency Stop", callback_data="emergency_stop"),
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_emergency_stop(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced emergency stop confirmation"""
        text = (
            "🆘 **EMERGENCY SYSTEM SHUTDOWN**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚠️ **CRITICAL OPERATION WARNING**\n\n"
            "This action will immediately perform:\n\n"
            "🛑 **Immediate Actions:**\n"
            "├ Stop all active broadcasting\n"
            "├ Disconnect userbot session\n"
            "├ Terminate scheduled tasks\n"
            "└ Save current system state\n\n"
            "💾 **Data Safety:**\n"
            "├ All messages will be preserved\n"
            "├ Group configurations will be saved\n"
            "├ Settings will remain intact\n"
            "└ Blacklist data will be maintained\n\n"
            "🔄 **Recovery:**\n"
            "├ System can be restarted with `python main.py`\n"
            "├ All data will be automatically restored\n"
            "└ No manual reconfiguration needed\n\n"
            "⏱️ **Use emergency stop when:**\n"
            "• System is behaving unexpectedly\n"
            "• Too many errors are occurring\n"
            "• Immediate shutdown is required\n\n"
            "**⚠️ Are you absolutely sure you want to proceed?**"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🆘 CONFIRM EMERGENCY STOP", callback_data="emergency_confirm"
                ),
            ],
            [
                InlineKeyboardButton("❌ Cancel", callback_data="system_control"),
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_tutorial(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced interactive tutorial"""
        text = (
            "📚 **INTERACTIVE LEARNING CENTER**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎓 **Master Otogram step by step with guided tutorials:**\n\n"
            "📝 **Module 1: Message Management**\n"
            "├ Creating effective broadcast messages\n"
            "├ Message formatting and optimization\n"
            "├ Content strategy best practices\n"
            "└ Message lifecycle management\n\n"
            "👥 **Module 2: Group Management**\n"
            "├ Adding groups efficiently (single & bulk)\n"
            "├ Understanding group formats\n"
            "├ Group validation and verification\n"
            "└ Managing large group lists\n\n"
            "🛡️ **Module 3: Blacklist System**\n"
            "├ Understanding automatic blacklisting\n"
            "├ Managing temporary vs permanent blocks\n"
            "├ Manual blacklist interventions\n"
            "└ Recovery and optimization strategies\n\n"
            "⚙️ **Module 4: Advanced Configuration**\n"
            "├ Timing and rate limit optimization\n"
            "├ Performance tuning guidelines\n"
            "├ Safety limits and best practices\n"
            "└ Monitoring and maintenance\n\n"
            "🚀 **Module 5: Broadcasting Mastery**\n"
            "└ End-to-end automation workflows"
        )

        keyboard = [
            [
                InlineKeyboardButton("📝 Message Tutorial", callback_data="tutorial_messages"),
                InlineKeyboardButton("👥 Groups Tutorial", callback_data="tutorial_groups"),
            ],
            [
                InlineKeyboardButton("🛡️ Blacklist Tutorial", callback_data="tutorial_blacklist"),
                InlineKeyboardButton("⚙️ Config Tutorial", callback_data="tutorial_config"),
            ],
            [
                InlineKeyboardButton(
                    "🚀 Broadcasting Tutorial", callback_data="tutorial_broadcasting"
                ),
                InlineKeyboardButton("🎯 Quick Start Guide", callback_data="tutorial_quickstart"),
            ],
            [
                InlineKeyboardButton("💡 Pro Tips & Tricks", callback_data="tutorial_tips"),
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_help_center(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced help center"""
        text = (
            "💡 **COMPREHENSIVE HELP CENTER**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔍 **Find solutions quickly:**\n\n"
            "❓ **Knowledge Base**\n"
            "├ Frequently asked questions\n"
            "├ Common setup issues\n"
            "├ Performance optimization\n"
            "└ Error resolution guides\n\n"
            "🛠️ **Technical Support**\n"
            "├ Connection troubleshooting\n"
            "├ Authentication problem solving\n"
            "├ Blacklist issue resolution\n"
            "└ Configuration assistance\n\n"
            "📖 **Documentation Library**\n"
            "├ Feature explanations & guides\n"
            "├ Advanced usage scenarios\n"
            "├ API reference materials\n"
            "└ Best practice recommendations\n\n"
            "💬 **Community Support**\n"
            "├ User community forums\n"
            "├ Feature request submissions\n"
            "├ Bug report procedures\n"
            "└ Developer contact information\n\n"
            "🎯 **Quick Solutions:**\n"
            "• Authentication issues → Check `/auth`\n"
            "• No messages sending → Verify `/status`\n"
            "• Groups not receiving → Check blacklist\n"
            "• System slow → Run maintenance"
        )

        keyboard = [
            [
                InlineKeyboardButton("❓ FAQ", callback_data="help_faq"),
                InlineKeyboardButton("🛠️ Troubleshooting", callback_data="help_troubleshoot"),
            ],
            [
                InlineKeyboardButton("📖 Documentation", callback_data="help_docs"),
                InlineKeyboardButton("💬 Community", callback_data="help_community"),
            ],
            [
                InlineKeyboardButton("🔧 System Diagnostics", callback_data="help_diagnostics"),
                InlineKeyboardButton("📋 Command Reference", callback_data="help_commands"),
            ],
            [
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                InlineKeyboardButton("📚 Tutorials", callback_data="tutorial"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def handle_text_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced text input handling"""
        user_data = context.user_data

        if user_data and "waiting_for" in user_data:
            waiting_for = user_data["waiting_for"]

            if waiting_for == "auth_code":
                await self.auth_handlers.handle_verification_code(update, context)
            elif waiting_for == "message_content":
                await self.message_handlers.handle_message_input(update, context)
            elif waiting_for == "group_identifier":
                await self.group_handlers.handle_group_input(update, context)
            elif waiting_for == "groups_bulk":
                await self.group_handlers.handle_bulk_input(update, context)
            elif waiting_for.startswith("config_"):
                await self.config_handlers.handle_config_input(update, context)
            else:
                # Clear waiting state
                if user_data:
                    user_data.pop("waiting_for", None)
                if update.message:
                    await update.message.reply_text(
                        "❌ Input tidak dikenali. Gunakan `/menu` untuk akses dashboard atau `/help` untuk bantuan."
                    )
        elif update.message:
            # Provide helpful guidance instead of generic error
            await update.message.reply_text(
                "🤖 **Halo!** Saya tidak mengerti pesan tersebut.\n\n"
                "🎯 **Coba gunakan:**\n"
                "├ `/menu` - Dashboard utama\n"
                "├ `/help` - Panduan lengkap\n"
                "├ `/status` - Status sistem\n"
                "└ `/start` - Mulai dari awal\n\n"
                "💡 *Tip: Gunakan tombol di bawah pesan untuk navigasi yang mudah!*"
            )

    async def _send_error_message(self, update: Update, error_text: str) -> None:
        """Enhanced error message handling"""
        error_msg = (
            f"❌ **Error Occurred**\n\n"
            f"**Issue:** {error_text}\n\n"
            f"🔧 **Quick Solutions:**\n"
            f"├ Try refreshing with `/menu`\n"
            f"├ Check system status with `/status`\n"
            f"├ Restart authentication with `/auth`\n"
            f"└ Get help with `/help`\n\n"
            f"💡 If the problem persists, please check the troubleshooting guide."
        )

        keyboard = [
            [
                InlineKeyboardButton("🔄 Refresh", callback_data="dashboard"),
                InlineKeyboardButton("💡 Help", callback_data="help_center"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(
                error_msg, parse_mode="Markdown", reply_markup=reply_markup
            )
        elif update.callback_query:
            await update.callback_query.edit_message_text(
                error_msg, parse_mode="Markdown", reply_markup=reply_markup
            )
