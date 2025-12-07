"""
Authentication service handling user authentication and session management
"""
from typing import Optional, Tuple
from .user import User
from .database import DatabaseManager


class AuthService:
    """Handles user authentication and session management"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.current_user: Optional[User] = None
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[User]]:
        """Authenticate user with provided credentials"""
        try:
            success, role = self.db_manager.verify_user(username, password)
            if success and role:
                self.current_user = User(
                    username=username,
                    role=role,
                    is_authenticated=True
                )
                return True, self.current_user
            else:
                self.current_user = User.create_unauthenticated()
                return False, None
        except Exception:
            self.current_user = User.create_unauthenticated()
            return False, None
    
    def logout(self):
        """Logout current user"""
        self.current_user = User.create_unauthenticated()
    
    def is_authenticated(self) -> bool:
        """Check if current user is authenticated"""
        return self.current_user is not None and self.current_user.is_authenticated
    
    def get_current_user(self) -> Optional[User]:
        """Get current authenticated user"""
        return self.current_user
    
    def has_admin_access(self) -> bool:
        """Check if current user has admin access"""
        if not self.current_user:
            return False
        return self.current_user.can_access_admin_features()
    
    def has_teacher_access(self) -> bool:
        """Check if current user has teacher access"""
        if not self.current_user:
            return False
        return self.current_user.can_access_teacher_features()