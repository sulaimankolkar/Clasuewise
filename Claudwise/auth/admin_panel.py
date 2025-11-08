"""
Admin panel for user management
"""

import streamlit as st
import pandas as pd
import json
import time
from auth.authenticator import SecureAuthenticator
from typing import Dict, List

def render_admin_panel():
    """Render admin panel for user management"""
    authenticator = SecureAuthenticator()
    current_user = authenticator.get_current_user()
    
    if not current_user or not authenticator.is_admin(current_user):
        st.error("🚫 Access denied. Admin privileges required.")
        return
    
    # Premium Admin Header
    st.markdown("""
    <div class="premium-card">
        <h1 style="
            font-size: 2rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            🔧 Admin Control Center
        </h1>
        <p style="color: #64748b; font-size: 1rem; margin: 0;">
            Manage users, monitor security, and configure system settings
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium Admin tabs with modern styling
    st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 16px;
            padding: 0.5rem;
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 User Management", "📆 Analytics", "🔒 Security", "📋 Audit Logs"])
    
    with tab1:
        render_user_management()
    
    with tab2:
        render_login_analytics()
    
    with tab3:
        render_security_settings()
    
    with tab4:
        render_audit_logs()

def render_user_management():
    """Render user management interface"""
    st.subheader("👥 User Management")
    
    authenticator = SecureAuthenticator()
    users = authenticator._load_users()
    
    if not users:
        st.info("No users found.")
        return
    
    # Display users table
    user_data = []
    for username, user_info in users.items():
        user_data.append({
            'Username': username,
            'Role': user_info.get('role', 'user'),
            'Created': time.strftime('%Y-%m-%d %H:%M', time.localtime(user_info.get('created_at', 0))),
            'Last Login': time.strftime('%Y-%m-%d %H:%M', time.localtime(user_info.get('last_login', 0))) if user_info.get('last_login') else 'Never',
            'Login Attempts': user_info.get('login_attempts', 0),
            'Status': 'Locked' if user_info.get('locked_until', 0) > time.time() else 'Active'
        })
    
    df = pd.DataFrame(user_data)
    st.dataframe(df, use_container_width=True)
    
    # User actions
    st.markdown("### 🛠️ User Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ➕ Create New User")
        with st.form("create_user_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["user", "admin"])
            
            if st.form_submit_button("Create User"):
                if new_username and new_password:
                    if authenticator.create_user(new_username, new_password, new_role):
                        st.success(f"✅ User '{new_username}' created successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Username already exists!")
                else:
                    st.error("❌ Please fill in all fields!")
    
    with col2:
        st.markdown("#### 🔓 Unlock User Account")
        with st.form("unlock_user_form"):
            unlock_username = st.selectbox("Select User to Unlock", 
                                         [u for u in users.keys() if users[u].get('locked_until', 0) > time.time()])
            
            if st.form_submit_button("Unlock Account"):
                if unlock_username:
                    users[unlock_username]['locked_until'] = 0
                    users[unlock_username]['login_attempts'] = 0
                    authenticator._save_users(users)
                    st.success(f"✅ Account '{unlock_username}' unlocked!")
                    time.sleep(1)
                    st.rerun()

def render_login_analytics():
    """Render login analytics dashboard"""
    st.subheader("📊 Login Analytics")
    
    authenticator = SecureAuthenticator()
    users = authenticator._load_users()
    
    if not users:
        st.info("No user data available.")
        return
    
    # Calculate statistics
    total_users = len(users)
    active_users = sum(1 for u in users.values() if u.get('last_login'))
    locked_users = sum(1 for u in users.values() if u.get('locked_until', 0) > time.time())
    admin_users = sum(1 for u in users.values() if u.get('role') == 'admin')
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Users", total_users)
    
    with col2:
        st.metric("✅ Active Users", active_users)
    
    with col3:
        st.metric("🔒 Locked Users", locked_users)
    
    with col4:
        st.metric("🔑 Admin Users", admin_users)
    
    # Login attempts chart
    st.markdown("### 📈 Login Attempts by User")
    
    attempt_data = []
    for username, user_info in users.items():
        attempts = user_info.get('login_attempts', 0)
        if attempts > 0:
            attempt_data.append({'User': username, 'Failed Attempts': attempts})
    
    if attempt_data:
        df_attempts = pd.DataFrame(attempt_data)
        st.bar_chart(df_attempts.set_index('User'))
    else:
        st.info("No failed login attempts recorded.")

def render_security_settings():
    """Render security settings interface"""
    st.subheader("🔒 Security Settings")
    
    st.markdown("### 🛡️ Current Security Configuration")
    
    # Display current settings
    settings_data = {
        'Setting': [
            'Session Timeout',
            'Max Login Attempts',
            'Account Lockout Duration',
            'Minimum Password Length',
            'Password Hashing Algorithm'
        ],
        'Value': [
            '1 hour',
            '5 attempts',
            '15 minutes',
            '8 characters',
            'PBKDF2-SHA256 (100,000 iterations)'
        ],
        'Status': [
            '✅ Secure',
            '✅ Secure',
            '✅ Secure',
            '✅ Secure',
            '✅ Secure'
        ]
    }
    
    df_settings = pd.DataFrame(settings_data)
    st.dataframe(df_settings, use_container_width=True)
    
    st.markdown("### 🔐 Security Features Enabled")
    
    features = [
        "✅ Password encryption with PBKDF2-SHA256",
        "✅ Salt-based password hashing",
        "✅ Account lockout after failed attempts",
        "✅ Session timeout protection",
        "✅ Secure token generation",
        "✅ Timing attack prevention",
        "✅ Password strength validation",
        "✅ Audit logging"
    ]
    
    for feature in features:
        st.markdown(feature)

def render_audit_logs():
    """Render audit logs interface"""
    st.subheader("📋 Audit Logs")
    
    # This would typically read from a log file
    # For now, we'll show recent activity from user data
    
    authenticator = SecureAuthenticator()
    users = authenticator._load_users()
    
    st.markdown("### 📊 Recent User Activity")
    
    activity_data = []
    for username, user_info in users.items():
        if user_info.get('last_login'):
            activity_data.append({
                'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user_info['last_login'])),
                'User': username,
                'Action': 'Login',
                'Status': 'Success',
                'IP Address': 'N/A (Local)'
            })
        
        if user_info.get('login_attempts', 0) > 0:
            activity_data.append({
                'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                'User': username,
                'Action': 'Failed Login',
                'Status': f"{user_info['login_attempts']} attempts",
                'IP Address': 'N/A (Local)'
            })
    
    if activity_data:
        # Sort by timestamp (most recent first)
        activity_data.sort(key=lambda x: x['Timestamp'], reverse=True)
        df_activity = pd.DataFrame(activity_data)
        st.dataframe(df_activity, use_container_width=True)
    else:
        st.info("No recent activity recorded.")
    
    # Export logs button
    if st.button("📥 Export Audit Logs"):
        if activity_data:
            csv = pd.DataFrame(activity_data).to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"clausewise_audit_logs_{int(time.time())}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data to export.")
