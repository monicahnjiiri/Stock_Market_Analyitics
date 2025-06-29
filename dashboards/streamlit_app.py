import streamlit as st
import pandas as pd
import psycopg2
from pymongo import MongoClient
import altair as alt
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Page settings
st.set_page_config(page_title="Stock Dashboard", layout="wide")

# Header
st.title("📈 Stock Data Analytics Dashboard")
st.markdown("""
This interactive dashboard is built using **Streamlit** and showcases a complete **ETL pipeline**, including:

- 🔍 Web scraping + API extraction  
- 🗃️ PostgreSQL + MongoDB storage  
- 📊 Interactive filtering + charts

Use the filters on the left to explore stock trends and company profiles by sector.
""")

# Load data from PostgreSQL
def load_postgres_data():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    df = pd.read_sql("SELECT symbol, date, open, close, volume FROM stock_quotes", conn)
    conn.close()
    return df

# Load data from MongoDB
def load_mongo_profiles():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["stocks"]
    collection = db["profiles"]
    profiles = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(profiles)

# Load data
pg_data = load_postgres_data()
mongo_data = load_mongo_profiles()

# Sidebar filters
st.sidebar.header("📌 Filter Options")
symbols = sorted(pg_data["symbol"].unique())
selected_symbol = st.sidebar.selectbox("Select Stock Symbol", symbols)

sectors = sorted(mongo_data["sector"].unique())
selected_sector = st.sidebar.selectbox("Filter by Sector", sectors)

# Filter PostgreSQL data by symbol
filtered_pg = pg_data[pg_data["symbol"] == selected_symbol].copy()
filtered_pg["date"] = pd.to_datetime(filtered_pg["date"])

# Convert to native datetime for Streamlit slider
min_date = filtered_pg["date"].min().to_pydatetime()
max_date = filtered_pg["date"].max().to_pydatetime()

# Date range filter
date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Apply date filter
filtered_pg = filtered_pg[
    (filtered_pg["date"] >= pd.to_datetime(date_range[0])) &
    (filtered_pg["date"] <= pd.to_datetime(date_range[1]))
]

# Altair chart: Price trends
st.subheader(f"📊 Price Trends for {selected_symbol}")
price_chart = alt.Chart(filtered_pg).mark_line().encode(
    x=alt.X("date:T", title="Date"),
    y=alt.Y("close:Q", title="Closing Price"),
    color=alt.value("steelblue"),
    tooltip=["date", "open", "close"]
).properties(width=800, height=300)
st.altair_chart(price_chart, use_container_width=True)

# Altair chart: Volume trends
st.subheader(f"🔁 Daily Volume for {selected_symbol}")
volume_chart = alt.Chart(filtered_pg).mark_bar().encode(
    x=alt.X("date:T", title="Date"),
    y=alt.Y("volume:Q", title="Volume"),
    tooltip=["date", "volume"]
).properties(width=800, height=300)
st.altair_chart(volume_chart, use_container_width=True)

# Summary stats
st.markdown("### 📌 Summary Stats")
st.write(f"📅 Time Range: {date_range[0].date()} → {date_range[1].date()}")
st.write(f"🔼 Max Close: {filtered_pg['close'].max():,.2f}")
st.write(f"🔽 Min Close: {filtered_pg['close'].min():,.2f}")
st.write(f"📉 Total Volume: {filtered_pg['volume'].sum():,.0f}")

# MongoDB company profiles table
st.subheader(f"🏢 Company Profiles in {selected_sector} Sector")
filtered_profiles = mongo_data[mongo_data["sector"] == selected_sector]
st.dataframe(filtered_profiles, use_container_width=True)

# Download buttons
st.sidebar.download_button(
    "Download Current Stock Data (CSV)",
    data=filtered_pg.to_csv(index=False),
    file_name=f"{selected_symbol}_stock_data.csv",
    mime="text/csv"
)

st.sidebar.download_button(
    "Download Sector Profiles (CSV)",
    data=filtered_profiles.to_csv(index=False),
    file_name=f"{selected_sector}_profiles.csv",
    mime="text/csv"
)
