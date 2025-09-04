"""
Blacklist Handlers - Handle blacklist management through bot
"""

from loguru import logger

from src.core.constants import MAX_GROUPS_DISPLAY
from src.services.blacklist_service import BlacklistService
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


class BlacklistHandlers:
    """Handlers for blacklist management"""

    def __init__(self) -> None:
        self.blacklist_service = BlacklistService()

    async def show_blacklist(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show blacklist entries"""
        try:
            blacklists = await self.blacklist_service.get_all_blacklists()
            stats = await self.blacklist_service.get_blacklist_stats()

            if not blacklists:
                text = (
                    "🚫 *Blacklist*\n\n"
                    "✅ Tidak ada grup yang di-blacklist.\n\n"
                    "Blacklist otomatis akan terisi ketika ada error pengiriman pesan."
                )
                keyboard: list[list[InlineKeyboardButton]] = []
            else:
                text = (
                    f"🚫 *Blacklist* ({stats['total']} total)\n\n"
                    f"🔴 **Permanen:** {stats['permanent']}\n"
                    f"🟡 **Sementara:** {stats['temporary']}\n"
                    f"⏰ **Kedaluwarsa:** {stats['expired']}\n\n"
                )

                keyboard: list[list[InlineKeyboardButton]] = []

                # Show permanent blacklists first
                permanent_count = 0
                temporary_count = 0

                for blacklist in blacklists[:MAX_GROUPS_DISPLAY]:  # Show first 10
                    identifier = blacklist.group_identifier or blacklist.group_id

                    if blacklist.blacklist_type.value == "permanent":
                        permanent_count += 1
                        text += f"🔴 {identifier}\n   └ {blacklist.reason.value}\n\n"

                        keyboard.append(
                            [
                                InlineKeyboardButton(
                                    f"🗑️ Hapus #{permanent_count}",
                                    callback_data=f"blacklist_remove_{blacklist.id}",
                                )
                            ]
                        )
                    else:
                        temporary_count += 1
                        time_remaining = blacklist.time_remaining

                        if blacklist.is_expired:
                            status = "⏰ Kedaluwarsa"
                        elif time_remaining:
                            hours = int(time_remaining.total_seconds() // 3600)
                            minutes = int((time_remaining.total_seconds() % 3600) // 60)
                            status = f"⏱️ {hours}j {minutes}m"
                        else:
                            status = "🟡 Aktif"

                        text += f"🟡 {identifier} ({status})\n   └ {blacklist.reason.value}\n\n"

                        keyboard.append(
                            [
                                InlineKeyboardButton(
                                    f"🗑️ Hapus #{temporary_count}",
                                    callback_data=f"blacklist_remove_{blacklist.id}",
                                )
                            ]
                        )

                if len(blacklists) > MAX_GROUPS_DISPLAY:
                    text += f"... dan {len(blacklists) - MAX_GROUPS_DISPLAY} entry lainnya\n\n"

                # Add cleanup button if there are expired entries
                if stats["expired"] > 0:
                    keyboard.append(
                        [
                            InlineKeyboardButton(
                                f"🧹 Bersihkan Yang Kedaluwarsa ({stats['expired']})",
                                callback_data="blacklist_cleanup",
                            )
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
            else:
                await update.callback_query.edit_message_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error showing blacklist: {e}")
            await self._send_error_message(update, "Gagal memuat blacklist")

    async def handle_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str
    ) -> None:
        """Handle blacklist-related callbacks"""
        if data == "blacklist_menu":
            await self.show_blacklist(update, context)
        elif data == "blacklist_cleanup":
            await self._cleanup_expired(update)
        elif data.startswith("blacklist_remove_"):
            blacklist_id = data.replace("blacklist_remove_", "")
            await self._confirm_remove_blacklist(update, blacklist_id)
        elif data.startswith("blacklist_remove_confirm_"):
            blacklist_id = data.replace("blacklist_remove_confirm_", "")
            await self._remove_blacklist(update, blacklist_id)

    async def _cleanup_expired(self, update: Update) -> None:
        """Clean up expired blacklist entries"""
        try:
            removed_count = await self.blacklist_service.cleanup_expired()

            if removed_count > 0:
                text = f"🧹 Berhasil membersihkan {removed_count} entry blacklist yang kedaluwarsa."
            else:
                text = "i Tidak ada entry blacklist yang kedaluwarsa untuk dibersihkan."

            keyboard = [
                [InlineKeyboardButton("🚫 Lihat Blacklist", callback_data="blacklist_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

        except Exception as e:
            logger.error(f"Error cleaning up blacklist: {e}")
            await update.callback_query.edit_message_text("❌ Gagal membersihkan blacklist.")

    async def _confirm_remove_blacklist(self, update: Update, blacklist_id: str) -> None:
        """Confirm blacklist removal"""
        try:
            blacklist = await self.blacklist_service.get_blacklist_entry_by_id(blacklist_id)

            if not blacklist:
                await update.callback_query.edit_message_text("❌ Entry blacklist tidak ditemukan.")
                return

            identifier = blacklist.group_identifier or blacklist.group_id

            text = (
                f"🗑️ *Konfirmasi Hapus Blacklist*\n\n"
                f"**Grup:** {identifier}\n"
                f"**Tipe:** {blacklist.blacklist_type.value.title()}\n"
                f"**Alasan:** {blacklist.reason.value}\n\n"
                f"⚠️ Apakah Anda yakin ingin menghapus entry ini dari blacklist?\n\n"
                f"Grup akan bisa menerima pesan lagi."
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "✅ Ya, Hapus", callback_data=f"blacklist_remove_confirm_{blacklist_id}"
                    ),
                    InlineKeyboardButton("❌ Batal", callback_data="blacklist_menu"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

        except Exception as e:
            logger.error(f"Error confirming blacklist removal: {e}")
            await update.callback_query.edit_message_text("❌ Gagal memuat entry blacklist.")

    async def _remove_blacklist(self, update: Update, blacklist_id: str) -> None:
        """Remove blacklist entry"""
        try:
            blacklist = await self.blacklist_service.get_blacklist_entry_by_id(blacklist_id)

            if not blacklist:
                await update.callback_query.edit_message_text("❌ Entry blacklist tidak ditemukan.")
                return

            success = await self.blacklist_service.remove_from_blacklist(blacklist.group_id)

            if success:
                identifier = blacklist.group_identifier or blacklist.group_id
                text = f"✅ Entry blacklist untuk {identifier} berhasil dihapus!"
            else:
                text = "❌ Gagal menghapus entry blacklist."

            keyboard = [
                [InlineKeyboardButton("🚫 Lihat Blacklist", callback_data="blacklist_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

        except Exception as e:
            logger.error(f"Error removing blacklist: {e}")
            await update.callback_query.edit_message_text("❌ Gagal menghapus entry blacklist.")

    async def _send_error_message(self, update: Update, error_text: str) -> None:
        """Send error message"""
        if update.message:
            await update.message.reply_text(f"❌ {error_text}")
        else:
            await update.callback_query.edit_message_text(f"❌ {error_text}")
