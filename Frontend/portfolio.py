import streamlit as st
import pandas as pd
from api_client import get_portfolio, add_portfolio, update_portfolio, delete_portfolio
from utils import show_api_error


def portfolio_page():
    st.title("Portfolio")

    token = st.session_state.token

    st.subheader("Current Holdings")
    response = get_portfolio(token)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and data:
            df=pd.DataFrame(data)
            df.index = df.index + 1
            st.dataframe(df , use_container_width=True)
        else:
            st.info("Portfolio is empty.")
    else:
        show_api_error(response)

    st.divider()
    st.subheader("Add Holding")

    symbol= st.text_input("symbol")
    quantity = st.number_input("Quantity", min_value=0.0, step=1.0)
    buy_price = st.number_input("Buy Price", min_value=0.0, step=0.1)

    if st.button("Add to Portfolio"):
        payload = {
            "symbol": symbol.upper(),
            "quantity": quantity,
            "buy_price": buy_price
        }
        response = add_portfolio(token, payload)
        if response.status_code in (200, 201):
            st.success("Holding added successfully.")
            st.rerun()
        else:
            show_api_error(response)

    st.divider()
    st.subheader("Update Holding")

    portfolio_id = st.number_input("Portfolio ID", min_value=1, step=1, key="portfolio_id_update")
    symbol= st.text_input("symbol",key="update_symbol")
    update_quantity = st.number_input("New Quantity", min_value=0.0, step=1.0, key="update_quantity")
    update_buy_price = st.number_input("New Buy Price", min_value=0.0, step=0.1, key="update_buy_price")

    if st.button("Update Holding"):
        payload = {
            "symbol": symbol.upper(),
            "quantity": update_quantity,
            "buy_price": update_buy_price
        }
        response = update_portfolio(token, int(portfolio_id), payload)
        if response.status_code == 200:
            st.success("Holding updated successfully.")
            st.rerun()
        else:
            show_api_error(response)

    st.divider()
    st.subheader("Delete Holding")

    delete_id = st.number_input("Portfolio ID to delete", min_value=1, step=1, key="portfolio_id_delete")

    if st.button("Delete Holding"):
        response = delete_portfolio(token, int(delete_id))
        if response.status_code == 200:
            st.success("Holding deleted successfully.")
            st.rerun()
        else:
            show_api_error(response)
