"""
Secure authentication system for ClauseWise
"""

import streamlit as st
import hashlib
import hmac
import secrets
import time
import json
import os
from typing import Dict, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureAuthenticator:
    """Secure authentication with multiple security layers"""
    
    def __init__(self, users_file: str = "auth/users.json", session_timeout: int = 3600):
        self.users_file = users_file
        self.session_timeout = session_timeout  # 1 hour default
        self.max_login_attempts = 5
        self.lockout_duration = 900  # 15 minutes
        self._ensure_users_file()
        
    def _ensure_users_file(self):
        """Ensure users file exists with default admin user"""
        if not os.path.exists(self.users_file):
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            
            # Create default admin user
            default_users = {
                "admin": {
                    "password_hash": self._hash_password("admin123"),
                    "salt": secrets.token_hex(32),
                    "role": "admin",
                    "created_at": time.time(),
                    "login_attempts": 0,
                    "locked_until": 0,
                    "last_login": None
                }
            }
            
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=2)
            
            logger.info("Created default users file with admin user")
    
    def _hash_password(self, password: str, salt: str = None) -> str:
        """Securely hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Use PBKDF2 with SHA-256 for secure password hashing
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 100,000 iterations
        )
        
        return f"{salt}${password_hash.hex()}"
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash"""
        try:
            salt, hash_hex = stored_hash.split('$')
            password_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return hmac.compare_digest(hash_hex, password_hash.hex())
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    def _load_users(self) -> Dict:
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            return {}
    
    def _save_users(self, users: Dict):
        """Save users to file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving users: {e}")
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to failed attempts"""
        users = self._load_users()
        if username not in users:
            return False
        
        user = users[username]
        locked_until = user.get('locked_until', 0)
        
        if locked_until > time.time():
            return True
        
        # Reset lock if time has passed
        if locked_until > 0:
            user['locked_until'] = 0
            user['login_attempts'] = 0
            self._save_users(users)
        
        return False
    
    def _record_login_attempt(self, username: str, success: bool):
        """Record login attempt and handle account locking"""
        users = self._load_users()
        if username not in users:
            return
        
        user = users[username]
        
        if success:
            user['login_attempts'] = 0
            user['locked_until'] = 0
            user['last_login'] = time.time()
        else:
            user['login_attempts'] = user.get('login_attempts', 0) + 1
            
            if user['login_attempts'] >= self.max_login_attempts:
                user['locked_until'] = time.time() + self.lockout_duration
                logger.warning(f"Account {username} locked due to failed attempts")
        
        self._save_users(users)
    
    def create_user(self, username: str, password: str, role: str = "user") -> bool:
        """Create a new user"""
        users = self._load_users()
        
        if username in users:
            return False
        
        users[username] = {
            "password_hash": self._hash_password(password),
            "role": role,
            "created_at": time.time(),
            "login_attempts": 0,
            "locked_until": 0,
            "last_login": None
        }
        
        self._save_users(users)
        logger.info(f"Created user: {username}")
        return True
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """Authenticate user with security checks"""
        if not username or not password:
            return False, "Username and password are required"
        
        # Check if account is locked
        if self._is_account_locked(username):
            return False, "Account is temporarily locked due to failed login attempts"
        
        users = self._load_users()
        
        if username not in users:
            # Record failed attempt even for non-existent users to prevent enumeration
            time.sleep(0.5)  # Prevent timing attacks
            return False, "Invalid username or password"
        
        user = users[username]
        
        if self._verify_password(password, user['password_hash']):
            self._record_login_attempt(username, True)
            return True, "Login successful"
        else:
            self._record_login_attempt(username, False)
            return False, "Invalid username or password"
    
    def create_session(self, username: str) -> str:
        """Create secure session token"""
        session_data = {
            'username': username,
            'created_at': time.time(),
            'expires_at': time.time() + self.session_timeout,
            'token': secrets.token_urlsafe(32)
        }
        
        # Store in Streamlit session state
        st.session_state['auth_session'] = session_data
        st.session_state['authenticated'] = True
        st.session_state['username'] = username
        
        return session_data['token']
    
    def validate_session(self) -> bool:
        """Validate current session"""
        if 'auth_session' not in st.session_state:
            return False
        
        session = st.session_state['auth_session']
        
        # Check if session has expired
        if time.time() > session['expires_at']:
            self.logout()
            return False
        
        # Extend session if user is active
        session['expires_at'] = time.time() + self.session_timeout
        st.session_state['auth_session'] = session
        
        return True
    
    def logout(self):
        """Clear session and logout user"""
        keys_to_clear = ['auth_session', 'authenticated', 'username']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def get_current_user(self) -> Optional[str]:
        """Get current authenticated user"""
        if self.validate_session():
            return st.session_state.get('username')
        return None
    
    def get_user_role(self, username: str) -> str:
        """Get user role"""
        users = self._load_users()
        return users.get(username, {}).get('role', 'user')
    
    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        # Verify old password first
        auth_success, _ = self.authenticate(username, old_password)
        if not auth_success:
            return False, "Current password is incorrect"
        
        # Validate new password strength
        if len(new_password) < 8:
            return False, "New password must be at least 8 characters long"
        
        users = self._load_users()
        users[username]['password_hash'] = self._hash_password(new_password)
        self._save_users(users)
        
        logger.info(f"Password changed for user: {username}")
        return True, "Password changed successfully"
    
    def is_admin(self, username: str) -> bool:
        """Check if user has admin role"""
        return self.get_user_role(username) == "admin"
