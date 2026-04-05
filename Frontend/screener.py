# import streamlit as st
# from api_client import run_screener
# from utils import show_api_error
# from components.result import render_results_table


# EXAMPLE_QUERIES = [
#     "Show companies with pe less than 20",
#     "Show companies with promoter holding greater than 50",
#     "Show companies with ebitda greater than 100000 in last 3 quarters",
#     "Show companies with market cap greater than 100000 and pe less than 25",
# ]


# def screener_page():
#     st.title("AI Stock Screener")

#     st.subheader("Natural Language Query")
#     query = st.text_area(
#         "Enter your stock query",
#         placeholder="Example: Show companies with pe less than 20 and promoter holding greater than 40",
#         height=120
#     )

#     st.caption("Examples:")
#     for q in EXAMPLE_QUERIES:
#         st.write(f"- {q}")

#     if st.button("Run Screener"):
#         if not query.strip():
#             st.warning("Please enter a query.")
#             return

#         with st.spinner("Generating DSL and running query..."):
#             response = run_screener(query, st.session_state.token)

#         if response.status_code == 200:
#             data = response.json()

#             st.session_state.last_screener_results = data.get("results", [])
#             st.session_state.last_screener_dsl = data.get("dsl")
#             st.session_state.last_screener_sql = data.get("sql")

#             st.success("Query executed successfully.")
#         else:
#             show_api_error(response)
#             return

#     if st.session_state.last_screener_dsl:
#         st.subheader("Generated DSL")
#         st.json(st.session_state.last_screener_dsl)

#     if st.session_state.last_screener_sql:
#         st.subheader("Generated SQL")
#         st.code(st.session_state.last_screener_sql, language="sql")

#     st.subheader("Results")
#     render_results_table(st.session_state.last_screener_results)
import streamlit as st
from api_client import run_screener
from utils import show_api_error
from api_client import get_company_details,show_company_details
import pandas as pd



def screener_page():
    st.title("AI Stock Screener")

    query = st.text_area(
        "Enter natural language query",
        placeholder="Example: show companies with pe less than 20 and promoter holding greater than 40"
    )

    if st.button("Run Screener"):
        if not query.strip():
            st.warning("Please enter a query.")
            return

        with st.spinner("Processing query..."):
            response = run_screener(query, st.session_state.token)

        if response.status_code == 200:
            data = response.json()

            st.session_state.last_screener_dsl = data.get("dsl")
            st.session_state.last_screener_sql = data.get("sql")
            st.session_state.last_screener_values = data.get("values")
            st.session_state.last_screener_results = data.get("results", [])

            st.success("Query executed successfully")

        else:
            show_api_error(response)
            return

    if st.session_state.get("last_screener_dsl"):
        st.subheader("Generated DSL")
        st.json(st.session_state.last_screener_dsl)

    if st.session_state.get("last_screener_sql","last_screener_values"):
        st.subheader("Generated SQL")
        st.code(st.session_state.last_screener_sql, language="sql")
        st.subheader("Parameters")
        st.code(st.session_state.last_screener_values,language="numeic")

    if st.session_state.get("last_screener_results") is not None:
        st.subheader("Results")
        results = st.session_state.last_screener_results

        if len(results) == 0:
            st.info("No companies matched the query.")
        else:
            st.code(results)
            # result=[item["company_name"] for item in results["Results"]]
            # symbol=[item["symbol"] for item in results["Results"]]
            df=pd.DataFrame(results["Results"])
            df.index = df.index + 1
            st.dataframe(df, use_container_width=True)

            # symbols = [row["symbol"] for row in results if "symbol" in row]
            symbol=[item["symbol"] for item in results["Results"]]

            if symbol:
                selected_symbol = st.selectbox(
                    "Select a company for details",
                    [""] + symbol
                )

                if selected_symbol:
                    # st.session_state.selected_symbol = selected_symbol
                    if st.button("Fetch Details"):
                        response = get_company_details(selected_symbol.strip(), st.session_state.token)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.subheader("Company Information")
                            # st.json(data)

                            st.dataframe(data, use_container_width=True)
                        else:
                            show_api_error(response)

                    if st.button("Show charts"):
                        response = show_company_details(selected_symbol.strip(), st.session_state.token)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.subheader("market price")
                            # st.json(data)
                            df=pd.DataFrame(data)
                            df.index = df.index + 1
                            st.line_chart(df.set_index("date")["close_price"])
                        else:
                            show_api_error(response)
    