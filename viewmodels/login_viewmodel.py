from PyQt6.QtCore import pyqtSignal
from .base_viewmodel import BaseViewModel
from models.auth_service import AuthService
from models.user import User


class LoginViewModel(BaseViewModel):
    login_success = pyqtSignal(User)
    login_failed = pyqtSignal()
    
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self._username = ""
        self._password = ""
    
    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, value: str):
        self._username = value
    
    @property
    def password(self) -> str:
        return self._password
    
    @password.setter
    def password(self, value: str):
        self._password = value
    
    def validate_inputs(self) -> bool:
        if not self._username.strip():
            self.notify_error("Введите логин")
            return False
        if not self._password:
            self.notify_error("Введите пароль")
            return False
        return True
    
    def login(self):
        try:
            if not self.validate_inputs():
                return
            
            success, user = self.auth_service.authenticate_user(
                self._username, 
                self._password
            )
            
            if success and user:
                self.login_success.emit(user)
                self.notify_success(f"Добро пожаловать, {user.username}!")
            else:
                self.login_failed.emit()
                self.notify_error("Неверный логин или пароль")
        except Exception as ex:
            self.handle_exception(ex, "Ошибка при попытке входа")
            self.login_failed.emit()
    
    def logout(self):
        self.auth_service.logout()