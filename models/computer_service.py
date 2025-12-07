from typing import List, Dict, Optional
from .computer import Computer
from .database import DatabaseManager

class ComputerService:
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_all_computers(self) -> Dict[str, List[Computer]]:

        try:
            raw_data = self.db_manager.get_all_computers()
            computers = {}
            for classroom, computer_list in raw_data.items():
                computers[classroom] = [Computer.from_dict(data) for data in computer_list]
            return computers
        except Exception:
            return {}
    
    def get_computers_by_classroom(self, classroom: str) -> List[Computer]:

        all_computers = self.get_all_computers()
        return all_computers.get(classroom, [])
    
    def add_computer(self, computer: Computer) -> bool:

        try:
            return self.db_manager.add_computer(
                computer.name,
                computer.ip_address,
                computer.classroom
            )
        except Exception:
            return False
    
    def update_computer_status(self, name: str, status: str) -> bool:

        try:
            return self.db_manager.update_computer_status(name, status)
        except Exception:
            return False
    
    def get_classrooms(self) -> List[str]:

        all_computers = self.get_all_computers()
        return list(all_computers.keys())