#!/usr/bin/env python3
"""
Setup Script for Telegram Automation System
Membantu user mengkonfigurasi credentials dan menjalankan sistem
"""
import os
import sys
from pathlib import Path


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("🤖 TELEGRAM AUTOMATION SYSTEM SETUP")
    print("="*60)
    print("Sistem otomatisasi pengiriman pesan massal ke grup Telegram")
    print("dengan manajemen lengkap melalui Telegram Bot.")
    print("="*60 + "\n")


def check_env_file():
    """Check if .env file exists and has required fields"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ File .env tidak ditemukan!")
        return False
    
    # Read .env file
    env_content = env_path.read_text()
    
    required_fields = [
        "TELEGRAM_API_ID",
        "TELEGRAM_API_HASH", 
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_PHONE_NUMBER"
    ]
    
    missing_fields = []
    
    for field in required_fields:
        if f"{field}=" not in env_content or f"{field}=\n" in env_content or f"{field}=" in env_content.split('\n')[-1]:
            # Check if field is empty
            for line in env_content.split('\n'):
                if line.startswith(f"{field}="):
                    value = line.split('=', 1)[1].strip()
                    if not value:
                        missing_fields.append(field)
                    break
            else:
                missing_fields.append(field)
    
    return missing_fields


def setup_credentials():
    """Setup Telegram credentials interactively"""
    print("🔧 SETUP CREDENTIALS TELEGRAM\n")
    
    print("Untuk menggunakan sistem ini, Anda membutuhkan:")
    print("1. 📱 Telegram API ID & Hash dari https://my.telegram.org")
    print("2. 🤖 Bot Token dari @BotFather")
    print("3. 📞 Nomor telepon untuk userbot\n")
    
    # Get credentials
    api_id = input("Masukkan TELEGRAM_API_ID: ").strip()
    api_hash = input("Masukkan TELEGRAM_API_HASH: ").strip()
    bot_token = input("Masukkan TELEGRAM_BOT_TOKEN: ").strip()
    phone_number = input("Masukkan TELEGRAM_PHONE_NUMBER (format: +628123456789): ").strip()
    
    # Validate inputs
    if not all([api_id, api_hash, bot_token, phone_number]):
        print("\n❌ Semua field harus diisi!")
        return False
    
    if not api_id.isdigit():
        print("\n❌ API ID harus berupa angka!")
        return False
    
    if not phone_number.startswith('+'):
        print("\n❌ Nomor telepon harus dimulai dengan + (contoh: +628123456789)")
        return False
    
    # Update .env file
    env_path = Path(".env")
    env_content = env_path.read_text()
    
    # Replace credentials
    env_content = env_content.replace("TELEGRAM_API_ID=", f"TELEGRAM_API_ID={api_id}")
    env_content = env_content.replace("TELEGRAM_API_HASH=", f"TELEGRAM_API_HASH={api_hash}")
    env_content = env_content.replace("TELEGRAM_BOT_TOKEN=", f"TELEGRAM_BOT_TOKEN={bot_token}")
    env_content = env_content.replace("TELEGRAM_PHONE_NUMBER=", f"TELEGRAM_PHONE_NUMBER={phone_number}")
    
    env_path.write_text(env_content)
    
    print("\n✅ Credentials berhasil disimpan ke .env file!")
    return True


def run_system():
    """Run the telegram automation system"""
    print("\n🚀 MENJALANKAN SISTEM...\n")
    print("Sistem akan:")
    print("1. 🔗 Koneksi ke database MongoDB")
    print("2. 🤖 Start management bot")
    print("3. 📱 Start userbot (akan minta OTP)")
    print("4. 🔄 Mulai broadcasting loop\n")
    
    input("Tekan ENTER untuk melanjutkan...")
    
    # Import and run main - Updated untuk reorganisasi
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from main import main
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Sistem dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error menjalankan sistem: {e}")
        print("\nPastikan:")
        print("- MongoDB sedang berjalan")
        print("- Credentials di .env benar")
        print("- Dependencies sudah terinstall (pip install -r requirements.txt)")


def main():
    """Main setup function"""
    print_banner()
    
    # Check if .env exists
    missing_fields = check_env_file()
    
    if missing_fields:
        print(f"❌ Field berikut masih kosong di .env: {', '.join(missing_fields)}\n")
        
        choice = input("Ingin setup credentials sekarang? (y/n): ").strip().lower()
        
        if choice == 'y':
            if not setup_credentials():
                print("\n❌ Setup credentials gagal. Silakan coba lagi.")
                sys.exit(1)
        else:
            print("\n📝 Silakan isi file .env secara manual dengan credentials Telegram Anda.")
            print("Format:")
            print("TELEGRAM_API_ID=12345678")
            print("TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890")
            print("TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
            print("TELEGRAM_PHONE_NUMBER=+628123456789")
            sys.exit(0)
    else:
        print("✅ File .env sudah lengkap!\n")
    
    # Ask if user wants to run the system
    choice = input("Ingin menjalankan sistem sekarang? (y/n): ").strip().lower()
    
    if choice == 'y':
        run_system()
    else:
        print("\n📚 Untuk menjalankan sistem nanti, gunakan:")
        print("python main.py")
        print("\n📖 Baca README.md untuk panduan lengkap")


if __name__ == "__main__":
    main()