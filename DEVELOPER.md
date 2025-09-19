# Developer Documentation

## Architecture Overview

Darkelf Shell is built with a modular architecture that separates concerns into distinct components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Main Window   │────│   Web Tabs      │────│   Personas      │
│   (UI Control)  │    │  (Browsing)     │    │ (Fingerprints)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Session Mgmt   │────│   Tor Manager   │────│ Panic Handler   │
│  (Persistence)  │    │   (Anonymity)   │    │  (Emergency)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Core Components

### 1. Main Window (`main_window.py`)
**Purpose**: Primary application interface and coordination
**Key Features**:
- Tab management and navigation
- Toolbar with Tor controls and persona selection
- Menu system for session and configuration management
- Status indicators for Tor, persona, and session state

**Key Methods**:
- `_add_new_tab()`: Creates new browser tabs with persona configuration
- `_toggle_tor()`: Manages Tor connection state
- `_trigger_panic()`: Initiates emergency shutdown procedures

### 2. Web Tab (`web_tab.py`)
**Purpose**: Individual browser tabs with persona-based configuration
**Key Features**:
- Custom QWebEngineProfile per tab
- Request interception for header modification
- JavaScript injection for fingerprinting protection
- Persona-specific browser settings

**Security Implementations**:
```python
# Canvas fingerprinting protection
canvas_protection_script = """
(function() {
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function() {
        // Add noise to canvas data
        const context = this.getContext('2d');
        // ... noise injection logic
    };
})();
"""
```

### 3. Persona Manager (`persona_manager.py`)
**Purpose**: User profile management with fingerprinting controls
**Key Features**:
- JSON-based persona storage
- Default persona creation (Anonymous, Researcher, Stealth)
- Configurable browser characteristics per persona

**Persona Structure**:
```python
@dataclass
class Persona:
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
```

### 4. Tor Manager (`tor_manager.py`)
**Purpose**: Tor integration and proxy management
**Key Features**:
- SOCKS5 proxy configuration
- Tor process management
- Circuit renewal (new identity)
- Connection monitoring

**Network Flow**:
```
Browser Request → SOCKS5 Proxy (127.0.0.1:9050) → Tor Network → Destination
```

### 5. Session Manager (`session_manager.py`)
**Purpose**: Tab state persistence and restoration
**Key Features**:
- SQLite-based session storage
- Tab history and state preservation
- Session cleanup and management

**Database Schema**:
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    persona_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_accessed TEXT NOT NULL,
    data TEXT NOT NULL
);

CREATE TABLE tabs (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    persona_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_accessed TEXT NOT NULL,
    history TEXT NOT NULL,
    scroll_position INTEGER DEFAULT 0,
    zoom_factor REAL DEFAULT 1.0
);
```

### 6. Panic Handler (`panic_handler.py`)
**Purpose**: Emergency data clearing and shutdown
**Key Features**:
- Immediate data destruction
- Cache and cookie clearing
- Process termination
- Residual file cleanup

## Security Features

### Fingerprinting Protection
1. **Canvas Protection**: Injects noise into canvas operations
2. **Audio Protection**: Adds randomization to audio fingerprinting
3. **User Agent Spoofing**: Configurable per persona
4. **Header Modification**: Custom Accept-Language and other headers
5. **JavaScript Controls**: Per-persona JavaScript enabling/disabling

### Privacy Controls
1. **No Persistent Storage**: Disabled local storage and persistent cookies
2. **Plugin Blocking**: Configurable plugin execution
3. **WebGL Control**: Can be disabled per persona
4. **Popup Blocking**: JavaScript popup prevention
5. **Cache Management**: No-cache HTTP policy

### Emergency Features
1. **Panic Key**: Configurable emergency shortcut (Ctrl+Shift+P)
2. **Data Clearing**: Immediate cache, cookie, and session deletion
3. **Process Termination**: Clean application shutdown
4. **Signal Handling**: Responds to SIGINT and SIGTERM

## Development Guidelines

### Adding New Features

#### New Persona Settings
1. Add field to `Persona` dataclass in `persona_manager.py`
2. Update default persona creation
3. Implement setting application in `web_tab.py`
4. Add UI controls in `main_window.py` if needed

#### Enhanced Privacy Controls
1. Add JavaScript injection in `_apply_persona_settings()`
2. Update request interceptor in `PersonaRequestInterceptor`
3. Modify QWebEngineProfile settings
4. Test fingerprinting effectiveness

#### Additional Tor Features
1. Extend `TorManager` class with new methods
2. Add UI controls in main window toolbar
3. Update status indicators
4. Handle errors appropriately

### Testing Procedures

#### Manual Testing
1. **Tor Integration**: Verify proxy setup and IP changes
2. **Persona Switching**: Test fingerprint variations
3. **Session Management**: Save/restore functionality
4. **Panic Functionality**: Data clearing verification
5. **Tab Management**: Multi-tab behavior

#### Automated Testing
```python
# Example test structure
import unittest
from darkelf_shell.persona_manager import PersonaManager

class TestPersonaManager(unittest.TestCase):
    def test_persona_creation(self):
        # Test persona creation and storage
        pass
    
    def test_default_personas(self):
        # Verify default personas are created
        pass
```

### Performance Considerations

#### Memory Management
- Each tab creates its own QWebEngineProfile
- Profiles are not shared between tabs for security
- Monitor memory usage with multiple tabs

#### Network Performance
- Tor introduces latency and bandwidth limitations
- Consider connection pooling for multiple tabs
- Monitor circuit creation frequency

#### Storage Efficiency
- Session database can grow large with many tabs
- Implement regular cleanup of old sessions
- Compress session data if necessary

## Security Considerations

### Threat Model
The application protects against:
- **Browser Fingerprinting**: Canvas, audio, font, screen metrics
- **Traffic Analysis**: Via Tor network anonymization
- **Local Data Persistence**: Through aggressive clearing
- **Emergency Discovery**: Via panic mode functionality

### Limitations
The application does NOT protect against:
- **System-level fingerprinting**: OS, hardware characteristics
- **Network-level attacks**: If Tor is compromised
- **Physical access**: To the system running the application
- **Advanced persistent threats**: With system-level access

### Best Practices for Users
1. **Tor Configuration**: Ensure proper Tor setup and verification
2. **Persona Rotation**: Regularly switch between personas
3. **Session Management**: Don't persist sensitive sessions
4. **Panic Procedures**: Test and understand panic functionality
5. **System Hardening**: Use in conjunction with other privacy tools

## Future Enhancements

### Planned Features
1. **Bridge Support**: Tor bridge configuration for censored networks
2. **Plugin System**: Extensible privacy protection modules
3. **Advanced Personas**: More sophisticated fingerprint simulation
4. **Network Analysis**: Built-in traffic analysis tools
5. **Educational Modules**: Interactive privacy education components

### Research Opportunities
1. **Fingerprinting Resistance**: Advanced anti-fingerprinting techniques
2. **Traffic Correlation**: Protection against traffic analysis
3. **Behavioral Obfuscation**: Simulating human browsing patterns
4. **Usability Studies**: Privacy tool effectiveness research