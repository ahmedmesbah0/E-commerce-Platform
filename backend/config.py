"""
Application Configuration
Centralized configuration for the e-commerce platform
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))
    DB_USER = os.getenv('DB_USER', 'ecommerce_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
    DB_NAME = os.getenv('DB_NAME', 'ecommerce_db')
    
    # JWT Configuration
    JWT_SECRET = os.getenv('JWT_SECRET', 'change-this-secret-key-in-production')
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
    
    # Security Configuration
    BCRYPT_ROUNDS = 12
    SESSION_TIMEOUT_MINUTES = 60
    
    # Application Settings
    APP_NAME = "E-Commerce Platform"
    APP_VERSION = "1.0.0"
    DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Payment Configuration (COD ONLY)
    PAYMENT_METHOD = "CASH_ON_DELIVERY"
    TAX_RATE = 0.10  # 10% tax
    DEFAULT_SHIPPING_FEE = 5.00
    
    # Loyalty Configuration
    LOYALTY_POINTS_RATE = 10  # $10 spent = 1 point
    LOYALTY_POINTS_VALUE = 0.01  # 1 point = $0.01
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # File Upload (for product images)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
    MAX_UPLOAD_SIZE_MB = 5
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    @staticmethod
    def get_database_uri():
        """Get complete database connection string"""
        return f"mysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
    
    @staticmethod
    def validate_config():
        """Validate required configuration"""
        errors = []
        
        if not Config.DB_USER:
            errors.append("DB_USER not configured")
        if not Config.DB_PASSWORD:
            errors.append("DB_PASSWORD not configured")
        if not Config.DB_NAME:
            errors.append("DB_NAME not configured")
        if Config.JWT_SECRET == 'change-this-secret-key-in-production':
            errors.append("WARNING: Using default JWT_SECRET. Change in production!")
            
        return errors

# Roles definition
ROLES = {
    'CUSTOMER': 'Customer',
    'SELLER': 'Seller',
    'ADMIN': 'Admin',
    'SUPPORT': 'Support Representative',
    'MANAGER': 'Manager',
    'INVESTOR': 'Investor',
    'SUPPLIER': 'Supplier',
    'DELIVERY': 'Delivery Partner',
    'MARKETING': 'Marketing Agent'
}

# Order Status
ORDER_STATUS = {
    'PENDING': 'PENDING',
    'CONFIRMED': 'CONFIRMED',
    'PROCESSING': 'PROCESSING',
    'SHIPPED': 'SHIPPED',
    'DELIVERED': 'DELIVERED',
    'CANCELLED': 'CANCELLED',
    'REFUNDED': 'REFUNDED'
}

# Payment Status
PAYMENT_STATUS = {
    'UNPAID': 'UNPAID',
    'PAY_ON_ARRIVAL': 'PAY_ON_ARRIVAL',
    'PAID': 'PAID',
    'REFUNDED': 'REFUNDED'
}

# Shipment Status
SHIPMENT_STATUS = {
    'PENDING': 'PENDING',
    'ASSIGNED': 'ASSIGNED',
    'PICKED_UP': 'PICKED_UP',
    'IN_TRANSIT': 'IN_TRANSIT',
    'OUT_FOR_DELIVERY': 'OUT_FOR_DELIVERY',
    'DELIVERED': 'DELIVERED',
    'FAILED': 'FAILED',
    'RETURNED': 'RETURNED'
}

# Ticket Status
TICKET_STATUS = {
    'OPEN': 'OPEN',
    'IN_PROGRESS': 'IN_PROGRESS',
    'WAITING_CUSTOMER': 'WAITING_CUSTOMER',
    'RESOLVED': 'RESOLVED',
    'CLOSED': 'CLOSED'
}

# Ticket Priority
TICKET_PRIORITY = {
    'LOW': 'LOW',
    'MEDIUM': 'MEDIUM',
    'HIGH': 'HIGH',
    'URGENT': 'URGENT'
}
