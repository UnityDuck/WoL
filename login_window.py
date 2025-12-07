from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from theme_manager import ThemeManager


class LoginWindow(QWidget):
    login_success = pyqtSignal(str)  # роль

    def __init__(self, auth_db):
        super().__init__()
        self.auth_db = auth_db
        current_theme = self.auth_db.get_theme()
        ThemeManager.apply_theme(current_theme)

        self.setWindowTitle("Авторизация")
        self.setFixedSize(350, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Логин:", self.username_input)
        form_layout.addRow("Пароль:", self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.attempt_login)

        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        success, role = self.auth_db.verify_password(username, password)
        if success:
            self.login_success.emit(role)
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль!")