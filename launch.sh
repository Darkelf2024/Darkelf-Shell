#!/bin/bash
# Launcher script for Darkelf Shell

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if Tor is available (optional)
if ! command -v tor &> /dev/null; then
    echo "Warning: Tor is not installed. Tor integration will not work."
    echo "Install Tor using: sudo apt-get install tor (Ubuntu/Debian) or brew install tor (macOS)"
fi

# Check if required Python packages are installed
python3 -c "import PyQt6; import PyQt6.QtWebEngineWidgets" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Required Python packages not installed."
    echo "Install dependencies using: pip install -r requirements.txt"
    exit 1
fi

# Launch Darkelf Shell
echo "Starting Darkelf Shell..."
python3 main.py "$@"