"""
Base ViewModel class providing common functionality for all ViewModels
"""
from typing import Any, Callable, Dict
from PyQt6.QtCore import QObject, pyqtSignal


class BaseViewModel(QObject):
    """Base class for all ViewModels providing common functionality"""
    
    # Signal for error notifications
    error_occurred = pyqtSignal(str)
    # Signal for success notifications
    success_occurred = pyqtSignal(str)
    # Signal for info notifications
    info_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._observers: Dict[str, list] = {}
    
    def notify_error(self, message: str):
        """Notify about an error"""
        self.error_occurred.emit(message)
    
    def notify_success(self, message: str):
        """Notify about a success"""
        self.success_occurred.emit(message)
    
    def notify_info(self, message: str):
        """Notify about an info message"""
        self.info_occurred.emit(message)
    
    def handle_exception(self, ex: Exception, context: str = ""):
        """Handle an exception and notify about it"""
        error_msg = f"{context}: {str(ex)}" if context else str(ex)
        self.notify_error(error_msg)