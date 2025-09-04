#!/usr/bin/env python3
"""
Personal Setup Wizard - Otogram Configuration
Simple credential setup for personal Telegram automation
"""

import sys
from pathlib import Path


def print_banner() -> None:
    """Simple setup banner"""
    print("\n" + "=" * 40)
    print("🤖 OTOGRAM - PERSONAL SETUP")
    print("=" * 40)
    print("Quick setup for Telegram automation")
    print("=" * 40 + "\n")


def check_env_file() -> bool:
    """Ensure .env file exists"""
    env_path = Path(__file__).parent.parent / ".env"

    if not env_path.exists():
        print("❌ No .env file found!")

        # Try to copy from example
        example_path = env_path.parent / ".env.example"
        if example_path.exists():
            import shutil

            shutil.copy2(example_path, env_path)
            print("✅ Created .env from example")
        else:
            print("❌ No .env.example found either!")
            print("💡 Create .env file manually with your credentials")
            return False

    print("✅ .env file exists")
    return True


def setup_credentials() -> bool:
    """Interactive credential setup"""
    print("🔧 CREDENTIAL SETUP\n")

    print("📋 You need:")
    print("1. API ID & Hash from https://my.telegram.org")
    print("2. Bot Token from @BotFather")
    print("3. Your phone number\n")

    # Get credentials
    api_id = input("TELEGRAM_API_ID: ").strip()
    api_hash = input("TELEGRAM_API_HASH: ").strip()
    bot_token = input("TELEGRAM_BOT_TOKEN: ").strip()
    phone = input("PHONE NUMBER (+country code): ").strip()

    if not all([api_id, api_hash, bot_token, phone]):
        print("\n❌ All fields required!")
        return False

    # Validate phone format
    if not phone.startswith("+"):
        print("⚠️ Adding + to phone number")
        phone = "+" + phone.lstrip("+")

    # Update .env file
    env_path = Path(__file__).parent.parent / ".env"
    try:
        env_content = env_path.read_text()

        # Simple find/replace
        replacements = {
            "TELEGRAM_API_ID=12345678": f"TELEGRAM_API_ID={api_id}",
            "TELEGRAM_API_HASH=your_api_hash": f"TELEGRAM_API_HASH={api_hash}",
            "TELEGRAM_BOT_TOKEN=your_bot_token": f"TELEGRAM_BOT_TOKEN={bot_token}",
            "TELEGRAM_PHONE_NUMBER=+628123456789": f"TELEGRAM_PHONE_NUMBER={phone}",
        }

        for old, new in replacements.items():
            env_content = env_content.replace(old, new)

        env_path.write_text(env_content)
        print("\n✅ Credentials saved to .env!")
        return True

    except Exception as e:
        print(f"\n❌ Failed to update .env: {e}")
        print("💡 Please edit .env file manually")
        return False


def run_health_check() -> None:
    """Run health check if available"""
    print("\n🩺 Running health check...")

    try:
        health_script = Path(__file__).parent / "health_check.py"
        if health_script.exists():
            import subprocess

            result = subprocess.run([sys.executable, str(health_script)])
            if result.returncode != 0:
                print("⚠️ Some issues found - check output above")
        else:
            print("⚠️ Health check script not found")
    except Exception as e:
        print(f"❌ Health check error: {e}")


def main() -> None:
    """Main setup wizard"""
    print_banner()

    # Check/create .env
    if not check_env_file():
        sys.exit(1)

    # Credential setup
    setup_choice = input("Setup credentials now? (y/n): ").strip().lower()

    if setup_choice == "y":
        if not setup_credentials():
            print("\n❌ Setup failed - edit .env manually")
            sys.exit(1)
    else:
        print("\n📝 Remember to edit .env with your credentials!")

    # Health check
    run_health_check()

    print("\n🎉 Setup complete!")
    print("\n📚 Next steps:")
    print("1. Start system: python main.py")
    print("2. Find your bot on Telegram")
    print("3. Send /start to begin")
    print("\n💡 Use 'make health' to check system anytime")


if __name__ == "__main__":
    main()
