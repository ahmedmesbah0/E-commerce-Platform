"""
Login Window
Professional login interface for the e-commerce platform
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QCheckBox, QMessageBox,
    QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
import logging
from backend.services.auth_service import AuthService
from gui.utils.theme import Theme

logger = logging.getLogger(__name__)


class LoginWindow(QWidget):
    """Login window widget"""
    
    login_successful = pyqtSignal(dict, str)  # user_data, token
    
    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'
        self.current_dashboard = None  # Store active dashboard reference
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle('E-Commerce Platform - Login')
        self.setMinimumSize(420, 650)  # Increased height for register button
        self.resize(450, 700)
        
        # Center window
        self.center_window()
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Add spacing at top
        main_layout.addStretch()
        
        # Logo/Title section
        title_label = QLabel('E-Commerce Platform')
        title_label.setProperty('class', 'title')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel('Academic Demonstration System')
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(30)
        
        # Login form container
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Username field
        username_label = QLabel('Username or Email')
        username_label.setFont(QFont('Segoe UI', 10, QFont.Weight.Medium))
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username or email')
        self.username_input.setMinimumHeight(45)
        self.username_input.returnPressed.connect(self.handle_login)
        form_layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel('Password')
        password_label.setFont(QFont('Segoe UI', 10, QFont.Weight.Medium))
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.returnPressed.connect(self.handle_login)
        form_layout.addWidget(self.password_input)
        
        # Remember me checkbox
        remember_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox('Remember me')
        remember_layout.addWidget(self.remember_checkbox)
        remember_layout.addStretch()
        form_layout.addLayout(remember_layout)
        
        # Login button
        self.login_button = QPushButton('Login')
        self.login_button.setMinimumHeight(45)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button_font = QFont()
        login_button_font.setPointSize(11)
        login_button_font.setBold(True)
        self.login_button.setFont(login_button_font)
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)
        
        # Register button
        self.register_button = QPushButton('Create New Account')
        self.register_button.setProperty('class', 'secondary')
        self.register_button.setMinimumHeight(45)
        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_button.clicked.connect(self.show_register_dialog)
        form_layout.addWidget(self.register_button)
        
        main_layout.addWidget(form_frame)
        
        main_layout.addSpacing(20)
        
        # Demo credentials info
        demo_frame = QFrame()
        demo_frame.setObjectName('demoFrame')
        demo_layout = QVBoxLayout(demo_frame)
        demo_layout.setContentsMargins(15, 15, 15, 15)
        
        demo_title = QLabel('Demo Credentials')
        demo_title.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        demo_layout.addWidget(demo_title)
        
        demo_info = QLabel(
            'Username: customer1 / seller1 / admin1\n'
            'support1 / manager1 / investor1\n'
            'supplier1 / delivery1 / marketing1\n\n'
            'Password: Password123 (all users)'
        )
        demo_info.setFont(QFont('Segoe UI', 9))
        demo_info.setWordWrap(True)  # Enable word wrapping
        demo_info.setAlignment(Qt.AlignmentFlag.AlignLeft)
        demo_layout.addWidget(demo_info)
        
        main_layout.addWidget(demo_frame)
        
        # Theme toggle button
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        self.theme_button = QPushButton('☀ Light Mode')
        self.theme_button.setProperty('class', 'secondary')
        self.theme_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_button.clicked.connect(self.toggle_theme)
        theme_layout.addWidget(self.theme_button)
        main_layout.addLayout(theme_layout)
        
        main_layout.addStretch()
        
        # Footer
        footer_label = QLabel('© 2024 E-Commerce Platform - University Project')
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setFont(QFont('Segoe UI', 8))
        main_layout.addWidget(footer_label)
        
        self.setLayout(main_layout)
    
    def center_window(self):
        """Center window on screen"""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(
                self,
                'Input Required',
                'Please enter both username and password.'
            )
            return
        
        # Disable login button during authentication
        self.login_button.setEnabled(False)
        self.login_button.setText('Logging in...')
        
        try:
            # Attempt login
            success, user_data, result = AuthService.login(username, password)
            
            if success:
                logger.info(f"Login successful for user: {username}")
                
                # Import dashboards here to avoid circular imports
                from gui.dashboards.customer_dashboard import CustomerDashboard
                from gui.dashboards.seller_dashboard import SellerDashboard
                from gui.dashboards.admin_dashboard import AdminDashboard
                from gui.dashboards.support_dashboard import SupportDashboard
                from gui.dashboards.manager_dashboard import ManagerDashboard
                from gui.dashboards.investor_dashboard import InvestorDashboard
                from gui.dashboards.supplier_dashboard import SupplierDashboard
                from gui.dashboards.delivery_dashboard import DeliveryDashboard
                from gui.dashboards.marketing_dashboard import MarketingDashboard
                
                # Determine dashboard based on primary role
                primary_role = user_data['roles'][0] if user_data['roles'] else None
                dashboard = None
                
                if primary_role == 'Customer':
                    dashboard = CustomerDashboard(user_data, result, self.current_theme)
                elif primary_role == 'Seller':
                    dashboard = SellerDashboard(user_data, result, self.current_theme)
                elif primary_role == 'Admin':
                    dashboard = AdminDashboard(user_data, result, self.current_theme)
                elif primary_role == 'Support Representative':
                    dashboard = SupportDashboard(user_data, result, self.current_theme)
                elif primary_role == 'Manager':
                    dashboard = ManagerDashboard(user_data, result, self.current_theme)
                elif primary_role == 'Investor':
                    dashboard = InvestorDashboard(user_data, result, self.current_theme)
                elif primary_role == 'Supplier':
                    dashboard = SupplierDashboard(user_data, result, self.current_theme)
                elif primary_role == 'Delivery Partner':
                    dashboard = DeliveryDashboard(user_data, result, self.current_theme)
                elif primary_role == 'Marketing Agent':
                    dashboard = MarketingDashboard(user_data, result, self.current_theme)
                else:
                    QMessageBox.warning(self, 'Error', 'Unknown role. Please contact administrator.')
                    return
                
                # Show dashboard and hide login window
                if dashboard:
                    self.current_dashboard = dashboard  # Store reference to prevent garbage collection
                    dashboard.show()
                    self.hide()
                    
                    # Connect dashboard logout signal to show login again
                    dashboard.logout_requested.connect(self.show_login_window)
            
            else:
                QMessageBox.warning(
                    self,
                    'Login Failed',
                    result  # Error message from AuthService
                )
                self.password_input.clear()
            
        except Exception as e:
            logger.error(f"Login error: {e}")
            QMessageBox.critical(
                self,
                'Error',
                'An unexpected error occurred during login.\nPlease try again.'
            )
        
        finally:
            # Re-enable login button
            self.login_button.setEnabled(True)
            self.login_button.setText('Login')
    
    def show_register_dialog(self):
        """Show registration dialog"""
        from gui.auth.register_dialog import RegisterDialog
        
        dialog = RegisterDialog(self)
        
        # Apply current theme to dialog
        if self.current_theme == 'dark':
            dialog.setStyleSheet(Theme.get_dark_stylesheet())
        else:
            dialog.setStyleSheet(Theme.get_light_stylesheet())
        
        # If registration successful, show success message
        if dialog.exec() == dialog.DialogCode.Accepted:
            QMessageBox.information(
                self,
                'Registration Complete',
                'Your account has been created successfully!\n\n'
                'Please login with your new credentials.'
            )
    
    def show_login_window(self):
        """Show login window again (after logout)"""
        self.username_input.clear()
        self.password_input.clear()
        self.show()
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        if self.current_theme == 'dark':
            self.current_theme = 'light'
            self.theme_button.setText('🌙 Dark Mode')
        else:
            self.current_theme = 'dark'
            self.theme_button.setText('☀ Light Mode')
        
        self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme"""
        if self.current_theme == 'dark':
            self.setStyleSheet(Theme.get_dark_stylesheet())
        else:
            self.setStyleSheet(Theme.get_light_stylesheet())
