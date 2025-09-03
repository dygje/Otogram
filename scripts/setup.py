#!/usr/bin/env python3
"""
Enhanced Setup Script for Telegram Automation System
Membantu user mengkonfigurasi credentials dan menjalankan sistem
"""
import os
import sys
from pathlib import Path


def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 70)
    print("🤖 TELEGRAM AUTOMATION SYSTEM - SETUP WIZARD")
    print("=" * 70)
    print("Sistema otomatisasi pengiriman pesan massal ke grup Telegram")
    print("dengan manajemen lengkap melalui Telegram Bot.")
    print("=" * 70 + "\n")


def check_env_file():
    """Check if .env file exists and validate required fields"""
    env_path = Path(__file__).parent.parent / ".env"

    if not env_path.exists():
        print("❌ File .env tidak ditemukan!")
        print("💡 Menyalin dari .env.example...")

        # Copy from .env.example
        example_path = env_path.parent / ".env.example"
        if example_path.exists():
            import shutil

            shutil.copy2(example_path, env_path)
            print("✅ File .env berhasil dibuat dari template!")
        else:
            print("❌ File .env.example juga tidak ditemukan!")
            return []

    # Read .env file
    env_content = env_path.read_text()

    required_fields = [
        "TELEGRAM_API_ID",
        "TELEGRAM_API_HASH",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_PHONE_NUMBER",
    ]

    missing_fields = []

    for field in required_fields:
        # Check if field exists and has value
        field_found = False
        for line in env_content.split("\n"):
            if line.strip().startswith(f"{field}="):
                value = line.split("=", 1)[1].strip()
                if value and not value.startswith("#"):
                    field_found = True
                break

        if not field_found:
            missing_fields.append(field)

    return missing_fields


def validate_credentials(
    api_id: str, api_hash: str, bot_token: str, phone_number: str
) -> tuple[bool, str]:
    """Validate credential formats"""

    # Validate API ID
    if not api_id.isdigit():
        return False, "API ID harus berupa angka (8 digit)"

    if len(api_id) != 8:
        return False, "API ID harus 8 digit"

    # Validate API Hash
    if len(api_hash) != 32:
        return False, "API Hash harus 32 karakter"

    # Validate Bot Token format
    if ":" not in bot_token or len(bot_token.split(":")[0]) < 8:
        return False, "Format Bot Token tidak valid (harus seperti: 123456789:ABC-DEF...)"

    # Validate Phone Number
    if not phone_number.startswith("+"):
        return False, "Nomor telepon harus dimulai dengan + (format internasional)"

    if len(phone_number) < 10:
        return False, "Nomor telepon terlalu pendek"

    return True, "Valid"


def setup_credentials():
    """Setup Telegram credentials interactively"""
    print("🔧 SETUP CREDENTIALS TELEGRAM\n")

    print("📋 Untuk menggunakan sistem ini, Anda membutuhkan:")
    print("1. 📱 Telegram API ID & Hash dari https://my.telegram.org")
    print("   - Login dengan nomor telepon Anda")
    print("   - Pilih 'API Development Tools'")
    print("   - Buat aplikasi baru dan catat API ID & Hash")
    print("")
    print("2. 🤖 Bot Token dari @BotFather")
    print("   - Kirim /newbot ke @BotFather di Telegram")
    print("   - Ikuti instruksi dan catat Bot Token")
    print("")
    print("3. 📞 Nomor telepon untuk userbot (sama dengan yang digunakan untuk API)")
    print("")

    max_attempts = 3
    for attempt in range(max_attempts):
        print(f"📝 Percobaan {attempt + 1}/{max_attempts}")
        print("-" * 40)

        # Get credentials
        api_id = input("Masukkan TELEGRAM_API_ID (8 digit): ").strip()
        api_hash = input("Masukkan TELEGRAM_API_HASH (32 karakter): ").strip()
        bot_token = input("Masukkan TELEGRAM_BOT_TOKEN: ").strip()
        phone_number = input("Masukkan TELEGRAM_PHONE_NUMBER (format: +628123456789): ").strip()

        # Validate inputs
        if not all([api_id, api_hash, bot_token, phone_number]):
            print("\n❌ Semua field harus diisi!")
            if attempt < max_attempts - 1:
                print("Silakan coba lagi...\n")
                continue
            else:
                return False

        # Validate formats
        is_valid, error_msg = validate_credentials(api_id, api_hash, bot_token, phone_number)

        if not is_valid:
            print(f"\n❌ {error_msg}")
            if attempt < max_attempts - 1:
                print("Silakan coba lagi...\n")
                continue
            else:
                return False

        # Update .env file
        env_path = Path(__file__).parent.parent / ".env"

        try:
            # Read current content
            env_content = env_path.read_text()

            # Replace credentials
            replacements = {
                "TELEGRAM_API_ID": api_id,
                "TELEGRAM_API_HASH": api_hash,
                "TELEGRAM_BOT_TOKEN": bot_token,
                "TELEGRAM_PHONE_NUMBER": phone_number,
            }

            for key, value in replacements.items():
                # Find the line and replace it
                lines = env_content.split("\n")
                for i, line in enumerate(lines):
                    if line.strip().startswith(f"{key}="):
                        lines[i] = f"{key}={value}"
                        break
                env_content = "\n".join(lines)

            env_path.write_text(env_content)

            print("\n✅ Credentials berhasil disimpan ke .env file!")
            print("\n📋 Ringkasan konfigurasi:")
            print(f"  • API ID: {api_id}")
            print(f"  • API Hash: {api_hash[:8]}...{api_hash[-4:]}")
            print(f"  • Bot Token: {bot_token[:15]}...")
            print(f"  • Phone: {phone_number}")

            return True

        except Exception as e:
            print(f"\n❌ Error menyimpan ke .env file: {e}")
            return False

    return False


def run_health_check():
    """Run health check to verify setup"""
    print("\n🩺 MENJALANKAN HEALTH CHECK...\n")

    try:
        # Run health check script
        health_script = Path(__file__).parent / "health_check.py"

        if health_script.exists():
            import subprocess

            result = subprocess.run(
                [sys.executable, str(health_script)], capture_output=True, text=True
            )

            print(result.stdout)
            if result.stderr:
                print("⚠️ Warnings/Errors:")
                print(result.stderr)

            return result.returncode == 0
        else:
            print("⚠️ Health check script tidak ditemukan")
            return True

    except Exception as e:
        print(f"❌ Error running health check: {e}")
        return False


def run_system():
    """Run the telegram automation system"""
    print("\n🚀 MENJALANKAN SISTEM...\n")
    print("Sistem akan:")
    print("1. 🔗 Koneksi ke database MongoDB")
    print("2. 🤖 Start management bot")
    print("3. 📱 Start userbot (akan minta OTP jika pertama kali)")
    print("4. 🔄 Mulai broadcasting loop")
    print("\n⚠️ PENTING:")
    print("- Pastikan MongoDB sudah running (mongod)")
    print("- Siapkan kode OTP dari Telegram")
    print("- Jika ada 2FA, siapkan password nya")
    print("")

    choice = input("Lanjutkan menjalankan sistem? (y/n): ").strip().lower()

    if choice != "y":
        print("Setup selesai. Jalankan sistem dengan: python main.py")
        return

    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from main import main
        import asyncio

        print("\n" + "=" * 50)
        print("🚀 STARTING TELEGRAM AUTOMATION SYSTEM...")
        print("=" * 50 + "\n")

        asyncio.run(main())

    except KeyboardInterrupt:
        print("\n👋 Sistem dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error menjalankan sistem: {e}")
        print("\n🔍 Troubleshooting:")
        print("- Pastikan MongoDB running: sudo systemctl status mongod")
        print("- Periksa credentials di .env file")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Jalankan health check: python scripts/health_check.py")


def main():
    """Main setup function"""
    print_banner()

    # Check if .env exists and validate fields
    missing_fields = check_env_file()

    if missing_fields:
        print(f"❌ Field berikut masih kosong di .env:")
        for field in missing_fields:
            print(f"  • {field}")
        print("")

        choice = input("Ingin setup credentials sekarang? (y/n): ").strip().lower()

        if choice == "y":
            if not setup_credentials():
                print("\n❌ Setup credentials gagal. Silakan coba lagi.")
                sys.exit(1)
        else:
            print("\n📝 Silakan isi file .env secara manual dengan credentials Telegram Anda.")
            print("\n📋 Format yang dibutuhkan:")
            print("TELEGRAM_API_ID=12345678")
            print("TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890")
            print("TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
            print("TELEGRAM_PHONE_NUMBER=+628123456789")
            print("\n💡 Lihat .env.example untuk referensi lengkap")
            sys.exit(0)
    else:
        print("✅ File .env sudah lengkap!\n")

    # Run health check
    print("🔍 Memverifikasi setup...")
    health_ok = run_health_check()

    if not health_ok:
        print("\n⚠️ Ada beberapa masalah dalam setup. Periksa error di atas.")
        choice = input("Tetap lanjutkan menjalankan sistem? (y/n): ").strip().lower()
        if choice != "y":
            print("Setup dibatalkan. Perbaiki masalah terlebih dahulu.")
            sys.exit(1)

    # Ask if user wants to run the system
    choice = input("\nIngin menjalankan sistem sekarang? (y/n): ").strip().lower()

    if choice == "y":
        run_system()
    else:
        print("\n🎉 Setup selesai!")
        print("\n📚 Langkah selanjutnya:")
        print("1. Jalankan sistem: python main.py")
        print("2. Buka bot di Telegram dan kirim /start")
        print("3. Gunakan /menu untuk mengelola sistem")
        print("\n📖 Baca README.md untuk panduan lengkap")


if __name__ == "__main__":
    main()
