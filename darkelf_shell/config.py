"""
Configuration management for Darkelf Shell
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Manages configuration settings for Darkelf Shell"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".darkelf_shell"
        self.config_file = self.config_dir / "config.json"
        self.personas_dir = self.config_dir / "personas"
        self.sessions_dir = self.config_dir / "sessions"
        
        self._ensure_directories()
        self._config = self._load_config()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        self.config_dir.mkdir(exist_ok=True)
        self.personas_dir.mkdir(exist_ok=True)
        self.sessions_dir.mkdir(exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Return default configuration
        return {
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
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            print(f"Failed to save configuration: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    @property
    def tor_enabled(self) -> bool:
        return self.get('tor.enabled', True)
    
    @property
    def socks_port(self) -> int:
        return self.get('tor.socks_port', 9050)
    
    @property
    def panic_key(self) -> str:
        return self.get('security.panic_key', 'Ctrl+Shift+P')