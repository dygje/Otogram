"""
Message Handlers - Handle message management through bot
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
    """Handlers for message management"""

    def __init__(self) -> None:
        self.message_service = MessageService()

    async def list_messages(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """List all messages"""
        try:
            messages = await self.message_service.get_all_messages()
            stats = await self.message_service.get_message_count()

            if not messages:
                text = "📝 *Daftar Pesan*\n\n❌ Belum ada pesan yang tersimpan.\n\nGunakan /addmessage untuk menambah pesan."
                keyboard = [[InlineKeyboardButton("+ Tambah Pesan", callback_data="messages_add")]]
            else:
                text = f"📝 *Daftar Pesan* ({stats['active']}/{stats['total']} aktif)\n\n"

                keyboard = []
                for i, msg in enumerate(messages[:MAX_MESSAGES_DISPLAY], 1):  # Show first 10
                    status = "✅" if msg.is_active else "❌"
                    content_preview = (
                        msg.content[:PREVIEW_MESSAGE_LENGTH] + "..."
                        if len(msg.content) > PREVIEW_MESSAGE_LENGTH
                        else msg.content
                    )
                    text += f"{i}. {status} {content_preview}\n   📊 Terpakai: {msg.usage_count} kali\n\n"

                    keyboard.append(
                        [
                            InlineKeyboardButton(
                                f"✏️ Edit #{i}", callback_data=f"messages_edit_{msg.id}"
                            ),
                            InlineKeyboardButton(
                                f"🗑️ Hapus #{i}", callback_data=f"messages_delete_{msg.id}"
                            ),
                        ]
                    )

                if len(messages) > MAX_MESSAGES_DISPLAY:
                    text += f"... dan {len(messages) - MAX_MESSAGES_DISPLAY} pesan lainnya\n\n"

                keyboard.append(
                    [InlineKeyboardButton("+ Tambah Pesan", callback_data="messages_add")]
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
            logger.error(f"Error listing messages: {e}")
            await self._send_error_message(update, "Gagal memuat daftar pesan")

    async def add_message_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start adding new message"""
        text = (
            "+ *Tambah Pesan Baru*\n\n"
            "Kirim pesan yang ingin Anda tambahkan untuk broadcast.\n\n"
            "⚠️ *Catatan:*\n"
            "• Hanya teks yang didukung (tanpa media)\n"
            "• Maksimal 4096 karakter\n"
            "• Pesan akan otomatis aktif\n\n"
            "Ketik pesan Anda sekarang:"
        )

        if context.user_data:
            context.user_data["waiting_for"] = "message_content"

        keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="messages_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

    async def handle_message_input(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle message content input"""
        try:
            if update.message and update.message.text:
                content = update.message.text.strip()
            else:
                if update.message:
                    await update.message.reply_text("❌ Pesan tidak boleh kosong. Coba lagi:")
                return

            if not content:
                if update.message:
                    await update.message.reply_text("❌ Pesan tidak boleh kosong. Coba lagi:")
                return

            if len(content) > TELEGRAM_MESSAGE_MAX_LENGTH:
                if update.message:
                    await update.message.reply_text(
                        f"❌ Pesan terlalu panjang ({len(content)} karakter). Maksimal {TELEGRAM_MESSAGE_MAX_LENGTH} karakter. Coba lagi:"
                    )
                return

            # Create message
            message_data = MessageCreate(content=content)
            message = await self.message_service.create_message(message_data)

            # Clear waiting state
            if context.user_data:
                context.user_data.pop("waiting_for", None)

            text = (
                f"✅ *Pesan Berhasil Ditambahkan*\n\n"
                f"📝 **Konten:** {content[:PREVIEW_MESSAGE_LENGTH_SHORT]}{'...' if len(content) > PREVIEW_MESSAGE_LENGTH_SHORT else ''}\n"
                f"🆔 **ID:** `{message.id}`\n"
                f"📅 **Dibuat:** {message.created_at.strftime('%d/%m/%Y %H:%M')}\n"
                f"✅ **Status:** Aktif\n\n"
                f"Pesan siap digunakan untuk broadcast!"
            )

            keyboard = [
                [InlineKeyboardButton("📝 Lihat Semua Pesan", callback_data="messages_menu")],
                [InlineKeyboardButton("+ Tambah Lagi", callback_data="messages_add")],
                [InlineKeyboardButton("🔙 Dashboard", callback_data="back_to_dashboard")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.message:
                await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

        except Exception as e:
            logger.error(f"Error adding message: {e}")
            if context.user_data:
                context.user_data.pop("waiting_for", None)
            await self._send_error_message(update, "Gagal menambahkan pesan")

    async def handle_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str
    ) -> None:
        """Handle message-related callbacks"""
        if data == "messages_menu":
            await self.list_messages(update, context)
        elif data == "messages_add":
            await self._show_add_message_prompt(update)
        elif data.startswith("messages_edit_"):
            message_id = data.replace("messages_edit_", "")
            await self._show_edit_message(update, message_id)
        elif data.startswith("messages_delete_"):
            message_id = data.replace("messages_delete_", "")
            await self._confirm_delete_message(update, message_id)
        elif data.startswith("messages_delete_confirm_"):
            message_id = data.replace("messages_delete_confirm_", "")
            await self._delete_message(update, message_id)

    async def _show_add_message_prompt(self, update: Update) -> None:
        """Show add message prompt"""
        text = (
            "+ *Tambah Pesan Baru*\n\n"
            "Kirim pesan yang ingin Anda tambahkan untuk broadcast.\n\n"
            "⚠️ *Catatan:*\n"
            "• Hanya teks yang didukung\n"
            "• Maksimal 4096 karakter\n"
            "• Pesan akan otomatis aktif"
        )

        keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="messages_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

            # Set waiting state - proper access to context
            if hasattr(update.callback_query, 'user') and update.callback_query.user:
                # We need to get the context properly, this is a simplified approach
                # In practice, this should be handled differently in the callback flow
                pass

    async def _show_edit_message(self, update: Update, message_id: str) -> None:
        """Show edit message options"""
        try:
            message = await self.message_service.get_message_by_id(message_id)

            if not message:
                if update.callback_query:
                    await update.callback_query.edit_message_text("❌ Pesan tidak ditemukan.")
                return

            status_text = "Aktif ✅" if message.is_active else "Nonaktif ❌"
            content_preview = (
                message.content[:PREVIEW_MESSAGE_LENGTH_LONG] + "..."
                if len(message.content) > PREVIEW_MESSAGE_LENGTH_LONG
                else message.content
            )

            text = (
                f"✏️ *Edit Pesan*\n\n"
                f"📝 **Konten:** {content_preview}\n"
                f"📊 **Terpakai:** {message.usage_count} kali\n"
                f"🔄 **Status:** {status_text}\n"
                f"📅 **Dibuat:** {message.created_at.strftime('%d/%m/%Y %H:%M')}\n\n"
                f"Pilih aksi:"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "❌ Nonaktifkan" if message.is_active else "✅ Aktifkan",
                        callback_data=f"messages_toggle_{message_id}",
                    )
                ],
                [InlineKeyboardButton("🗑️ Hapus", callback_data=f"messages_delete_{message_id}")],
                [InlineKeyboardButton("🔙 Kembali", callback_data="messages_menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error showing edit message: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Gagal memuat pesan.")

    async def _confirm_delete_message(self, update: Update, message_id: str) -> None:
        """Confirm message deletion"""
        text = (
            "🗑️ *Konfirmasi Hapus Pesan*\n\n"
            "⚠️ Apakah Anda yakin ingin menghapus pesan ini?\n\n"
            "Aksi ini tidak dapat dibatalkan."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Ya, Hapus", callback_data=f"messages_delete_confirm_{message_id}"
                ),
                InlineKeyboardButton("❌ Batal", callback_data="messages_menu"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

    async def _delete_message(self, update: Update, message_id: str) -> None:
        """Delete message"""
        try:
            success = await self.message_service.delete_message(message_id)

            text = "✅ Pesan berhasil dihapus!" if success else "❌ Gagal menghapus pesan."

            keyboard = [[InlineKeyboardButton("📝 Lihat Pesan", callback_data="messages_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.callback_query:
                await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

        except Exception as e:
            logger.error(f"Error deleting message: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text("❌ Gagal menghapus pesan.")

    async def _send_error_message(self, update: Update, error_text: str) -> None:
        """Send error message"""
        if update.message:
            await update.message.reply_text(f"❌ {error_text}")
        elif update.callback_query:
            await update.callback_query.edit_message_text(f"❌ {error_text}")
