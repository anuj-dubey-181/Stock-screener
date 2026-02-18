import yfinance as yf
import json

# Choose stock symbol
symbols = ["INFY.NS", "TCS.NS", "WIPRO.NS"]

for symbol in symbols:
    ticker = yf.Ticker(symbol)
    # repeat logic


    # 1. Fetch Company Info
    company_info = {
        "symbol": symbol,
        "company_name": ticker.info.get("longName"),
        "sector": ticker.info.get("sector"),
        "industry": ticker.info.get("industry"),
        "market_cap": ticker.info.get("marketCap"),
        "country": ticker.info.get("country"),
    }


    # 2. Fetch Fundamental Metrics
    fundamentals = {
        "pe_ratio": ticker.info.get("trailingPE"),
        "forward_pe": ticker.info.get("forwardPE"),
        "peg_ratio": ticker.info.get("pegRatio"),
        "price_to_book": ticker.info.get("priceToBook"),
        "profit_margin": ticker.info.get("profitMargins"),
        "revenue_growth": ticker.info.get("revenueGrowth"),
    }


    # 3. Fetch Historical Data (last 1 year)
    historical = ticker.history(period="1y")

    historical_data = historical.reset_index().to_dict(orient="records")


    # Combine all data
    stock_data = {
        "company_info": company_info,
        "fundamentals": fundamentals,
        "historical_data": historical_data,
    }


    # Save to JSON file
    filename = f"data/{symbol.replace('.', '_')}_data.json"

    with open(filename, "w") as f:
        json.dump(stock_data, f, indent=4, default=str)


    print(f"Data saved to {filename}")
