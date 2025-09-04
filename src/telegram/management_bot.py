"""
Management Bot - Telegram bot for managing the system
"""

from loguru import logger

from src.core.config import settings
from src.core.constants import MAX_RECENT_ITEMS_DISPLAY, PREVIEW_MESSAGE_LENGTH
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
    """Telegram bot for system management"""

    def __init__(self) -> None:
        self.app: Application | None = None
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
        await self.app.updater.start_polling()

        logger.info("🤖 Management bot is running")

    async def stop(self) -> None:
        """Stop the management bot"""
        if self.app:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()

    def _add_handlers(self) -> None:
        """Add command and callback handlers"""

        # Main commands
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("menu", self.main_menu))
        self.app.add_handler(CommandHandler("status", self.status_command))

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
        """Handle /start command"""
        welcome_text = (
            "🤖 *Telegram Automation System* v1.1\n\n"
            "🎯 *Sistem Otomatisasi Pesan Massal*\n"
            "├ 📤 Pengiriman otomatis ke grup\n"
            "├ 🚫 Blacklist management otomatis\n"
            "├ ⚡ SlowMode skip optimization\n"
            "└ 🔄 Auto recovery system\n\n"
            "*🚀 Pilih menu untuk memulai:*"
        )

        keyboard = [
            [
                InlineKeyboardButton("📋 Dashboard", callback_data="dashboard"),
                InlineKeyboardButton("⚙️ Quick Setup", callback_data="quick_setup"),
            ],
            [
                InlineKeyboardButton("📚 Tutorial", callback_data="tutorial"),
                InlineKeyboardButton("❓ Help Center", callback_data="help_center"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(
                welcome_text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def main_menu(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show modern main menu dashboard"""
        # Get system stats (we'll implement this)
        stats_text = await self._get_system_stats()

        text = f"📊 *SYSTEM DASHBOARD*\n═══════════════════\n\n{stats_text}\n*🎛️ Control Center:*"

        keyboard = [
            [
                InlineKeyboardButton("📝 Messages", callback_data="messages_dashboard"),
                InlineKeyboardButton("👥 Groups", callback_data="groups_dashboard"),
            ],
            [
                InlineKeyboardButton("🚫 Blacklist", callback_data="blacklist_dashboard"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings_dashboard"),
            ],
            [
                InlineKeyboardButton("📊 Analytics", callback_data="analytics"),
                InlineKeyboardButton("🔄 System Control", callback_data="system_control"),
            ],
            [
                InlineKeyboardButton("🆘 Emergency Stop", callback_data="emergency_stop"),
                InlineKeyboardButton("🔄 Refresh Stats", callback_data="dashboard"),
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
        """Show system status"""
        # This will be implemented with actual status checking
        status_text = (
            "📊 *Status Sistem*\n\n"
            "🤖 Management Bot: ✅ Running\n"
            "🔄 Userbot: ✅ Connected\n"
            "🗄️ Database: ✅ Connected\n\n"
            "📝 Pesan Aktif: Memuat...\n"
            "👥 Grup Aktif: Memuat...\n"
            "🚫 Blacklist: Memuat...\n\n"
            "🔄 Siklus Terakhir: Belum berjalan\n"
            "⏰ Siklus Berikutnya: Menunggu..."
        )

        if update.message:
            await update.message.reply_text(status_text, parse_mode="Markdown")

    async def help_command(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        help_text = (
            "🤖 *OTOGRAM AUTOMATION SYSTEM*\n\n"
            "📋 *Available Commands:*\n\n"
            "/start - Initialize bot interface\n"
            "/menu - Main dashboard with quick actions\n"
            "/status - Real-time system status & statistics\n"
            "/messages - Manage broadcast messages\n"
            "/addmessage - Add new broadcast message\n"
            "/groups - Manage target groups\n"
            "/addgroup - Add single group\n"
            "/addgroups - Add multiple groups (bulk)\n"
            "/config - System configuration\n"
            "/blacklist - View blacklist management\n"
            "/help - Show this help message\n\n"
            "🎯 *Quick Start:*\n"
            "1. Add messages: /addmessage\n"
            "2. Add groups: /addgroup or /addgroups\n"
            "3. Configure: /config\n"
            "4. Monitor: /status\n\n"
            "📚 For detailed help, use /menu and explore!"
        )

        if update.message:
            await update.message.reply_text(help_text, parse_mode="Markdown")

    async def _get_system_stats(self) -> str:
        """Get system statistics for dashboard"""
        try:
            # Get stats from services
            message_stats = await self.message_handlers.message_service.get_message_count()
            group_stats = await self.group_handlers.group_service.get_group_stats()
            blacklist_stats = await self.blacklist_handlers.blacklist_service.get_blacklist_stats()

            # Calculate percentages
            active_msg_pct = (message_stats["active"] / max(message_stats["total"], 1)) * 100
            active_grp_pct = (group_stats["active"] / max(group_stats["total"], 1)) * 100

            # Status indicators
            msg_status = "🟢" if message_stats["active"] > 0 else "🔴"
            grp_status = "🟢" if group_stats["active"] > 0 else "🔴"
            bl_status = "🟡" if blacklist_stats["total"] > 0 else "🟢"

            stats = (
                f"📝 *Messages:* {msg_status} {message_stats['active']}/{message_stats['total']} active ({active_msg_pct:.0f}%)\n"
                f"👥 *Groups:* {grp_status} {group_stats['active']}/{group_stats['total']} active ({active_grp_pct:.0f}%)\n"
                f"🚫 *Blacklist:* {bl_status} {blacklist_stats['total']} entries ({blacklist_stats['temporary']} temp)\n"
                f"⚡ *System:* 🟢 Running • 🔄 Auto-mode ON\n"
            )

            return stats

        except Exception:
            return "📊 *Status:* ⚠️ Loading stats..."

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle callback queries with modern routing"""
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
        elif data == "quick_setup":
            await self._show_quick_setup(update, context)
        elif data == "tutorial":
            await self._show_tutorial(update, context)
        elif data == "help_center":
            await self._show_help_center(update, context)

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
        """Show quick setup wizard"""
        text = (
            "🚀 *QUICK SETUP WIZARD*\n"
            "═══════════════════\n\n"
            "Setup sistem dalam 3 langkah mudah:\n\n"
            "1️⃣ **Tambah Pesan** - Pesan untuk broadcast\n"
            "2️⃣ **Tambah Grup** - Target grup penerima\n"
            "3️⃣ **Mulai Broadcasting** - Sistem berjalan otomatis\n\n"
            "*Pilih langkah yang ingin Anda mulai:*"
        )

        keyboard = [
            [InlineKeyboardButton("1️⃣ Setup Pesan", callback_data="setup_messages")],
            [InlineKeyboardButton("2️⃣ Setup Grup", callback_data="setup_groups")],
            [InlineKeyboardButton("3️⃣ Setup Complete", callback_data="setup_complete")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="dashboard")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_messages_dashboard(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Show messages dashboard with modern layout"""
        try:
            messages = await self.message_handlers.message_service.get_all_messages()
            stats = await self.message_handlers.message_service.get_message_count()

            text = (
                f"📝 *MESSAGES CONTROL CENTER*\n"
                f"═══════════════════════════\n\n"
                f"📊 **Overview:**\n"
                f"├ Total: {stats['total']} messages\n"
                f"├ Active: {stats['active']} messages 🟢\n"
                f"├ Inactive: {stats['inactive']} messages 🔴\n"
                f"└ Ready for broadcast: {'Yes ✅' if stats['active'] > 0 else 'No ❌'}\n\n"
            )

            if messages:
                text += "*📋 Recent Messages:*\n"
                for i, msg in enumerate(messages[:MAX_RECENT_ITEMS_DISPLAY], 1):
                    status = "🟢" if msg.is_active else "🔴"
                    preview = (
                        msg.content[:PREVIEW_MESSAGE_LENGTH] + "..."
                        if len(msg.content) > PREVIEW_MESSAGE_LENGTH
                        else msg.content
                    )
                    text += f"{i}. {status} {preview}\n"

                if len(messages) > MAX_RECENT_ITEMS_DISPLAY:
                    text += f"... and {len(messages) - MAX_RECENT_ITEMS_DISPLAY} more\n"
            else:
                text += "❌ *No messages found*\n"

            keyboard = [
                [
                    InlineKeyboardButton("+ Add Message", callback_data="messages_add"),
                    InlineKeyboardButton("📋 View All", callback_data="messages_menu"),
                ],
                [
                    InlineKeyboardButton("🔄 Bulk Actions", callback_data="messages_bulk"),
                    InlineKeyboardButton("📊 Analytics", callback_data="messages_analytics"),
                ],
                [InlineKeyboardButton("🔙 Back to Dashboard", callback_data="dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception:
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Error loading messages dashboard")

    async def _show_groups_dashboard(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Show groups dashboard with modern layout"""
        try:
            groups = await self.group_handlers.group_service.get_all_groups()
            stats = await self.group_handlers.group_service.get_group_stats()

            text = (
                f"👥 *GROUPS CONTROL CENTER*\n"
                f"═══════════════════════════\n\n"
                f"📊 **Overview:**\n"
                f"├ Total: {stats['total']} groups\n"
                f"├ Active: {stats['active']} groups 🟢\n"
                f"├ Inactive: {stats['inactive']} groups 🔴\n"
                f"└ Ready to receive: {'Yes ✅' if stats['active'] > 0 else 'No ❌'}\n\n"
            )

            if groups:
                text += "*📋 Recent Groups:*\n"
                for i, group in enumerate(groups[:MAX_RECENT_ITEMS_DISPLAY], 1):
                    status = "🟢" if group.is_active else "🔴"
                    name = group.group_title or group.group_username or group.group_id or "Unknown"
                    text += f"{i}. {status} {name}\n"

                if len(groups) > MAX_RECENT_ITEMS_DISPLAY:
                    text += f"... and {len(groups) - MAX_RECENT_ITEMS_DISPLAY} more\n"
            else:
                text += "❌ *No groups found*\n"

            keyboard = [
                [
                    InlineKeyboardButton("+ Add Group", callback_data="groups_add"),
                    InlineKeyboardButton("📋 Add Bulk", callback_data="groups_bulk"),
                ],
                [
                    InlineKeyboardButton("👥 View All", callback_data="groups_menu"),
                    InlineKeyboardButton("📊 Group Stats", callback_data="groups_analytics"),
                ],
                [InlineKeyboardButton("🔙 Back to Dashboard", callback_data="dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception:
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Error loading groups dashboard")

    async def _show_blacklist_dashboard(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Show blacklist dashboard"""
        try:
            stats = await self.blacklist_handlers.blacklist_service.get_blacklist_stats()

            status_icon = "🟢" if stats["total"] == 0 else "🟡" if stats["permanent"] == 0 else "🔴"

            text = (
                f"🚫 *BLACKLIST MONITORING*\n"
                f"═══════════════════════\n\n"
                f"🎯 **System Status:** {status_icon}\n\n"
                f"📊 **Statistics:**\n"
                f"├ Total Blacklisted: {stats['total']}\n"
                f"├ 🔴 Permanent: {stats['permanent']}\n"
                f"├ 🟡 Temporary: {stats['temporary']}\n"
                f"└ ⏰ Expired: {stats['expired']}\n\n"
            )

            if stats["total"] > 0:
                text += "*📋 Blacklist Health:*\n"
                if stats["expired"] > 0:
                    text += f"⚠️ {stats['expired']} entries need cleanup\n"
                if stats["permanent"] > 0:
                    text += f"🔴 {stats['permanent']} permanent blocks\n"
                if stats["temporary"] > 0:
                    text += f"🟡 {stats['temporary']} temporary blocks\n"
            else:
                text += "✅ *All groups are healthy!*\n"

            keyboard = [
                [
                    InlineKeyboardButton("📋 View Blacklist", callback_data="blacklist_menu"),
                    InlineKeyboardButton("🧹 Cleanup", callback_data="blacklist_cleanup"),
                ],
                [
                    InlineKeyboardButton("📊 Analytics", callback_data="blacklist_analytics"),
                    InlineKeyboardButton("⚙️ Settings", callback_data="blacklist_settings"),
                ],
                [InlineKeyboardButton("🔙 Back to Dashboard", callback_data="dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception:
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ Error loading blacklist dashboard"
                )

    async def _show_settings_dashboard(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Show settings dashboard"""
        text = (
            "⚙️ *SYSTEM SETTINGS*\n"
            "═══════════════════\n\n"
            "*🎛️ Configuration Categories:*\n\n"
            "📨 **Messaging Settings**\n"
            "├ Message delays\n"
            "├ Cycle intervals\n"
            "└ Broadcasting behavior\n\n"
            "🚫 **Blacklist Settings**\n"
            "├ Auto cleanup rules\n"
            "├ Retry attempts\n"
            "└ Error handling\n\n"
            "🔧 **System Settings**\n"
            "├ Logging level\n"
            "├ Performance tuning\n"
            "└ Safety limits\n"
        )

        keyboard = [
            [
                InlineKeyboardButton("📨 Messaging", callback_data="config_messaging"),
                InlineKeyboardButton("🚫 Blacklist", callback_data="config_blacklist"),
            ],
            [
                InlineKeyboardButton("🔧 System", callback_data="config_system"),
                InlineKeyboardButton("📋 View All", callback_data="config_menu"),
            ],
            [
                InlineKeyboardButton("🔄 Reset Defaults", callback_data="config_reset"),
                InlineKeyboardButton("💾 Backup Config", callback_data="config_backup"),
            ],
            [InlineKeyboardButton("🔙 Back to Dashboard", callback_data="dashboard")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_system_control(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Show system control panel"""
        text = (
            "🎛️ *SYSTEM CONTROL PANEL*\n"
            "═══════════════════════════\n\n"
            "⚠️ **Advanced Controls**\n"
            "*Use with caution - these affect system operation*\n\n"
            "🔄 **Broadcasting Control:**\n"
            "├ Pause/Resume cycles\n"
            "├ Force next cycle\n"
            "└ Skip current cycle\n\n"
            "🧹 **Maintenance:**\n"
            "├ Cleanup expired blacklist\n"
            "├ Database optimization\n"
            "└ Clear logs\n\n"
            "🔧 **System:**\n"
            "├ Restart services\n"
            "├ Reload configuration\n"
            "└ Emergency stop\n"
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
                InlineKeyboardButton("🧹 Maintenance", callback_data="system_maintenance"),
                InlineKeyboardButton("🔄 Restart", callback_data="system_restart"),
            ],
            [
                InlineKeyboardButton("🆘 Emergency Stop", callback_data="emergency_stop"),
                InlineKeyboardButton("🔙 Back", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_tutorial(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show interactive tutorial"""
        text = (
            "📚 *INTERACTIVE TUTORIAL*\n"
            "═══════════════════════\n\n"
            "🎓 **Learn how to use the system step by step:**\n\n"
            "📝 **Lesson 1: Messages**\n"
            "├ How to create effective messages\n"
            "├ Message formatting tips\n"
            "└ Best practices\n\n"
            "👥 **Lesson 2: Groups**\n"
            "├ Adding groups (single & bulk)\n"
            "├ Group formats & validation\n"
            "└ Group management\n\n"
            "🚫 **Lesson 3: Blacklist**\n"
            "├ Understanding blacklist types\n"
            "├ Automatic management\n"
            "└ Manual interventions\n\n"
            "⚙️ **Lesson 4: Configuration**\n"
            "├ Timing settings\n"
            "├ Performance tuning\n"
            "└ Safety limits\n"
        )

        keyboard = [
            [
                InlineKeyboardButton("📝 Messages Tutorial", callback_data="tutorial_messages"),
                InlineKeyboardButton("👥 Groups Tutorial", callback_data="tutorial_groups"),
            ],
            [
                InlineKeyboardButton("🚫 Blacklist Tutorial", callback_data="tutorial_blacklist"),
                InlineKeyboardButton("⚙️ Config Tutorial", callback_data="tutorial_config"),
            ],
            [
                InlineKeyboardButton("🎯 Quick Start Guide", callback_data="tutorial_quickstart"),
                InlineKeyboardButton("💡 Tips & Tricks", callback_data="tutorial_tips"),
            ],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="dashboard")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_help_center(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show help center with FAQ and troubleshooting"""
        text = (
            "🆘 *HELP CENTER*\n"
            "═══════════════\n\n"
            "🔍 **Quick Solutions:**\n\n"
            "❓ **Frequently Asked Questions**\n"
            "├ Setup and configuration\n"
            "├ Common errors\n"
            "└ Performance issues\n\n"
            "🛠️ **Troubleshooting**\n"
            "├ Connection problems\n"
            "├ Authentication errors\n"
            "└ Blacklist issues\n\n"
            "📖 **Documentation**\n"
            "├ Feature explanations\n"
            "├ Advanced usage\n"
            "└ Best practices\n\n"
            "💬 **Support**\n"
            "├ Contact information\n"
            "├ Bug reporting\n"
            "└ Feature requests\n"
        )

        keyboard = [
            [
                InlineKeyboardButton("❓ FAQ", callback_data="help_faq"),
                InlineKeyboardButton("🛠️ Troubleshooting", callback_data="help_troubleshoot"),
            ],
            [
                InlineKeyboardButton("📖 Documentation", callback_data="help_docs"),
                InlineKeyboardButton("💬 Contact Support", callback_data="help_support"),
            ],
            [
                InlineKeyboardButton("🔧 System Diagnostics", callback_data="help_diagnostics"),
                InlineKeyboardButton("📋 Command Reference", callback_data="help_commands"),
            ],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="dashboard")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_analytics(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show system analytics"""
        text = (
            "📊 *SYSTEM ANALYTICS*\n"
            "═══════════════════\n\n"
            "📈 **Performance Metrics:**\n"
            "├ Messages sent today: 0\n"
            "├ Success rate: 0%\n"
            "├ Average cycle time: 0m\n"
            "└ Groups reached: 0\n\n"
            "🎯 **Broadcasting Stats:**\n"
            "├ Total cycles: 0\n"
            "├ Last cycle: Not started\n"
            "├ Next cycle: Pending\n"
            "└ Uptime: 0h 0m\n\n"
            "🚫 **Error Analysis:**\n"
            "├ SlowMode blocks: 0\n"
            "├ FloodWait events: 0\n"
            "├ Permanent blocks: 0\n"
            "└ Recovery rate: 0%\n\n"
            "*📝 Note: Analytics will populate after first broadcast cycle*"
        )

        keyboard = [
            [
                InlineKeyboardButton("📊 Detailed Stats", callback_data="analytics_detailed"),
                InlineKeyboardButton("📈 Charts", callback_data="analytics_charts"),
            ],
            [
                InlineKeyboardButton("📋 Export Data", callback_data="analytics_export"),
                InlineKeyboardButton("🔄 Refresh", callback_data="analytics"),
            ],
            [InlineKeyboardButton("🔙 Back to Dashboard", callback_data="dashboard")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_emergency_stop(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Show emergency stop confirmation"""
        text = (
            "🆘 *EMERGENCY STOP*\n"
            "═══════════════════\n\n"
            "⚠️ **WARNING: CRITICAL ACTION**\n\n"
            "This will immediately:\n"
            "├ 🛑 Stop all broadcasting\n"
            "├ 🔌 Disconnect userbot\n"
            "├ 💾 Save current state\n"
            "└ 🏁 Shutdown system\n\n"
            "⏱️ **Use emergency stop when:**\n"
            "• System is misbehaving\n"
            "• Too many errors occurring\n"
            "• Need immediate halt\n\n"
            "🔄 **To restart:** Run `python main.py`\n\n"
            "**Are you sure you want to proceed?**"
        )

        keyboard = [
            [
                InlineKeyboardButton("🆘 CONFIRM STOP", callback_data="emergency_confirm"),
                InlineKeyboardButton("❌ Cancel", callback_data="system_control"),
            ],
            [InlineKeyboardButton("🔙 Back to Dashboard", callback_data="dashboard")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def handle_text_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle text input for various operations"""
        user_data = context.user_data

        if "waiting_for" in user_data:
            waiting_for = user_data["waiting_for"]

            if waiting_for == "message_content":
                await self.message_handlers.handle_message_input(update, context)
            elif waiting_for == "group_identifier":
                await self.group_handlers.handle_group_input(update, context)
            elif waiting_for == "groups_bulk":
                await self.group_handlers.handle_bulk_input(update, context)
            elif waiting_for.startswith("config_"):
                await self.config_handlers.handle_config_input(update, context)
            else:
                # Clear waiting state
                user_data.pop("waiting_for", None)
                await update.message.reply_text(
                    "❌ Input tidak dikenali. Gunakan /menu untuk memulai."
                )
        else:
            await update.message.reply_text(
                "❓ Saya tidak mengerti. Gunakan /menu untuk melihat pilihan yang tersedia."
            )
