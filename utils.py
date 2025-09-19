#!/usr/bin/env python3
"""
Utility script for Darkelf Shell testing and configuration
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up"""
    print("=== Darkelf Shell Environment Check ===\n")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version OK")
    
    # Check required packages
    required_packages = ['PyQt6', 'PyQt6.QtWebEngineWidgets', 'sqlite3', 'json']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} not available")
            missing_packages.append(package)
    
    # Check Tor availability
    tor_available = os.system("which tor > /dev/null 2>&1") == 0
    if tor_available:
        print("✅ Tor executable found")
    else:
        print("⚠️  Tor executable not found")
    
    # Check configuration directory
    config_dir = Path.home() / ".darkelf_shell"
    print(f"\nConfiguration directory: {config_dir}")
    
    if config_dir.exists():
        print("✅ Config directory exists")
    else:
        print("⚠️  Config directory will be created on first run")
    
    print(f"\nMissing packages: {missing_packages if missing_packages else 'None'}")
    
    return len(missing_packages) == 0

def create_sample_config():
    """Create sample configuration files"""
    config_dir = Path.home() / ".darkelf_shell"
    config_dir.mkdir(exist_ok=True)
    
    # Create sample main config
    config_file = config_dir / "config.json"
    sample_config = {
        "tor": {
            "enabled": True,
            "socks_port": 9050,
            "control_port": 9051,
            "auto_start": False
        },
        "security": {
            "panic_key": "Ctrl+Shift+P",
            "clear_history_on_exit": True,
            "disable_javascript": False,
            "disable_plugins": True
        },
        "ui": {
            "theme": "dark",
            "show_status_bar": True,
            "tab_position": "top"
        },
        "default_persona": "anonymous"
    }
    
    with open(config_file, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print(f"✅ Created sample config: {config_file}")
    
    # Create personas directory
    personas_dir = config_dir / "personas"
    personas_dir.mkdir(exist_ok=True)
    print(f"✅ Created personas directory: {personas_dir}")
    
    # Create sessions directory
    sessions_dir = config_dir / "sessions"
    sessions_dir.mkdir(exist_ok=True)
    print(f"✅ Created sessions directory: {sessions_dir}")

def cleanup_data():
    """Clean up all Darkelf Shell data"""
    config_dir = Path.home() / ".darkelf_shell"
    
    if not config_dir.exists():
        print("No data to clean up")
        return
    
    print("⚠️  This will delete ALL Darkelf Shell data!")
    response = input("Are you sure? (yes/no): ")
    
    if response.lower() == 'yes':
        import shutil
        shutil.rmtree(config_dir)
        print("✅ All data cleaned up")
    else:
        print("Cleanup cancelled")

def list_sessions():
    """List all saved sessions"""
    config_dir = Path.home() / ".darkelf_shell"
    sessions_db = config_dir / "sessions.db"
    
    if not sessions_db.exists():
        print("No sessions database found")
        return
    
    try:
        with sqlite3.connect(sessions_db) as conn:
            cursor = conn.execute("""
                SELECT id, name, persona_id, created_at, last_accessed,
                       (SELECT COUNT(*) FROM tabs WHERE session_id = sessions.id) as tab_count
                FROM sessions
                ORDER BY last_accessed DESC
            """)
            
            sessions = cursor.fetchall()
            
            if not sessions:
                print("No sessions found")
                return
            
            print("\n=== Saved Sessions ===")
            print("ID\t\tName\t\tPersona\t\tTabs\tLast Accessed")
            print("-" * 80)
            
            for session in sessions:
                session_id, name, persona_id, created_at, last_accessed, tab_count = session
                print(f"{session_id[:8]}...\t{name[:15]}\t{persona_id[:10]}\t{tab_count}\t{last_accessed[:19]}")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def test_tor_connection():
    """Test Tor connection"""
    import socket
    try:
        import socks
    except ImportError:
        print("❌ PySocks not available. Install with: pip install PySocks")
        return False
    
    print("Testing Tor connection...")
    
    try:
        # Test SOCKS proxy connection
        s = socks.socksocket()
        s.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        s.settimeout(10)
        
        # Try to connect to check.torproject.org
        s.connect(("check.torproject.org", 80))
        s.close()
        
        print("✅ Tor connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Tor connection failed: {e}")
        print("Make sure Tor is running: sudo systemctl start tor")
        return False

def main():
    """Main utility function"""
    if len(sys.argv) < 2:
        print("Darkelf Shell Utility")
        print("\nUsage:")
        print("  python utils.py check      - Check environment")
        print("  python utils.py config     - Create sample config")
        print("  python utils.py sessions   - List saved sessions")
        print("  python utils.py cleanup    - Clean up all data")
        print("  python utils.py test-tor   - Test Tor connection")
        return
    
    command = sys.argv[1].lower()
    
    if command == "check":
        check_environment()
    elif command == "config":
        create_sample_config()
    elif command == "sessions":
        list_sessions()
    elif command == "cleanup":
        cleanup_data()
    elif command == "test-tor":
        test_tor_connection()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()