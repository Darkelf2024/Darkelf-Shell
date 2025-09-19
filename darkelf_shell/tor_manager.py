"""
Tor integration for anonymous browsing
"""

import socket
import socks
import subprocess
import time
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtNetwork import QNetworkProxy, QNetworkProxyFactory


class TorManager(QObject):
    """Manages Tor connection and proxy settings"""
    
    tor_status_changed = pyqtSignal(bool)  # True if connected, False if disconnected
    tor_error = pyqtSignal(str)
    
    def __init__(self, socks_port: int = 9050, control_port: int = 9051):
        super().__init__()
        self.socks_port = socks_port
        self.control_port = control_port
        self.tor_process = None
        self._connected = False
    
    @property
    def is_connected(self) -> bool:
        """Check if Tor is connected"""
        return self._connected
    
    def check_tor_connection(self) -> bool:
        """Check if Tor is running and accessible"""
        try:
            # Test SOCKS proxy connection
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, "127.0.0.1", self.socks_port)
            s.settimeout(10)
            
            # Try to connect to a test service
            s.connect(("check.torproject.org", 80))
            s.close()
            
            self._connected = True
            self.tor_status_changed.emit(True)
            return True
            
        except Exception as e:
            self._connected = False
            self.tor_status_changed.emit(False)
            return False
    
    def setup_proxy(self):
        """Configure Qt network proxy to use Tor"""
        if not self.is_connected:
            return False
        
        # Set up SOCKS5 proxy for Qt
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.ProxyType.Socks5Proxy)
        proxy.setHostName("127.0.0.1")
        proxy.setPort(self.socks_port)
        
        QNetworkProxy.setApplicationProxy(proxy)
        return True
    
    def clear_proxy(self):
        """Remove proxy settings"""
        QNetworkProxy.setApplicationProxy(QNetworkProxy())
    
    def get_new_identity(self):
        """Request a new Tor identity (new circuit)"""
        try:
            # Connect to Tor control port to request new identity
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", self.control_port))
            
            # Send NEWNYM command (authenticate first if needed)
            s.send(b"AUTHENTICATE\r\n")
            s.recv(1024)  # Read response
            
            s.send(b"SIGNAL NEWNYM\r\n")
            response = s.recv(1024)
            s.close()
            
            if b"250 OK" in response:
                return True
            else:
                self.tor_error.emit("Failed to get new identity")
                return False
                
        except Exception as e:
            self.tor_error.emit(f"Error requesting new identity: {str(e)}")
            return False
    
    def start_tor(self):
        """Start Tor process (if not already running)"""
        if self.check_tor_connection():
            return True
        
        try:
            # Try to start Tor
            self.tor_process = subprocess.Popen([
                "tor",
                "--SocksPort", str(self.socks_port),
                "--ControlPort", str(self.control_port),
                "--DataDirectory", "/tmp/darkelf_tor",
                "--ExitNodes", "{us},{ca},{gb},{de},{fr}",
                "--StrictNodes", "1"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for Tor to start
            time.sleep(5)
            
            return self.check_tor_connection()
            
        except FileNotFoundError:
            self.tor_error.emit("Tor executable not found. Please install Tor.")
            return False
        except Exception as e:
            self.tor_error.emit(f"Failed to start Tor: {str(e)}")
            return False
    
    def stop_tor(self):
        """Stop Tor process"""
        if self.tor_process:
            self.tor_process.terminate()
            self.tor_process.wait()
            self.tor_process = None
        
        self._connected = False
        self.tor_status_changed.emit(False)
        self.clear_proxy()


class TorChecker(QThread):
    """Background thread to periodically check Tor connection"""
    
    connection_status = pyqtSignal(bool)
    
    def __init__(self, tor_manager: TorManager):
        super().__init__()
        self.tor_manager = tor_manager
        self.running = True
    
    def run(self):
        """Check Tor connection every 30 seconds"""
        while self.running:
            status = self.tor_manager.check_tor_connection()
            self.connection_status.emit(status)
            self.msleep(30000)  # 30 seconds
    
    def stop(self):
        """Stop the checker thread"""
        self.running = False
        self.wait()