"""
Persona management system for configurable user profiles
"""

import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Persona:
    """Represents a user persona with specific configuration"""
    
    id: str
    name: str
    user_agent: str
    accept_language: str
    timezone: str
    screen_resolution: str
    color_depth: int
    javascript_enabled: bool
    plugins_enabled: bool
    webgl_enabled: bool
    canvas_fingerprinting_protection: bool
    audio_fingerprinting_protection: bool
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert persona to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Persona':
        """Create persona from dictionary"""
        return cls(**data)


class PersonaManager:
    """Manages user personas for the shell"""
    
    def __init__(self, personas_dir: Path):
        self.personas_dir = personas_dir
        self.personas_dir.mkdir(exist_ok=True)
        self._personas = {}
        self._load_personas()
        self._ensure_default_personas()
    
    def _load_personas(self):
        """Load all personas from disk"""
        for persona_file in self.personas_dir.glob("*.json"):
            try:
                with open(persona_file, 'r') as f:
                    data = json.load(f)
                    persona = Persona.from_dict(data)
                    self._personas[persona.id] = persona
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Failed to load persona {persona_file}: {e}")
    
    def _ensure_default_personas(self):
        """Create default personas if none exist"""
        if not self._personas:
            self._create_default_personas()
    
    def _create_default_personas(self):
        """Create a set of default personas"""
        default_personas = [
            {
                "id": "anonymous",
                "name": "Anonymous",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "accept_language": "en-US,en;q=0.9",
                "timezone": "UTC",
                "screen_resolution": "1920x1080",
                "color_depth": 24,
                "javascript_enabled": True,
                "plugins_enabled": False,
                "webgl_enabled": False,
                "canvas_fingerprinting_protection": True,
                "audio_fingerprinting_protection": True,
                "description": "Basic anonymous browsing persona"
            },
            {
                "id": "researcher",
                "name": "Security Researcher",
                "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "accept_language": "en-US,en;q=0.9",
                "timezone": "UTC",
                "screen_resolution": "1366x768",
                "color_depth": 24,
                "javascript_enabled": True,
                "plugins_enabled": False,
                "webgl_enabled": False,
                "canvas_fingerprinting_protection": True,
                "audio_fingerprinting_protection": True,
                "description": "Research-focused persona with enhanced privacy"
            },
            {
                "id": "stealth",
                "name": "Maximum Stealth",
                "user_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
                "accept_language": "en-US,en;q=0.5",
                "timezone": "UTC",
                "screen_resolution": "1024x768",
                "color_depth": 16,
                "javascript_enabled": False,
                "plugins_enabled": False,
                "webgl_enabled": False,
                "canvas_fingerprinting_protection": True,
                "audio_fingerprinting_protection": True,
                "description": "Maximum privacy and anonymity settings"
            }
        ]
        
        for persona_data in default_personas:
            persona = Persona.from_dict(persona_data)
            self.save_persona(persona)
    
    def get_persona(self, persona_id: str) -> Optional[Persona]:
        """Get a persona by ID"""
        return self._personas.get(persona_id)
    
    def list_personas(self) -> List[Persona]:
        """Get all available personas"""
        return list(self._personas.values())
    
    def save_persona(self, persona: Persona):
        """Save a persona to disk"""
        self._personas[persona.id] = persona
        
        persona_file = self.personas_dir / f"{persona.id}.json"
        try:
            with open(persona_file, 'w') as f:
                json.dump(persona.to_dict(), f, indent=2)
        except IOError as e:
            print(f"Failed to save persona {persona.id}: {e}")
    
    def delete_persona(self, persona_id: str) -> bool:
        """Delete a persona"""
        if persona_id in self._personas:
            del self._personas[persona_id]
            
            persona_file = self.personas_dir / f"{persona_id}.json"
            if persona_file.exists():
                try:
                    persona_file.unlink()
                    return True
                except IOError as e:
                    print(f"Failed to delete persona file {persona_id}: {e}")
        
        return False
    
    def create_persona(self, name: str, **kwargs) -> Persona:
        """Create a new persona"""
        persona_id = str(uuid.uuid4())
        
        # Default values
        defaults = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "accept_language": "en-US,en;q=0.9",
            "timezone": "UTC",
            "screen_resolution": "1920x1080",
            "color_depth": 24,
            "javascript_enabled": True,
            "plugins_enabled": False,
            "webgl_enabled": False,
            "canvas_fingerprinting_protection": True,
            "audio_fingerprinting_protection": True,
            "description": ""
        }
        
        # Override with provided kwargs
        defaults.update(kwargs)
        
        persona = Persona(
            id=persona_id,
            name=name,
            **defaults
        )
        
        self.save_persona(persona)
        return persona