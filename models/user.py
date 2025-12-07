"""
User model representing a user in the application
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Represents a user in the system"""
    id: Optional[int] = None
    username: str = ""
    role: str = ""
    is_authenticated: bool = False
    
    @classmethod
    def create_unauthenticated(cls):
        """Create an unauthenticated user instance"""
        return cls(is_authenticated=False)
    
    def can_access_admin_features(self) -> bool:
        """Check if user can access admin features"""
        return self.role == "admin"
    
    def can_access_teacher_features(self) -> bool:
        """Check if user can access teacher features"""
        return self.role in ["teacher", "admin"]