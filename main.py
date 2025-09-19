#!/usr/bin/env python3
"""
Darkelf Shell - A Tor-enabled, persona-configurable WebView shell
with multi-tab browsing, session management, and panic-safety controls.

This is a teaching/research framework that demonstrates advanced client behaviors.
"""

import sys
import os
import signal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from darkelf_shell.main_window import DarkelfMainWindow
from darkelf_shell.panic_handler import PanicHandler
from darkelf_shell.config import Config


def signal_handler(signum, frame):
    """Handle system signals for panic situations"""
    print(f"Signal {signum} received, initiating panic procedure...")
    PanicHandler.panic_shutdown()
    sys.exit(0)


def main():
    """Main entry point for Darkelf Shell"""
    # Set up signal handlers for panic situations
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Darkelf Shell")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Darkelf Research")
    
    # Initialize configuration
    config = Config()
    
    # Create and show main window
    main_window = DarkelfMainWindow(config)
    main_window.show()
    
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        PanicHandler.panic_shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()