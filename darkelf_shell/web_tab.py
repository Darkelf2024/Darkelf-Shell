"""
Web tab component with persona-based configuration
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QUrl, pyqtSignal, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineUrlRequestInterceptor

from .persona_manager import Persona
from .tor_manager import TorManager


class PersonaRequestInterceptor(QWebEngineUrlRequestInterceptor):
    """Intercepts web requests to apply persona settings"""
    
    def __init__(self, persona: Persona):
        super().__init__()
        self.persona = persona
    
    def interceptRequest(self, info):
        """Intercept and modify requests based on persona"""
        # Set custom headers based on persona
        headers = info.httpHeaders()
        
        # Set User-Agent
        headers[b'User-Agent'] = self.persona.user_agent.encode()
        
        # Set Accept-Language
        headers[b'Accept-Language'] = self.persona.accept_language.encode()
        
        # Add additional privacy headers
        headers[b'DNT'] = b'1'  # Do Not Track
        headers[b'Sec-GPC'] = b'1'  # Global Privacy Control
        
        info.setHttpHeaders(headers)


class DarkelfWebPage(QWebEnginePage):
    """Custom web page with enhanced privacy features"""
    
    def __init__(self, profile: QWebEngineProfile, persona: Persona):
        super().__init__(profile)
        self.persona = persona
        
        # Configure page settings based on persona
        settings = self.settings()
        
        # JavaScript control
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled, 
            persona.javascript_enabled
        )
        
        # Plugin control
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.PluginsEnabled,
            persona.plugins_enabled
        )
        
        # WebGL control
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.WebGLEnabled,
            persona.webgl_enabled
        )
        
        # Additional privacy settings
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalStorageEnabled,
            False
        )
        
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,
            False
        )
        
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls,
            False
        )
    
    def javaScriptAlert(self, securityOrigin: QUrl, msg: str):
        """Handle JavaScript alerts (can be customized per persona)"""
        if self.persona.javascript_enabled:
            super().javaScriptAlert(securityOrigin, msg)
    
    def javaScriptConfirm(self, securityOrigin: QUrl, msg: str) -> bool:
        """Handle JavaScript confirms"""
        if self.persona.javascript_enabled:
            return super().javaScriptConfirm(securityOrigin, msg)
        return False
    
    def javaScriptPrompt(self, securityOrigin: QUrl, msg: str, defaultValue: str) -> tuple:
        """Handle JavaScript prompts"""
        if self.persona.javascript_enabled:
            return super().javaScriptPrompt(securityOrigin, msg, defaultValue)
        return False, ""


class DarkelfWebTab(QWidget):
    """Individual web tab with persona-based configuration"""
    
    title_changed = pyqtSignal(str)
    url_changed = pyqtSignal(str)
    
    def __init__(self, persona: Persona, tor_manager: TorManager):
        super().__init__()
        self.persona = persona
        self.tor_manager = tor_manager
        
        self._setup_ui()
        self._apply_persona_settings()
    
    def _setup_ui(self):
        """Set up the web view"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create custom profile for this tab
        self.profile = QWebEngineProfile(f"persona_{self.persona.id}")
        
        # Configure profile settings
        self._configure_profile()
        
        # Create custom page
        self.page = DarkelfWebPage(self.profile, self.persona)
        
        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.setPage(self.page)
        
        layout.addWidget(self.web_view)
        
        # Connect signals
        self.web_view.titleChanged.connect(self.title_changed.emit)
        self.web_view.urlChanged.connect(lambda url: self.url_changed.emit(url.toString()))
    
    def _configure_profile(self):
        """Configure the web profile based on persona settings"""
        # Set request interceptor for custom headers
        self.interceptor = PersonaRequestInterceptor(self.persona)
        self.profile.setRequestInterceptor(self.interceptor)
        
        # Configure profile settings
        settings = self.profile.settings()
        
        # Disable various tracking and fingerprinting methods
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.AutoLoadImages,
            True  # Usually keep enabled for usability
        )
        
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows,
            False
        )
        
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard,
            False
        )
        
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.SpatialNavigationEnabled,
            False
        )
        
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.TouchIconsEnabled,
            False
        )
        
        # Set cache policy for privacy
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.NoCache)
        
        # Set persistent cookies policy
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies
        )
    
    def _apply_persona_settings(self):
        """Apply persona-specific settings"""
        # Inject JavaScript for fingerprinting protection if enabled
        if self.persona.canvas_fingerprinting_protection:
            self._inject_canvas_protection()
        
        if self.persona.audio_fingerprinting_protection:
            self._inject_audio_protection()
        
        # Set zoom factor based on persona screen resolution
        self._set_zoom_based_on_resolution()
    
    def _inject_canvas_protection(self):
        """Inject JavaScript to protect against canvas fingerprinting"""
        canvas_protection_script = """
        (function() {
            const originalGetContext = HTMLCanvasElement.prototype.getContext;
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            
            // Add noise to canvas operations
            HTMLCanvasElement.prototype.toDataURL = function() {
                const context = this.getContext('2d');
                if (context) {
                    const imageData = context.getImageData(0, 0, this.width, this.height);
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        imageData.data[i] += Math.random() * 2 - 1;
                    }
                    context.putImageData(imageData, 0, 0);
                }
                return originalToDataURL.apply(this, arguments);
            };
        })();
        """
        
        self.page.runJavaScript(canvas_protection_script)
    
    def _inject_audio_protection(self):
        """Inject JavaScript to protect against audio fingerprinting"""
        audio_protection_script = """
        (function() {
            const originalGetChannelData = AudioBuffer.prototype.getChannelData;
            AudioBuffer.prototype.getChannelData = function() {
                const originalData = originalGetChannelData.apply(this, arguments);
                for (let i = 0; i < originalData.length; i++) {
                    originalData[i] += (Math.random() - 0.5) * 0.0001;
                }
                return originalData;
            };
        })();
        """
        
        self.page.runJavaScript(audio_protection_script)
    
    def _set_zoom_based_on_resolution(self):
        """Set zoom factor based on persona screen resolution"""
        resolution = self.persona.screen_resolution
        try:
            width, height = map(int, resolution.split('x'))
            
            # Adjust zoom based on resolution (simplified logic)
            if width <= 1024:
                zoom_factor = 0.8
            elif width <= 1366:
                zoom_factor = 0.9
            elif width >= 1920:
                zoom_factor = 1.1
            else:
                zoom_factor = 1.0
            
            self.web_view.setZoomFactor(zoom_factor)
            
        except (ValueError, AttributeError):
            # Default zoom if resolution parsing fails
            self.web_view.setZoomFactor(1.0)
    
    def apply_persona(self, persona: Persona):
        """Apply a new persona to this tab"""
        self.persona = persona
        
        # Update interceptor
        self.interceptor.persona = persona
        
        # Recreate page with new persona settings
        old_url = self.web_view.url()
        self.page = DarkelfWebPage(self.profile, persona)
        self.web_view.setPage(self.page)
        
        # Reapply persona settings
        self._apply_persona_settings()
        
        # Reload current page to apply new settings
        if not old_url.isEmpty():
            self.web_view.load(old_url)
    
    def navigate_to(self, url: str):
        """Navigate to a URL"""
        if url.startswith('about:'):
            # Handle special URLs
            if url == 'about:blank':
                self.web_view.setHtml('<html><body style="background-color: #2b2b2b; color: #ffffff;"><h1>Darkelf Shell</h1><p>Anonymous Research Browser</p></body></html>')
            return
        
        self.web_view.load(QUrl(url))
    
    def go_back(self):
        """Go back in history"""
        self.web_view.back()
    
    def go_forward(self):
        """Go forward in history"""
        self.web_view.forward()
    
    def refresh(self):
        """Refresh the page"""
        self.web_view.reload()
    
    def get_current_url(self) -> str:
        """Get current URL"""
        return self.web_view.url().toString()
    
    def get_title(self) -> str:
        """Get current page title"""
        return self.web_view.title()
    
    def get_history(self) -> list:
        """Get navigation history"""
        history = self.web_view.history()
        urls = []
        
        for i in range(history.count()):
            item = history.itemAt(i)
            urls.append(item.url().toString())
        
        return urls