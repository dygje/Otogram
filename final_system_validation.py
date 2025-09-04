#!/usr/bin/env python3
"""
Final System Validation for Otogram Telegram Automation System
Tests the actual running system without interfering with it
"""

import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

import requests

# Configuration
BOT_TOKEN = "8118820592:AAFX05zaXmmW3nWY2pM7s90Pbqn8f1ptc0M"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


class FinalSystemValidator:
    """Final validation of the running system"""

    def __init__(self):
        self.results = {
            'bot_connectivity': False,
            'system_running': False,
            'database_connected': False,
            'no_critical_errors': False,
            'system_stable': False
        }
        self.details = {}

    def validate_bot_connectivity(self):
        """Validate Telegram bot connectivity and commands"""
        print("🔍 Validating Bot Connectivity...")
        
        try:
            # Test bot API
            response = requests.get(f"{BASE_URL}/getMe", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data['result']
                    self.results['bot_connectivity'] = True
                    self.details['bot_info'] = {
                        'name': bot_info.get('first_name'),
                        'username': bot_info.get('username'),
                        'id': bot_info.get('id'),
                        'can_join_groups': bot_info.get('can_join_groups'),
                    }
                    print(f"   ✅ Bot @{bot_info.get('username')} is accessible and responsive")
                    return True
            
            print("   ❌ Bot not accessible")
            return False
            
        except Exception as e:
            print(f"   ❌ Bot connectivity error: {e}")
            return False

    def validate_system_running(self):
        """Validate system process is running"""
        print("🔍 Validating System Process...")
        
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            
            if 'main.py' in result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'main.py' in line and 'python' in line:
                        parts = line.split()
                        if len(parts) > 1:
                            pid = parts[1]
                            self.results['system_running'] = True
                            self.details['system_pid'] = pid
                            print(f"   ✅ System running with PID {pid}")
                            return True
            
            print("   ❌ System process not found")
            return False
            
        except Exception as e:
            print(f"   ❌ Error checking system process: {e}")
            return False

    def validate_database_connection(self):
        """Validate database connection from logs"""
        print("🔍 Validating Database Connection...")
        
        try:
            log_file = Path("/app/logs/app.log")
            if log_file.exists():
                with open(log_file, 'r') as f:
                    content = f.read()
                
                # Look for recent database connection
                recent_lines = content.split('\n')[-50:]  # Last 50 lines
                
                db_connected = False
                for line in recent_lines:
                    if "✅ Connected to MongoDB: otogram" in line:
                        db_connected = True
                        break
                
                if db_connected:
                    self.results['database_connected'] = True
                    print("   ✅ MongoDB connection confirmed")
                    return True
                else:
                    print("   ❌ No recent MongoDB connection found")
                    return False
            else:
                print("   ❌ Log file not found")
                return False
                
        except Exception as e:
            print(f"   ❌ Error checking database connection: {e}")
            return False

    def validate_no_critical_errors(self):
        """Validate no critical errors in recent logs"""
        print("🔍 Validating System Health...")
        
        try:
            log_file = Path("/app/logs/app.log")
            if log_file.exists():
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                
                # Check last 30 lines for errors
                recent_lines = lines[-30:]
                errors = [line for line in recent_lines if 'ERROR' in line]
                
                if len(errors) == 0:
                    self.results['no_critical_errors'] = True
                    print("   ✅ No critical errors in recent logs")
                    return True
                else:
                    print(f"   ❌ {len(errors)} errors found in recent logs")
                    for error in errors[-3:]:  # Show last 3 errors
                        print(f"      {error.strip()}")
                    return False
            else:
                print("   ❌ Log file not found")
                return False
                
        except Exception as e:
            print(f"   ❌ Error checking logs: {e}")
            return False

    def validate_system_stability(self):
        """Validate system stability and readiness"""
        print("🔍 Validating System Stability...")
        
        try:
            log_file = Path("/app/logs/app.log")
            if log_file.exists():
                with open(log_file, 'r') as f:
                    content = f.read()
                
                # Look for system readiness indicators
                indicators = [
                    "✅ Telegram services started",
                    "🎯 System ready!",
                    "Management bot is running"
                ]
                
                found_indicators = 0
                for indicator in indicators:
                    if indicator in content:
                        found_indicators += 1
                
                if found_indicators >= 2:
                    self.results['system_stable'] = True
                    print(f"   ✅ System stable ({found_indicators}/3 indicators found)")
                    return True
                else:
                    print(f"   ❌ System stability unclear ({found_indicators}/3 indicators)")
                    return False
            else:
                print("   ❌ Log file not found")
                return False
                
        except Exception as e:
            print(f"   ❌ Error checking system stability: {e}")
            return False

    def run_validation(self):
        """Run complete system validation"""
        print("🤖 FINAL OTOGRAM SYSTEM VALIDATION")
        print("=" * 50)
        print(f"Validation started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all validations
        validations = [
            ("Bot Connectivity", self.validate_bot_connectivity),
            ("System Process", self.validate_system_running),
            ("Database Connection", self.validate_database_connection),
            ("System Health", self.validate_no_critical_errors),
            ("System Stability", self.validate_system_stability),
        ]
        
        passed = 0
        total = len(validations)
        
        for name, validation_func in validations:
            if validation_func():
                passed += 1
        
        # Print results
        print(f"\n📊 VALIDATION RESULTS")
        print("=" * 30)
        print(f"Validations passed: {passed}/{total}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        
        # System status
        print(f"\n🎯 SYSTEM STATUS:")
        if passed == total:
            print("🟢 EXCELLENT: All validations passed - System fully operational")
        elif passed >= 4:
            print("🟡 GOOD: Most validations passed - System mostly operational")
        elif passed >= 3:
            print("🟠 FAIR: Some validations passed - System partially operational")
        else:
            print("🔴 POOR: Multiple validations failed - System has issues")
        
        # Detailed status
        print(f"\n📋 DETAILED STATUS:")
        status_items = [
            ("Bot API Connectivity", self.results['bot_connectivity']),
            ("System Process Running", self.results['system_running']),
            ("Database Connected", self.results['database_connected']),
            ("No Critical Errors", self.results['no_critical_errors']),
            ("System Stable", self.results['system_stable']),
        ]
        
        for item, status in status_items:
            icon = "✅" if status else "❌"
            print(f"   {icon} {item}")
        
        # Bot details if available
        if 'bot_info' in self.details:
            bot = self.details['bot_info']
            print(f"\n🤖 BOT INFORMATION:")
            print(f"   Name: {bot['name']}")
            print(f"   Username: @{bot['username']}")
            print(f"   ID: {bot['id']}")
            print(f"   Can join groups: {bot['can_join_groups']}")
        
        # System details if available
        if 'system_pid' in self.details:
            print(f"\n⚙️  SYSTEM INFORMATION:")
            print(f"   Process ID: {self.details['system_pid']}")
            print(f"   Status: Running")
        
        # Final recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if passed >= 4:
            print("✅ System is ready for use!")
            print("📱 You can interact with @otogrambot on Telegram")
            print("🚀 Available commands:")
            print("   • /start - Initialize bot interface")
            print("   • /menu - Main dashboard")
            print("   • /help - Show help information")
            print("   • /status - System status")
            print("   • /messages - Manage messages")
            print("   • /groups - Manage groups")
            print("   • /config - System configuration")
        else:
            print("⚠️  System needs attention before use")
            print("🔧 Check failed validations above")
            print("📋 Review system logs for details")
        
        return 0 if passed >= 4 else 1


def main():
    """Main validation function"""
    validator = FinalSystemValidator()
    return validator.run_validation()


if __name__ == "__main__":
    sys.exit(main())