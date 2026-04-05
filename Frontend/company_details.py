# import streamlit as st
# from api_client import get_company_details
# from utils import show_api_error



# def company_details_page():
#     st.title("Company Details")

#     default_symbol = st.session_state.get("selected_symbol") or ""
#     symbol = st.text_input("Enter symbol", value=default_symbol)

#     if st.button("Fetch Details"):
#         if not symbol.strip():
#             st.warning("Please enter a symbol.")
#             return

#         response = get_company_details(symbol.strip(), st.session_state.token)

#         if response.status_code == 200:
#             data = response.json()
#             st.subheader("Company Information")
#             # st.json(data)
#             st.dataframe(data, use_container_width=True)

#         else:
#             show_api_error(response)
