"""
Panic Handler for emergency shutdown and data clearing
"""

import os
import shutil
import sqlite3
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal


class PanicHandler(QObject):
    """Handles panic situations with emergency shutdown and data clearing"""
    
    panic_triggered = pyqtSignal()
    
    @staticmethod
    def panic_shutdown():
        """Emergency shutdown with data clearing"""
        print("PANIC SHUTDOWN INITIATED")
        
        config_dir = Path.home() / ".darkelf_shell"
        
        # Clear browser cache and temporary files
        PanicHandler._clear_browser_data()
        
        # Clear session database
        PanicHandler._clear_sessions(config_dir)
        
        # Clear temporary files
        PanicHandler._clear_temp_files()
        
        print("Panic shutdown complete - sensitive data cleared")
    
    @staticmethod
    def _clear_browser_data():
        """Clear browser cache, cookies, and local storage"""
        # Clear Qt WebEngine cache
        cache_paths = [
            Path.home() / ".cache" / "darkelf_shell",
            Path.home() / ".local" / "share" / "darkelf_shell",
        ]
        
        for cache_path in cache_paths:
            if cache_path.exists():
                try:
                    shutil.rmtree(cache_path)
                    print(f"Cleared cache: {cache_path}")
                except Exception as e:
                    print(f"Failed to clear cache {cache_path}: {e}")
    
    @staticmethod
    def _clear_sessions(config_dir: Path):
        """Clear session database"""
        sessions_db = config_dir / "sessions.db"
        if sessions_db.exists():
            try:
                sessions_db.unlink()
                print("Cleared sessions database")
            except Exception as e:
                print(f"Failed to clear sessions database: {e}")
    
    @staticmethod
    def _clear_temp_files():
        """Clear temporary files"""
        temp_dirs = [
            Path("/tmp") / "darkelf_shell",
            Path.home() / ".darkelf_shell" / "temp"
        ]
        
        for temp_dir in temp_dirs:
            if temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir)
                    print(f"Cleared temp directory: {temp_dir}")
                except Exception as e:
                    print(f"Failed to clear temp directory {temp_dir}: {e}")
    
    def trigger_panic(self):
        """Trigger panic mode"""
        self.panic_triggered.emit()
        PanicHandler.panic_shutdown()