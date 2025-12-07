#!/usr/bin/env python3
"""
Application startup script with database connection check
"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox

# Add the workspace to the Python path
sys.path.insert(0, '/workspace')

from main import Application
from models.database import DatabaseManager
from config import Config


def main():
    """Main entry point with database connection check"""
    app = QApplication(sys.argv)
    
    # Check if we can connect to the database
    db_config = Config.get_db_config()
    db_manager = DatabaseManager(**db_config)
    
    if not db_manager.test_connection():
        # Show warning about database connection
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Предупреждение")
        msg.setText("Не удалось подключиться к базе данных PostgreSQL.")
        msg.setInformativeText(
            "Убедитесь, что PostgreSQL запущен и настроен с параметрами:\n"
            f"  Хост: {db_config['host']}\n"
            f"  Порт: {db_config['port']}\n"
            f"  Пользователь: {db_config['user']}\n\n"
            "По умолчанию используются следующие учетные данные:\n"
            "  Логин: teacher, Пароль: 123456\n"
            "  Логин: admin, Пароль: admin123"
        )
        msg.exec()
        return 1
    
    # Initialize and run the application
    try:
        application = Application()
        application.run()
    except Exception as e:
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Icon.Critical)
        error_msg.setWindowTitle("Ошибка")
        error_msg.setText(f"Произошла ошибка при запуске приложения: {str(e)}")
        error_msg.exec()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())