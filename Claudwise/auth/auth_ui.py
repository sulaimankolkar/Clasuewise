"""
Authentication UI components for ClauseWise
"""
import streamlit as st
import time
import base64
from auth.authenticator import SecureAuthenticator

# -------------------------------------------------------------------
#  LOGIN PAGE (Parchement + Scales Background)
# -------------------------------------------------------------------

def render_login_page():
    """Render the login page with parchment texture and scale background"""

    # Load the legal-scale background
    try:
        with open("assets/bg.png", "rb") as img_file:
            bg_base64 = base64.b64encode(img_file.read()).decode()
    except:
        bg_base64 = ""

    # Parchment background texture
    parchment_url = "https://upload.wikimedia.org/wikipedia/commons/f/fd/Parchment_1.jpg"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Crimson+Text:wght@400;500;600&display=swap');

        .stApp {{
            font-family: 'Crimson Text', serif;
            background: 
                linear-gradient(135deg, rgba(20,16,8,0.95) 0%, rgba(40,30,20,0.85) 50%, rgba(60,45,30,0.75) 100%),
                url("data:image/png;base64,{bg_base64}");
            background-size: cover;
            background-position: center right;
            background-repeat: no-repeat;
            background-attachment: fixed;
            min-height: 100vh;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(ellipse at top right, rgba(139,94,60,0.3) 0%, transparent 50%),
                linear-gradient(to right, rgba(20,16,8,0.9) 25%, rgba(40,30,20,0.6) 60%, rgba(0,0,0,0.2) 100%);
            z-index: 0;
            pointer-events: none;
        }}

        .login-wrapper {{
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            justify-content: flex-start;
            min-height: 100vh;
            padding: 2rem 0 0 2rem;
        }}

        .logo-section {{
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
            color: #F4E4BC;
            text-align: center;
            padding: 1rem 2rem;
            font-family: 'Cinzel', serif;
            font-size: 2.2rem;
            font-weight: 700;
            border-radius: 20px;
            letter-spacing: 2px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            border: 3px solid #8B5E3C;
            position: relative;
            margin-bottom: 1.5rem;
            box-shadow: 
                0 15px 35px rgba(0,0,0,0.4),
                0 8px 20px rgba(139,94,60,0.3);
            backdrop-filter: blur(10px);
        }}

        .logo-section::after {{
            content: '⚖️';
            position: absolute;
            top: 50%;
            right: 1.5rem;
            transform: translateY(-50%);
            font-size: 2rem;
            opacity: 0.7;
        }}

        .form-container {{
            background: 
                linear-gradient(145deg, rgba(255,255,255,0.95) 0%, rgba(250,245,235,0.92) 50%, rgba(245,240,230,0.90) 100%);
            border-radius: 20px;
            box-shadow: 
                0 20px 40px rgba(0,0,0,0.3),
                0 10px 25px rgba(139,94,60,0.2),
                inset 0 1px 0 rgba(255,255,255,0.6);
            border: 2px solid #8B5E3C;
            padding: 2rem;
            width: 420px;
            position: relative;
            backdrop-filter: blur(15px);
            transition: all 0.3s ease;
        }}

        .form-container:hover {{
            box-shadow: 
                0 25px 50px rgba(0,0,0,0.4),
                0 15px 30px rgba(139,94,60,0.3),
                inset 0 1px 0 rgba(255,255,255,0.7);
            transform: translateY(-2px);
        }}


        .form-title {{
            font-family: 'Cinzel', serif;
            font-size: 1.4rem;
            font-weight: 600;
            color: #2C1810;
            text-align: center;
            margin-bottom: 1.5rem;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
        }}

        .field-label {{
            font-family: 'Cinzel', serif;
            font-size: 0.95rem;
            font-weight: 600;
            color: #2C1810;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .stTextInput > div > div > input {{
            background: linear-gradient(145deg, rgba(255,255,255,0.98), rgba(250,245,235,0.95)) !important;
            border: 2px solid #8B5E3C !important;
            border-radius: 30px !important;
            padding: 0.9rem 1.4rem !important;
            color: #2C1810 !important;
            font-size: 1.05rem !important;
            font-family: 'Crimson Text', serif !important;
            box-shadow: 
                inset 0 2px 4px rgba(0,0,0,0.1),
                0 2px 8px rgba(139,94,60,0.2) !important;
            transition: all 0.3s ease !important;
        }}

        .stTextInput > div > div > input:focus {{
            border-color: #CD853F !important;
            box-shadow: 
                inset 0 2px 4px rgba(0,0,0,0.1),
                0 0 0 3px rgba(205,133,63,0.3),
                0 4px 12px rgba(139,94,60,0.3) !important;
            transform: translateY(-1px) !important;
        }}

        .stButton > button {{
            background: linear-gradient(145deg, #8B5E3C 0%, #A0522D 50%, #8B5E3C 100%) !important;
            border: none !important;
            border-radius: 30px !important;
            color: #F4E4BC !important;
            font-family: 'Cinzel', serif !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            padding: 1rem 2.5rem !important;
            width: 100% !important;
            margin-top: 2rem !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            box-shadow: 
                0 6px 12px rgba(0,0,0,0.3),
                0 3px 6px rgba(139,94,60,0.4) !important;
            transition: all 0.3s ease !important;
            position: relative !important;
            overflow: hidden !important;
        }}

        .stButton > button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }}

        .stButton > button:hover {{
            background: linear-gradient(145deg, #A0522D 0%, #CD853F 50%, #A0522D 100%) !important;
            transform: translateY(-3px) !important;
            box-shadow: 
                0 8px 16px rgba(0,0,0,0.4),
                0 4px 8px rgba(139,94,60,0.5) !important;
        }}

        .stButton > button:hover::before {{
            left: 100%;
        }}

        .login-link {{
            text-align: center;
            margin-top: 1.5rem;
            font-family: 'Crimson Text', serif;
            font-size: 1rem;
            color: #2C1810;
            padding: 1rem;
            background: rgba(255,255,255,0.3);
            border-radius: 15px;
            backdrop-filter: blur(5px);
        }}
        
        .login-link span {{
            color: #8B4513;
            font-weight: 700;
            text-decoration: none;
            cursor: pointer;
            padding: 0.3rem 0.8rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            display: inline-block;
        }}

        .login-link span:hover {{
            color: #CD853F;
            background: rgba(139,69,19,0.1);
            transform: translateY(-1px);
        }}

        .credentials-box {{
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border: 2px solid #d97706;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            text-align: center;
            box-shadow: 0 4px 12px rgba(217, 119, 6, 0.2);
        }}

        .credentials-title {{
            font-family: 'Cinzel', serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: #92400e;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }}

        .credential-item {{
            background: rgba(255,255,255,0.7);
            border-radius: 10px;
            padding: 0.8rem;
            margin: 0.5rem 0;
            font-family: 'Crimson Text', serif;
            color: #78350f;
            border: 1px solid #f59e0b;
        }}

        .credential-label {{
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .credential-value {{
            font-family: 'Courier New', monospace;
            font-size: 1rem;
            font-weight: 700;
            color: #92400e;
            background: rgba(217, 119, 6, 0.1);
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            margin-top: 0.3rem;
            display: inline-block;
        }}

        /* Responsive Design */
        @media (max-width: 1200px) {{
            .login-wrapper {{ 
                padding: 1.5rem 0 0 1.5rem; 
            }}
            .form-container {{ 
                width: 400px; 
            }}
        }}

        @media (max-width: 900px) {{
            .login-wrapper {{ 
                align-items: center;
                justify-content: center;
                padding: 1rem; 
            }}
            .form-container {{ 
                width: 90%; 
                max-width: 420px;
            }}
            .logo-section {{
                font-size: 1.8rem;
                letter-spacing: 1px;
                width: 90%;
                max-width: 420px;
            }}
        }}

        @media (max-width: 600px) {{
            .form-container {{ 
                width: 95%; 
                padding: 1.5rem 1.2rem;
            }}
            .logo-section {{
                font-size: 1.5rem;
                padding: 0.8rem 1.5rem;
                width: 95%;
            }}
            .form-title {{
                font-size: 1.2rem;
            }}
            .credentials-box {{
                padding: 1rem;
                margin: 1rem 0;
            }}
        }}
    </style>

    <div class="login-wrapper">
        <div class="logo-section">CLAUSEWISE</div>
        <div class="form-container">
    """, unsafe_allow_html=True)

    # Demo Credentials Display
    st.markdown("""
    <div class="credentials-box">
        <div class="credentials-title">
            🎯 Demo Login Credentials
        </div>
        <div class="credential-item">
            <div class="credential-label">Admin Access</div>
            <div class="credential-value">admin</div>
            <div class="credential-value">admin123</div>
        </div>
        <div style="font-size: 0.8rem; color: #78350f; margin-top: 0.5rem; font-style: italic;">
            Use these credentials to access the application
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ------------------------ Form Logic --------------------------
    if st.session_state.get('show_register', False):
        st.markdown('<h2 class="form-title">Create New Account</h2>', unsafe_allow_html=True)
        with st.form("signup_form"):
            st.markdown('<div class="field-label">Name</div>', unsafe_allow_html=True)
            name = st.text_input("", placeholder="Enter your full name", key="name_input")

            st.markdown('<div class="field-label">Email</div>', unsafe_allow_html=True)
            email = st.text_input("", placeholder="Enter your email address", key="email_input")

            st.markdown('<div class="field-label">Password</div>', unsafe_allow_html=True)
            password = st.text_input("", type="password", placeholder="Create a password", key="password_input")

            signup_submitted = st.form_submit_button("Sign Up")

        if signup_submitted:
            if name and email and password:
                authenticator = SecureAuthenticator()
                success = authenticator.create_user(email, password, "user")
                if success:
                    st.success("✅ Account created successfully! Please login.")
                    time.sleep(2)
                    st.session_state['show_register'] = False
                    st.rerun()
                else:
                    st.error("❌ Email already exists!")
            else:
                st.warning("⚠️ Please fill in all fields")

        st.markdown("""
        <div class="login-link">
            Already Registered? <span onclick="window.location.reload()">Login</span>
        </div>
        """, unsafe_allow_html=True)

    else:
        with st.form("login_form"):
            st.markdown('<div class="field-label">Email</div>', unsafe_allow_html=True)
            email = st.text_input("", placeholder="Enter your email", key="login_email")

            st.markdown('<div class="field-label">Password</div>', unsafe_allow_html=True)
            password = st.text_input("", type="password", placeholder="Enter your password", key="login_password")

            login_submitted = st.form_submit_button("Login")

        if login_submitted:
            if email and password:
                authenticator = SecureAuthenticator()
                success, message = authenticator.authenticate(email, password)
                if success:
                    authenticator.create_session(email)
                    st.success("✅ Login successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
            else:
                st.warning("⚠️ Please enter both email and password")

        st.markdown("""
        <div class="login-link">
            Don't have an account? <span onclick="window.location.reload()">Sign Up</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


# -------------------------------------------------------------------
#  REGISTER PAGE (optional fallback)
# -------------------------------------------------------------------
def render_register_page():
    st.info("Registration handled via the parchment login screen.")


# -------------------------------------------------------------------
#  USER MENU + CHANGE PASSWORD + AUTH GUARD
# -------------------------------------------------------------------
def render_user_menu():
    authenticator = SecureAuthenticator()
    current_user = authenticator.get_current_user()

    if current_user:
        st.sidebar.markdown(f"### 👤 {current_user}")
        st.sidebar.divider()
        if st.sidebar.button("🚪 Logout"):
            authenticator.logout()
            st.success("Logged out successfully.")
            time.sleep(1)
            st.rerun()


def render_change_password_modal():
    if st.session_state.get('show_change_password', False):
        st.markdown("### 🔒 Change Password")
        with st.form("change_password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input("Confirm New Password", type="password")
            submit = st.form_submit_button("Change Password")

        if submit:
            authenticator = SecureAuthenticator()
            current_user = authenticator.get_current_user()
            if new_password != confirm_new_password:
                st.error("❌ Passwords do not match.")
            else:
                success, message = authenticator.change_password(current_user, current_password, new_password)
                if success:
                    st.success("✅ Password changed successfully!")
                    time.sleep(1)
                    st.session_state['show_change_password'] = False
                    st.rerun()
                else:
                    st.error(f"❌ {message}")


def require_authentication():
    """Decorator function to require authentication"""
    authenticator = SecureAuthenticator()

    if not authenticator.validate_session():
        if st.session_state.get('show_register', False):
            render_register_page()
        else:
            render_login_page()
        return False
    return True
