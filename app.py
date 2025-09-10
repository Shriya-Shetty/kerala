import streamlit as st
from supabase import create_client, Client
import os

# ------------------------------
# Supabase Connection
# ------------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in .env")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------------------
# Streamlit Config
# ------------------------------
st.set_page_config(page_title="SwastyaSetu", page_icon="💊", layout="centered")

st.title("💊 SwastyaSetu")
st.subheader("Welcome — Please login or create an account")

# ------------------------------
# Tabs for Login / Create Account
# ------------------------------
tab1, tab2 = st.tabs(["🔑 Login", "🆕 Create Account"])

# ------------------------------
# Login Tab
# ------------------------------
with tab1:
    st.write("Login with your credentials")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                st.success(f"✅ Logged in as {res.user.email}")
                st.session_state["user"] = res.user.email
                st.session_state["role"] = res.user.user_metadata.get("role", "Unknown")
            else:
                st.error("❌ Invalid credentials")
        except Exception as e:
            st.error(f"Error: {e}")

# ------------------------------
# Create Account Tab
# ------------------------------
with tab2:
    st.write("Create a new account")

    new_email = st.text_input("Email", key="create_email")
    new_password = st.text_input("Password", type="password", key="create_password")
    role = st.selectbox("Role", ["Hospital", "Doctor", "Government", "Admin"], key="create_role")

    if st.button("Create Account"):
        try:
            res = supabase.auth.sign_up(
                {
                    "email": new_email,
                    "password": new_password,
                    "options": {
                        "data": {"role": role}  # store role in metadata
                    },
                }
            )
            if res.user:
                st.success(f"✅ Account created for {res.user.email} as {role}")
            else:
                st.error("❌ Could not create account")
        except Exception as e:
            st.error(f"Error: {e}")

