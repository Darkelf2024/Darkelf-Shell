"""
Session management for tab state and browsing history
"""

import sqlite3
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class TabSession:
    """Represents a browser tab session"""
    id: str
    url: str
    title: str
    persona_id: str
    created_at: datetime
    last_accessed: datetime
    history: List[str]
    scroll_position: int = 0
    zoom_factor: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_accessed'] = self.last_accessed.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TabSession':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_accessed'] = datetime.fromisoformat(data['last_accessed'])
        return cls(**data)


@dataclass
class BrowsingSession:
    """Represents a complete browsing session"""
    id: str
    name: str
    persona_id: str
    created_at: datetime
    last_accessed: datetime
    tabs: List[TabSession]
    active_tab: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'persona_id': self.persona_id,
            'created_at': self.created_at.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'tabs': [tab.to_dict() for tab in self.tabs],
            'active_tab': self.active_tab
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BrowsingSession':
        """Create from dictionary"""
        tabs = [TabSession.from_dict(tab_data) for tab_data in data['tabs']]
        return cls(
            id=data['id'],
            name=data['name'],
            persona_id=data['persona_id'],
            created_at=datetime.fromisoformat(data['created_at']),
            last_accessed=datetime.fromisoformat(data['last_accessed']),
            tabs=tabs,
            active_tab=data.get('active_tab')
        )


class SessionManager:
    """Manages browsing sessions and tab persistence"""
    
    def __init__(self, sessions_dir: Path):
        self.sessions_dir = sessions_dir
        self.db_path = sessions_dir / "sessions.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize the session database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    persona_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_accessed TEXT NOT NULL,
                    data TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tabs (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    persona_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_accessed TEXT NOT NULL,
                    history TEXT NOT NULL,
                    scroll_position INTEGER DEFAULT 0,
                    zoom_factor REAL DEFAULT 1.0,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            """)
    
    def save_session(self, session: BrowsingSession):
        """Save a browsing session"""
        with sqlite3.connect(self.db_path) as conn:
            # Save session metadata
            conn.execute("""
                INSERT OR REPLACE INTO sessions 
                (id, name, persona_id, created_at, last_accessed, data)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session.id,
                session.name,
                session.persona_id,
                session.created_at.isoformat(),
                session.last_accessed.isoformat(),
                json.dumps({
                    'active_tab': session.active_tab
                })
            ))
            
            # Clear existing tabs for this session
            conn.execute("DELETE FROM tabs WHERE session_id = ?", (session.id,))
            
            # Save tabs
            for tab in session.tabs:
                conn.execute("""
                    INSERT INTO tabs 
                    (id, session_id, url, title, persona_id, created_at, 
                     last_accessed, history, scroll_position, zoom_factor)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    tab.id,
                    session.id,
                    tab.url,
                    tab.title,
                    tab.persona_id,
                    tab.created_at.isoformat(),
                    tab.last_accessed.isoformat(),
                    json.dumps(tab.history),
                    tab.scroll_position,
                    tab.zoom_factor
                ))
    
    def load_session(self, session_id: str) -> Optional[BrowsingSession]:
        """Load a browsing session"""
        with sqlite3.connect(self.db_path) as conn:
            # Load session metadata
            cursor = conn.execute("""
                SELECT name, persona_id, created_at, last_accessed, data
                FROM sessions WHERE id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            name, persona_id, created_at, last_accessed, data = row
            session_data = json.loads(data)
            
            # Load tabs
            cursor = conn.execute("""
                SELECT id, url, title, persona_id, created_at, last_accessed,
                       history, scroll_position, zoom_factor
                FROM tabs WHERE session_id = ?
                ORDER BY created_at
            """, (session_id,))
            
            tabs = []
            for tab_row in cursor.fetchall():
                tab_id, url, title, tab_persona_id, tab_created_at, tab_last_accessed, history, scroll_pos, zoom = tab_row
                
                tab = TabSession(
                    id=tab_id,
                    url=url,
                    title=title,
                    persona_id=tab_persona_id,
                    created_at=datetime.fromisoformat(tab_created_at),
                    last_accessed=datetime.fromisoformat(tab_last_accessed),
                    history=json.loads(history),
                    scroll_position=scroll_pos,
                    zoom_factor=zoom
                )
                tabs.append(tab)
            
            return BrowsingSession(
                id=session_id,
                name=name,
                persona_id=persona_id,
                created_at=datetime.fromisoformat(created_at),
                last_accessed=datetime.fromisoformat(last_accessed),
                tabs=tabs,
                active_tab=session_data.get('active_tab')
            )
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all available sessions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, name, persona_id, created_at, last_accessed,
                       (SELECT COUNT(*) FROM tabs WHERE session_id = sessions.id) as tab_count
                FROM sessions
                ORDER BY last_accessed DESC
            """)
            
            sessions = []
            for row in cursor.fetchall():
                session_id, name, persona_id, created_at, last_accessed, tab_count = row
                sessions.append({
                    'id': session_id,
                    'name': name,
                    'persona_id': persona_id,
                    'created_at': created_at,
                    'last_accessed': last_accessed,
                    'tab_count': tab_count
                })
            
            return sessions
    
    def delete_session(self, session_id: str):
        """Delete a session and its tabs"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM tabs WHERE session_id = ?", (session_id,))
            conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    
    def cleanup_old_sessions(self, days: int = 30):
        """Clean up sessions older than specified days"""
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        cutoff_iso = datetime.fromtimestamp(cutoff_time).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            # Get sessions to delete
            cursor = conn.execute("""
                SELECT id FROM sessions WHERE last_accessed < ?
            """, (cutoff_iso,))
            
            session_ids = [row[0] for row in cursor.fetchall()]
            
            # Delete tabs and sessions
            for session_id in session_ids:
                conn.execute("DELETE FROM tabs WHERE session_id = ?", (session_id,))
                conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            
            return len(session_ids)