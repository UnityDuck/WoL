import sys
from PyQt6.QtWidgets import QApplication
from auth_db import AuthDatabase
from login_window import LoginWindow
from main_window import MainWindow


class AppManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.auth_db = AuthDatabase()
        self.login_window = None
        self.main_window = None

    def show_login(self):
        self.login_window = LoginWindow(self.auth_db)
        self.login_window.login_success.connect(self.on_login_success)
        self.login_window.show()

    def on_login_success(self, role: str):
        self.login_window.close()
        self.main_window = MainWindow(role, self.auth_db)
        self.main_window.show()

    def run(self):
        self.show_login()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    manager = AppManager()
    manager.run()