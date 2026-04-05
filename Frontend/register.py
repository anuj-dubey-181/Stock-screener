import streamlit as st
from api_client import register_user
from utils import show_api_error


def register_page():
    st.title("Register")

    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")

    if st.button("Create Account"):
        if not email or not password or not confirm_password:
            st.warning("Please fill all fields.")
            return

        if password != confirm_password:
            st.warning("Passwords do not match.")
            return

        response = register_user(email, password)

        if response.status_code in (200, 201):
            st.success("Registration successful. Please login.")
            st.session_state.current_page = "Login"
            st.rerun()
        else:
            show_api_error(response)