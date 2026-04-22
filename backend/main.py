from fastapi import FastAPI
from database import Base, engine

from routes import (
    auth_routes,
    company_routes,
    portfolio_routes,
    alert_routes,
    screener_routes,
)

print("creating tables")
Base.metadata.create_all(bind=engine)
print("created")

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(company_routes.router)
app.include_router(portfolio_routes.router)
app.include_router(alert_routes.router)
app.include_router(screener_routes.router)


@app.get("/")
def home():
    return {"message": "Stock Screener API Running"}
