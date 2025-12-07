from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    role: str = ""
    is_authenticated: bool = False
    
    @classmethod
    def create_unauthenticated(cls):
        return cls(is_authenticated=False)
    
    def can_access_admin_features(self) -> bool:
        return self.role == "admin"
    
    def can_access_teacher_features(self) -> bool:
        return self.role in ["teacher", "admin"]