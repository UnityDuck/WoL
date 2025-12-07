"""
Main ViewModel handling main application logic
"""
from PyQt6.QtCore import pyqtSignal
from typing import List
from .base_viewmodel import BaseViewModel
from models.auth_service import AuthService
from models.computer_service import ComputerService
from models.settings_service import SettingsService
from models.user import User
from models.computer import Computer


class MainViewModel(BaseViewModel):
    """ViewModel for main application window"""
    
    # Signal emitted when computers data changes
    computers_changed = pyqtSignal()
    # Signal emitted when classrooms list changes
    classrooms_changed = pyqtSignal()
    # Signal emitted when theme changes
    theme_changed = pyqtSignal(str)
    # Signal emitted when user logs out
    user_logged_out = pyqtSignal()
    
    def __init__(self, 
                 auth_service: AuthService, 
                 computer_service: ComputerService,
                 settings_service: SettingsService):
        super().__init__()
        self.auth_service = auth_service
        self.computer_service = computer_service
        self.settings_service = settings_service
        
        # Initialize current user from auth service
        self._current_user = self.auth_service.get_current_user()
        self._current_classroom = ""
        self._computers = []
    
    @property
    def current_user(self) -> User:
        """Get current authenticated user"""
        return self._current_user or User.create_unauthenticated()
    
    @property
    def current_classroom(self) -> str:
        """Get current selected classroom"""
        return self._current_classroom
    
    @current_classroom.setter
    def current_classroom(self, value: str):
        """Set current classroom and update computers"""
        self._current_classroom = value
        self.update_computers_for_classroom()
    
    @property
    def computers(self) -> List[Computer]:
        """Get current computers list"""
        return self._computers
    
    def load_classrooms(self) -> List[str]:
        """Load list of available classrooms"""
        try:
            classrooms = self.computer_service.get_classrooms()
            self.classrooms_changed.emit()
            return classrooms
        except Exception as ex:
            self.handle_exception(ex, "Ошибка при загрузке списка кабинетов")
            return []
    
    def update_computers_for_classroom(self):
        """Update computers list based on current classroom"""
        try:
            self._computers = self.computer_service.get_computers_by_classroom(
                self._current_classroom
            )
            self.computers_changed.emit()
        except Exception as ex:
            self.handle_exception(ex, "Ошибка при загрузке компьютеров")
            self._computers = []
    
    def get_all_computers(self) -> dict:
        """Get all computers grouped by classroom"""
        try:
            return self.computer_service.get_all_computers()
        except Exception as ex:
            self.handle_exception(ex, "Ошибка при загрузке всех компьютеров")
            return {}
    
    def refresh_data(self):
        """Refresh all data"""
        self.load_classrooms()
        if self._current_classroom:
            self.update_computers_for_classroom()
    
    def change_theme(self, theme: str):
        """Change application theme"""
        try:
            success = self.settings_service.set_theme(theme)
            if success:
                self.theme_changed.emit(theme)
                self.notify_info("Тема изменена")
            else:
                self.notify_error("Не удалось изменить тему")
        except Exception as ex:
            self.handle_exception(ex, "Ошибка при изменении темы")
    
    def get_current_theme(self) -> str:
        """Get current theme"""
        try:
            return self.settings_service.get_theme()
        except Exception as ex:
            self.handle_exception(ex, "Ошибка при получении темы")
            return "light"
    
    def logout(self):
        """Logout current user"""
        self.auth_service.logout()
        self._current_user = User.create_unauthenticated()
        self.user_logged_out.emit()
        self.notify_info("Вы успешно вышли из системы")
    
    def can_access_admin_features(self) -> bool:
        """Check if current user can access admin features"""
        return self.auth_service.has_admin_access()
    
    def can_access_teacher_features(self) -> bool:
        """Check if current user can access teacher features"""
        return self.auth_service.has_teacher_access()