"""
Authentication Service
Handles user login, logout, token management
"""

from typing import Optional, Dict, Tuple
from datetime import datetime
import logging
from backend.database import db
from backend.utils.security import SecurityUtils
from backend.config import Config

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service"""
    
    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Authenticate user and generate session token
        
        Args:
            username: Username or email
            password: Plain text password
            
        Returns:
            Tuple of (success, user_data, token) or (False, None, error_message)
        """
        try:
            # Find user by username or email
            query = """
                SELECT u.user_id, u.username, u.email, u.password_hash,
                       u.first_name, u.last_name, u.is_active
                FROM users u
                WHERE (u.username = %s OR u.email = %s) AND u.is_active = TRUE
            """
            user = db.execute_query(query, (username, username), fetch_one=True)
            
            if not user:
                logger.warning(f"Login attempt for non-existent user: {username}")
                return False, None, "Invalid username or password"
            
            # Verify password
            if not SecurityUtils.verify_password(password, user['password_hash']):
                logger.warning(f"Failed login attempt for user: {username}")
                return False, None, "Invalid username or password"
            
            # Get user roles
            roles_query = """
                SELECT r.role_name
                FROM user_roles ur
                JOIN roles r ON ur.role_id = r.role_id
                WHERE ur.user_id = %s
            """
            roles_result = db.execute_query(roles_query, (user['user_id'],))
            roles = [r['role_name'] for r in roles_result] if roles_result else []
            
            if not roles:
                logger.warning(f"User {username} has no roles assigned")
                return False, None, "User has no roles assigned. Contact administrator."
            
            # Generate JWT token
            token = SecurityUtils.generate_token(
                user['user_id'],
                user['username'],
                roles
            )
            
            # Create session record
            session_query = """
                INSERT INTO sessions (user_id, token, expires_at, is_active)
                VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL %s HOUR), TRUE)
            """
            db.execute_update(session_query, (
                user['user_id'],
                token,
                Config.JWT_EXPIRATION_HOURS
            ))
            
            # Update last login
            update_login_query = "UPDATE users SET last_login = NOW() WHERE user_id = %s"
            db.execute_update(update_login_query, (user['user_id'],))
            
            # Log successful login
            AuthService._log_audit(user['user_id'], 'LOGIN', 'USER', user['user_id'])
            
            user_data = {
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'roles': roles
            }
            
            logger.info(f"Successful login for user: {username}")
            return True, user_data, token
            
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False, None, "An error occurred during login"
    
    @staticmethod
    def logout(token: str) -> bool:
        """
        Logout user by invalidating session
        
        Args:
            token: Session token
            
        Returns:
            True if successful
        """
        try:
            # Verify token first
            payload = SecurityUtils.verify_token(token)
            if not payload:
                return False
            
            # Deactivate session
            query = "UPDATE sessions SET is_active = FALSE WHERE token = %s"
            db.execute_update(query, (token,))
            
            # Log logout
            AuthService._log_audit(payload['user_id'], 'LOGOUT', 'USER', payload['user_id'])
            
            logger.info(f"User {payload['username']} logged out")
            return True
            
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return False
    
    @staticmethod
    def validate_session(token: str) -> Optional[Dict]:
        """
        Validate session token and return user data
        
        Args:
            token: Session token
            
        Returns:
            User data dict or None if invalid
        """
        try:
            # Verify JWT token
            payload = SecurityUtils.verify_token(token)
            if not payload:
                return None
            
            # Check if session is still active in database
            query = """
                SELECT s.user_id, s.expires_at, s.is_active,
                       u.username, u.email, u.first_name, u.last_name
                FROM sessions s
                JOIN users u ON s.user_id = u.user_id
                WHERE s.token = %s AND s.is_active = TRUE AND s.expires_at > NOW()
            """
            session = db.execute_query(query, (token,), fetch_one=True)
            
            if not session:
                return None
            
            # Get current roles (in case they changed)
            roles_query = """
                SELECT r.role_name
                FROM user_roles ur
                JOIN roles r ON ur.role_id = r.role_id
                WHERE ur.user_id = %s
            """
            roles_result = db.execute_query(roles_query, (session['user_id'],))
            roles = [r['role_name'] for r in roles_result] if roles_result else []
            
            return {
                'user_id': session['user_id'],
                'username': session['username'],
                'email': session['email'],
                'first_name': session['first_name'],
                'last_name': session['last_name'],
                'roles': roles
            }
            
        except Exception as e:
            logger.error(f"Error validating session: {e}")
            return None
    
    @staticmethod
    def register_user(username: str, email: str, password: str, first_name: str,
                     last_name: str, phone: str = None, role_name: str = 'Customer') -> Tuple[bool, Optional[str]]:
        """
        Register a new user
        
        Args:
            username: Desired username
            email: Email address
            password: Plain text password
            first_name: First name
            last_name: Last name
            phone: Phone number (optional)
            role_name: Role to assign (default: Customer)
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Validate inputs
            is_valid, error_msg = SecurityUtils.validate_username(username)
            if not is_valid:
                return False, error_msg
            
            if not SecurityUtils.validate_email(email):
                return False, "Invalid email format"
            
            is_valid, error_msg = SecurityUtils.validate_password_strength(password)
            if not is_valid:
                return False, error_msg
            
            if phone and not SecurityUtils.validate_phone(phone):
                return False, "Invalid phone number format"
            
            # Check if username/email already exists
            check_query = """
                SELECT user_id FROM users 
                WHERE username = %s OR email = %s
            """
            existing = db.execute_query(check_query, (username, email), fetch_one=True)
            if existing:
                return False, "Username or email already exists"
            
            # Hash password
            password_hash = SecurityUtils.hash_password(password)
            
            # Create user
            insert_query = """
                INSERT INTO users (username, email, password_hash, first_name, last_name, phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            user_id = db.execute_update(insert_query, (
                username, email, password_hash, first_name, last_name, phone
            ))
            
            # Assign role
            role_query = "SELECT role_id FROM roles WHERE role_name = %s"
            role = db.execute_query(role_query, (role_name,), fetch_one=True)
            
            if role:
                assign_role_query = """
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (%s, %s)
                """
                db.execute_update(assign_role_query, (user_id, role['role_id']))
            
            # If customer, initialize loyalty
            if role_name == 'Customer':
                bronze_tier_query = "SELECT tier_id FROM loyalty_tiers WHERE tier_name = 'Bronze'"
                bronze_tier = db.execute_query(bronze_tier_query, fetch_one=True)
                
                if bronze_tier:
                    loyalty_query = """
                        INSERT INTO customer_loyalty (customer_id, current_points, lifetime_points, tier_id)
                        VALUES (%s, 0, 0, %s)
                    """
                    db.execute_update(loyalty_query, (user_id, bronze_tier['tier_id']))
            
            logger.info(f"New user registered: {username}")
            return True, None
            
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return False, "An error occurred during registration"
    
    @staticmethod
    def _log_audit(user_id: int, action: str, resource_type: str, resource_id: int):
        """Log audit trail"""
        try:
            query = """
                INSERT INTO audit_log (user_id, action, resource_type, resource_id)
                VALUES (%s, %s, %s, %s)
            """
            db.execute_update(query, (user_id, action, resource_type, resource_id))
        except Exception as e:
            logger.error(f"Error logging audit: {e}")
