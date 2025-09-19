# Installation and Usage Guide

## Quick Start

### 1. Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Tor (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install tor

# Install Tor (macOS)
brew install tor

# Install Tor (Windows) - Download from https://www.torproject.org/download/
```

### 2. Run Darkelf Shell
```bash
# Direct Python execution
python3 main.py

# Or use the launcher script
./launch.sh
```

## System Requirements

### Minimum Requirements
- Python 3.8 or higher
- 2GB RAM
- 500MB disk space
- Network connection for Tor

### Recommended Requirements
- Python 3.10+
- 4GB RAM
- 1GB disk space
- Dedicated Tor installation

## Troubleshooting

### Common Issues

#### PyQt6 Installation Issues
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt6 python3-pyqt6.qtwebengine

# macOS
pip install --upgrade pip
pip install PyQt6 PyQtWebEngine

# Windows
pip install PyQt6 PyQtWebEngine
```

#### Tor Connection Issues
```bash
# Check if Tor is running
sudo systemctl status tor

# Start Tor manually
sudo systemctl start tor

# Check Tor configuration
cat /etc/tor/torrc
```

#### Permission Issues
```bash
# Fix launcher permissions
chmod +x launch.sh

# Fix config directory permissions
chmod -R 755 ~/.darkelf_shell/
```

### Error Messages

**"Tor executable not found"**
- Install Tor using your system's package manager
- Verify Tor is in your PATH: `which tor`

**"Failed to start Tor"**
- Check if Tor is already running: `ps aux | grep tor`
- Verify port 9050 is available: `netstat -an | grep 9050`
- Check Tor logs: `sudo journalctl -u tor`

**"PyQt6 module not found"**
- Install PyQt6: `pip install PyQt6 PyQtWebEngine`
- Use virtual environment: `python -m venv venv && source venv/bin/activate`

## Configuration Examples

### Basic Privacy Configuration
```json
{
  "tor": {
    "enabled": true,
    "socks_port": 9050,
    "auto_start": true
  },
  "security": {
    "panic_key": "Ctrl+Shift+P",
    "clear_history_on_exit": true,
    "disable_javascript": false
  }
}
```

### Maximum Security Configuration
```json
{
  "tor": {
    "enabled": true,
    "socks_port": 9050,
    "auto_start": true
  },
  "security": {
    "panic_key": "Ctrl+Shift+P",
    "clear_history_on_exit": true,
    "disable_javascript": true,
    "disable_plugins": true
  },
  "default_persona": "stealth"
}
```

## Performance Optimization

### Memory Usage
- Close unused tabs regularly
- Clear browsing data frequently
- Use minimal personas for better performance

### Network Performance
- Use Tor bridges if connection is slow
- Configure fewer Tor hops for faster browsing (less secure)
- Monitor Tor circuit creation frequency

## Security Best Practices

### Before Using
1. Verify Tor is properly configured
2. Check for DNS leaks
3. Test panic functionality
4. Review persona settings

### During Use
1. Use different personas for different activities
2. Request new Tor identities regularly
3. Monitor connection status
4. Be aware of JavaScript fingerprinting

### After Use
1. Clear all browsing data
2. Close application completely
3. Verify data deletion
4. Check for residual files