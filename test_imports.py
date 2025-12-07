"""
Simple test script to verify imports work correctly
"""
import sys
import os

# Add workspace to path
sys.path.insert(0, '/workspace')

def test_imports():
    """Test that all modules can be imported without errors"""
    try:
        print("Testing imports...")
        
        # Test model imports
        from models.database import DatabaseManager
        from models.user import User
        from models.computer import Computer
        from models.auth_service import AuthService
        from models.computer_service import ComputerService
        from models.settings_service import SettingsService
        print("✓ Model imports successful")
        
        # Test viewmodel imports
        from viewmodels.base_viewmodel import BaseViewModel
        from viewmodels.login_viewmodel import LoginViewModel
        from viewmodels.main_viewmodel import MainViewModel
        print("✓ ViewModel imports successful")
        
        # Test view imports
        from views.login_view import LoginView
        from views.main_view import MainView
        print("✓ View imports successful")
        
        # Test utility imports
        from utils.theme_manager import ThemeManager
        print("✓ Utility imports successful")
        
        # Test config import
        from config import Config
        print("✓ Config import successful")
        
        print("\nAll imports successful! MVVM architecture is properly structured.")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)