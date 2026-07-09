# AI-Powered Stock Screener and Advisory Platform

## Overview

The AI-Powered Stock Screener and Advisory Platform is a full-stack application that allows users to screen and analyze stocks using natural language queries. The system converts user queries into structured database queries using an AI-based parser and DSL (Domain Specific Language) compiler, executes them on financial data, and returns filtered stock results.

The platform also includes portfolio tracking, watchlist management, alerts, search history, and interactive financial dashboards.

---

## Key Features

### AI Stock Screener

* Natural language query interface
* Query converted to **DSL → SQL**
* Financial filters: P/E, Market Cap, Revenue, EBITDA, Profit Margin, Price Growth
* Sector-based filtering
* Time-based filters: Last year, Last 6 months, Last 4 quarters
* Sorting and pagination
* Query execution time logging

### Portfolio Management

* Add, remove, increase, decrease stocks
* Track investment value, current value, profit/loss
* Portfolio allocation chart
* Portfolio growth visualization
* Return percentage calculation

### Watchlist

* Add and remove stocks
* Track selected companies

### Search History

* Stores user queries
* Displays recent searches
* Updates timestamp when the same query is searched again

### Alerts

* Create alerts based on stock conditions
* Store and manage alert rules

### Market Dashboard

* Browse all companies
* View financial metrics
* Add to portfolio or watchlist

### Logging & Performance Monitoring

* Logs user query, DSL, SQL query, and execution time
* Used for debugging and optimization

---

## System Architecture

```
    User Query (Natural Language)
            ↓
    LLM Parser → DSL
            ↓
    SQL Compiler
            ↓
    SQLite Database
            ↓
    FastAPI Backend
            ↓
    Streamlit Frontend Dashboard
```

---

## Database Tables

| Table          | Description    |
| -------------- | -------------- |
| symbols        | Company info   |
| fundamentals   | Financial data |
| price_growth   | Growth data    |
| users          | User accounts  |
| portfolio      | User holdings  |
| watchlist      | Saved stocks   |
| alerts         | Alert rules    |
| search_history | User queries   |

---

## Tech Stack

* **Frontend:** Streamlit, Plotly
* **Backend:** FastAPI, Python, SQLite
* **AI:** Gemini API, Rule-based fallback parser
* **Data:** Yahoo Finance API (yfinance)

---

## How to Run

### Install dependencies

```
pip install -r requirements.txt
```

### Create database

```
python backend/database/create_db.py
```

### Run backend

```
uvicorn backend.main:app --reload
```

### Run frontend

```
streamlit run frontend/app.py
```

---

## Example Queries

* Show companies with PE ratio less than 25
* Find companies with profit margin greater than 15
* Show IT sector companies with high revenue
* Find companies with price growth greater than 10% last year
* Show top 5 companies by market cap
* Find undervalued companies with strong fundamentals
