"""
Support Dashboard - Support Representative interface
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTabWidget, QFrame, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
import logging
from backend.database import db
from gui.utils.theme import Theme

logger = logging.getLogger(__name__)

class SupportDashboard(QMainWindow):
    logout_requested = pyqtSignal()
    
    def __init__(self, user_data, token, theme='dark'):
        super().__init__()
        self.user_data = user_data
        self.token = token
        self.current_theme = theme
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        self.setWindowTitle("Support Dashboard")
        self.setMinimumSize(1200, 800)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Top bar
        top_bar = QFrame()
        top_layout = QHBoxLayout(top_bar)
        title = QLabel("🎧 Support Dashboard")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        top_layout.addWidget(title)
        top_layout.addStretch()
        
        logout_btn = QPushButton("Logout")
        logout_btn.setProperty('class', 'danger')
        logout_btn.clicked.connect(self.handle_logout)
        top_layout.addWidget(logout_btn)
        layout.addWidget(top_bar)
        
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_tickets_tab(), "📋 Tickets")
        tabs.addTab(self.create_profile_tab(), "👤 Profile")
        layout.addWidget(tabs)
    
    def create_tickets_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Ticket #", "Customer", "Subject", "Priority", "Status"])
        layout.addWidget(table)
        return widget
    
    def create_profile_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(f"Name: {self.user_data['first_name']} {self.user_data['last_name']}"))
        layout.addWidget(QLabel(f"Email: {self.user_data['email']}"))
        layout.addWidget(QLabel("Role: Support Representative"))
        layout.addStretch()
        return widget
    
    def apply_theme(self):
        self.setStyleSheet(Theme.get_dark_stylesheet() if self.current_theme == 'dark' else Theme.get_light_stylesheet())
    
    def handle_logout(self):
        from backend.services.auth_service import AuthService
        AuthService.logout(self.token)
        self.logout_requested.emit()
        self.close()
