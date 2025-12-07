"""
Main View - the main application window UI
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,
    QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from viewmodels.main_viewmodel import MainViewModel
from models.user import User
from utils.theme_manager import ThemeManager


class MainView(QWidget):
    """Main application window UI"""
    
    def __init__(self, view_model: MainViewModel):
        super().__init__()
        self.view_model = view_model
        self.setup_ui()
        self.connect_signals()
        self.initialize_data()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Set up window properties
        self.setWindowTitle(f"Управление ПК")
        self.resize(900, 650)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Top panel with user info, theme selector and logout
        top_panel = QHBoxLayout()
        
        # User info
        self.user_info_label = QLabel()
        self.user_info_label.setStyleSheet("font-weight: bold; color: #2c3e50; padding: 5px;")
        top_panel.addWidget(self.user_info_label)
        
        # Spacer
        top_panel.addStretch()
        
        # Theme selector
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Тема интерфейса:"))
        self.theme_combo = QComboBox()
        theme_map_ui = {"light": "Светлая", "dark": "Тёмная", "glass": "Стекло"}
        self.theme_combo.addItems(theme_map_ui.values())
        theme_layout.addWidget(self.theme_combo)
        top_panel.addLayout(theme_layout)
        
        # Logout button
        self.logout_button = QPushButton("Выйти")
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        top_panel.addWidget(self.logout_button)
        
        main_layout.addLayout(top_panel)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        
        # Classroom selection
        classroom_layout = QHBoxLayout()
        classroom_layout.addWidget(QLabel("Кабинет:"))
        self.classroom_combo = QComboBox()
        classroom_layout.addWidget(self.classroom_combo)
        classroom_layout.addStretch()
        main_layout.addLayout(classroom_layout)
        
        # Computers table
        self.pc_table = QTableWidget()
        self.pc_table.setColumnCount(4)  # Name, IP, Status, Actions
        self.pc_table.setHorizontalHeaderLabels(["Имя компьютера", "IP-адрес", "Статус", "Действия"])
        
        # Configure header
        header = self.pc_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        main_layout.addWidget(self.pc_table)
        
        self.setLayout(main_layout)
    
    def connect_signals(self):
        """Connect UI signals to ViewModel"""
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        self.classroom_combo.currentTextChanged.connect(self.on_classroom_changed)
        self.logout_button.clicked.connect(self.on_logout_clicked)
        
        # Connect ViewModel signals
        self.view_model.computers_changed.connect(self.update_pc_table)
        self.view_model.classrooms_changed.connect(self.update_classroom_combo)
        self.view_model.theme_changed.connect(self.on_theme_updated)
        self.view_model.user_logged_out.connect(self.on_user_logged_out)
        self.view_model.error_occurred.connect(self.on_error)
        self.view_model.success_occurred.connect(self.on_success)
        self.view_model.info_occurred.connect(self.on_info)
    
    def initialize_data(self):
        """Initialize UI with data from ViewModel"""
        # Update user info
        self.update_user_info()
        
        # Load classrooms
        self.update_classroom_combo()
        
        # Apply current theme
        current_theme = self.view_model.get_current_theme()
        theme_map_ui = {"light": "Светлая", "dark": "Тёмная", "glass": "Стекло"}
        current_ui = theme_map_ui.get(current_theme, "Светлая")
        self.theme_combo.setCurrentText(current_ui)
        ThemeManager.apply_theme(current_theme)
    
    def update_user_info(self):
        """Update user information display"""
        user = self.view_model.current_user
        if user.is_authenticated:
            role_text = "Администратор" if user.role == "admin" else "Преподаватель"
            self.user_info_label.setText(f"Пользователь: {user.username} | Роль: {role_text}")
        else:
            self.user_info_label.setText("Гость")
    
    def update_classroom_combo(self):
        """Update classroom selection combo box"""
        self.classroom_combo.clear()
        classrooms = self.view_model.load_classrooms()
        self.classroom_combo.addItems(classrooms)
    
    def update_pc_table(self):
        """Update the computers table"""
        computers = self.view_model.computers
        self.pc_table.setRowCount(len(computers))
        
        for row, computer in enumerate(computers):
            # Computer name
            name_item = QTableWidgetItem(computer.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.pc_table.setItem(row, 0, name_item)
            
            # IP address
            ip_item = QTableWidgetItem(computer.ip_address)
            ip_item.setFlags(ip_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.pc_table.setItem(row, 1, ip_item)
            
            # Status
            status_item = QTableWidgetItem(computer.status.title())
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            # Color code status
            if computer.is_online():
                status_item.setBackground(Qt.GlobalColor.green)
                status_item.setForeground(Qt.GlobalColor.white)
            elif computer.is_offline():
                status_item.setBackground(Qt.GlobalColor.red)
                status_item.setForeground(Qt.GlobalColor.white)
            elif computer.is_in_maintenance():
                status_item.setBackground(Qt.GlobalColor.orange)
                status_item.setForeground(Qt.GlobalColor.black)
            self.pc_table.setItem(row, 2, status_item)
            
            # Actions (buttons for changing status)
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(3)
            
            # Online button
            online_btn = QPushButton("Онлайн")
            online_btn.setFixedSize(60, 25)
            online_btn.clicked.connect(lambda _, name=computer.name: self.set_computer_status(name, "online"))
            
            # Offline button
            offline_btn = QPushButton("Оффлайн")
            offline_btn.setFixedSize(60, 25)
            offline_btn.clicked.connect(lambda _, name=computer.name: self.set_computer_status(name, "offline"))
            
            # Maintenance button
            maint_btn = QPushButton("Обслуживание")
            maint_btn.setFixedSize(80, 25)
            maint_btn.clicked.connect(lambda _, name=computer.name: self.set_computer_status(name, "maintenance"))
            
            actions_layout.addWidget(online_btn)
            actions_layout.addWidget(offline_btn)
            actions_layout.addWidget(maint_btn)
            actions_layout.addStretch()
            
            self.pc_table.setCellWidget(row, 3, actions_widget)
        
        # Resize columns to fit content
        self.pc_table.resizeColumnsToContents()
    
    def set_computer_status(self, name: str, status: str):
        """Set computer status"""
        try:
            success = self.view_model.computer_service.update_computer_status(name, status)
            if success:
                self.view_model.refresh_data()  # Refresh the view
                self.view_model.notify_success(f"Статус компьютера {name} изменен на {status}")
            else:
                self.view_model.notify_error(f"Не удалось изменить статус компьютера {name}")
        except Exception as ex:
            self.view_model.handle_exception(ex, f"Ошибка при изменении статуса компьютера {name}")
    
    def on_theme_changed(self, ui_name: str):
        """Handle theme selection change"""
        ui_to_theme = {"Светлая": "light", "Тёмная": "dark", "Стекло": "glass"}
        theme = ui_to_theme.get(ui_name, "light")
        self.view_model.change_theme(theme)
    
    def on_theme_updated(self, theme: str):
        """Handle theme update from ViewModel"""
        ThemeManager.apply_theme(theme)
        if theme == "glass":
            self.view_model.notify_info(
                "Для лучшего отображения эффекта стекла рекомендуется перезапустить приложение."
            )
    
    def on_classroom_changed(self, classroom: str):
        """Handle classroom selection change"""
        self.view_model.current_classroom = classroom
    
    def on_logout_clicked(self):
        """Handle logout button click"""
        reply = QMessageBox.question(
            self, 
            "Подтверждение", 
            "Вы действительно хотите выйти?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.view_model.logout()
    
    def on_user_logged_out(self):
        """Handle user logout"""
        self.close()
    
    def on_error(self, message: str):
        """Handle error notification"""
        QMessageBox.critical(self, "Ошибка", message)
    
    def on_success(self, message: str):
        """Handle success notification"""
        QMessageBox.information(self, "Успех", message)
    
    def on_info(self, message: str):
        """Handle info notification"""
        QMessageBox.information(self, "Информация", message)