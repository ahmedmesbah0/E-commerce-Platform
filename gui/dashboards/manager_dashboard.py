"""Remaining dashboards - Manager, Investor, Supplier, Delivery Partner, Marketing Agent"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QFrame, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from backend.services.auth_service import AuthService
from gui.utils.theme import Theme

class BaseDashboard(QMainWindow):
    logout_requested = pyqtSignal()
    
    def __init__(self, user_data, token, title, theme='dark'):
        super().__init__()
        self.user_data = user_data
        self.token = token
        self.current_theme = theme
        self.setWindowTitle(title)
        self.setMinimumSize(1200, 800)
        self.init_ui(title)
        self.apply_theme()
    
    def init_ui(self, title):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        top_bar = QFrame()
        top_layout = QHBoxLayout(top_bar)
        title_label = QLabel(title)
        title_label.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        
        logout_btn = QPushButton("Logout")
        logout_btn.setProperty('class', 'danger')
        logout_btn.clicked.connect(self.handle_logout)
        top_layout.addWidget(logout_btn)
        layout.addWidget(top_bar)
        
        info = QLabel(f"Welcome, {self.user_data['first_name']} {self.user_data['last_name']}\n\n"
                     f"Email: {self.user_data['email']}\n"
                     f"Role: {', '.join(self.user_data['roles'])}")
        info.setFont(QFont('Segoe UI', 12))
        layout.addWidget(info)
        layout.addStretch()
    
    def apply_theme(self):
        self.setStyleSheet(Theme.get_dark_stylesheet() if self.current_theme == 'dark' else Theme.get_light_stylesheet())
    
    def handle_logout(self):
        AuthService.logout(self.token)
        self.logout_requested.emit()
        self.close()

class ManagerDashboard(BaseDashboard):
    def __init__(self, user_data, token, theme='dark'):
        super().__init__(user_data, token, "📊 Manager Dashboard", theme)

class InvestorDashboard(BaseDashboard):
    def __init__(self, user_data, token, theme='dark'):
        super().__init__(user_data, token, "💰 Investor Dashboard", theme)

class SupplierDashboard(BaseDashboard):
    def __init__(self, user_data, token, theme='dark'):
        super().__init__(user_data, token, "📦 Supplier Dashboard", theme)

class DeliveryDashboard(BaseDashboard):
    def __init__(self, user_data, token, theme='dark'):
        super().__init__(user_data, token, "🚚 Delivery Partner Dashboard", theme)

class MarketingDashboard(BaseDashboard):
    def __init__(self, user_data, token, theme='dark'):
        super().__init__(user_data, token, "📢 Marketing Agent Dashboard", theme)
