#!/usr/bin/env python3
"""
Simple Setup Script for Personal Telegram Automation
Quick credential setup and system verification
"""

import sys
from pathlib import Path


def print_banner() -> None:
    """Print simple banner"""
    print("\n" + "=" * 50)
    print("🤖 OTOGRAM - PERSONAL SETUP")
    print("=" * 50)
    print("Simple Telegram automation for personal use")
    print("=" * 50 + "\n")


def check_env_file() -> bool:
    """Check if .env file exists and has basic credentials"""
    env_path = Path(__file__).parent.parent / ".env"

    if not env_path.exists():
        print("❌ File .env tidak ditemukan!")
        print("💡 Menyalin dari .env.example...")

        example_path = env_path.parent / ".env.example"
        if example_path.exists():
            import shutil
            shutil.copy2(example_path, env_path)
            print("✅ File .env berhasil dibuat!")
        else:
            print("❌ File .env.example tidak ditemukan!")
            return False

    print("✅ File .env ditemukan")
    return True


def setup_credentials() -> bool:
    """Simple credential setup"""
    print("🔧 SETUP CREDENTIALS\n")
    
    print("📋 Yang dibutuhkan:")
    print("1. Telegram API ID & Hash dari https://my.telegram.org")
    print("2. Bot Token dari @BotFather")
    print("3. Nomor telepon Anda\n")

    # Simple input
    api_id = input("TELEGRAM_API_ID: ").strip()
    api_hash = input("TELEGRAM_API_HASH: ").strip()
    bot_token = input("TELEGRAM_BOT_TOKEN: ").strip()
    phone = input("TELEGRAM_PHONE_NUMBER (contoh: +628123456789): ").strip()

    if not all([api_id, api_hash, bot_token, phone]):
        print("\n❌ Semua field harus diisi!")
        return False

    # Update .env file
    env_path = Path(__file__).parent.parent / ".env"
    try:
        env_content = env_path.read_text()
        
        # Simple replacements
        env_content = env_content.replace("TELEGRAM_API_ID=12345678", f"TELEGRAM_API_ID={api_id}")
        env_content = env_content.replace("TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890", f"TELEGRAM_API_HASH={api_hash}")
        env_content = env_content.replace("TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11", f"TELEGRAM_BOT_TOKEN={bot_token}")
        env_content = env_content.replace("TELEGRAM_PHONE_NUMBER=+628123456789", f"TELEGRAM_PHONE_NUMBER={phone}")
        
        env_path.write_text(env_content)
        print("\n✅ Credentials berhasil disimpan!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def run_health_check() -> bool:
    """Simple health check"""
    print("\n🩺 Menjalankan health check...")
    
    try:
        health_script = Path(__file__).parent / "health_check.py"
        if health_script.exists():
            import subprocess
            result = subprocess.run([sys.executable, str(health_script)], check=False)
            return result.returncode == 0
        else:
            print("⚠️ Health check script tidak ditemukan")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main() -> None:
    """Simple main setup"""
    print_banner()

    # Check .env
    if not check_env_file():
        sys.exit(1)

    # Ask for credential setup
    choice = input("Setup credentials sekarang? (y/n): ").strip().lower()
    
    if choice == "y":
        if not setup_credentials():
            print("\n❌ Setup gagal. Edit file .env secara manual.")
            sys.exit(1)
    else:
        print("\n📝 Edit file .env secara manual dengan credentials Anda.")

    # Health check
    if run_health_check():
        print("\n🎉 Setup selesai!")
        print("\n📚 Langkah selanjutnya:")
        print("1. Jalankan: python main.py")
        print("2. Buka bot di Telegram dan kirim /start")
    else:
        print("\n⚠️ Ada masalah dalam setup. Periksa konfigurasi.")


if __name__ == "__main__":
    main()