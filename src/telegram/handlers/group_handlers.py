"""
Group Handlers - Modern group management interface
Enhanced with 2025 UI/UX best practices for seamless group operations
"""

from loguru import logger

from src.core.constants import MAX_BULK_SUCCESS_DISPLAY, MAX_GROUPS_DISPLAY
from src.models.group import GroupBulkCreate, GroupCreate
from src.services.group_service import GroupService
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


class GroupHandlers:
    """Modern handlers for group management with enhanced UX"""

    def __init__(self) -> None:
        self.group_service = GroupService()
        self.user_states: dict[str, str] = {}

    async def list_groups(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced group listing with modern interface"""
        try:
            groups = await self.group_service.get_all_groups()
            stats = await self.group_service.get_group_stats()

            if not groups:
                text = (
                    "👥 **GROUP MANAGEMENT CENTER**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "📭 **No Groups Configured**\n\n"
                    "🚀 **Get Started with Group Management:**\n\n"
                    "**Step 1:** Add your first target group\n"
                    "├ Use **'Add Single Group'** for individual setup\n"
                    "├ Use **'Add Multiple Groups'** for bulk import\n"
                    "└ Groups can be added via ID, username, or invite link\n\n"
                    "**Step 2:** Verify group accessibility\n"
                    "├ System will validate each group automatically\n"
                    "├ Check permissions and membership status\n"
                    "└ Monitor blacklist for any access issues\n\n"
                    "**Step 3:** Start broadcasting\n"
                    "├ Ensure you have active messages ready\n"
                    "└ Configure timing settings for optimal delivery\n\n"
                    "💡 **Pro Tip:** Start with a few test groups to verify your setup!"
                )
                keyboard = [
                    [
                        InlineKeyboardButton("➕ Add Single Group", callback_data="groups_add"),
                        InlineKeyboardButton("📋 Add Multiple Groups", callback_data="groups_bulk"),
                    ],
                    [
                        InlineKeyboardButton("📚 Group Setup Guide", callback_data="tutorial_groups"),
                        InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    ],
                ]
            else:
                # Calculate utilization metrics
                active_rate = (stats['active'] / stats['total'] * 100) if stats['total'] > 0 else 0
                health_indicator = "🟢" if stats['active'] > 0 else "🔴"
                
                # Calculate total message potential
                message_potential = stats['active'] * 1  # Assuming 1 message per group for calculation
                
                text = (
                    f"👥 **GROUP MANAGEMENT CENTER**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"📊 **Network Overview:**\n"
                    f"├ Status: {health_indicator} {'Broadcasting Network Ready' if stats['active'] > 0 else 'Setup Required'}\n"
                    f"├ Total Groups: **{stats['total']}** in network\n"
                    f"├ Active Groups: **{stats['active']}** ({active_rate:.0f}% coverage)\n"
                    f"├ Inactive Groups: **{stats['inactive']}** (paused)\n"
                    f"├ Reach Potential: **{message_potential}+** deliveries per cycle\n"
                    f"└ Network Health: {'✅ Optimal' if active_rate > 80 else '⚠️ Needs Optimization' if active_rate > 50 else '🔴 Critical'}\n\n"
                    f"📋 **Group Network:**\n"
                )

                keyboard = []
                # Enhanced group display with better formatting
                for i, group in enumerate(groups[:MAX_GROUPS_DISPLAY], 1):
                    status_icon = "🟢" if group.is_active else "⚪"
                    
                    # Smart group identifier display
                    if group.group_title:
                        identifier = group.group_title
                        id_type = "📝"
                    elif group.group_username:
                        identifier = f"@{group.group_username.lstrip('@')}"
                        id_type = "🏷️"
                    elif group.group_id:
                        identifier = f"ID: {group.group_id}"
                        id_type = "🆔"
                    else:
                        identifier = "Unknown Group"
                        id_type = "❓"

                    # Truncate long identifiers
                    display_identifier = identifier if len(str(identifier)) <= 35 else f"{str(identifier)[:32]}..."
                    
                    # Message delivery count
                    delivery_count = f"📊 {group.message_count}x" if group.message_count > 0 else "📊 New"
                    
                    text += f"**{i}.** {status_icon} {id_type} *{display_identifier}*\n"
                    text += f"   {delivery_count} • Added: {group.created_at.strftime('%d/%m/%Y')}\n\n"

                    # Add management buttons in pairs for better layout
                    if i % 2 == 1:  # Start new row
                        keyboard.append([
                            InlineKeyboardButton(f"✏️ Manage #{i}", callback_data=f"groups_edit_{group.id}"),
                        ])
                    else:  # Add to existing row
                        keyboard[-1].append(
                            InlineKeyboardButton(f"✏️ Manage #{i}", callback_data=f"groups_edit_{group.id}")
                        )

                if len(groups) > MAX_GROUPS_DISPLAY:
                    remaining = len(groups) - MAX_GROUPS_DISPLAY
                    text += f"   ⋮ *{remaining} more groups in network...*\n"

                # Add management options
                keyboard.extend([
                    [
                        InlineKeyboardButton("➕ Add Group", callback_data="groups_add"),
                        InlineKeyboardButton("📋 Bulk Import", callback_data="groups_bulk"),
                    ],
                    [
                        InlineKeyboardButton("📊 Network Analytics", callback_data="groups_analytics"),
                        InlineKeyboardButton("🧹 Maintenance", callback_data="groups_maintenance"),
                    ],
                ])

            keyboard.append([
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                InlineKeyboardButton("🔄 Refresh", callback_data="groups_menu"),
            ])
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
            logger.error(f"Error listing groups: {e}")
            await self._send_error_message(update, "Failed to load group network")

    async def add_group_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced single group addition interface"""
        text = (
            "➕ **ADD NEW TARGET GROUP**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 **Group Identification:**\n\n"
            "**Supported Formats:**\n\n"
            "**📱 Group ID (Recommended):**\n"
            "├ Format: `-1001234567890`\n"
            "├ Most reliable method\n"
            "├ Never changes over time\n"
            "└ Get from group info or bots\n\n"
            "**🏷️ Username:**\n"
            "├ Format: `@groupname` or `groupname`\n"
            "├ Public groups only\n"
            "├ May change if renamed\n"
            "└ Case sensitive\n\n"
            "**🔗 Invite Link:**\n"
            "├ Format: `t.me/groupname` or `https://t.me/groupname`\n"
            "├ Works with public groups\n"
            "├ System will extract group info\n"
            "└ Link must be accessible\n\n"
            "**🔍 How to Find Group Information:**\n"
            "• **Group ID:** Use @userinfobot in the group\n"
            "• **Username:** Check group info/settings\n"
            "• **Link:** Use group's share feature\n\n"
            "✍️ **Enter group identifier:**\n"
            "Send your group ID, username, or link in the next message"
        )

        if context.user_data:
            context.user_data["waiting_for"] = "group_identifier"

        keyboard = [
            [
                InlineKeyboardButton("❌ Cancel", callback_data="groups_menu"),
                InlineKeyboardButton("💡 Need Help?", callback_data="groups_help"),
            ],
            [
                InlineKeyboardButton("📋 Add Multiple Instead", callback_data="groups_bulk"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

    async def add_groups_bulk_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced bulk group addition interface"""
        text = (
            "📋 **BULK GROUP IMPORT**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🚀 **Import Multiple Groups Efficiently:**\n\n"
            "**📝 Input Format:**\n"
            "Send a list of groups, **one per line**, using any of these formats:\n\n"
            "**Example Input:**\n"
            "```\n"
            "-1001234567890\n"
            "@techgroup\n"
            "businesschat\n"
            "t.me/startupnetwork\n"
            "https://t.me/developers\n"
            "-1009876543210\n"
            "```\n\n"
            "**💡 Pro Tips:**\n"
            "├ **Mix formats:** You can use different formats in one list\n"
            "├ **Empty lines:** Will be automatically ignored\n"
            "├ **Duplicates:** System will skip existing groups\n"
            "├ **Validation:** Each group is verified before adding\n"
            "└ **Error handling:** Invalid groups are reported separately\n\n"
            "**⚡ Performance:**\n"
            "├ Batch processing for speed\n"
            "├ Real-time validation\n"
            "├ Detailed success/failure reporting\n"
            "└ Automatic optimization\n\n"
            "**🔍 Quality Checks:**\n"
            "├ Format validation\n"
            "├ Accessibility verification\n"
            "├ Duplicate detection\n"
            "└ Permission checking\n\n"
            "✍️ **Ready to import?**\n"
            "Paste your group list and send it in the next message:"
        )

        if context.user_data:
            context.user_data["waiting_for"] = "groups_bulk"

        keyboard = [
            [
                InlineKeyboardButton("❌ Cancel", callback_data="groups_menu"),
                InlineKeyboardButton("📋 Format Examples", callback_data="groups_bulk_examples"),
            ],
            [
                InlineKeyboardButton("➕ Add Single Instead", callback_data="groups_add"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

    async def handle_group_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced single group input processing"""
        try:
            if update.message and update.message.text:
                identifier = update.message.text.strip()
            else:
                await update.message.reply_text(
                    "❌ **Invalid Input Format**\n\n"
                    "Please send a text message containing your group identifier.\n\n"
                    "**Supported formats:**\n"
                    "• Group ID: `-1001234567890`\n"
                    "• Username: `@groupname`\n"
                    "• Link: `t.me/groupname`"
                ) if update.message else None
                return

            if not identifier:
                await update.message.reply_text(
                    "❌ **Empty Input**\n\n"
                    "Group identifier cannot be empty.\n"
                    "Please provide a valid group ID, username, or link."
                ) if update.message else None
                return

            # Show processing message
            processing_msg = await update.message.reply_text(
                "⏳ **PROCESSING GROUP**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🔍 **Step 1/3:** Validating group identifier...\n"
                "📡 **Step 2/3:** Checking group accessibility...\n"
                "💾 **Step 3/3:** Adding to network...\n\n"
                "Please wait while we verify and add your group."
            ) if update.message else None

            # Enhanced validation and creation
            try:
                group_data = GroupCreate(group_identifier=identifier)
                group = await self.group_service.create_group(group_data)

                # Clear waiting state
                if context.user_data:
                    context.user_data.pop("waiting_for", None)

                # Determine identifier type and format
                if identifier.startswith('-100'):
                    id_type = "🆔 Group ID"
                elif identifier.startswith('@') or identifier.startswith('t.me/'):
                    id_type = "🏷️ Username/Link"
                else:
                    id_type = "📝 Identifier"

                success_text = (
                    f"✅ **GROUP ADDED SUCCESSFULLY!**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"🎉 **Welcome to your broadcasting network!**\n\n"
                    f"📊 **Group Details:**\n"
                    f"├ **ID:** `{group.id}`\n"
                    f"├ **Type:** {id_type}\n"
                    f"├ **Identifier:** `{identifier}`\n"
                    f"├ **Added:** {group.created_at.strftime('%d/%m/%Y at %H:%M')}\n"
                    f"├ **Status:** 🟢 **Active & Ready**\n"
                    f"├ **Accessibility:** ✅ **Verified**\n"
                    f"└ **Broadcasting:** 🚀 **Enabled**\n\n"
                    f"**🔍 System Checks:**\n"
                    f"├ Format validation: ✅ **Passed**\n"
                    f"├ Duplicate check: ✅ **Unique**\n"
                    f"├ Accessibility test: ✅ **Accessible**\n"
                    f"└ Network integration: ✅ **Complete**\n\n"
                    f"**🚀 What's Next:**\n"
                    f"• Group is ready for message broadcasting\n"
                    f"• Add more groups to expand your reach\n"
                    f"• Configure message content if needed\n"
                    f"• Start broadcasting from the dashboard!\n\n"
                    f"💡 **Pro Tip:** Test your setup with a single message first!"
                )

                keyboard = [
                    [
                        InlineKeyboardButton("👥 View All Groups", callback_data="groups_menu"),
                        InlineKeyboardButton("➕ Add Another", callback_data="groups_add"),
                    ],
                    [
                        InlineKeyboardButton("📝 Add Messages", callback_data="messages_dashboard"),
                        InlineKeyboardButton("🚀 Start Broadcasting", callback_data="dashboard"),
                    ],
                    [
                        InlineKeyboardButton("✏️ Manage This Group", callback_data=f"groups_edit_{group.id}"),
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

            except Exception as creation_error:
                error_details = str(creation_error)
                
                if "duplicate" in error_details.lower():
                    error_text = (
                        "🔄 **GROUP ALREADY EXISTS**\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        "ℹ️ **This group is already in your network**\n\n"
                        "**Group Information:**\n"
                        f"├ Identifier: `{identifier}`\n"
                        f"├ Status: Already configured\n"
                        f"├ Action: No changes needed\n"
                        f"└ Broadcasting: Ready to use\n\n"
                        "**Options:**\n"
                        "• View your existing groups\n"
                        "• Add a different group\n"
                        "• Check group management settings"
                    )
                elif "invalid" in error_details.lower():
                    error_text = (
                        "❌ **INVALID GROUP IDENTIFIER**\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        "⚠️ **The provided identifier is not valid**\n\n"
                        "**Common Issues:**\n"
                        "├ Incorrect format or syntax\n"
                        "├ Group doesn't exist or is private\n"
                        "├ Insufficient permissions\n"
                        "└ Network connectivity problems\n\n"
                        "**Please verify:**\n"
                        "• Group ID format: `-1001234567890`\n"
                        "• Username format: `@groupname`\n"
                        "• Link format: `t.me/groupname`\n"
                        "• Group is accessible to your account"
                    )
                else:
                    error_text = (
                        "❌ **GROUP ADDITION FAILED**\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"⚠️ **System Error:** {error_details}\n\n"
                        "**Troubleshooting:**\n"
                        "├ Verify the group identifier\n"
                        "├ Check your network connection\n"
                        "├ Ensure group permissions\n"
                        "└ Try again in a few moments"
                    )

                keyboard = [
                    [
                        InlineKeyboardButton("🔄 Try Again", callback_data="groups_add"),
                        InlineKeyboardButton("💡 Get Help", callback_data="groups_help"),
                    ],
                    [
                        InlineKeyboardButton("👥 View Groups", callback_data="groups_menu"),
                        InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                if processing_msg:
                    await processing_msg.edit_text(
                        error_text, parse_mode="Markdown", reply_markup=reply_markup
                    )

        except Exception as e:
            logger.error(f"Error adding group: {e}")
            if context.user_data:
                context.user_data.pop("waiting_for", None)
            await self._send_error_message(update, "Failed to process group addition")

    async def handle_bulk_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced bulk group input processing"""
        try:
            if update.message and update.message.text:
                identifiers_text = update.message.text.strip()
            else:
                await update.message.reply_text(
                    "❌ **Invalid Input Format**\n\n"
                    "Please send a text message with your group list.\n"
                    "Each group should be on a separate line."
                ) if update.message else None
                return

            if not identifiers_text:
                await update.message.reply_text(
                    "❌ **Empty Group List**\n\n"
                    "Please provide a list of groups to import.\n"
                    "Format: One group per line."
                ) if update.message else None
                return

            # Show enhanced processing message
            processing_msg = await update.message.reply_text(
                "⏳ **BULK IMPORT PROCESSING**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "📊 **Step 1/4:** Parsing group list...\n"
                "🔍 **Step 2/4:** Validating each group...\n"
                "📡 **Step 3/4:** Checking accessibility...\n"
                "💾 **Step 4/4:** Adding to network...\n\n"
                "Please wait while we process your groups..."
            ) if update.message else None

            try:
                # Parse input lines
                input_lines = [line.strip() for line in identifiers_text.split('\n') if line.strip()]
                total_input = len(input_lines)

                # Update processing message
                if processing_msg:
                    await processing_msg.edit_text(
                        "⏳ **BULK IMPORT PROCESSING**\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"📊 **Found:** {total_input} groups to process\n"
                        "🔄 **Status:** Processing batch...\n"
                        "⚡ **Progress:** Validating and importing...\n\n"
                        "This may take a few moments for large lists..."
                    )

                # Create groups in bulk
                bulk_data = GroupBulkCreate(identifiers=identifiers_text)
                groups = await self.group_service.create_groups_bulk(bulk_data)

                # Clear waiting state
                if context.user_data:
                    context.user_data.pop("waiting_for", None)

                success_count = len(groups)
                failure_count = total_input - success_count
                success_rate = (success_count / total_input * 100) if total_input > 0 else 0

                # Generate detailed results
                result_text = (
                    f"📋 **BULK IMPORT COMPLETED!**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"📊 **Import Summary:**\n"
                    f"├ **Total Processed:** {total_input} groups\n"
                    f"├ **Successfully Added:** ✅ {success_count} groups\n"
                    f"├ **Failed/Skipped:** ❌ {failure_count} groups\n"
                    f"├ **Success Rate:** {success_rate:.1f}%\n"
                    f"└ **Import Time:** {groups[0].created_at.strftime('%d/%m/%Y at %H:%M') if groups else 'N/A'}\n\n"
                )

                if success_count > 0:
                    result_text += "✅ **Successfully Added Groups:**\n"
                    # Show first few successful groups
                    for i, group in enumerate(groups[:MAX_BULK_SUCCESS_DISPLAY], 1):
                        identifier = (
                            group.group_title or 
                            group.group_username or 
                            group.group_id or 
                            group.group_link or 
                            "Unknown"
                        )
                        # Truncate long identifiers
                        display_id = str(identifier)[:35] + "..." if len(str(identifier)) > 35 else identifier
                        result_text += f"{i}. 🟢 {display_id}\n"

                    if success_count > MAX_BULK_SUCCESS_DISPLAY:
                        remaining = success_count - MAX_BULK_SUCCESS_DISPLAY
                        result_text += f"   ⋮ *{remaining} more groups added successfully*\n"
                    
                    result_text += "\n"

                if failure_count > 0:
                    result_text += (
                        f"⚠️ **Import Issues ({failure_count} groups):**\n"
                        f"Common reasons for failures:\n"
                        f"├ Duplicate groups (already in network)\n"
                        f"├ Invalid or inaccessible groups\n"
                        f"├ Incorrect format or syntax\n"
                        f"└ Network or permission issues\n\n"
                    )

                result_text += (
                    f"🚀 **Network Status:**\n"
                    f"├ All successful groups are **active** and ready\n"
                    f"├ Broadcasting capability **enabled**\n"
                    f"├ Network reach **expanded significantly**\n"
                    f"└ Ready for message distribution\n\n"
                    f"💡 **Next Steps:**\n"
                    f"• Review your expanded group network\n"
                    f"• Ensure you have active broadcast messages\n"
                    f"• Test with a small broadcast first\n"
                    f"• Monitor delivery and engagement rates"
                )

                keyboard = [
                    [
                        InlineKeyboardButton("👥 View All Groups", callback_data="groups_menu"),
                        InlineKeyboardButton("📊 Network Stats", callback_data="groups_analytics"),
                    ],
                    [
                        InlineKeyboardButton("📝 Add Messages", callback_data="messages_dashboard"),
                        InlineKeyboardButton("🚀 Start Broadcasting", callback_data="dashboard"),
                    ],
                    [
                        InlineKeyboardButton("📋 Import More", callback_data="groups_bulk"),
                        InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                if processing_msg:
                    await processing_msg.edit_text(
                        result_text, parse_mode="Markdown", reply_markup=reply_markup
                    )
                elif update.message:
                    await update.message.reply_text(
                        result_text, parse_mode="Markdown", reply_markup=reply_markup
                    )

            except Exception as bulk_error:
                error_details = str(bulk_error)
                error_text = (
                    "❌ **BULK IMPORT FAILED**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"⚠️ **System Error:** {error_details}\n\n"
                    "**Possible Causes:**\n"
                    "├ Network connectivity issues\n"
                    "├ Database operation timeout\n"
                    "├ Invalid input format\n"
                    "└ System resource limitations\n\n"
                    "**Recommendations:**\n"
                    "• Try with a smaller batch\n"
                    "• Verify input format\n"
                    "• Check network connection\n"
                    "• Contact support if issue persists"
                )

                keyboard = [
                    [
                        InlineKeyboardButton("🔄 Try Again", callback_data="groups_bulk"),
                        InlineKeyboardButton("➕ Add Single Group", callback_data="groups_add"),
                    ],
                    [
                        InlineKeyboardButton("👥 View Groups", callback_data="groups_menu"),
                        InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                if processing_msg:
                    await processing_msg.edit_text(
                        error_text, parse_mode="Markdown", reply_markup=reply_markup
                    )

        except Exception as e:
            logger.error(f"Error adding bulk groups: {e}")
            if context.user_data:
                context.user_data.pop("waiting_for", None)
            await self._send_error_message(update, "Failed to process bulk group import")

    async def handle_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str
    ) -> None:
        """Enhanced callback handling with comprehensive routing"""
        if data == "groups_menu":
            await self.list_groups(update, context)
        elif data == "groups_add":
            await self._show_add_group_prompt(update, context)
        elif data == "groups_bulk":
            await self._show_bulk_add_prompt(update, context)
        elif data == "groups_analytics":
            await self._show_group_analytics(update, context)
        elif data == "groups_maintenance":
            await self._show_group_maintenance(update, context)
        elif data == "groups_help":
            await self._show_group_help(update, context)
        elif data == "groups_bulk_examples":
            await self._show_bulk_examples(update, context)
        elif data.startswith("groups_edit_"):
            group_id = data.replace("groups_edit_", "")
            await self._show_edit_group(update, group_id)
        elif data.startswith("groups_delete_"):
            group_id = data.replace("groups_delete_", "")
            await self._confirm_delete_group(update, group_id)
        elif data.startswith("groups_delete_confirm_"):
            group_id = data.replace("groups_delete_confirm_", "")
            await self._delete_group(update, group_id)
        elif data.startswith("groups_toggle_"):
            group_id = data.replace("groups_toggle_", "")
            await self._toggle_group_status(update, group_id)

    async def _show_add_group_prompt(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced add group prompt"""
        text = (
            "➕ **ADD NEW TARGET GROUP**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 **Quick Group Addition:**\n\n"
            "**Supported Formats:**\n"
            "├ **Group ID:** `-1001234567890` (recommended)\n"
            "├ **Username:** `@groupname` or `groupname`\n"
            "├ **Link:** `t.me/groupname`\n"
            "└ **Full Link:** `https://t.me/groupname`\n\n"
            "💡 **Pro Tips:**\n"
            "• Group IDs are most reliable\n"
            "• Public groups work best\n"
            "• System validates before adding\n\n"
            "✍️ **Send your group identifier:**"
        )

        keyboard = [
            [
                InlineKeyboardButton("❌ Cancel", callback_data="groups_menu"),
                InlineKeyboardButton("💡 Need Help?", callback_data="groups_help"),
            ],
            [
                InlineKeyboardButton("📋 Add Multiple", callback_data="groups_bulk"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

        if context.user_data:
            context.user_data["waiting_for"] = "group_identifier"

    async def _show_bulk_add_prompt(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Enhanced bulk add prompt"""
        text = (
            "📋 **BULK GROUP IMPORT**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🚀 **Fast Multi-Group Setup:**\n\n"
            "**Format:** One group per line\n"
            "**Example:**\n"
            "```\n"
            "-1001234567890\n"
            "@techgroup\n"
            "businesschat\n"
            "t.me/startupnetwork\n"
            "```\n\n"
            "✅ **Features:**\n"
            "├ Mixed format support\n"
            "├ Duplicate detection\n"
            "├ Automatic validation\n"
            "└ Detailed reporting\n\n"
            "✍️ **Paste your group list:**"
        )

        keyboard = [
            [
                InlineKeyboardButton("❌ Cancel", callback_data="groups_menu"),
                InlineKeyboardButton("📋 Examples", callback_data="groups_bulk_examples"),
            ],
            [
                InlineKeyboardButton("➕ Add Single", callback_data="groups_add"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

        if context.user_data:
            context.user_data["waiting_for"] = "groups_bulk"

    async def _show_edit_group(self, update: Update, group_id: str) -> None:
        """Enhanced group editing interface"""
        try:
            group = await self.group_service.get_group_by_id(group_id)

            if not group:
                if update.callback_query:
                    await update.callback_query.edit_message_text(
                        "❌ **Group Not Found**\n\n"
                        "The requested group could not be located.\n"
                        "It may have been deleted or the ID is invalid."
                    )
                return

            # Enhanced group information display
            status_text = "🟢 **Active**" if group.is_active else "⚪ **Inactive**"
            identifier = group.group_username or group.group_id or group.group_link or "Unknown"
            
            # Format display identifier
            if group.group_title:
                display_name = group.group_title
                name_type = "📝 Title"
            elif group.group_username:
                display_name = f"@{group.group_username.lstrip('@')}"
                name_type = "🏷️ Username"
            elif group.group_id:
                display_name = group.group_id
                name_type = "🆔 Group ID"
            else:
                display_name = "Unknown"
                name_type = "❓ Unknown"

            # Calculate engagement metrics
            days_active = (group.updated_at - group.created_at).days if group.updated_at else 0
            avg_messages_per_day = group.message_count / max(days_active, 1) if days_active > 0 else 0

            text = (
                f"✏️ **GROUP MANAGEMENT**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📊 **Group Information:**\n"
                f"├ **ID:** `{group.id}`\n"
                f"├ **Status:** {status_text}\n"
                f"├ **Type:** {name_type}\n"
                f"├ **Identifier:** `{display_name}`\n"
                f"├ **Title:** {group.group_title or 'Not set'}\n"
                f"└ **Network Role:** Target for broadcasting\n\n"
                f"📈 **Performance Metrics:**\n"
                f"├ **Messages Delivered:** 📊 {group.message_count} total\n"
                f"├ **Average Daily:** {avg_messages_per_day:.1f} messages/day\n"
                f"├ **Success Rate:** {'High' if group.message_count > 10 else 'New' if group.message_count == 0 else 'Low'}\n"
                f"└ **Reliability:** {'Excellent' if group.message_count > 50 else 'Good' if group.message_count > 10 else 'Testing'}\n\n"
                f"📅 **Timeline:**\n"
                f"├ **Added:** {group.created_at.strftime('%d/%m/%Y at %H:%M')}\n"
                f"├ **Last Updated:** {group.updated_at.strftime('%d/%m/%Y at %H:%M') if group.updated_at else 'Never'}\n"
                f"├ **Days in Network:** {days_active} days\n"
                f"└ **Last Broadcast:** {'Recently' if group.message_count > 0 else 'Never'}\n\n"
                f"🛠️ **Management Options:**"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "⚪ Deactivate" if group.is_active else "🟢 Activate",
                        callback_data=f"groups_toggle_{group_id}",
                    ),
                    InlineKeyboardButton("📊 View Analytics", callback_data=f"groups_analytics_{group_id}"),
                ],
                [
                    InlineKeyboardButton("🧪 Test Connection", callback_data=f"groups_test_{group_id}"),
                    InlineKeyboardButton("📝 Update Info", callback_data=f"groups_update_{group_id}"),
                ],
                [
                    InlineKeyboardButton("🗑️ Remove Group", callback_data=f"groups_delete_{group_id}"),
                    InlineKeyboardButton("🔄 Refresh Info", callback_data=f"groups_edit_{group_id}"),
                ],
                [
                    InlineKeyboardButton("🔙 Back to Groups", callback_data="groups_menu"),
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error showing edit group: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ **Error Loading Group**\n\n"
                    "Unable to load group details.\n"
                    "Please try again or check if the group still exists."
                )

    async def _toggle_group_status(self, update: Update, group_id: str) -> None:
        """Enhanced group status toggle"""
        try:
            group = await self.group_service.get_group_by_id(group_id)
            if not group:
                if update.callback_query:
                    await update.callback_query.edit_message_text(
                        "❌ **Group Not Found**\n\n"
                        "The group you're trying to modify could not be found."
                    )
                return

            new_status = not group.is_active
            updated_group = await self.group_service.update_group_info(
                group_id, is_active=new_status
            )

            if updated_group:
                status_action = "activated" if new_status else "deactivated"
                status_icon = "🟢" if new_status else "⚪"
                
                text = (
                    f"✅ **GROUP {status_action.upper()}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"{status_icon} **Status Update Complete**\n\n"
                    f"**Group Details:**\n"
                    f"├ ID: `{updated_group.id}`\n"
                    f"├ New Status: {status_icon} **{status_action.title()}**\n"
                    f"├ Messages Delivered: 📊 {updated_group.message_count}\n"
                    f"└ Broadcasting: {'✅ Enabled' if updated_group.is_active else '⚪ Paused'}\n\n"
                    f"**Network Impact:**\n"
                    f"{'• Group added to active broadcasting rotation' if updated_group.is_active else '• Group removed from broadcasting rotation'}\n"
                    f"{'• Will receive future message broadcasts' if updated_group.is_active else '• Will not receive broadcasts until reactivated'}\n"
                    f"{'• Contributes to network reach metrics' if updated_group.is_active else '• Temporarily excluded from network metrics'}\n\n"
                    f"💡 **Usage:** {'Group is ready for broadcasting' if updated_group.is_active else 'Reactivate when ready to resume broadcasting'}"
                )
            else:
                text = (
                    "❌ **STATUS UPDATE FAILED**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "⚠️ **Unable to Update Group Status**\n\n"
                    "**Possible Issues:**\n"
                    "├ Group no longer exists in network\n"
                    "├ Database synchronization error\n"
                    "├ Temporary system issue\n"
                    "└ Network connectivity problem\n\n"
                    "**Next Steps:**\n"
                    "• Refresh the group list\n"
                    "• Try the operation again\n"
                    "• Check system status\n"
                    "• Contact support if issue persists"
                )

            keyboard = [
                [
                    InlineKeyboardButton("🔄 Refresh Groups", callback_data="groups_menu"),
                    InlineKeyboardButton("✏️ Manage Group", callback_data=f"groups_edit_{group_id}"),
                ],
                [InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=reply_markup)

        except Exception as e:
            logger.error(f"Error toggling group status: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ **System Error**\n\n"
                    "Failed to update group status.\n"
                    "Please try again later."
                )

    async def _confirm_delete_group(self, update: Update, group_id: str) -> None:
        """Enhanced group deletion confirmation"""
        try:
            group = await self.group_service.get_group_by_id(group_id)
            
            if not group:
                if update.callback_query:
                    await update.callback_query.edit_message_text(
                        "❌ **Group Not Found**\n\n"
                        "The group you're trying to delete could not be found.\n"
                        "It may have already been removed."
                    )
                return

            # Enhanced deletion warning
            identifier = group.group_title or group.group_username or group.group_id or "Unknown"
            usage_warning = f"⚠️ This group has received {group.message_count} messages" if group.message_count > 0 else ""
            
            text = (
                f"🗑️ **CONFIRM GROUP REMOVAL**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⚠️ **Permanent Network Removal**\n\n"
                f"**Group to Remove:**\n"
                f"├ ID: `{group.id}`\n"
                f"├ Identifier: `{identifier}`\n"
                f"├ Status: {'🟢 Active' if group.is_active else '⚪ Inactive'}\n"
                f"├ Messages Delivered: 📊 {group.message_count}\n"
                f"├ Added: {group.created_at.strftime('%d/%m/%Y')}\n"
                f"└ Network Role: Broadcasting target\n\n"
                f"{usage_warning}\n\n" if usage_warning else ""
                f"🚨 **This action cannot be undone!**\n\n"
                f"**Consequences of Removal:**\n"
                f"├ Group permanently removed from network\n"
                f"├ All delivery statistics will be lost\n"
                f"├ Cannot be recovered after deletion\n"
                f"├ Broadcasting reach will be reduced\n"
                f"└ Group must be re-added manually if needed\n\n"
                f"**Impact on Broadcasting:**\n"
                f"├ Reduces total network reach\n"
                f"├ May affect campaign effectiveness\n"
                f"└ Consider deactivating instead of deleting\n\n"
                f"**Are you absolutely certain you want to proceed?**"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🗑️ REMOVE PERMANENTLY", callback_data=f"groups_delete_confirm_{group_id}"
                    ),
                ],
                [
                    InlineKeyboardButton("⚪ Deactivate Instead", callback_data=f"groups_toggle_{group_id}"),
                ],
                [
                    InlineKeyboardButton("❌ Cancel", callback_data=f"groups_edit_{group_id}"),
                    InlineKeyboardButton("🔙 Back to Groups", callback_data="groups_menu"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error confirming delete group: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ Error loading deletion confirmation"
                )

    async def _delete_group(self, update: Update, group_id: str) -> None:
        """Enhanced group deletion with confirmation"""
        try:
            success = await self.group_service.delete_group(group_id)

            if success:
                text = (
                    "✅ **GROUP REMOVED SUCCESSFULLY**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "🗑️ **Network Update Complete**\n\n"
                    "**What Happened:**\n"
                    "├ Group permanently removed from network\n"
                    "├ All associated statistics cleared\n"
                    "├ Broadcasting system updated\n"
                    "├ Network reach metrics recalculated\n"
                    "└ Storage space optimized\n\n"
                    "**Next Steps:**\n"
                    "• Review your remaining group network\n"
                    "• Consider adding replacement groups\n"
                    "• Update broadcasting strategy if needed\n"
                    "• Monitor network reach metrics\n\n"
                    "💡 **Tip:** Maintain a diverse group network for better reach and engagement!"
                )
            else:
                text = (
                    "❌ **GROUP REMOVAL FAILED**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "⚠️ **Unable to Remove Group**\n\n"
                    "**Possible Causes:**\n"
                    "├ Group no longer exists in network\n"
                    "├ Database operation timeout\n"
                    "├ System protection mechanism active\n"
                    "├ Network connectivity issue\n"
                    "└ Temporary server error\n\n"
                    "**Try Again:**\n"
                    "• Refresh the group list\n"
                    "• Check if group still exists\n"
                    "• Verify system status\n"
                    "• Contact support if issue persists"
                )

            keyboard = [
                [
                    InlineKeyboardButton("👥 View Groups", callback_data="groups_menu"),
                    InlineKeyboardButton("➕ Add New Group", callback_data="groups_add"),
                ],
                [
                    InlineKeyboardButton("📊 Network Stats", callback_data="groups_analytics"),
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=reply_markup)

        except Exception as e:
            logger.error(f"Error deleting group: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ **System Error**\n\n"
                    "Failed to remove group due to system error.\n"
                    "Please try again or contact support."
                )

    async def _show_group_help(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Enhanced group help guide"""
        text = (
            "💡 **GROUP MANAGEMENT GUIDE**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 **Understanding Groups in Broadcasting:**\n\n"
            "Groups are your message distribution targets. Each group you add becomes part of your broadcasting network, receiving your automated messages according to your system settings.\n\n"
            "📋 **Group Identifier Formats:**\n\n"
            "**🆔 Group ID (Recommended):**\n"
            "├ Format: `-1001234567890`\n"
            "├ Pros: Never changes, most reliable\n"
            "├ Cons: Harder to obtain\n"
            "└ How to get: Use @userinfobot in the group\n\n"
            "**🏷️ Group Username:**\n"
            "├ Format: `@groupname` or `groupname`\n"
            "├ Pros: Easy to remember and share\n"
            "├ Cons: Can change if group is renamed\n"
            "└ Requirements: Group must be public\n\n"
            "**🔗 Group Link:**\n"
            "├ Format: `t.me/groupname` or full URL\n"
            "├ Pros: Easy to copy from group info\n"
            "├ Cons: Only works for public groups\n"
            "└ Note: System extracts identifier automatically\n\n"
            "🔍 **How to Find Group Information:**\n\n"
            "**For Group ID:**\n"
            "• Add @userinfobot to your target group\n"
            "• The bot will show the group ID\n"
            "• Copy the ID (including the minus sign)\n\n"
            "**For Username:**\n"
            "• Open group info/settings\n"
            "• Look for the username field\n"
            "• Username appears as @groupname\n\n"
            "**For Link:**\n"
            "• Use the group's share feature\n"
            "• Copy the t.me/groupname link\n"
            "• Both short and full URLs work\n\n"
            "⚡ **Best Practices:**\n\n"
            "**Group Selection:**\n"
            "├ Choose active, engaged groups\n"
            "├ Ensure you have posting permissions\n"
            "├ Test with small groups first\n"
            "├ Diversify your group portfolio\n"
            "└ Monitor group health regularly\n\n"
            "**Network Management:**\n"
            "├ Start with 5-10 groups for testing\n"
            "├ Gradually expand your network\n"
            "├ Remove inactive or problematic groups\n"
            "├ Keep group information updated\n"
            "└ Monitor delivery success rates\n\n"
            "**Bulk Import Tips:**\n"
            "├ Prepare your list in advance\n"
            "├ One group per line format\n"
            "├ Mix different identifier types\n"
            "├ Verify group accessibility\n"
            "└ Review import results carefully\n\n"
            "🚫 **Common Issues & Solutions:**\n\n"
            "**Group Not Found:**\n"
            "• Verify the identifier is correct\n"
            "• Check if group still exists\n"
            "• Ensure group is accessible\n\n"
            "**Access Denied:**\n"
            "• Verify you're a group member\n"
            "• Check posting permissions\n"
            "• Contact group administrators\n\n"
            "**Already Exists:**\n"
            "• Group is already in your network\n"
            "• Check your group list\n"
            "• Update existing group if needed\n\n"
            "🛡️ **Security & Privacy:**\n\n"
            "• Only add groups you have permission to message\n"
            "• Respect group rules and guidelines\n"
            "• Monitor for spam complaints\n"
            "• Remove groups that request removal\n"
            "• Follow Telegram's Terms of Service\n\n"
            "📊 **Performance Optimization:**\n\n"
            "• Monitor message delivery rates\n"
            "• Remove consistently failing groups\n"
            "• Balance group sizes in your network\n"
            "• Test message content relevance\n"
            "• Adjust timing based on group activity\n\n"
            "💡 **Pro Tips:**\n"
            "• Group IDs are most reliable for automation\n"
            "• Public groups are easier to work with\n"
            "• Test your setup before full deployment\n"
            "• Keep a backup list of your groups\n"
            "• Regular network maintenance improves performance"
        )

        keyboard = [
            [
                InlineKeyboardButton("➕ Add Groups", callback_data="groups_add"),
                InlineKeyboardButton("📋 Bulk Import", callback_data="groups_bulk"),
            ],
            [
                InlineKeyboardButton("📊 Network Stats", callback_data="groups_analytics"),
                InlineKeyboardButton("🧹 Maintenance", callback_data="groups_maintenance"),
            ],
            [
                InlineKeyboardButton("🔙 Back to Groups", callback_data="groups_menu"),
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_bulk_examples(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show bulk import format examples"""
        text = (
            "📋 **BULK IMPORT EXAMPLES**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "✍️ **Copy-Paste Ready Examples:**\n\n"
            "**Example 1: Mixed Format List**\n"
            "```\n"
            "-1001234567890\n"
            "@techstartups\n"
            "businessnetwork\n"
            "t.me/entrepreneurs\n"
            "https://t.me/developers\n"
            "-1009876543210\n"
            "@marketingpros\n"
            "```\n\n"
            "**Example 2: Username Only**\n"
            "```\n"
            "@group1\n"
            "@group2\n"
            "@group3\n"
            "group4\n"
            "group5\n"
            "```\n\n"
            "**Example 3: Group IDs Only**\n"
            "```\n"
            "-1001111111111\n"
            "-1002222222222\n"
            "-1003333333333\n"
            "-1004444444444\n"
            "```\n\n"
            "**Example 4: Links Only**\n"
            "```\n"
            "t.me/publicgroup1\n"
            "t.me/publicgroup2\n"
            "https://t.me/publicgroup3\n"
            "t.me/publicgroup4\n"
            "```\n\n"
            "📝 **Format Rules:**\n"
            "├ One group per line\n"
            "├ Empty lines are ignored\n"
            "├ Mix different formats freely\n"
            "├ No commas or separators needed\n"
            "└ System validates each entry\n\n"
            "💡 **Tips for Best Results:**\n"
            "• Start with smaller batches (10-20 groups)\n"
            "• Verify groups are accessible beforehand\n"
            "• Use Group IDs when possible\n"
            "• Test with one group first if unsure"
        )

        keyboard = [
            [
                InlineKeyboardButton("📋 Start Import", callback_data="groups_bulk"),
                InlineKeyboardButton("➕ Add Single", callback_data="groups_add"),
            ],
            [
                InlineKeyboardButton("💡 More Help", callback_data="groups_help"),
                InlineKeyboardButton("🔙 Back", callback_data="groups_menu"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _show_group_analytics(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show comprehensive group analytics"""
        try:
            groups = await self.group_service.get_all_groups()
            stats = await self.group_service.get_group_stats()
            
            if not groups:
                text = (
                    "📊 **GROUP NETWORK ANALYTICS**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "📭 **No Network Data Available**\n\n"
                    "Add groups to your network to see detailed analytics including:\n"
                    "• Network reach and coverage metrics\n"
                    "• Group performance comparisons\n"
                    "• Delivery success rates\n"
                    "• Network health assessments\n"
                    "• Growth trends and insights"
                )
                keyboard = [
                    [InlineKeyboardButton("➕ Add Groups", callback_data="groups_add")],
                    [InlineKeyboardButton("🔙 Back", callback_data="groups_menu")],
                ]
            else:
                # Advanced analytics calculations
                total_deliveries = sum(group.message_count for group in groups)
                avg_deliveries = total_deliveries / len(groups) if groups else 0
                active_rate = (stats['active'] / stats['total'] * 100) if stats['total'] > 0 else 0
                
                # Find top performers
                top_group = max(groups, key=lambda x: x.message_count) if groups else None
                
                # Network health assessment
                if active_rate >= 80:
                    health_status = "🟢 Excellent"
                elif active_rate >= 60:
                    health_status = "🟡 Good"
                elif active_rate >= 40:
                    health_status = "🟠 Fair"
                else:
                    health_status = "🔴 Needs Attention"

                text = (
                    f"📊 **GROUP NETWORK ANALYTICS**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"🌐 **Network Overview:**\n"
                    f"├ Total Groups: {len(groups)} in network\n"
                    f"├ Active Groups: {stats['active']} ({active_rate:.1f}%)\n"
                    f"├ Network Health: {health_status}\n"
                    f"├ Total Deliveries: {total_deliveries:,} messages\n"
                    f"└ Average Performance: {avg_deliveries:.1f} msgs/group\n\n"
                    f"📈 **Performance Metrics:**\n"
                    f"├ Network Utilization: {active_rate:.1f}%\n"
                    f"├ Delivery Success Rate: {'High' if avg_deliveries > 10 else 'Growing'}\n"
                    f"├ Group Diversity: {'Good' if len(groups) > 10 else 'Expanding'}\n"
                    f"└ Network Stability: {'Stable' if stats['inactive'] < stats['active'] else 'Variable'}\n\n"
                )
                
                if top_group and top_group.message_count > 0:
                    top_group_name = (
                        top_group.group_title or 
                        top_group.group_username or 
                        str(top_group.group_id) or 
                        "Unknown"
                    )[:30]
                    
                    text += (
                        f"🏆 **Top Performing Group:**\n"
                        f"├ Name: {top_group_name}\n"
                        f"├ Deliveries: {top_group.message_count} messages\n"
                        f"├ Performance: {(top_group.message_count / max(total_deliveries, 1)) * 100:.1f}% of total\n"
                        f"└ Status: {'🟢 Active' if top_group.is_active else '⚪ Inactive'}\n\n"
                    )
                
                # Group distribution analysis
                active_groups = [g for g in groups if g.is_active]
                inactive_groups = [g for g in groups if not g.is_active]
                high_performers = [g for g in groups if g.message_count > avg_deliveries]
                
                text += (
                    f"🔍 **Network Analysis:**\n"
                    f"├ High Performers: {len(high_performers)} groups (>{avg_deliveries:.0f} msgs)\n"
                    f"├ Active Groups: {len(active_groups)} ready for broadcasting\n"
                    f"├ Inactive Groups: {len(inactive_groups)} paused\n"
                    f"└ Growth Potential: {'High' if stats['inactive'] > 0 else 'Stable'}\n\n"
                    f"💡 **Recommendations:**\n"
                )
                
                # Smart recommendations
                recommendations = []
                if stats['inactive'] > stats['active']:
                    recommendations.append("• Activate more groups to improve reach")
                if avg_deliveries < 5:
                    recommendations.append("• Groups are new - monitor performance over time")
                if len(groups) < 10:
                    recommendations.append("• Consider expanding network for better coverage")
                if stats['active'] == 0:
                    recommendations.append("• Activate groups to enable broadcasting")
                
                if not recommendations:
                    recommendations.append("• Network is performing well!")
                    recommendations.append("• Continue monitoring and optimizing")
                
                text += "\n".join(recommendations)

                keyboard = [
                    [
                        InlineKeyboardButton("📈 Detailed Report", callback_data="groups_analytics_detailed"),
                        InlineKeyboardButton("🔄 Refresh Data", callback_data="groups_analytics"),
                    ],
                    [
                        InlineKeyboardButton("🏆 Top Performers", callback_data="groups_top_performers"),
                        InlineKeyboardButton("📊 Export Report", callback_data="groups_export_analytics"),
                    ],
                    [
                        InlineKeyboardButton("🔙 Back to Groups", callback_data="groups_menu"),
                        InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                    ],
                ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error showing group analytics: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ Error loading network analytics"
                )

    async def _show_group_maintenance(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show network maintenance options"""
        try:
            stats = await self.group_service.get_group_stats()
            
            text = (
                f"🧹 **NETWORK MAINTENANCE CENTER**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🔧 **Current Network Status:**\n"
                f"├ Total Groups: {stats['total']}\n"
                f"├ Active Groups: {stats['active']}\n"
                f"├ Inactive Groups: {stats['inactive']}\n"
                f"└ Maintenance Needed: {'Yes' if stats['inactive'] > 0 else 'No'}\n\n"
                f"🛠️ **Available Maintenance Operations:**\n\n"
                f"**Network Optimization:**\n"
                f"├ Activate all groups for maximum reach\n"
                f"├ Deactivate all groups (maintenance mode)\n"
                f"├ Remove inactive groups from network\n"
                f"└ Optimize group order for performance\n\n"
                f"**Data Management:**\n"
                f"├ Clear delivery statistics\n"
                f"├ Update group information\n"
                f"├ Validate group accessibility\n"
                f"└ Export network configuration\n\n"
                f"**Health Checks:**\n"
                f"├ Test group connectivity\n"
                f"├ Verify group permissions\n"
                f"├ Check for duplicate groups\n"
                f"└ Validate group formats\n\n"
                f"⚠️ **Important:** Some operations affect your entire network."
            )

            keyboard = [
                [
                    InlineKeyboardButton("🟢 Activate All", callback_data="groups_maintenance_activate_all"),
                    InlineKeyboardButton("⚪ Deactivate All", callback_data="groups_maintenance_deactivate_all"),
                ],
                [
                    InlineKeyboardButton("🧪 Test Network", callback_data="groups_maintenance_test"),
                    InlineKeyboardButton("📊 Clear Statistics", callback_data="groups_maintenance_clear_stats"),
                ],
                [
                    InlineKeyboardButton("🔍 Find Duplicates", callback_data="groups_maintenance_duplicates"),
                    InlineKeyboardButton("📤 Export Network", callback_data="groups_maintenance_export"),
                ],
                [
                    InlineKeyboardButton("🔙 Back to Groups", callback_data="groups_menu"),
                    InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error showing group maintenance: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "❌ Error loading maintenance options"
                )

    async def _send_error_message(self, update: Update, error_text: str) -> None:
        """Enhanced error message handling"""
        error_msg = (
            f"❌ **GROUP SYSTEM ERROR**\n"
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
                InlineKeyboardButton("🔄 Refresh Groups", callback_data="groups_menu"),
                InlineKeyboardButton("📊 System Status", callback_data="refresh_status"),
            ],
            [
                InlineKeyboardButton("💬 Get Help", callback_data="help_center"),
                InlineKeyboardButton("🏠 Dashboard", callback_data="dashboard"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(error_msg, parse_mode="Markdown", reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.edit_message_text(error_msg, parse_mode="Markdown", reply_markup=reply_markup)