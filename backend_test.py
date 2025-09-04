#!/usr/bin/env python3
"""
Telegram Bot System Testing
Tests the Otogram Telegram Automation System
"""

import asyncio
import sys
import time
from datetime import datetime
from pathlib import Path

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

import requests
from loguru import logger

# Telegram Bot API Configuration
BOT_TOKEN = "8118820592:AAFX05zaXmmW3nWY2pM7s90Pbqn8f1ptc0M"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Test Chat ID (you can use your own chat ID for testing)
# For now, we'll test basic bot connectivity without sending messages
TEST_CHAT_ID = None  # Will be set if we find a chat


class TelegramBotTester:
    """Test Telegram Bot functionality"""

    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.bot_info = None
        self.test_chat_id = None

    def run_test(self, name: str, test_func, *args, **kwargs):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            result = test_func(*args, **kwargs)
            if result:
                self.tests_passed += 1
                print(f"✅ Passed - {name}")
                return True
            else:
                print(f"❌ Failed - {name}")
                return False
        except Exception as e:
            print(f"❌ Failed - {name}: {str(e)}")
            return False

    def test_bot_connectivity(self):
        """Test if bot is accessible via Telegram API"""
        try:
            response = requests.get(f"{BASE_URL}/getMe", timeout=10)
            if response.status_code == 200:
                self.bot_info = response.json()
                if self.bot_info.get('ok'):
                    bot_data = self.bot_info['result']
                    print(f"   Bot Name: {bot_data.get('first_name', 'Unknown')}")
                    print(f"   Username: @{bot_data.get('username', 'Unknown')}")
                    print(f"   Bot ID: {bot_data.get('id', 'Unknown')}")
                    return True
            return False
        except Exception as e:
            print(f"   Connection error: {e}")
            return False

    def test_bot_commands(self):
        """Test if bot has proper command setup"""
        try:
            response = requests.get(f"{BASE_URL}/getMyCommands", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    commands = data.get('result', [])
                    print(f"   Commands configured: {len(commands)}")
                    for cmd in commands[:5]:  # Show first 5 commands
                        print(f"   - /{cmd.get('command')}: {cmd.get('description')}")
                    return True
            return False
        except Exception as e:
            print(f"   Error getting commands: {e}")
            return False

    def test_webhook_info(self):
        """Check webhook configuration"""
        try:
            response = requests.get(f"{BASE_URL}/getWebhookInfo", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    webhook_info = data.get('result', {})
                    webhook_url = webhook_info.get('url', '')
                    if webhook_url:
                        print(f"   Webhook URL: {webhook_url}")
                        print(f"   Pending updates: {webhook_info.get('pending_update_count', 0)}")
                    else:
                        print("   No webhook configured (using polling)")
                    return True
            return False
        except Exception as e:
            print(f"   Error getting webhook info: {e}")
            return False

    def test_recent_updates(self):
        """Check for recent bot updates/messages"""
        try:
            response = requests.get(f"{BASE_URL}/getUpdates?limit=5", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    updates = data.get('result', [])
                    print(f"   Recent updates: {len(updates)}")
                    
                    # Look for a test chat ID from recent updates
                    for update in updates:
                        if 'message' in update:
                            chat_id = update['message']['chat']['id']
                            if not self.test_chat_id:
                                self.test_chat_id = chat_id
                                print(f"   Found test chat ID: {chat_id}")
                    
                    return True
            return False
        except Exception as e:
            print(f"   Error getting updates: {e}")
            return False

    def test_system_logs(self):
        """Check system logs for errors"""
        try:
            log_file = Path("/app/logs/app.log")
            if log_file.exists():
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                
                recent_lines = lines[-20:]  # Last 20 lines
                error_count = sum(1 for line in recent_lines if 'ERROR' in line)
                warning_count = sum(1 for line in recent_lines if 'WARNING' in line)
                
                print(f"   Recent log lines: {len(recent_lines)}")
                print(f"   Errors in recent logs: {error_count}")
                print(f"   Warnings in recent logs: {warning_count}")
                
                # Show recent errors if any
                if error_count > 0:
                    print("   Recent errors:")
                    for line in recent_lines:
                        if 'ERROR' in line:
                            print(f"     {line.strip()}")
                
                return error_count == 0  # Pass if no errors
            else:
                print("   Log file not found")
                return False
        except Exception as e:
            print(f"   Error reading logs: {e}")
            return False

    def test_database_connectivity(self):
        """Test MongoDB connectivity indirectly through logs"""
        try:
            log_file = Path("/app/logs/app.log")
            if log_file.exists():
                with open(log_file, 'r') as f:
                    content = f.read()
                
                # Look for database connection messages
                if "✅ Connected to MongoDB" in content:
                    print("   Database connection confirmed in logs")
                    return True
                elif "❌" in content and "database" in content.lower():
                    print("   Database connection issues found in logs")
                    return False
                else:
                    print("   No clear database status in logs")
                    return False
            return False
        except Exception as e:
            print(f"   Error checking database logs: {e}")
            return False

    def test_system_process(self):
        """Test if system process is running"""
        try:
            import subprocess
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if 'main.py' in result.stdout:
                # Extract PID
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'main.py' in line and 'python' in line:
                        parts = line.split()
                        if len(parts) > 1:
                            pid = parts[1]
                            print(f"   System running with PID: {pid}")
                            return True
            print("   System process not found")
            return False
        except Exception as e:
            print(f"   Error checking process: {e}")
            return False

    def test_configuration_validity(self):
        """Test if configuration is valid"""
        try:
            from src.core.config import settings
            
            print(f"   API ID configured: {'Yes' if settings.TELEGRAM_API_ID else 'No'}")
            print(f"   API Hash configured: {'Yes' if settings.TELEGRAM_API_HASH else 'No'}")
            print(f"   Bot Token configured: {'Yes' if settings.TELEGRAM_BOT_TOKEN else 'No'}")
            print(f"   Phone Number configured: {'Yes' if settings.TELEGRAM_PHONE_NUMBER else 'No'}")
            
            return settings.is_configured()
        except Exception as e:
            print(f"   Error checking configuration: {e}")
            return False

    def run_all_tests(self):
        """Run all tests"""
        print("🤖 OTOGRAM TELEGRAM AUTOMATION SYSTEM TESTING")
        print("=" * 50)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Core connectivity tests
        self.run_test("Bot API Connectivity", self.test_bot_connectivity)
        self.run_test("Bot Commands Setup", self.test_bot_commands)
        self.run_test("Webhook Configuration", self.test_webhook_info)
        self.run_test("Recent Bot Updates", self.test_recent_updates)
        
        # System health tests
        self.run_test("System Process Status", self.test_system_process)
        self.run_test("Configuration Validity", self.test_configuration_validity)
        self.run_test("Database Connectivity", self.test_database_connectivity)
        self.run_test("System Logs Check", self.test_system_logs)
        
        # Print results
        print(f"\n📊 TEST RESULTS")
        print("=" * 30)
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_run - self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 ALL TESTS PASSED! System is healthy.")
            return 0
        else:
            print(f"\n⚠️  {self.tests_run - self.tests_passed} tests failed. Check issues above.")
            return 1


def main():
    """Main test function"""
    tester = TelegramBotTester()
    return tester.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())