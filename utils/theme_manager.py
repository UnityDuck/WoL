from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt


class ThemeManager:
    @staticmethod
    def apply_theme(theme_name: str):
        app = QApplication.instance()
        if not app:
            return

        app.setStyleSheet("")  # сброс кастомного CSS

        if theme_name == "light":
            ThemeManager._apply_light(app)
        elif theme_name == "dark":
            ThemeManager._apply_dark(app)
        elif theme_name == "glass":
            ThemeManager._apply_glass(app)
        else:
            ThemeManager._apply_light(app)

    @staticmethod
    def _apply_light(app):
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(230, 230, 230))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Button, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        app.setPalette(palette)
        app.setFont(QFont("Segoe UI", 10))

    @staticmethod
    def _apply_dark(app):
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(70, 70, 70))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        app.setPalette(palette)
        app.setFont(QFont("Segoe UI", 10))

    @staticmethod
    def _apply_glass(app):
        app.setStyle("Fusion")
        # Палитра — светлая основа
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(250, 250, 250))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Base, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.Text, QColor(20, 20, 20))
        palette.setColor(QPalette.ColorRole.Button, QColor(235, 235, 235))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(100, 180, 255))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        app.setPalette(palette)
        app.setFont(QFont("Segoe UI", 10))

        app.setStyleSheet("""
            QMainWindow, QWidget {
                background: rgba(255, 255, 255, 230);
                border-radius: 12px;
            }
            QTableWidget {
                background: rgba(250, 250, 250, 240);
                border: 1px solid rgba(200, 200, 200, 120);
                border-radius: 8px;
                gridline-color: rgba(200, 200, 200, 100);
            }
            QHeaderView::section {
                background: rgba(240, 240, 240, 220);
                padding: 4px;
                border: none;
                border-right: 1px solid rgba(200, 200, 200, 100);
            }
            QLineEdit, QComboBox {
                background: rgba(255, 255, 255, 240);
                border: 1px solid rgba(180, 180, 180, 120);
                border-radius: 6px;
                padding: 4px;
            }
            QPushButton {
                background: rgba(240, 240, 240, 220);
                border: 1px solid rgba(180, 180, 180, 100);
                border-radius: 8px;
                padding: 6px;
                color: #1e1e1e;
            }
            QPushButton:hover {
                background: rgba(220, 220, 220, 230);
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #ccc;
            }
        """)