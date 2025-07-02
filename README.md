# Stock Market Analytics

A stock market ETL pipeline with API endpoints and interactive dashboards.

## Table of Contents
- [🔧 Tech Stack](#-tech-stack)
- [📂 Project Structure](#-project-structure)
- [⚙️ How to Use](#️-how-to-use)
- [🧪 Automation](#-automation)

## 🔧 Tech Stack
Python, Jupyter Notebook

PostgreSQL – storing structured stock price data

MongoDB – storing semi-structured company profiles

Elasticsearch + Kibana – indexing data and visualizing trends

FastAPI – exposing stock data via a REST API

Streamlit – (optional) interactive dashboard for rapid UI

Windows Task Scheduler – automating daily ETL execution

## 📂 Project Structure
```bash
├── api/                  # FastAPI app
├── automation/           # ETL scheduler
├── dashboards/           # Streamlit and Kibana simulations
├── data/                 # Raw and processed data
├── etl/                  # Indexing + pipeline scripts
├── notebooks/            # Jupyter exploration
├── requirements.txt
```

## ⚙️ How to Use
Clone the repo and install requirements:

```bash
git clone https://github.com/monicahnjiiri/Stock_Market_Analyitics.git
pip install -r requirements.txt
```

Load or generate your `full_stock_history.json`.

Run:
- `automated_etl_pipeline.py` to process data
- `Elasticsearch.py` to index data
- `fastapi_stock_api.py` to expose an API
- `streamlit_app.py` for interactive dashboard
- Kibana dashboard visuals are simulated in:

        dashboards/kibana_simulation.html
        
        dashboards/kibana_simulation.py

## 🧪 Automation
ETL is scheduled via Windows Task Scheduler for daily runs.
Other options like cron jobs, Airflow, or cloud tools can also be used.
