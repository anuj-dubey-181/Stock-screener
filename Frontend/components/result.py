import streamlit as st
import pandas as pd


def render_results_table(results: list):
    if not results:
        st.info("No matching companies found.")
        return

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

    possible_symbol_cols = ["symbol", "ticker", "company_symbol"]
    symbol_col = None

    for col in possible_symbol_cols:
        if col in df.columns:
            symbol_col = col
            break

    if symbol_col:
        selected_symbol = st.selectbox(
            "Open company details",
            [""] + df[symbol_col].dropna().astype(str).tolist()
        )
        if selected_symbol:
            st.session_state.selected_symbol = selected_symbol
            st.success(f"Selected: {selected_symbol}")