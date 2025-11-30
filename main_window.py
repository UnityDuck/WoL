# main_window.py
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from theme_manager import ThemeManager


class MainWindow(QWidget):
    def __init__(self, role: str, auth_db):
        super().__init__()
        self.role = role
        self.auth_db = auth_db
        self.current_theme = self.auth_db.get_theme()
        ThemeManager.apply_theme(self.current_theme)

        self.computers = self.load_computers()
        self.setWindowTitle(f"Управление ПК — {role}")
        self.resize(850, 600)
        self.init_ui()

    def load_computers(self):
        try:
            with open("computers.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить computers.json:\n{e}")
            return {}

    def init_ui(self):
        layout = QVBoxLayout()

        # Панель выбора темы
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Тема интерфейса:"))
        self.theme_combo = QComboBox()
        theme_map_ui = {"light": "Светлая", "dark": "Тёмная", "glass": "Стекло"}
        self.theme_combo.addItems(theme_map_ui.values())
        current_ui = theme_map_ui.get(self.current_theme, "Светлая")
        self.theme_combo.setCurrentText(current_ui)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)

        # Выбор кабинета
        room_layout = QHBoxLayout()
        room_layout.addWidget(QLabel("Кабинет:"))
        self.classroom_combo = QComboBox()
        self.classroom_combo.addItems(self.computers.keys())
        self.classroom_combo.currentTextChanged.connect(self.update_pc_table)
        room_layout.addWidget(self.classroom_combo)
        layout.addLayout(room_layout)

        # Таблица ПК
        self.pc_table = QTableWidget(0, 3)
        self.pc_table.setHorizontalHeaderLabels(["Имя компьютера", "IP-адрес", "Статус"])
        header = self.pc_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.pc_table)

        self.setLayout(layout)
        self.update_pc_table()

    def update_pc_table(self):
        room = self.classroom_combo.currentText()
        pcs = self.computers.get(room, [])
        self.pc_table.setRowCount(len(pcs))
        for row, pc in enumerate(pcs):
            self.pc_table.setItem(row, 0, QTableWidgetItem(pc["name"]))
            self.pc_table.setItem(row, 1, QTableWidgetItem(pc["ip"]))
            status_item = QTableWidgetItem("Онлайн / Оффлайн")
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.pc_table.setItem(row, 2, status_item)

    def on_theme_changed(self, ui_name: str):
        ui_to_theme = {"Светлая": "light", "Тёмная": "dark", "Стекло": "glass"}
        theme = ui_to_theme.get(ui_name, "light")
        self.auth_db.set_theme(theme)
        ThemeManager.apply_theme(theme)
        if theme == "glass":
            QMessageBox.information(
                self,
                "Тема «Стекло»",
                "Для лучшего отображения эффекта стекла рекомендуется перезапустить приложение."
            )