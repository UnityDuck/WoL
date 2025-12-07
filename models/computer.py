from dataclasses import dataclass
from typing import Optional


@dataclass
class Computer:
    """Represents a computer in the system"""
    id: Optional[int] = None
    name: str = ""
    ip_address: str = ""
    classroom: str = ""
    status: str = "online"  # "online", "offline", "maintenance"
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Computer instance from dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            ip_address=data.get('ip', data.get('ip_address', '')),
            classroom=data.get('classroom', ''),
            status=data.get('status', 'online')
        )
    
    def to_dict(self) -> dict:
        """Convert Computer instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'ip_address': self.ip_address,
            'classroom': self.classroom,
            'status': self.status
        }
    
    def is_online(self) -> bool:
        """Check if computer is online"""
        return self.status.lower() == 'online'
    
    def is_offline(self) -> bool:
        """Check if computer is offline"""
        return self.status.lower() == 'offline'
    
    def is_in_maintenance(self) -> bool:
        """Check if computer is in maintenance"""
        return self.status.lower() == 'maintenance'