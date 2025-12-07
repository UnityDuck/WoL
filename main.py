import sys
from PyQt6.QtWidgets import QApplication
from models.database import DatabaseManager
from models.auth_service import AuthService
from models.computer_service import ComputerService
from models.settings_service import SettingsService
from viewmodels.login_viewmodel import LoginViewModel
from viewmodels.main_viewmodel import MainViewModel
from views.login_view import LoginView
from views.main_view import MainView
from config import Config


class Application:
    
    def __init__(self):
        self.app = QApplication(sys.argv)

        db_config = Config.get_db_config()
        self.db_manager = DatabaseManager(**db_config)
        self.auth_service = AuthService(self.db_manager)
        self.computer_service = ComputerService(self.db_manager)
        self.settings_service = SettingsService(self.db_manager)

        self.login_viewmodel = LoginViewModel(self.auth_service)
        self.main_viewmodel = MainViewModel(
            self.auth_service,
            self.computer_service,
            self.settings_service
        )

        self.login_view = LoginView(self.login_viewmodel)
        self.main_view = None

        self.login_view.login_success.connect(self.on_login_success)
    
    def on_login_success(self, user):
        # Create and show main window
        self.main_view = MainView(self.main_viewmodel)
        self.main_view.show()

        role_text = "Администратор" if user.role == "admin" else "Преподаватель"
        self.main_view.setWindowTitle(f"Управление ПК — {role_text}")
    
    def run(self):
        self.login_view.show()
        sys.exit(self.app.exec())


def main():
    application = Application()
    application.run()


if __name__ == "__main__":
    main()