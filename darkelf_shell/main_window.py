"""
Main window for Darkelf Shell
"""

import uuid
from datetime import datetime
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, 
                            QWidget, QMenuBar, QStatusBar, QToolBar, QLineEdit,
                            QPushButton, QComboBox, QLabel, QMessageBox, QDialog,
                            QApplication)
from PyQt6.QtCore import Qt, QUrl, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage

from .config import Config
from .persona_manager import PersonaManager, Persona
from .session_manager import SessionManager, BrowsingSession, TabSession
from .tor_manager import TorManager, TorChecker
from .panic_handler import PanicHandler
from .web_tab import DarkelfWebTab


class DarkelfMainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.persona_manager = PersonaManager(config.personas_dir)
        self.session_manager = SessionManager(config.sessions_dir)
        self.tor_manager = TorManager(config.socks_port)
        self.panic_handler = PanicHandler()
        
        self.current_persona = None
        self.current_session = None
        
        self._setup_ui()
        self._setup_tor()
        self._connect_signals()
        self._load_default_persona()
        
        # Set up panic key
        self._setup_panic_key()
        
        # Start Tor checker
        self.tor_checker = TorChecker(self.tor_manager)
        self.tor_checker.connection_status.connect(self._update_tor_status)
        self.tor_checker.start()
    
    def _setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Darkelf Shell - Anonymous Research Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Toolbar
        self.toolbar = self._create_toolbar()
        layout.addWidget(self.toolbar)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self._close_tab)
        layout.addWidget(self.tab_widget)
        
        # Menu bar
        self._create_menu_bar()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status indicators
        self.tor_status_label = QLabel("Tor: Disconnected")
        self.persona_status_label = QLabel("Persona: None")
        self.session_status_label = QLabel("Session: None")
        
        self.status_bar.addWidget(self.tor_status_label)
        self.status_bar.addWidget(QLabel(" | "))
        self.status_bar.addWidget(self.persona_status_label)
        self.status_bar.addWidget(QLabel(" | "))
        self.status_bar.addWidget(self.session_status_label)
        
        # Add first tab
        self._add_new_tab()
    
    def _create_toolbar(self) -> QWidget:
        """Create the main toolbar"""
        toolbar_widget = QWidget()
        layout = QHBoxLayout(toolbar_widget)
        
        # Navigation buttons
        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.refresh_btn = QPushButton("⟳")
        self.home_btn = QPushButton("🏠")
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL...")
        self.url_bar.returnPressed.connect(self._navigate_to_url)
        
        # New tab button
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.clicked.connect(self._add_new_tab)
        
        # Persona selector
        self.persona_combo = QComboBox()
        self.persona_combo.currentTextChanged.connect(self._change_persona)
        self._update_persona_combo()
        
        # Tor controls
        self.tor_btn = QPushButton("Connect Tor")
        self.tor_btn.clicked.connect(self._toggle_tor)
        
        self.new_identity_btn = QPushButton("New Identity")
        self.new_identity_btn.clicked.connect(self._new_tor_identity)
        self.new_identity_btn.setEnabled(False)
        
        # Panic button
        self.panic_btn = QPushButton("🚨 PANIC")
        self.panic_btn.setStyleSheet("QPushButton { background-color: red; color: white; font-weight: bold; }")
        self.panic_btn.clicked.connect(self._trigger_panic)
        
        # Add to layout
        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.home_btn)
        layout.addWidget(self.url_bar, 1)  # Stretch factor
        layout.addWidget(self.new_tab_btn)
        layout.addWidget(QLabel("Persona:"))
        layout.addWidget(self.persona_combo)
        layout.addWidget(self.tor_btn)
        layout.addWidget(self.new_identity_btn)
        layout.addWidget(self.panic_btn)
        
        # Connect navigation buttons
        self.back_btn.clicked.connect(self._go_back)
        self.forward_btn.clicked.connect(self._go_forward)
        self.refresh_btn.clicked.connect(self._refresh_page)
        self.home_btn.clicked.connect(self._go_home)
        
        return toolbar_widget
    
    def _create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_tab_action = QAction("New Tab", self)
        new_tab_action.setShortcut(QKeySequence.StandardKey.AddTab)
        new_tab_action.triggered.connect(self._add_new_tab)
        file_menu.addAction(new_tab_action)
        
        file_menu.addSeparator()
        
        save_session_action = QAction("Save Session", self)
        save_session_action.setShortcut(QKeySequence("Ctrl+S"))
        save_session_action.triggered.connect(self._save_session)
        file_menu.addAction(save_session_action)
        
        load_session_action = QAction("Load Session", self)
        load_session_action.setShortcut(QKeySequence("Ctrl+O"))
        load_session_action.triggered.connect(self._load_session)
        file_menu.addAction(load_session_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        new_identity_action = QAction("New Tor Identity", self)
        new_identity_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        new_identity_action.triggered.connect(self._new_tor_identity)
        tools_menu.addAction(new_identity_action)
        
        clear_data_action = QAction("Clear Browsing Data", self)
        clear_data_action.triggered.connect(self._clear_browsing_data)
        tools_menu.addAction(clear_data_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_tor(self):
        """Set up Tor connection"""
        if self.config.tor_enabled:
            if self.config.get('tor.auto_start', False):
                self.tor_manager.start_tor()
            else:
                self.tor_manager.check_tor_connection()
    
    def _connect_signals(self):
        """Connect signals"""
        self.panic_handler.panic_triggered.connect(self._on_panic_triggered)
        self.tor_manager.tor_status_changed.connect(self._update_tor_status)
        self.tor_manager.tor_error.connect(self._show_tor_error)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
    
    def _setup_panic_key(self):
        """Set up the panic key shortcut"""
        panic_action = QAction("Panic", self)
        panic_action.setShortcut(QKeySequence(self.config.panic_key))
        panic_action.triggered.connect(self._trigger_panic)
        self.addAction(panic_action)
    
    def _load_default_persona(self):
        """Load the default persona"""
        default_persona_id = self.config.get('default_persona', 'anonymous')
        persona = self.persona_manager.get_persona(default_persona_id)
        
        if persona:
            self.current_persona = persona
            self._update_persona_status()
            
            # Update combo box selection
            for i in range(self.persona_combo.count()):
                if self.persona_combo.itemData(i) == persona.id:
                    self.persona_combo.setCurrentIndex(i)
                    break
    
    def _update_persona_combo(self):
        """Update the persona combo box"""
        self.persona_combo.clear()
        
        for persona in self.persona_manager.list_personas():
            self.persona_combo.addItem(persona.name, persona.id)
    
    def _add_new_tab(self, url: str = "about:blank"):
        """Add a new tab"""
        if not self.current_persona:
            QMessageBox.warning(self, "No Persona", "Please select a persona before creating a new tab.")
            return
        
        web_tab = DarkelfWebTab(self.current_persona, self.tor_manager)
        
        # Add tab to widget
        tab_index = self.tab_widget.addTab(web_tab, "New Tab")
        self.tab_widget.setCurrentIndex(tab_index)
        
        # Connect signals
        web_tab.title_changed.connect(lambda title, tab=web_tab: self._update_tab_title(tab, title))
        web_tab.url_changed.connect(self._update_url_bar)
        
        # Navigate to URL
        if url != "about:blank":
            web_tab.navigate_to(url)
        
        return web_tab
    
    def _close_tab(self, index: int):
        """Close a tab"""
        if self.tab_widget.count() <= 1:
            # Don't close the last tab, just navigate to blank page
            current_tab = self.tab_widget.currentWidget()
            if current_tab:
                current_tab.navigate_to("about:blank")
            return
        
        widget = self.tab_widget.widget(index)
        self.tab_widget.removeTab(index)
        widget.deleteLater()
    
    def _update_tab_title(self, tab: 'DarkelfWebTab', title: str):
        """Update tab title"""
        index = self.tab_widget.indexOf(tab)
        if index >= 0:
            # Truncate title if too long
            display_title = title[:30] + "..." if len(title) > 30 else title
            self.tab_widget.setTabText(index, display_title or "Untitled")
    
    def _update_url_bar(self, url: str):
        """Update URL bar with current page URL"""
        if self.tab_widget.currentWidget():
            self.url_bar.setText(url)
    
    def _navigate_to_url(self):
        """Navigate current tab to URL in address bar"""
        url = self.url_bar.text().strip()
        if not url:
            return
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://', 'about:')):
            url = 'https://' + url
        
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.navigate_to(url)
    
    def _go_back(self):
        """Go back in current tab"""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.go_back()
    
    def _go_forward(self):
        """Go forward in current tab"""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.go_forward()
    
    def _refresh_page(self):
        """Refresh current tab"""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.refresh()
    
    def _go_home(self):
        """Navigate to home page"""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.navigate_to("about:blank")
    
    def _on_tab_changed(self, index: int):
        """Handle tab change"""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            self._update_url_bar(current_tab.get_current_url())
    
    def _change_persona(self, persona_name: str):
        """Change current persona"""
        persona_id = self.persona_combo.currentData()
        if persona_id:
            persona = self.persona_manager.get_persona(persona_id)
            if persona:
                self.current_persona = persona
                self._update_persona_status()
                
                # Apply persona to current tab
                current_tab = self.tab_widget.currentWidget()
                if current_tab:
                    current_tab.apply_persona(persona)
    
    def _toggle_tor(self):
        """Toggle Tor connection"""
        if self.tor_manager.is_connected:
            self.tor_manager.clear_proxy()
            self.tor_manager.stop_tor()
        else:
            if self.tor_manager.start_tor() or self.tor_manager.check_tor_connection():
                self.tor_manager.setup_proxy()
    
    def _new_tor_identity(self):
        """Request new Tor identity"""
        if self.tor_manager.is_connected:
            if self.tor_manager.get_new_identity():
                self.status_bar.showMessage("New Tor identity requested", 3000)
            else:
                self.status_bar.showMessage("Failed to get new identity", 3000)
    
    def _update_tor_status(self, connected: bool):
        """Update Tor status in UI"""
        if connected:
            self.tor_status_label.setText("Tor: Connected")
            self.tor_btn.setText("Disconnect Tor")
            self.new_identity_btn.setEnabled(True)
        else:
            self.tor_status_label.setText("Tor: Disconnected")
            self.tor_btn.setText("Connect Tor")
            self.new_identity_btn.setEnabled(False)
    
    def _update_persona_status(self):
        """Update persona status in UI"""
        if self.current_persona:
            self.persona_status_label.setText(f"Persona: {self.current_persona.name}")
        else:
            self.persona_status_label.setText("Persona: None")
    
    def _show_tor_error(self, error: str):
        """Show Tor error message"""
        QMessageBox.warning(self, "Tor Error", error)
    
    def _trigger_panic(self):
        """Trigger panic mode"""
        reply = QMessageBox.warning(
            self, "Panic Mode", 
            "This will immediately close the application and clear all browsing data. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.panic_handler.trigger_panic()
            QApplication.quit()
    
    def _on_panic_triggered(self):
        """Handle panic trigger"""
        QApplication.quit()
    
    def _save_session(self):
        """Save current browsing session"""
        # Implementation for session saving dialog
        pass
    
    def _load_session(self):
        """Load a browsing session"""
        # Implementation for session loading dialog
        pass
    
    def _clear_browsing_data(self):
        """Clear all browsing data"""
        reply = QMessageBox.question(
            self, "Clear Data", 
            "Clear all browsing data including history, cookies, and cache?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear all tabs
            while self.tab_widget.count() > 1:
                self.tab_widget.removeTab(self.tab_widget.count() - 1)
            
            # Reset first tab
            current_tab = self.tab_widget.currentWidget()
            if current_tab:
                current_tab.navigate_to("about:blank")
            
            self.status_bar.showMessage("Browsing data cleared", 3000)
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, "About Darkelf Shell",
            "Darkelf Shell v1.0.0\n\n"
            "A Tor-enabled, persona-configurable WebView shell with multi-tab browsing, "
            "session management, and panic-safety controls.\n\n"
            "This is a teaching/research framework that demonstrates advanced client behaviors."
        )
    
    def closeEvent(self, event):
        """Handle application close"""
        # Stop Tor checker
        if hasattr(self, 'tor_checker'):
            self.tor_checker.stop()
        
        # Clean up Tor
        if self.tor_manager.is_connected:
            self.tor_manager.clear_proxy()
        
        # Clear data if configured
        if self.config.get('security.clear_history_on_exit', True):
            self._clear_browsing_data()
        
        event.accept()