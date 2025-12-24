"""
Security Utilities
Password hashing, JWT tokens, input validation
"""

import bcrypt
import jwt
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging
from backend.config import Config

logger = logging.getLogger(__name__)


class SecurityUtils:
    """Security utility functions"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=Config.BCRYPT_ROUNDS)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            password: Plain text password
            hashed_password: Hashed password from database
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    @staticmethod
    def generate_token(user_id: int, username: str, roles: list) -> str:
        """
        Generate a JWT token
        
        Args:
            user_id: User ID
            username: Username
            roles: List of role names
            
        Returns:
            JWT token string
        """
        expiration = datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
        
        payload = {
            'user_id': user_id,
            'username': username,
            'roles': roles,
            'exp': expiration,
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, Config.JWT_SECRET, algorithm='HS256')
        return token
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded payload dict or None if invalid
        """
        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: Email address string
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format
        
        Args:
            phone: Phone number string
            
        Returns:
            True if valid, False otherwise
        """
        # Allow +, digits, spaces, hyphens, parentheses
        pattern = r'^\+?[\d\s\-\(\)]{10,20}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """
        Validate password strength
        
        Args:
            password: Password string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        return True, ""
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 1000) -> str:
        """
        Sanitize user input to prevent injection attacks
        
        Args:
            text: Input text
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
        """
        if text is None:
            return ""
        
        # Trim to max length
        text = str(text)[:max_length]
        
        # Remove any potential SQL injection patterns (basic)
        dangerous_patterns = [
            r'--',  # SQL comments
            r';',   # Statement separator
            r'/*',  # Multi-line comment start
            r'*/',  # Multi-line comment end
        ]
        
        for pattern in dangerous_patterns:
            text = text.replace(pattern, '')
        
        return text.strip()
    
    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        """
        Validate username format
        
        Args:
            username: Username string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(username) > 50:
            return False, "Username must be at most 50 characters long"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, ""


class PermissionChecker:
    """Check user permissions"""
    
    @staticmethod
    def has_role(user_roles: list, required_role: str) -> bool:
        """
        Check if user has a specific role
        
        Args:
            user_roles: List of user's role names
            required_role: Required role name
            
        Returns:
            True if user has the role
        """
        return required_role in user_roles
    
    @staticmethod
    def has_any_role(user_roles: list, required_roles: list) -> bool:
        """
        Check if user has any of the specified roles
        
        Args:
            user_roles: List of user's role names
            required_roles: List of required role names
            
        Returns:
            True if user has at least one of the roles
        """
        return any(role in user_roles for role in required_roles)
    
    @staticmethod
    def has_all_roles(user_roles: list, required_roles: list) -> bool:
        """
        Check if user has all of the specified roles
        
        Args:
            user_roles: List of user's role names
            required_roles: List of required role names
            
        Returns:
            True if user has all the roles
        """
        return all(role in user_roles for role in required_roles)
    
    @staticmethod
    def is_admin(user_roles: list) -> bool:
        """Check if user is an admin"""
        return 'Admin' in user_roles
    
    @staticmethod
    def is_customer(user_roles: list) -> bool:
        """Check if user is a customer"""
        return 'Customer' in user_roles
    
    @staticmethod
    def is_seller(user_roles: list) -> bool:
        """Check if user is a seller"""
        return 'Seller' in user_roles
    
    @staticmethod
    def is_support(user_roles: list) -> bool:
        """Check if user is a support representative"""
        return 'Support Representative' in user_roles
    
    @staticmethod
    def is_delivery_partner(user_roles: list) -> bool:
        """Check if user is a delivery partner"""
        return 'Delivery Partner' in user_roles
