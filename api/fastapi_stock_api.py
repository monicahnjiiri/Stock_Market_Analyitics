# fastapi_stock_api.py
from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

def get_latest_stock(symbol):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT symbol, date, open, close FROM stock_quotes
        WHERE symbol = %s
        ORDER BY "date" DESC
        LIMIT 1
    """, (symbol,))
    row = cur.fetchone()
    conn.close()

    if row:
        return {
            "symbol": row[0],
            "date": row[1],
            "open": float(row[2]),
            "close": float(row[3])
        }
    return {"error": "Symbol not found"}

@app.get("/")
def home():
    return {"message": "Welcome to the Stock Analytics API"}

@app.get("/stock/{symbol}")
def stock(symbol: str):
    return get_latest_stock(symbol.upper())
