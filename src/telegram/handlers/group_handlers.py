"""
Group Handlers - Handle group management through bot
"""

from loguru import logger

from src.core.constants import MAX_BULK_SUCCESS_DISPLAY, MAX_GROUPS_DISPLAY
from src.models.group import GroupBulkCreate, GroupCreate
from src.services.group_service import GroupService
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


class GroupHandlers:
    """Handlers for group management"""

    def __init__(self) -> None:
        self.group_service = GroupService()

    async def list_groups(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """List all groups"""
        try:
            groups = await self.group_service.get_all_groups()
            stats = await self.group_service.get_group_stats()

            if not groups:
                text = "👥 *Daftar Grup*\n\n❌ Belum ada grup yang tersimpan.\n\nGunakan /addgroup untuk menambah grup."
                keyboard = [
                    [InlineKeyboardButton("+ Tambah Grup", callback_data="groups_add")],
                    [InlineKeyboardButton("📋 Tambah Massal", callback_data="groups_bulk")],
                ]
            else:
                text = f"👥 *Daftar Grup* ({stats['active']}/{stats['total']} aktif)\n\n"

                keyboard = []
                for i, group in enumerate(groups[:MAX_GROUPS_DISPLAY], 1):  # Show first 10
                    status = "✅" if group.is_active else "❌"

                    # Display identifier
                    if group.group_title:
                        identifier = group.group_title
                    elif group.group_username:
                        identifier = group.group_username
                    elif group.group_id:
                        identifier = group.group_id
                    else:
                        identifier = "Unknown"

                    text += f"{i}. {status} {identifier}\n   📊 Pesan: {group.message_count}\n\n"

                    keyboard.append(
                        [
                            InlineKeyboardButton(
                                f"✏️ Edit #{i}", callback_data=f"groups_edit_{group.id}"
                            ),
                            InlineKeyboardButton(
                                f"🗑️ Hapus #{i}", callback_data=f"groups_delete_{group.id}"
                            ),
                        ]
                    )

                if len(groups) > MAX_GROUPS_DISPLAY:
                    text += f"... dan {len(groups) - MAX_GROUPS_DISPLAY} grup lainnya\n\n"

                keyboard.extend(
                    [
                        [InlineKeyboardButton("+ Tambah Grup", callback_data="groups_add")],
                        [InlineKeyboardButton("📋 Tambah Massal", callback_data="groups_bulk")],
                    ]
                )

            keyboard.append(
                [InlineKeyboardButton("🔙 Dashboard", callback_data="back_to_dashboard")]
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
            logger.error(f"Error listing groups: {e}")
            await self._send_error_message(update, "Gagal memuat daftar grup")

    async def add_group_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start adding single group"""
        text = (
            "+ *Tambah Grup Baru*\n\n"
            "Kirim ID grup, username, atau link grup yang ingin ditambahkan.\n\n"
            "📋 *Format yang didukung:*\n"
            "• ID Grup: `-1001234567890`\n"
            "• Username: `@namagrup`\n"
            "• Link: `t.me/namagrup`\n\n"
            "Kirim identifier grup sekarang:"
        )

        if context.user_data:
            context.user_data["waiting_for"] = "group_identifier"

        keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="groups_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

    async def add_groups_bulk_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Start adding multiple groups"""
        text = (
            "📋 *Tambah Grup Massal*\n\n"
            "Kirim daftar grup (satu per baris) yang ingin ditambahkan.\n\n"
            "📋 *Format yang didukung:*\n"
            "• ID Grup: `-1001234567890`\n"
            "• Username: `@namagrup`\n"
            "• Link: `t.me/namagrup`\n\n"
            "📝 *Contoh:*\n"
            "```\n@grup1\n@grup2\n-1001234567890\nt.me/grup3\n```\n\n"
            "Kirim daftar grup sekarang:"
        )

        if context.user_data:
            context.user_data["waiting_for"] = "groups_bulk"

        keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="groups_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

    async def handle_group_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle single group input"""
        try:
            if update.message and update.message.text:
                identifier = update.message.text.strip()
            else:
                if update.message:
                    await update.message.reply_text(
                        "❌ Identifier grup tidak boleh kosong. Coba lagi:"
                    )
                return

            if not identifier:
                if update.message:
                    await update.message.reply_text(
                        "❌ Identifier grup tidak boleh kosong. Coba lagi:"
                    )
                return

            # Create group
            group_data = GroupCreate(group_identifier=identifier)
            group = await self.group_service.create_group(group_data)

            # Clear waiting state
            if context.user_data:
                context.user_data.pop("waiting_for", None)

            text = (
                f"✅ *Grup Berhasil Ditambahkan*\n\n"
                f"🆔 **ID:** `{group.id}`\n"
                f"📝 **Identifier:** `{identifier}`\n"
                f"📅 **Ditambahkan:** {group.created_at.strftime('%d/%m/%Y %H:%M')}\n"
                f"✅ **Status:** Aktif\n\n"
                f"Grup siap menerima broadcast!"
            )

            keyboard = [
                [InlineKeyboardButton("👥 Lihat Semua Grup", callback_data="groups_menu")],
                [InlineKeyboardButton("+ Tambah Lagi", callback_data="groups_add")],
                [InlineKeyboardButton("🔙 Dashboard", callback_data="back_to_dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.message:
                await update.message.reply_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error adding group: {e}")
            if context.user_data:
                context.user_data.pop("waiting_for", None)
            await self._send_error_message(update, "Gagal menambahkan grup")

    async def handle_bulk_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle bulk groups input"""
        try:
            if update.message and update.message.text:
                identifiers_text = update.message.text.strip()
            else:
                if update.message:
                    await update.message.reply_text("❌ Daftar grup tidak boleh kosong. Coba lagi:")
                return

            if not identifiers_text:
                if update.message:
                    await update.message.reply_text("❌ Daftar grup tidak boleh kosong. Coba lagi:")
                return

            # Create groups in bulk
            bulk_data = GroupBulkCreate(identifiers=identifiers_text)
            groups = await self.group_service.create_groups_bulk(bulk_data)

            # Clear waiting state
            if context.user_data:
                context.user_data.pop("waiting_for", None)

            success_count = len(groups)
            identifiers_list = bulk_data.get_identifiers_list()
            total_count = len(identifiers_list)

            text = (
                f"📋 *Hasil Penambahan Grup Massal*\n\n"
                f"✅ **Berhasil:** {success_count}/{total_count} grup\n"
                f"📅 **Ditambahkan:** {groups[0].created_at.strftime('%d/%m/%Y %H:%M') if groups else 'N/A'}\n\n"
            )

            if success_count > 0:
                text += "**Grup yang berhasil ditambahkan:**\n"
                for i, group in enumerate(groups[:MAX_BULK_SUCCESS_DISPLAY], 1):  # Show first 5
                    identifier = (
                        group.group_username or group.group_id or group.group_link or "Unknown"
                    )
                    text += f"{i}. {identifier}\n"

                if success_count > MAX_BULK_SUCCESS_DISPLAY:
                    text += f"... dan {success_count - MAX_BULK_SUCCESS_DISPLAY} grup lainnya\n"

            if success_count < total_count:
                text += (
                    f"\n❌ {total_count - success_count} grup gagal ditambahkan (mungkin sudah ada)"
                )

            keyboard = [
                [InlineKeyboardButton("👥 Lihat Semua Grup", callback_data="groups_menu")],
                [InlineKeyboardButton("📋 Tambah Lagi", callback_data="groups_bulk")],
                [InlineKeyboardButton("🔙 Dashboard", callback_data="back_to_dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.message:
                await update.message.reply_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error adding bulk groups: {e}")
            if context.user_data:
                context.user_data.pop("waiting_for", None)
            await self._send_error_message(update, "Gagal menambahkan grup massal")

    async def handle_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str
    ) -> None:
        """Handle group-related callbacks"""
        if data == "groups_menu":
            await self.list_groups(update, context)
        elif data == "groups_add":
            await self._show_add_group_prompt(update, context)
        elif data == "groups_bulk":
            await self._show_bulk_add_prompt(update, context)
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
        """Show add group prompt"""
        text = (
            "+ *Tambah Grup Baru*\n\n"
            "Kirim ID grup, username, atau link grup.\n\n"
            "📋 *Format:*\n"
            "• `-1001234567890`\n"
            "• `@namagrup`\n"
            "• `t.me/namagrup`"
        )

        keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="groups_menu")]]
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
        """Show bulk add prompt"""
        text = (
            "📋 *Tambah Grup Massal*\n\n"
            "Kirim daftar grup (satu per baris):\n\n"
            "```\n@grup1\n@grup2\n-1001234567890\nt.me/grup3\n```"
        )

        keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="groups_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

        if context.user_data:
            context.user_data["waiting_for"] = "groups_bulk"

    async def _show_edit_group(self, update: Update, group_id: str) -> None:
        """Show edit group options"""
        try:
            group = await self.group_service.get_group_by_id(group_id)

            if not group:
                if update.callback_query:
                    await update.callback_query.edit_message_text("❌ Grup tidak ditemukan.")
                return

            status_text = "Aktif ✅" if group.is_active else "Nonaktif ❌"
            identifier = group.group_username or group.group_id or group.group_link or "Unknown"

            text = (
                f"✏️ *Edit Grup*\n\n"
                f"📝 **Identifier:** {identifier}\n"
                f"🏷️ **Judul:** {group.group_title or 'Belum diset'}\n"
                f"📊 **Pesan Terkirim:** {group.message_count}\n"
                f"🔄 **Status:** {status_text}\n"
                f"📅 **Ditambahkan:** {group.created_at.strftime('%d/%m/%Y %H:%M')}\n\n"
                f"Pilih aksi:"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "❌ Nonaktifkan" if group.is_active else "✅ Aktifkan",
                        callback_data=f"groups_toggle_{group_id}",
                    )
                ],
                [InlineKeyboardButton("🗑️ Hapus", callback_data=f"groups_delete_{group_id}")],
                [InlineKeyboardButton("🔙 Kembali", callback_data="groups_menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error showing edit group: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Gagal memuat grup.")

    async def _toggle_group_status(self, update: Update, group_id: str) -> None:
        """Toggle group active status"""
        try:
            group = await self.group_service.get_group_by_id(group_id)
            if not group:
                if update.callback_query:
                    await update.callback_query.edit_message_text("❌ Grup tidak ditemukan.")
                return

            new_status = not group.is_active
            updated_group = await self.group_service.update_group_info(
                group_id, is_active=new_status
            )

            if updated_group:
                status_text = "diaktifkan" if new_status else "dinonaktifkan"
                text = f"✅ Grup berhasil {status_text}!"
            else:
                text = "❌ Gagal mengubah status grup."

            keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="groups_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

        except Exception as e:
            logger.error(f"Error toggling group status: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Gagal mengubah status grup.")

    async def _confirm_delete_group(self, update: Update, group_id: str) -> None:
        """Confirm group deletion"""
        text = (
            "🗑️ *Konfirmasi Hapus Grup*\n\n"
            "⚠️ Apakah Anda yakin ingin menghapus grup ini?\n\n"
            "Aksi ini tidak dapat dibatalkan."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Ya, Hapus", callback_data=f"groups_delete_confirm_{group_id}"
                ),
                InlineKeyboardButton("❌ Batal", callback_data="groups_menu"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _delete_group(self, update: Update, group_id: str) -> None:
        """Delete group"""
        try:
            success = await self.group_service.delete_group(group_id)

            text = "✅ Grup berhasil dihapus!" if success else "❌ Gagal menghapus grup."

            keyboard = [[InlineKeyboardButton("👥 Lihat Grup", callback_data="groups_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

        except Exception as e:
            logger.error(f"Error deleting group: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Gagal menghapus grup.")

    async def _send_error_message(self, update: Update, error_text: str) -> None:
        """Send error message"""
        if update.message:
            await update.message.reply_text(f"❌ {error_text}")
        elif update.callback_query:
            await update.callback_query.edit_message_text(f"❌ {error_text}")
