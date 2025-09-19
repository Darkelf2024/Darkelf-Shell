# Darkelf Shell

A Tor-enabled, persona-configurable WebView shell with multi-tab browsing, session management, and panic-safety controls. This is a teaching/research framework that demonstrates advanced client behaviors for anonymous web browsing.

## Features

### Core Functionality
- **Multi-tab browsing** with independent persona configurations
- **Tor integration** for anonymous browsing through SOCKS proxy
- **Persona management** for configurable user profiles and fingerprinting protection
- **Session management** for saving and restoring browsing sessions
- **Panic-safety controls** for emergency data clearing

### Privacy & Security
- **Fingerprinting protection** against canvas, audio, and other tracking methods
- **Configurable JavaScript and plugin controls** per persona
- **Automatic data clearing** on exit (configurable)
- **Emergency panic mode** with instant data destruction
- **Custom request headers** and user agent spoofing

### Research & Teaching Features
- **Multiple personas** for testing different browser fingerprints
- **Session persistence** for research continuity
- **Configurable privacy settings** for educational demonstrations
- **Tor circuit management** with new identity requests

## Installation

### Prerequisites
- Python 3.8+
- PyQt6 and PyQtWebEngine
- Tor (for anonymous browsing)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install Tor
On Ubuntu/Debian:
```bash
sudo apt-get install tor
```

On macOS:
```bash
brew install tor
```

On Windows: Download from [Tor Project](https://www.torproject.org/download/)

## Usage

### Basic Usage
```bash
python main.py
```

### First Run
1. The application will create a configuration directory at `~/.darkelf_shell/`
2. Default personas (Anonymous, Security Researcher, Maximum Stealth) will be created
3. Tor connection will be attempted if enabled in configuration

### Key Features

#### Personas
- Select different personas from the toolbar dropdown
- Each persona has unique fingerprinting characteristics:
  - User agent strings
  - Screen resolution simulation
  - JavaScript/plugin permissions
  - Canvas and audio fingerprinting protection

#### Tor Integration
- Click "Connect Tor" to establish anonymous connection
- "New Identity" button requests fresh Tor circuits
- Status indicators show connection state

#### Panic Mode
- Emergency button (🚨 PANIC) or Ctrl+Shift+P
- Instantly clears all browsing data and exits
- Cannot be undone - use carefully!

#### Session Management
- Save current tabs and state via File → Save Session
- Restore previous sessions via File → Load Session
- Automatic cleanup of old sessions

## Configuration

Configuration files are stored in `~/.darkelf_shell/`:
- `config.json` - Main application settings
- `personas/` - Individual persona configurations
- `sessions/` - Saved browsing sessions
- `sessions.db` - Session database

### Key Configuration Options
```json
{
  "tor": {
    "enabled": true,
    "socks_port": 9050,
    "auto_start": false
  },
  "security": {
    "panic_key": "Ctrl+Shift+P",
    "clear_history_on_exit": true,
    "disable_javascript": false
  }
}
```

## Security Notes

⚠️ **Research Tool Warning**: This is a teaching and research framework. While it implements various privacy protections, it should not be considered a production-ready privacy tool for sensitive activities.

### Important Considerations
- Tor must be properly configured and running
- WebRTC and other potential leak vectors may still be present
- JavaScript fingerprinting protection is basic
- DNS leaks are possible if Tor is not properly configured
- System-level tracking (OS fingerprinting) is not addressed

## Development

### Project Structure
```
darkelf_shell/
├── __init__.py
├── config.py              # Configuration management
├── main_window.py         # Main application window
├── web_tab.py            # Individual web tabs with persona support
├── persona_manager.py     # Persona configuration and management
├── session_manager.py     # Session persistence and restoration
├── tor_manager.py         # Tor integration and proxy management
└── panic_handler.py       # Emergency data clearing
```

### Adding New Features
1. **New Persona Settings**: Modify `persona_manager.py` and `web_tab.py`
2. **Additional Privacy Controls**: Update `web_tab.py` JavaScript injection
3. **Enhanced Tor Features**: Extend `tor_manager.py`
4. **UI Improvements**: Modify `main_window.py`

## Educational Use Cases

### Cybersecurity Training
- Demonstrate browser fingerprinting techniques
- Show impact of different privacy settings
- Illustrate Tor anonymity concepts
- Practice operational security procedures

### Privacy Research
- Test website tracking mechanisms
- Compare persona effectiveness
- Analyze traffic patterns through Tor
- Study browser behavior variations

### Penetration Testing
- Simulate different client environments
- Test web application security controls
- Practice reconnaissance techniques
- Demonstrate social engineering vectors

## License

This project is provided for educational and research purposes. Users are responsible for complying with applicable laws and regulations.

## Contributing

This is a research and teaching framework. Contributions that enhance educational value or improve privacy protections are welcome.

## Disclaimer

Darkelf Shell is provided as-is for educational and research purposes only. The authors are not responsible for any misuse or legal consequences arising from its use. Users must comply with applicable laws and regulations.