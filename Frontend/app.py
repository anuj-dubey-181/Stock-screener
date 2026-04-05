# import streamlit as st
# from config import APP_TITLE
# from utils import init_session_state
# from components.sidebar import render_sidebar
# from Frontend.login import login_page
# from Frontend.register import register_page
# from Frontend.screener import screener_page
# from Frontend.portfolio import portfolio_page
# from Frontend.alert import alerts_page
# from Frontend.company_details import company_details_page

# st.set_page_config(page_title=APP_TITLE, layout="wide")

# init_session_state()
# render_sidebar()

# st.title(APP_TITLE)

# page = st.session_state.current_page

# if page == "Login":
#     login_page()
# elif page == "Register":
#     register_page()
# elif page == "Screener":
#     screener_page()
# elif page == "Portfolio":
#     portfolio_page()
# elif page == "Alerts":
#     alerts_page()
# elif page == "Company Details":
#     company_details_page()

import streamlit as st
from login import login_page
from register import register_page
from screener import screener_page
from portfolio import portfolio_page
from alert import alerts_page
# from company_details import company_details_page


st.set_page_config(page_title="AI Stock Screener", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None

if "selected_symbol" not in st.session_state:
    st.session_state.selected_symbol = ""

if "last_screener_dsl" not in st.session_state:
    st.session_state.last_screener_dsl = None

if "last_screener_sql" not in st.session_state:
    st.session_state.last_screener_sql = None

if "last_screener_results" not in st.session_state:
    st.session_state.last_screener_results = []


def logout():
    st.session_state.token = None
    st.session_state.selected_symbol = ""
    st.session_state.last_screener_dsl = None
    st.session_state.last_screener_sql = None
    st.session_state.last_screener_results = []


st.sidebar.title("Navigation")

if not st.session_state.token:
    auth_choice = st.sidebar.radio("Go to", ["Login", "Register"])

    if auth_choice == "Login":
        login_page()
    else:
        register_page()

else:
    st.sidebar.success("Logged in")

    if "user_email" in st.session_state:
        st.sidebar.write(st.session_state.user_email)

    page = st.sidebar.radio(
        "Go to",
        ["Screener", "Portfolio", "Alerts"]
    )

    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    if page == "Screener":
        screener_page()
    elif page == "Portfolio":
        portfolio_page()
    elif page == "Alerts":
        alerts_page()
    # elif page == "Company Details":
    #     company_details_page()

