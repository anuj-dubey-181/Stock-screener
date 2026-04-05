import streamlit as st
from api_client import login_user
from utils import show_api_error


def login_page():
    st.title("Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter email and password.")
            return

        response = login_user(email, password)

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data.get("access_token")
            st.session_state.user_email = email
            st.session_state.current_page = "Screener"
            st.success("Login successful.")
            st.rerun()
        else:
            show_api_error(response)