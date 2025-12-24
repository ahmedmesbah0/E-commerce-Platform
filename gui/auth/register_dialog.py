"""
Registration Dialog
Allow new customers to create accounts
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import logging
from backend.services.auth_service import AuthService

logger = logging.getLogger(__name__)


class RegisterDialog(QDialog):
    """Customer registration dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle('Register New Account')
        self.setMinimumSize(450, 500)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Title
        title = QLabel('Create Customer Account')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel('Register as a new customer')
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Choose a username')
        self.username_input.setMinimumHeight(40)
        form_layout.addRow('Username:', self.username_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('your.email@example.com')
        self.email_input.setMinimumHeight(40)
        form_layout.addRow('Email:', self.email_input)
        
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText('First name')
        self.first_name_input.setMinimumHeight(40)
        form_layout.addRow('First Name:', self.first_name_input)
        
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText('Last name')
        self.last_name_input.setMinimumHeight(40)
        form_layout.addRow('Last Name:', self.last_name_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('+1234567890 (optional)')
        self.phone_input.setMinimumHeight(40)
        form_layout.addRow('Phone:', self.phone_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText('Choose a strong password')
        self.password_input.setMinimumHeight(40)
        form_layout.addRow('Password:', self.password_input)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText('Confirm your password')
        self.confirm_password_input.setMinimumHeight(40)
        form_layout.addRow('Confirm Password:', self.confirm_password_input)
        
        layout.addLayout(form_layout)
        
        # Password requirements
        requirements = QLabel(
            '• Password must be at least 8 characters\n'
            '• Include uppercase and lowercase letters\n'
            '• Include at least one number'
        )
        requirements_font = QFont()
        requirements_font.setPointSize(9)
        requirements.setFont(requirements_font)
        requirements.setStyleSheet('color: #888;')
        layout.addWidget(requirements)
        
        layout.addSpacing(10)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.setProperty('class', 'secondary')
        cancel_btn.setMinimumHeight(45)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        self.register_btn = QPushButton('Register as Customer')
        self.register_btn.setProperty('class', 'success')
        self.register_btn.setMinimumHeight(45)
        register_font = QFont()
        register_font.setBold(True)
        self.register_btn.setFont(register_font)
        self.register_btn.clicked.connect(self.handle_register)
        button_layout.addWidget(self.register_btn)
        
        layout.addLayout(button_layout)
    
    def handle_register(self):
        """Handle registration"""
        # Get input values
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Validate required fields
        if not all([username, email, first_name, last_name, password, confirm_password]):
            QMessageBox.warning(
                self,
                'Missing Information',
                'Please fill in all required fields.\n(Phone is optional)'
            )
            return
        
        # Check password match
        if password != confirm_password:
            QMessageBox.warning(
                self,
                'Password Mismatch',
                'Passwords do not match. Please try again.'
            )
            self.confirm_password_input.clear()
            return
        
        # Disable button during registration
        self.register_btn.setEnabled(False)
        self.register_btn.setText('Creating account...')
        
        try:
            # Register user (default role is Customer)
            success, error_msg = AuthService.register_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone if phone else None,
                role_name='Customer'  # Default to Customer role
            )
            
            if success:
                QMessageBox.information(
                    self,
                    'Registration Successful',
                    f'Welcome {first_name}!\n\n'
                    f'Your customer account has been created.\n'
                    f'Username: {username}\n\n'
                    f'You can now login with your credentials.'
                )
                self.accept()  # Close dialog with success
            else:
                QMessageBox.warning(
                    self,
                    'Registration Failed',
                    f'Could not create account:\n\n{error_msg}'
                )
        
        except Exception as e:
            logger.error(f"Registration error: {e}")
            QMessageBox.critical(
                self,
                'Error',
                'An unexpected error occurred during registration.\nPlease try again.'
            )
        
        finally:
            # Re-enable button
            self.register_btn.setEnabled(True)
            self.register_btn.setText('Register as Customer')
