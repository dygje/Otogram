#!/usr/bin/env python3
"""
Quick CI test to verify all commands work as expected
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd: str, description: str) -> bool:
    """Run a command and return success status"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd="/app")
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Test all CI commands"""
    print("🚀 TESTING CI COMMANDS")
    print("=" * 50)
    
    commands = [
        ("ruff check src/ scripts/ tests/", "Ruff linting"),
        ("ruff format --check src/ scripts/ tests/", "Ruff formatting"),  
        ("mypy src/ scripts/", "MyPy type checking"),
        ("pytest tests/ -v --cov=src --cov-report=xml --cov-fail-under=15", "Pytest with coverage"),
        ("python scripts/health_check.py", "Health check"),
    ]
    
    passed = 0
    total = len(commands)
    
    for cmd, desc in commands:
        if run_command(cmd, desc):
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTS: {passed}/{total} commands passed")
    
    if passed == total:
        print("🎉 ALL CI COMMANDS WORK - CI SHOULD PASS!")
        return 0
    else:
        print("⚠️  Some commands failed - CI may still have issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())