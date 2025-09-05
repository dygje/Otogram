"""
Message Handlers - Modern message management interface
Enhanced with 2025 UI/UX best practices for optimal user experience
"""

from loguru import logger

from src.core.constants import (
    MAX_MESSAGES_DISPLAY,
    PREVIEW_MESSAGE_LENGTH,
    PREVIEW_MESSAGE_LENGTH_LONG,
    PREVIEW_MESSAGE_LENGTH_SHORT,
    TELEGRAM_MESSAGE_MAX_LENGTH,
)
from src.models.message import MessageCreate
from src.services.message_service import MessageService
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


class MessageHandlers:
    """Modern handlers for message management with enhanced UX"""

    def __init__(self) -> None:
        self.message_service = MessageService()

    async def list_messages(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced message listing with modern design"""
        try:
            messages = await self.message_service.get_all_messages()
            stats = await self.message_service.get_message_count()

            if not messages:
                text = (
                    "📝 **MESSAGE MANAGEMENT CENTER**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "📭 **No Messages Found**\n\n"
                    "🚀 **Get Started:**\n\n"
                    "**Step 1:** Create your first broadcast message\n"
                    "├ Click **'Add Message'** below\n"
                    "├ Write engaging content for your audience\n"
                    "└ Save and activate for broadcasting\n\n"
                    "**Step 2:** Configure target groups\n"
                    "├ Add groups that should receive messages\n"
                    "└ System will handle delivery automatically\n\n"
                    "💡 **Pro Tip:** Start with 1-2 messages to test the system!"
                )
                keyboard = [
                    [InlineKeyboardButton("➕ Create First Message", callback_data="messages_add")],
                    [
                        InlineKeyboardButton(
                            "📚 Message Tutorial", callback_data="tutorial_messages"
                        ),
                        InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    ],
                ]
            else:
                # Calculate utilization rate
                active_rate = (stats["active"] / stats["total"] * 100) if stats["total"] > 0 else 0
                health_indicator = "🟢" if stats["active"] > 0 else "🔴"

                text = (
                    f"📝 **MESSAGE MANAGEMENT CENTER**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"📊 **Collection Overview:**\n"
                    f"├ Status: {health_indicator} {'Ready for Broadcasting' if stats['active'] > 0 else 'Setup Required'}\n"
                    f"├ Total Messages: **{stats['total']}** in collection\n"
                    f"├ Active Messages: **{stats['active']}** ({active_rate:.0f}% utilization)\n"
                    f"├ Inactive Messages: **{stats['inactive']}** (paused)\n"
                    f"└ Broadcasting Ready: {'✅ Yes' if stats['active'] > 0 else '❌ Needs Active Messages'}\n\n"
                    f"📋 **Message Library:**\n"
                )

                keyboard = []
                # Show messages with better formatting
                for i, msg in enumerate(messages[:MAX_MESSAGES_DISPLAY], 1):
                    status_icon = "🟢" if msg.is_active else "⚪"
                    usage_indicator = f"📊 {msg.usage_count}x" if msg.usage_count > 0 else "📊 New"

                    content_preview = (
                        msg.content[:PREVIEW_MESSAGE_LENGTH] + "..."
                        if len(msg.content) > PREVIEW_MESSAGE_LENGTH
                        else msg.content
                    )

                    text += f"**{i}.** {status_icon} *{content_preview}*\n"
                    text += f"   {usage_indicator} • ID: `{msg.id[:8]}...`\n\n"

                    # Add edit buttons in pairs for better layout
                    if i % 2 == 1:  # Start new row for odd numbers
                        keyboard.append(
                            [
                                InlineKeyboardButton(
                                    f"✏️ Edit #{i}", callback_data=f"messages_edit_{msg.id}"
                                ),
                            ]
                        )
                    else:  # Add to existing row for even numbers
                        keyboard[-1].append(
                            InlineKeyboardButton(
                                f"✏️ Edit #{i}", callback_data=f"messages_edit_{msg.id}"
                            )
                        )

                if len(messages) > MAX_MESSAGES_DISPLAY:
                    remaining = len(messages) - MAX_MESSAGES_DISPLAY
                    text += f"   ⋮ *{remaining} more messages in collection...*\n"

                # Add management buttons
                keyboard.extend(
                    [
                        [
                            InlineKeyboardButton("➕ Add Message", callback_data="messages_add"),
                            InlineKeyboardButton("🔄 Bulk Actions", callback_data="messages_bulk"),
                        ],
                        [
                            InlineKeyboardButton(
                                "📊 Usage Analytics", callback_data="messages_analytics"
                            ),
                            InlineKeyboardButton(
                                "⚙️ Advanced Options", callback_data="messages_advanced"
                            ),
                        ],
                    ]
                )

            keyboard.append(
                [
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    InlineKeyboardButton("🔄 Refresh", callback_data="messages_menu"),
                ]
            )
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.message:
                await update.message.reply_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )
            elif update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error listing messages: {e}")
            await self._send_error_message(update, "Failed to load message collection")

    async def add_message_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced add message interface"""
        text = (
            "➕ **CREATE NEW BROADCAST MESSAGE**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📝 **Content Guidelines:**\n\n"
            "✅ **What to Include:**\n"
            "├ Clear, engaging message content\n"
            "├ Call-to-action if needed\n"
            "├ Relevant information for your audience\n"
            "└ Professional formatting\n\n"
            "📏 **Technical Requirements:**\n"
            "├ **Format:** Text only (no media)\n"
            "├ **Length:** Maximum 4,096 characters\n"
            "├ **Encoding:** UTF-8 (supports emojis)\n"
            "└ **Status:** Auto-activated upon creation\n\n"
            "💡 **Pro Tips:**\n"
            "• Keep messages concise and focused\n"
            "• Use formatting (*bold*, _italic_) for emphasis\n"
            "• Test with a small group first\n"
            "• Consider your audience's timezone\n\n"
            "✍️ **Ready to create?**\n"
            "Type your message content and send it in the next message:"
        )

        if context.user_data:
            context.user_data["waiting_for"] = "message_content"

        keyboard = [
            [
                InlineKeyboardButton("❌ Cancel", callback_data="messages_menu"),
                InlineKeyboardButton("📚 Tips & Examples", callback_data="messages_help"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

    async def handle_message_input(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced message input handling with validation"""
        try:
            if update.message and update.message.text:
                content = update.message.text.strip()
            else:
                await update.message.reply_text(
                    "❌ **Invalid Input**\n\n"
                    "Please send a text message with your content.\n"
                    "Media messages are not supported for broadcasting."
                ) if update.message else None
                return

            # Enhanced validation
            if not content:
                await update.message.reply_text(
                    "❌ **Empty Message**\n\n"
                    "Your message content cannot be empty.\n"
                    "Please write your broadcast message and try again."
                ) if update.message else None
                return

            if len(content) > TELEGRAM_MESSAGE_MAX_LENGTH:
                await update.message.reply_text(
                    f"❌ **Message Too Long**\n\n"
                    f"**Current Length:** {len(content):,} characters\n"
                    f"**Maximum Allowed:** {TELEGRAM_MESSAGE_MAX_LENGTH:,} characters\n"
                    f"**Excess:** {len(content) - TELEGRAM_MESSAGE_MAX_LENGTH:,} characters\n\n"
                    f"Please shorten your message and try again."
                ) if update.message else None
                return

            # Show processing message
            processing_msg = (
                await update.message.reply_text(
                    "⏳ **CREATING MESSAGE**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "📝 Processing your message...\n"
                    "⚡ Validating content and format...\n\n"
                    "Please wait a moment..."
                )
                if update.message
                else None
            )

            # Create message
            message_data = MessageCreate(content=content)
            message = await self.message_service.create_message(message_data)

            # Clear waiting state
            if context.user_data:
                context.user_data.pop("waiting_for", None)

            # Calculate message metrics
            word_count = len(content.split())
            line_count = len(content.split("\n"))
            char_utilization = (len(content) / TELEGRAM_MESSAGE_MAX_LENGTH) * 100

            success_text = (
                f"✅ **MESSAGE CREATED SUCCESSFULLY!**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🎉 **Your broadcast message is ready!**\n\n"
                f"📊 **Message Details:**\n"
                f"├ **ID:** `{message.id}`\n"
                f"├ **Length:** {len(content):,} characters ({char_utilization:.1f}% of limit)\n"
                f"├ **Words:** {word_count:,} words\n"
                f"├ **Lines:** {line_count} lines\n"
                f"├ **Created:** {message.created_at.strftime('%d/%m/%Y at %H:%M')}\n"
                f"├ **Status:** 🟢 **Active & Ready**\n"
                f"└ **Usage:** 📊 Ready for broadcasting\n\n"
                f"📝 **Content Preview:**\n"
                f"*{content[:PREVIEW_MESSAGE_LENGTH_SHORT]}{'...' if len(content) > PREVIEW_MESSAGE_LENGTH_SHORT else ''}*\n\n"
                f"🚀 **What's Next:**\n"
                f"• Your message is automatically activated\n"
                f"• Add target groups for broadcasting\n"
                f"• Configure system settings if needed\n"
                f"• Start broadcasting from the dashboard!"
            )

            keyboard = [
                [
                    InlineKeyboardButton("📝 View All Messages", callback_data="messages_menu"),
                    InlineKeyboardButton("➕ Add Another", callback_data="messages_add"),
                ],
                [
                    InlineKeyboardButton("👥 Add Groups", callback_data="groups_dashboard"),
                    InlineKeyboardButton("🚀 Start Broadcasting", callback_data="dashboard"),
                ],
                [
                    InlineKeyboardButton(
                        "✏️ Edit This Message", callback_data=f"messages_edit_{message.id}"
                    ),
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if processing_msg:
                await processing_msg.edit_text(
                    success_text, parse_mode="Markdown", reply_markup=reply_markup
                )
            elif update.message:
                await update.message.reply_text(
                    success_text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error adding message: {e}")
            if context.user_data:
                context.user_data.pop("waiting_for", None)
            await self._send_error_message(update, "Failed to create message")

    async def handle_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str
    ) -> None:
        """Enhanced callback handling with comprehensive routing"""
        if data == "messages_menu":
            await self.list_messages(update, context)
        elif data == "messages_add":
            await self._show_add_message_prompt(update, context)
        elif data == "messages_bulk":
            await self._show_bulk_actions(update, context)
        elif data == "messages_analytics":
            await self._show_message_analytics(update, context)
        elif data == "messages_advanced":
            await self._show_advanced_options(update, context)
        elif data == "messages_help":
            await self._show_message_help(update, context)
        elif data.startswith("messages_edit_"):
            message_id = data.replace("messages_edit_", "")
            await self._show_edit_message(update, message_id)
        elif data.startswith("messages_toggle_"):
            message_id = data.replace("messages_toggle_", "")
            await self._toggle_message_status(update, message_id)
        elif data.startswith("messages_delete_"):
            message_id = data.replace("messages_delete_", "")
            await self._confirm_delete_message(update, message_id)
        elif data.startswith("messages_delete_confirm_"):
            message_id = data.replace("messages_delete_confirm_", "")
            await self._delete_message(update, message_id)
        elif data.startswith("messages_duplicate_"):
            message_id = data.replace("messages_duplicate_", "")
            await self._duplicate_message(update, message_id)

    async def _show_add_message_prompt(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced add message prompt with better guidance"""
        text = (
            "➕ **CREATE NEW BROADCAST MESSAGE**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📝 **Message Composition:**\n\n"
            "**Content Guidelines:**\n"
            "├ Write clear, engaging content\n"
            "├ Use proper formatting for readability\n"
            "├ Include relevant call-to-actions\n"
            "└ Keep your audience in mind\n\n"
            "**Technical Limits:**\n"
            "├ Maximum: 4,096 characters\n"
            "├ Format: Text only (no media)\n"
            "├ Encoding: Full Unicode support\n"
            "└ Status: Auto-activated when saved\n\n"
            "✍️ **Type your message content in the next message:**"
        )

        keyboard = [
            [
                InlineKeyboardButton("❌ Cancel", callback_data="messages_menu"),
                InlineKeyboardButton("💡 Writing Tips", callback_data="messages_help"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

        if context.user_data:
            context.user_data["waiting_for"] = "message_content"

    async def _show_edit_message(self, update: Update, message_id: str) -> None:
        """Enhanced message editing interface"""
        try:
            message = await self.message_service.get_message_by_id(message_id)

            if not message:
                if update.callback_query:
                    await update.callback_query.edit_message_text(
                        "❌ **Message Not Found**\n\n"
                        "The requested message could not be located.\n"
                        "It may have been deleted or the ID is invalid."
                    )
                return

            # Calculate message metrics
            word_count = len(message.content.split())
            line_count = len(message.content.split("\n"))
            char_utilization = (len(message.content) / TELEGRAM_MESSAGE_MAX_LENGTH) * 100
            status_text = "🟢 **Active**" if message.is_active else "⚪ **Inactive**"

            content_preview = (
                message.content[:PREVIEW_MESSAGE_LENGTH_LONG] + "..."
                if len(message.content) > PREVIEW_MESSAGE_LENGTH_LONG
                else message.content
            )

            text = (
                f"✏️ **MESSAGE EDITOR**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📊 **Message Information:**\n"
                f"├ **ID:** `{message.id}`\n"
                f"├ **Status:** {status_text}\n"
                f"├ **Length:** {len(message.content):,} chars ({char_utilization:.1f}% of limit)\n"
                f"├ **Words:** {word_count:,} words\n"
                f"├ **Lines:** {line_count} lines\n"
                f"├ **Usage Count:** 📊 {message.usage_count} broadcasts\n"
                f"├ **Created:** {message.created_at.strftime('%d/%m/%Y at %H:%M')}\n"
                f"└ **Last Modified:** {message.updated_at.strftime('%d/%m/%Y at %H:%M') if message.updated_at else 'Never'}\n\n"
                f"📝 **Content Preview:**\n"
                f"*{content_preview}*\n\n"
                f"🛠️ **Available Actions:**"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "⚪ Deactivate" if message.is_active else "🟢 Activate",
                        callback_data=f"messages_toggle_{message_id}",
                    ),
                    InlineKeyboardButton(
                        "📋 Duplicate", callback_data=f"messages_duplicate_{message_id}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "📊 View Analytics", callback_data=f"messages_analytics_{message_id}"
                    ),
                    InlineKeyboardButton(
                        "📝 View Full Content", callback_data=f"messages_view_{message_id}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🗑️ Delete Message", callback_data=f"messages_delete_{message_id}"
                    ),
                    InlineKeyboardButton(
                        "🔄 Refresh Info", callback_data=f"messages_edit_{message_id}"
                    ),
                ],
                [
                    InlineKeyboardButton("🔙 Back to List", callback_data="messages_menu"),
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error showing edit message: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ **Error Loading Message**\n\n"
                    "Unable to load message details.\n"
                    "Please try again or check if the message still exists."
                )

    async def _show_bulk_actions(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced bulk actions interface"""
        try:
            stats = await self.message_service.get_message_count()

            text = (
                f"🔄 **BULK MESSAGE ACTIONS**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📊 **Current Collection:**\n"
                f"├ Total Messages: {stats['total']}\n"
                f"├ Active Messages: {stats['active']}\n"
                f"├ Inactive Messages: {stats['inactive']}\n"
                f"└ Ready for Actions: {'✅ Yes' if stats['total'] > 0 else '❌ No Messages'}\n\n"
                f"🛠️ **Available Bulk Operations:**\n\n"
                f"**Status Management:**\n"
                f"├ Activate all messages for broadcasting\n"
                f"├ Deactivate all messages (pause)\n"
                f"└ Toggle status of selected messages\n\n"
                f"**Collection Management:**\n"
                f"├ Export message collection\n"
                f"├ Import messages from file\n"
                f"├ Clear usage statistics\n"
                f"└ Optimize message storage\n\n"
                f"**Maintenance Operations:**\n"
                f"├ Remove duplicate messages\n"
                f"├ Clean up unused messages\n"
                f"└ Validate all message content\n\n"
                f"⚠️ **Note:** Bulk operations affect multiple messages at once."
            )

            keyboard = [
                [
                    InlineKeyboardButton("🟢 Activate All", callback_data="messages_bulk_activate"),
                    InlineKeyboardButton(
                        "⚪ Deactivate All", callback_data="messages_bulk_deactivate"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "📊 Clear Statistics", callback_data="messages_bulk_clear_stats"
                    ),
                    InlineKeyboardButton(
                        "🧹 Remove Duplicates", callback_data="messages_bulk_dedupe"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "📤 Export Collection", callback_data="messages_bulk_export"
                    ),
                    InlineKeyboardButton(
                        "📥 Import Messages", callback_data="messages_bulk_import"
                    ),
                ],
                [
                    InlineKeyboardButton("🔙 Back to Messages", callback_data="messages_menu"),
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error showing bulk actions: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ Error loading bulk actions interface"
                )

    async def _show_message_analytics(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced message analytics dashboard"""
        try:
            messages = await self.message_service.get_all_messages()
            stats = await self.message_service.get_message_count()

            if not messages:
                text = (
                    "📊 **MESSAGE ANALYTICS**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "📭 **No Data Available**\n\n"
                    "Create some messages first to see analytics data.\n"
                    "Analytics will show usage patterns, performance metrics, and optimization suggestions."
                )
                keyboard = [
                    [InlineKeyboardButton("➕ Create Messages", callback_data="messages_add")],
                    [InlineKeyboardButton("🔙 Back", callback_data="messages_menu")],
                ]
            else:
                # Calculate analytics
                total_usage = sum(msg.usage_count for msg in messages)
                avg_usage = total_usage / len(messages) if messages else 0
                most_used = max(messages, key=lambda x: x.usage_count) if messages else None
                active_rate = (stats["active"] / stats["total"] * 100) if stats["total"] > 0 else 0

                # Content analysis
                total_chars = sum(len(msg.content) for msg in messages)
                avg_length = total_chars / len(messages) if messages else 0

                text = (
                    f"📊 **MESSAGE ANALYTICS DASHBOARD**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"📈 **Performance Metrics:**\n"
                    f"├ Collection Size: {len(messages)} messages\n"
                    f"├ Total Broadcasts: {total_usage:,} sends\n"
                    f"├ Average Usage: {avg_usage:.1f} sends per message\n"
                    f"├ Activation Rate: {active_rate:.1f}% active\n"
                    f"└ Efficiency Score: {min(100, active_rate + (avg_usage * 10)):.0f}/100\n\n"
                    f"📝 **Content Analysis:**\n"
                    f"├ Average Length: {avg_length:.0f} characters\n"
                    f"├ Total Characters: {total_chars:,} chars\n"
                    f"├ Content Variety: {'High' if len(set(msg.content[:50] for msg in messages)) > len(messages) * 0.8 else 'Medium'}\n"
                    f"└ Optimization Level: {'Good' if avg_length < 1000 else 'Needs Review'}\n\n"
                )

                if most_used and most_used.usage_count > 0:
                    text += (
                        f"🏆 **Top Performer:**\n"
                        f"├ Message: *{most_used.content[:50]}...*\n"
                        f"├ Usage: {most_used.usage_count} broadcasts\n"
                        f"└ Status: {'🟢 Active' if most_used.is_active else '⚪ Inactive'}\n\n"
                    )

                text += (
                    f"💡 **Recommendations:**\n"
                    f"• {'Create more active messages' if stats['active'] < 3 else 'Good message variety'}\n"
                    f"• {'Review inactive messages' if stats['inactive'] > stats['active'] else 'Good activation rate'}\n"
                    f"• {'Consider shorter messages' if avg_length > 1500 else 'Good message length'}"
                )

                keyboard = [
                    [
                        InlineKeyboardButton(
                            "📈 Detailed Report", callback_data="messages_analytics_detailed"
                        ),
                        InlineKeyboardButton("🔄 Refresh Data", callback_data="messages_analytics"),
                    ],
                    [
                        InlineKeyboardButton(
                            "📊 Export Report", callback_data="messages_analytics_export"
                        ),
                        InlineKeyboardButton(
                            "💡 Optimization Tips", callback_data="messages_optimization"
                        ),
                    ],
                    [
                        InlineKeyboardButton("🔙 Back to Messages", callback_data="messages_menu"),
                        InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    ],
                ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error showing message analytics: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Error loading analytics data")

    async def _show_message_help(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced message help and writing tips"""
        text = (
            "💡 **MESSAGE WRITING GUIDE**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "✍️ **Effective Message Writing:**\n\n"
            "**🎯 Content Strategy:**\n"
            "├ Start with a compelling hook\n"
            "├ Keep your main message clear and concise\n"
            "├ Include a specific call-to-action\n"
            "└ End with value or benefit statement\n\n"
            "**📝 Formatting Best Practices:**\n"
            "├ Use **bold** for important points\n"
            "├ Use *italics* for emphasis\n"
            "├ Use `code` for technical terms\n"
            "├ Break text into readable paragraphs\n"
            "└ Use emojis sparingly for engagement\n\n"
            "**📏 Length Guidelines:**\n"
            "├ **Short Messages (< 500 chars):** Quick announcements\n"
            "├ **Medium Messages (500-1500 chars):** Detailed updates\n"
            "├ **Long Messages (1500+ chars):** Comprehensive content\n"
            "└ **Maximum Limit:** 4,096 characters\n\n"
            "**⚡ Engagement Tips:**\n"
            "├ Ask questions to encourage interaction\n"
            "├ Use urgency words when appropriate\n"
            "├ Personalize content for your audience\n"
            "├ Include relevant hashtags or keywords\n"
            "└ Test different message styles\n\n"
            "**🚫 What to Avoid:**\n"
            "├ Excessive capitalization (LOOKS LIKE SHOUTING)\n"
            "├ Too many emojis in one message\n"
            "├ Unclear or vague calls-to-action\n"
            "├ Grammar and spelling errors\n"
            "└ Overly promotional language\n\n"
            "**📊 Performance Optimization:**\n"
            "├ Monitor which messages get the best response\n"
            "├ A/B test different versions\n"
            "├ Adapt content based on audience feedback\n"
            "└ Update messages based on analytics\n\n"
            "**💡 Pro Tips:**\n"
            "• Write like you're talking to a friend\n"
            "• Use active voice instead of passive\n"
            "• Focus on benefits, not just features\n"
            "• Keep sentences short and punchy\n"
            "• End with a clear next step"
        )

        keyboard = [
            [
                InlineKeyboardButton("✍️ Start Writing", callback_data="messages_add"),
                InlineKeyboardButton("📊 See Examples", callback_data="messages_examples"),
            ],
            [
                InlineKeyboardButton("🔙 Back to Messages", callback_data="messages_menu"),
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _confirm_delete_message(self, update: Update, message_id: str) -> None:
        """Enhanced delete confirmation with safety checks"""
        try:
            message = await self.message_service.get_message_by_id(message_id)

            if not message:
                if update.callback_query:
                    await update.callback_query.edit_message_text(
                        "❌ **Message Not Found**\n\n"
                        "The message you're trying to delete could not be found.\n"
                        "It may have already been deleted."
                    )
                return

            # Safety information
            preview = (
                message.content[:100] + "..." if len(message.content) > 100 else message.content
            )
            usage_warning = (
                f"⚠️ This message has been used {message.usage_count} times"
                if message.usage_count > 0
                else ""
            )

            text = (
                f"🗑️ **CONFIRM MESSAGE DELETION**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⚠️ **Permanent Action Warning**\n\n"
                f"**Message to Delete:**\n"
                f"├ ID: `{message.id}`\n"
                f"├ Status: {'🟢 Active' if message.is_active else '⚪ Inactive'}\n"
                f"├ Usage: 📊 {message.usage_count} broadcasts\n"
                f"├ Created: {message.created_at.strftime('%d/%m/%Y')}\n"
                f"└ Length: {len(message.content):,} characters\n\n"
                f"📝 **Preview:**\n"
                f"*{preview}*\n\n"
                f"{usage_warning}\n\n"
                if usage_warning
                else ""
                "🚨 **This action cannot be undone!**\n\n"
                "**Consequences:**\n"
                "├ Message will be permanently removed\n"
                "├ All usage statistics will be lost\n"
                "├ Cannot be recovered after deletion\n"
                "└ Broadcasting system will be updated\n\n"
                "**Are you absolutely sure you want to proceed?**"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🗑️ DELETE PERMANENTLY",
                        callback_data=f"messages_delete_confirm_{message_id}",
                    ),
                ],
                [
                    InlineKeyboardButton("❌ Cancel", callback_data=f"messages_edit_{message_id}"),
                    InlineKeyboardButton("🔙 Back to List", callback_data="messages_menu"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error confirming delete message: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ Error loading deletion confirmation"
                )

    async def _delete_message(self, update: Update, message_id: str) -> None:
        """Enhanced message deletion with confirmation"""
        try:
            success = await self.message_service.delete_message(message_id)

            if success:
                text = (
                    "✅ **MESSAGE DELETED SUCCESSFULLY**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "🗑️ **Deletion Complete**\n\n"
                    "**What Happened:**\n"
                    "├ Message permanently removed from collection\n"
                    "├ All associated statistics cleared\n"
                    "├ Broadcasting system updated\n"
                    "└ Storage space optimized\n\n"
                    "**Next Steps:**\n"
                    "• Review your remaining messages\n"
                    "• Consider creating replacement content\n"
                    "• Update your broadcasting strategy\n\n"
                    "💡 **Tip:** Maintain a diverse message collection for better engagement!"
                )
            else:
                text = (
                    "❌ **DELETION FAILED**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "⚠️ **Unable to Delete Message**\n\n"
                    "**Possible Causes:**\n"
                    "├ Message no longer exists\n"
                    "├ Database connection issue\n"
                    "├ System protection mechanism\n"
                    "└ Temporary server error\n\n"
                    "**Try Again:**\n"
                    "• Refresh the message list\n"
                    "• Check if message still exists\n"
                    "• Contact support if issue persists"
                )

            keyboard = [
                [
                    InlineKeyboardButton("📝 View Messages", callback_data="messages_menu"),
                    InlineKeyboardButton("➕ Add New Message", callback_data="messages_add"),
                ],
                [InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error deleting message: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ **System Error**\n\n"
                    "Failed to delete message due to system error.\n"
                    "Please try again or contact support."
                )

    async def _toggle_message_status(self, update: Update, message_id: str) -> None:
        """Enhanced message status toggle with feedback"""
        try:
            updated_message = await self.message_service.toggle_message_status(message_id)

            if updated_message:
                status_action = "activated" if updated_message.is_active else "deactivated"
                status_icon = "🟢" if updated_message.is_active else "⚪"

                text = (
                    f"✅ **MESSAGE {status_action.upper()}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"{status_icon} **Status Update Complete**\n\n"
                    f"**Message Details:**\n"
                    f"├ ID: `{updated_message.id}`\n"
                    f"├ New Status: {status_icon} **{status_action.title()}**\n"
                    f"├ Usage Count: 📊 {updated_message.usage_count} broadcasts\n"
                    f"└ Broadcasting: {'✅ Enabled' if updated_message.is_active else '⚪ Paused'}\n\n"
                    f"**Impact:**\n"
                    f"{'• Message is now available for broadcasting' if updated_message.is_active else '• Message will not be used in broadcasts'}\n"
                    f"{'• Will be included in rotation cycles' if updated_message.is_active else '• Excluded from rotation cycles'}\n"
                    f"{'• Contributes to automation goals' if updated_message.is_active else '• Temporarily paused from system'}\n\n"
                    f"💡 **Tip:** {'Deactivate messages temporarily if you want to pause specific content' if updated_message.is_active else 'Reactivate when ready to resume using this message'}"
                )
            else:
                text = (
                    "❌ **STATUS UPDATE FAILED**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "⚠️ **Unable to Update Message**\n\n"
                    "**Possible Issues:**\n"
                    "├ Message no longer exists\n"
                    "├ Database synchronization error\n"
                    "├ Temporary system issue\n"
                    "└ Insufficient permissions\n\n"
                    "**Next Steps:**\n"
                    "• Refresh the message list\n"
                    "• Try the operation again\n"
                    "• Check system status\n"
                    "• Contact support if issue persists"
                )

            keyboard = [
                [
                    InlineKeyboardButton("🔄 Refresh List", callback_data="messages_menu"),
                    InlineKeyboardButton(
                        "✏️ Edit Message", callback_data=f"messages_edit_{message_id}"
                    ),
                ],
                [InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error toggling message status: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ **System Error**\n\n"
                    "Failed to update message status.\n"
                    "Please try again later."
                )

    async def _duplicate_message(self, update: Update, message_id: str) -> None:
        """Create a duplicate of an existing message"""
        try:
            original_message = await self.message_service.get_message_by_id(message_id)

            if not original_message:
                if update.callback_query:
                    await update.callback_query.edit_message_text("❌ Original message not found")
                return

            # Create duplicate with modified content
            duplicate_content = f"{original_message.content}\n\n[Duplicate - Edit as needed]"
            duplicate_data = MessageCreate(content=duplicate_content)
            new_message = await self.message_service.create_message(duplicate_data)

            text = (
                f"📋 **MESSAGE DUPLICATED SUCCESSFULLY**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"✅ **Duplicate Created**\n\n"
                f"**Original Message:**\n"
                f"├ ID: `{original_message.id}`\n"
                f"├ Usage: {original_message.usage_count} broadcasts\n"
                f"└ Status: {'🟢 Active' if original_message.is_active else '⚪ Inactive'}\n\n"
                f"**New Duplicate:**\n"
                f"├ ID: `{new_message.id}`\n"
                f"├ Status: 🟢 **Active & Ready**\n"
                f"├ Usage: 📊 0 broadcasts (new)\n"
                f"└ Note: Contains '[Duplicate - Edit as needed]' marker\n\n"
                f"💡 **Next Steps:**\n"
                f"• Edit the duplicate to customize content\n"
                f"• Remove the duplicate marker text\n"
                f"• Use both messages for A/B testing"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "✏️ Edit Duplicate", callback_data=f"messages_edit_{new_message.id}"
                    ),
                    InlineKeyboardButton("📝 View All", callback_data="messages_menu"),
                ],
                [InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error duplicating message: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Failed to duplicate message")

    async def _show_advanced_options(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Show advanced message management options"""
        text = (
            "⚙️ **ADVANCED MESSAGE OPTIONS**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔧 **Advanced Features:**\n\n"
            "**Content Management:**\n"
            "├ Message templates and presets\n"
            "├ Content validation and optimization\n"
            "├ Automatic content suggestions\n"
            "└ Message performance prediction\n\n"
            "**Scheduling & Automation:**\n"
            "├ Time-based message activation\n"
            "├ Conditional message rules\n"
            "├ Automated content rotation\n"
            "└ Smart delivery optimization\n\n"
            "**Analytics & Insights:**\n"
            "├ Deep performance analytics\n"
            "├ A/B testing framework\n"
            "├ Audience response tracking\n"
            "└ Content effectiveness scoring\n\n"
            "**Integration Features:**\n"
            "├ External content sources\n"
            "├ API-based message updates\n"
            "├ Webhook notifications\n"
            "└ Third-party tool integration\n\n"
            "💡 **Note:** Some features may require additional setup or premium access."
        )

        keyboard = [
            [
                InlineKeyboardButton("📋 Message Templates", callback_data="messages_templates"),
                InlineKeyboardButton(
                    "🤖 Auto Optimization", callback_data="messages_auto_optimize"
                ),
            ],
            [
                InlineKeyboardButton("📊 Deep Analytics", callback_data="messages_deep_analytics"),
                InlineKeyboardButton("🧪 A/B Testing", callback_data="messages_ab_testing"),
            ],
            [
                InlineKeyboardButton("⏰ Scheduling", callback_data="messages_scheduling"),
                InlineKeyboardButton("🔗 Integrations", callback_data="messages_integrations"),
            ],
            [
                InlineKeyboardButton("🔙 Back to Messages", callback_data="messages_menu"),
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _send_error_message(self, update: Update, error_text: str) -> None:
        """Enhanced error message handling"""
        error_msg = (
            f"❌ **MESSAGE SYSTEM ERROR**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"**Issue:** {error_text}\n\n"
            f"🔧 **Troubleshooting Steps:**\n"
            f"├ Refresh the interface with `/menu`\n"
            f"├ Check your internet connection\n"
            f"├ Verify system status with `/status`\n"
            f"├ Try the operation again\n"
            f"└ Contact support if issue persists\n\n"
            f"💡 **Quick Actions:**"
        )

        keyboard = [
            [
                InlineKeyboardButton("🔄 Refresh Messages", callback_data="messages_menu"),
                InlineKeyboardButton("📊 System Status", callback_data="refresh_status"),
            ],
            [
                InlineKeyboardButton("💬 Get Help", callback_data="help_center"),
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
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
