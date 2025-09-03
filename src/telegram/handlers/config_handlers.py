"""
Configuration Handlers - Handle system configuration through bot
"""

from loguru import logger

from src.services.config_service import ConfigService
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


class ConfigHandlers:
    """Handlers for configuration management"""

    def __init__(self):
        self.config_service = ConfigService()

    async def show_config(self, update: Update, _context: ContextTypes.DEFAULT_TYPE):
        """Show system configuration"""
        try:
            configs = await self.config_service.get_all_configs()

            if not configs:
                text = "⚙️ *Konfigurasi Sistem*\n\n❌ Tidak ada konfigurasi yang tersedia."
                keyboard = [[InlineKeyboardButton("🔙 Menu Utama", callback_data="main_menu")]]
            else:
                text = "⚙️ *Konfigurasi Sistem*\n\n"

                # Group by category
                categories = {}
                for config in configs:
                    if config.category not in categories:
                        categories[config.category] = []
                    categories[config.category].append(config)

                keyboard = []

                for category, cat_configs in categories.items():
                    text += f"**{category.title()}:**\n"
                    for config in cat_configs:
                        value = config.get_typed_value()
                        editable = "✏️" if config.is_editable else "🔒"
                        text += f"• {editable} {config.key}: `{value}`\n"

                        if config.is_editable:
                            keyboard.append(
                                [
                                    InlineKeyboardButton(
                                        f"✏️ {config.key}", callback_data=f"config_edit_{config.id}"
                                    )
                                ]
                            )
                    text += "\n"

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
            logger.error(f"Error showing config: {e}")
            await self._send_error_message(update, "Gagal memuat konfigurasi")

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
        """Handle configuration-related callbacks"""
        if data == "config_menu":
            await self.show_config(update, context)
        elif data.startswith("config_edit_"):
            config_id = data.replace("config_edit_", "")
            await self._show_edit_config(update, context, config_id)

    async def handle_config_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle configuration value input"""
        try:
            waiting_for = context.user_data.get("waiting_for", "")

            if waiting_for.startswith("config_"):
                config_id = waiting_for.replace("config_", "")
                new_value = update.message.text.strip()

                # Get the configuration
                config = await self.config_service.get_config_by_id(config_id)
                if not config:
                    await update.message.reply_text("❌ Konfigurasi tidak ditemukan.")
                    return

                # Validate and convert value based on type
                try:
                    if config.value_type == "int":
                        converted_value = int(new_value)
                    elif config.value_type == "float":
                        converted_value = float(new_value)
                    elif config.value_type == "bool":
                        converted_value = new_value.lower() in ("true", "1", "yes", "on")
                    else:
                        converted_value = new_value

                    # Update configuration
                    updated_config = await self.config_service.set_config(
                        config.key, converted_value
                    )

                    if updated_config:
                        text = (
                            f"✅ *Konfigurasi Berhasil Diperbarui*\n\n"
                            f"**{config.key}:** `{converted_value}`\n"
                            f"📝 {config.description or 'Tidak ada deskripsi'}\n\n"
                            f"Perubahan akan diterapkan pada siklus berikutnya."
                        )
                    else:
                        text = "❌ Gagal memperbarui konfigurasi."

                except ValueError:
                    text = f"❌ Nilai tidak valid untuk tipe {config.value_type}. Coba lagi."
                    context.user_data.pop("waiting_for", None)
                    await update.message.reply_text(text)
                    return

                # Clear waiting state
                context.user_data.pop("waiting_for", None)

                keyboard = [
                    [InlineKeyboardButton("⚙️ Lihat Konfigurasi", callback_data="config_menu")],
                    [InlineKeyboardButton("🔙 Dashboard", callback_data="back_to_dashboard")],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    text, parse_mode="Markdown", reply_markup=reply_markup
                )

        except Exception as e:
            logger.error(f"Error handling config input: {e}")
            context.user_data.pop("waiting_for", None)
            await self._send_error_message(update, "Gagal memperbarui konfigurasi")

    async def _show_edit_config(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, config_id: str
    ):
        """Show edit configuration prompt"""
        try:
            config = await self.config_service.get_config_by_id(config_id)

            if not config:
                await update.callback_query.edit_message_text("❌ Konfigurasi tidak ditemukan.")
                return

            if not config.is_editable:
                await update.callback_query.edit_message_text(
                    "❌ Konfigurasi ini tidak dapat diedit."
                )
                return

            current_value = config.get_typed_value()

            text = (
                f"✏️ *Edit Konfigurasi*\n\n"
                f"**Key:** {config.key}\n"
                f"**Nilai Saat Ini:** `{current_value}`\n"
                f"**Tipe:** {config.value_type}\n"
                f"**Deskripsi:** {config.description or 'Tidak ada deskripsi'}\n\n"
                f"Kirim nilai baru:"
            )

            # Set waiting state
            context.user_data["waiting_for"] = f"config_{config_id}"

            keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="config_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.callback_query.edit_message_text(
                text, parse_mode="Markdown", reply_markup=reply_markup
            )

        except Exception as e:
            logger.error(f"Error showing edit config: {e}")
            await update.callback_query.edit_message_text("❌ Gagal memuat konfigurasi.")

    async def _send_error_message(self, update: Update, error_text: str):
        """Send error message"""
        if update.message:
            await update.message.reply_text(f"❌ {error_text}")
        else:
            await update.callback_query.edit_message_text(f"❌ {error_text}")
