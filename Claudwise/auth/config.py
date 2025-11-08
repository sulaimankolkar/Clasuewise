"""
Authentication configuration settings
"""

# Security Settings
SESSION_TIMEOUT = 3600  # 1 hour in seconds
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutes in seconds

# Password Requirements
MIN_PASSWORD_LENGTH = 8
REQUIRE_UPPERCASE = True
REQUIRE_LOWERCASE = True
REQUIRE_NUMBERS = True
REQUIRE_SPECIAL_CHARS = True

# File Paths
USERS_FILE = "auth/users.json"
LOGS_FILE = "auth/auth_logs.json"

# Security Headers (for future web deployment)
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'"
}

# Rate Limiting
RATE_LIMIT_REQUESTS = 100  # requests per window
RATE_LIMIT_WINDOW = 3600   # 1 hour window

# Audit Logging
ENABLE_AUDIT_LOGGING = True
LOG_FAILED_ATTEMPTS = True
LOG_SUCCESSFUL_LOGINS = True
LOG_PASSWORD_CHANGES = True
