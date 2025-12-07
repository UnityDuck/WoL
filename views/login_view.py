"""
Login View - the login window UI
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal
from viewmodels.login_viewmodel import LoginViewModel


class LoginView(QWidget):
    """Login window UI"""
    
    # Signal emitted when login is successful
    login_success = pyqtSignal(object)  # User object
    
    def __init__(self, view_model: LoginViewModel):
        super().__init__()
        self.view_model = view_model
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Авторизация")
        self.setFixedSize(350, 200)
        
        layout = QVBoxLayout()
        
        # Form layout for inputs
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("Логин:", self.username_input)
        form_layout.addRow("Пароль:", self.password_input)
        
        # Login button
        self.login_button = QPushButton("Войти")
        self.login_button.setDefault(True)  # Make it the default button (Enter key)
        
        # Layout arrangement
        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)
        
        self.setLayout(layout)
    
    def connect_signals(self):
        """Connect UI signals to ViewModel"""
        self.login_button.clicked.connect(self.on_login_clicked)
        self.view_model.login_success.connect(self.on_login_success)
        self.view_model.login_failed.connect(self.on_login_failed)
        self.view_model.error_occurred.connect(self.on_error)
        self.view_model.success_occurred.connect(self.on_success)
        
        # Also connect Enter key in password field to login
        self.password_input.returnPressed.connect(self.on_login_clicked)
    
    def on_login_clicked(self):
        """Handle login button click"""
        # Update ViewModel properties
        self.view_model.username = self.username_input.text().strip()
        self.view_model.password = self.password_input.text()
        
        # Attempt login
        self.view_model.login()
    
    def on_login_success(self, user):
        """Handle successful login"""
        self.login_success.emit(user)
        self.close()
    
    def on_login_failed(self):
        """Handle failed login"""
        # Clear password field
        self.password_input.clear()
        # Focus back to username
        self.username_input.setFocus()
    
    def on_error(self, message: str):
        """Handle error notification"""
        QMessageBox.critical(self, "Ошибка", message)
    
    def on_success(self, message: str):
        """Handle success notification"""
        QMessageBox.information(self, "Успех", message)
    
    def showEvent(self, event):
        """Override show event to focus on username field"""
        super().showEvent(event)
        self.username_input.setFocus()