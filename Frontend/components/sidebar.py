import streamlit as st
from utils import is_logged_in, logout


def render_sidebar():
    st.sidebar.title("Navigation")

    if is_logged_in():
        st.sidebar.success("Logged in")
        if st.session_state.get("user_email"):
            st.sidebar.caption(st.session_state.user_email)

        page = st.sidebar.radio(
            "Go to",
            ["Screener", "Portfolio", "Alerts", "Company Details"]
        )
        st.session_state.current_page = page

        if st.sidebar.button("Logout"):
            logout()
            st.rerun()
    else:
        page = st.sidebar.radio(
            "Go to",
            ["Login", "Register"]
        )
        st.session_state.current_page = page