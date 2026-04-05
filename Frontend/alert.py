import streamlit as st
import pandas as pd
from api_client import get_alerts, create_alert, delete_alert
from utils import show_api_error
import requests
from config import API_BASE_URL



def alerts_page():
    st.title("Alerts")

    token = st.session_state.token

    st.subheader("Existing Alerts")
    response = get_alerts(token)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and data:
            df=pd.DataFrame(data)
            df.index = df.index + 1
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No alerts created yet.")
    else:
        show_api_error(response)

    st.divider()
    st.subheader("Create Alert")

    symbol = st.text_input("symbol", key="alert_symbol")
    metric = st.selectbox(
        "Metric",
        ["pe_ratio", "market_cap", "promoter_holding", "ebitda", "peg_ratio"]
    )
    operator = st.selectbox("Operator", ["<", ">", "<=", ">=", "="])
    value = st.number_input("Value", step=1)

    if st.button("Create Alert"):
        payload = {
            "symbol": symbol.upper(),
            "metric": metric,
            "operator": operator,
            "value": value
        }
        response = create_alert(token, payload)
        if response.status_code in (200, 201):
            res=response.json()
            if res.get("status") == "duplicate":
                st.warning(res.get("message","alert already exist"))
            else:
                st.success(res.get("message","Alert created successfully."))
            # st.success("Alert created successfully.")
            st.rerun()
        else:
            show_api_error(response)

    st.divider()
    st.subheader("Delete Alert")

    alert_id = st.text_input("Alert ID", key="alert_delete_id")

    if st.button("Delete Alert"):
        response = delete_alert(token, alert_id)
        if response.status_code == 200:
            st.success("Alert deleted successfully.")
            st.rerun()
        else:
            show_api_error(response)

    st.subheader("⚡ Triggered Alerts")

    alerts = requests.get(f"{API_BASE_URL}/alerts/check").json()

    for a in alerts:
        st.error(f"""
        🚨 {a['symbol']} triggered alert!
        {a['metric']} = {a['value']} (target {a['target']})
        """)