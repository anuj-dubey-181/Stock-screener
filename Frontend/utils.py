import streamlit as st


def init_session_state():
    defaults = {
        "token": None,
        "current_page": "Login",
        "selected_symbol": None,
        "last_screener_results": [],
        "last_screener_dsl": None,
        "last_screener_sql": None,
        "user_email": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def is_logged_in() -> bool:
    return st.session_state.get("token") is not None


def logout():
    st.session_state.token = None
    st.session_state.user_email = None
    st.session_state.current_page = "Login"
    st.session_state.selected_symbol = None
    st.session_state.last_screener_results = []
    st.session_state.last_screener_dsl = None
    st.session_state.last_screener_sql = None


def show_api_error(response):
    try:
        data = response.json()
        if isinstance(data, dict):
            detail = data.get("detail") or data.get("message") or str(data)
            st.error(detail)
        else:
            st.error(str(data))
    except Exception:
        st.error(response.text if response.text else "Something went wrong.")