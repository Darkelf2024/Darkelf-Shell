#!/usr/bin/env python3
"""
Basic functionality test for Darkelf Shell (headless mode)
"""

import sys
import tempfile
import json
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_config_system():
    """Test configuration management"""
    print("Testing configuration system...")
    
    try:
        from darkelf_shell.config import Config
        
        # Test with temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            config = Config()
            
            # Test basic configuration
            assert config.tor_enabled == True
            assert config.socks_port == 9050
            assert config.panic_key == 'Ctrl+Shift+P'
            
            # Test setting and getting values
            config.set('test.value', 'test_data')
            assert config.get('test.value') == 'test_data'
            
        print("✅ Configuration system working")
        return True
        
    except Exception as e:
        print(f"❌ Configuration system failed: {e}")
        return False

def test_persona_manager():
    """Test persona management"""
    print("Testing persona manager...")
    
    try:
        from darkelf_shell.persona_manager import PersonaManager, Persona
        
        with tempfile.TemporaryDirectory() as temp_dir:
            personas_dir = Path(temp_dir) / "personas"
            manager = PersonaManager(personas_dir)
            
            # Test default personas creation
            personas = manager.list_personas()
            assert len(personas) >= 3  # Should have at least 3 default personas
            
            # Test getting specific persona
            anonymous = manager.get_persona('anonymous')
            assert anonymous is not None
            assert anonymous.name == 'Anonymous'
            
            # Test creating new persona
            new_persona = manager.create_persona(
                'test_persona',
                user_agent='Test Agent',
                javascript_enabled=False
            )
            assert new_persona.name == 'test_persona'
            assert new_persona.javascript_enabled == False
            
        print("✅ Persona manager working")
        return True
        
    except Exception as e:
        print(f"❌ Persona manager failed: {e}")
        return False

def test_session_manager():
    """Test session management"""
    print("Testing session manager...")
    
    try:
        from darkelf_shell.session_manager import SessionManager, BrowsingSession, TabSession
        from datetime import datetime
        import uuid
        
        with tempfile.TemporaryDirectory() as temp_dir:
            sessions_dir = Path(temp_dir) / "sessions"
            manager = SessionManager(sessions_dir)
            
            # Create test session
            session_id = str(uuid.uuid4())
            tab_id = str(uuid.uuid4())
            
            tab = TabSession(
                id=tab_id,
                url="https://example.com",
                title="Test Page",
                persona_id="anonymous",
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                history=["https://example.com"]
            )
            
            session = BrowsingSession(
                id=session_id,
                name="Test Session",
                persona_id="anonymous",
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                tabs=[tab],
                active_tab=tab_id
            )
            
            # Test saving and loading
            manager.save_session(session)
            loaded_session = manager.load_session(session_id)
            
            assert loaded_session is not None
            assert loaded_session.name == "Test Session"
            assert len(loaded_session.tabs) == 1
            assert loaded_session.tabs[0].url == "https://example.com"
            
        print("✅ Session manager working")
        return True
        
    except Exception as e:
        print(f"❌ Session manager failed: {e}")
        return False

def test_tor_manager():
    """Test Tor manager (without actual Tor connection)"""
    print("Testing Tor manager...")
    
    try:
        from darkelf_shell.tor_manager import TorManager
        
        # Test basic initialization
        tor_manager = TorManager()
        assert tor_manager.socks_port == 9050
        assert tor_manager.control_port == 9051
        
        # Test connection check (will fail without Tor, but shouldn't crash)
        connected = tor_manager.check_tor_connection()
        # Should return False since Tor isn't running
        assert connected == False
        
        print("✅ Tor manager basic functionality working")
        return True
        
    except Exception as e:
        print(f"❌ Tor manager failed: {e}")
        return False

def test_panic_handler():
    """Test panic handler"""
    print("Testing panic handler...")
    
    try:
        from darkelf_shell.panic_handler import PanicHandler
        
        # Test basic initialization
        handler = PanicHandler()
        
        # Test static methods (without actually triggering)
        # These should not crash
        PanicHandler._clear_temp_files()
        
        print("✅ Panic handler working")
        return True
        
    except Exception as e:
        print(f"❌ Panic handler failed: {e}")
        return False

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    modules = [
        'darkelf_shell.config',
        'darkelf_shell.persona_manager',
        'darkelf_shell.session_manager',
        'darkelf_shell.tor_manager',
        'darkelf_shell.panic_handler'
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError as e:
            print(f"❌ {module} import failed: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def main():
    """Run all tests"""
    print("=== Darkelf Shell Basic Functionality Test ===\n")
    
    tests = [
        test_imports,
        test_config_system,
        test_persona_manager,
        test_session_manager,
        test_tor_manager,
        test_panic_handler
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}\n")
    
    print(f"=== Test Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("🎉 All basic functionality tests passed!")
        print("Note: GUI and Tor integration require proper environment setup.")
    else:
        print("⚠️  Some tests failed. Check error messages above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)