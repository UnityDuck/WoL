from typing import Any, Callable, Dict
from PyQt6.QtCore import QObject, pyqtSignal


class BaseViewModel(QObject):
    error_occurred = pyqtSignal(str)
    success_occurred = pyqtSignal(str)
    info_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._observers: Dict[str, list] = {}
    
    def notify_error(self, message: str):
        self.error_occurred.emit(message)
    
    def notify_success(self, message: str):
        self.success_occurred.emit(message)
    
    def notify_info(self, message: str):
        self.info_occurred.emit(message)
    
    def handle_exception(self, ex: Exception, context: str = ""):
        error_msg = f"{context}: {str(ex)}" if context else str(ex)
        self.notify_error(error_msg)