"""
Settings service handling application settings
"""
from .database import DatabaseManager


class SettingsService:
    """Handles application settings"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_theme(self) -> str:
        """Get current theme"""
        return self.db_manager.get_theme()
    
    def set_theme(self, theme: str) -> bool:
        """Set theme"""
        return self.db_manager.set_theme(theme)