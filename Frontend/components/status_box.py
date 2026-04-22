import streamlit as st


def show_loading(message="Loading..."):
    return st.spinner(message)


def show_success(message: str):
    st.success(message)


def show_warning(message: str):
    st.warning(message)


def show_info(message: str):
    st.info(message)