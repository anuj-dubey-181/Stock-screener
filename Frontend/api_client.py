import requests
from config import API_BASE_URL


def _headers(token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def register_user(email, password):
    return requests.post(
        f"{API_BASE_URL}/auth/register",
        json={"email": email, "password": password},
        headers=_headers()
    )


def login_user(email, password):
    return requests.post(
        f"{API_BASE_URL}/auth/login",
        json={"email": email, "password": password},
        headers=_headers()
    )


def run_screener(query, token=None):
    return requests.post(
        f"{API_BASE_URL}/screener/nlp",
        json={"query": query},
        headers=_headers(token)
    )


def get_company_details(symbol, token=None):
    return requests.get(
        f"{API_BASE_URL}/company/{symbol}",
        headers=_headers(token)
    )

def show_company_details(symbol, token=None):
    return requests.get(
        f"{API_BASE_URL}/company/{symbol}/history",
        headers=_headers(token)
    )


def get_portfolio(token):
    return requests.get(
        f"{API_BASE_URL}/portfolio",
        headers=_headers(token)
    )


def add_portfolio(token,payload):
    return requests.post(
        f"{API_BASE_URL}/portfolio",
        json=payload,
        headers=_headers(token)
    )


def update_portfolio(token, portfolio_id, payload):
    return requests.put(
        f"{API_BASE_URL}/portfolio/{portfolio_id}",
        json=payload,
        headers=_headers(token)
    )


def delete_portfolio(token, portfolio_id):
    return requests.delete(
        f"{API_BASE_URL}/portfolio/{portfolio_id}",
        headers=_headers(token)
    )


def get_alerts(token):
    return requests.get(
        f"{API_BASE_URL}/alerts",
        headers=_headers(token)
    )


def create_alert(token, payload):
    return requests.post(
        f"{API_BASE_URL}/alerts",
        json=payload ,
        headers=_headers(token)
    )


def delete_alert(token, alert_id):
    return requests.delete(
        f"{API_BASE_URL}/alerts/{alert_id}",
        headers=_headers(token)
    )