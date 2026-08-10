
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.screener_routes import router as screener_router
from routes.stocks import router as stocks_router
from routes.portfolio_routes import router as portfolio_router
from routes.alert_routes import router as alerts_router
from sqlalchemy import text
from database import SessionLocal
from redis_client import check_redis_connection


app = FastAPI(

    title="AI Stock Screener",

    version="1.0.0"

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(screener_router)
app.include_router(stocks_router)
app.include_router(portfolio_router)
app.include_router(alerts_router)

@app.get("/")
def root():

    return {
        "message": "Stock Screener API is running",
        "status": "healthy"
    }
def home():

    return {

        "message": "AI Stock Screener API",

        "version": "1.0.0",

        "docs": "/docs"

    }


@app.get("/health")
def health():

    database_status = False

    db = SessionLocal()

    try:

        db.execute(text("SELECT 1"))

        database_status = True

    except Exception:

        database_status = False

    finally:

        db.close()

    redis_status = check_redis_connection()

    return {
        "status": (
            "healthy"
            if database_status and redis_status
            else "degraded"
        ),
        "database": database_status,
        "redis": redis_status
    }
