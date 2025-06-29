import requests
import json
import time
import pandas as pd
from bs4 import BeautifulSoup
import psycopg2
from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    filename='etl_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ETLPipeline:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.symbols = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]
        self.setup_connections()
    
    def setup_connections(self):
        """Setup database connections"""
        try:
            # PostgreSQL connection
            self.pg_conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            
            # MongoDB connection
            self.mongo_client = MongoClient("mongodb://localhost:27017/")
            self.mongo_db = self.mongo_client["stocks"]
            
            logging.info("Database connections established")
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            raise
    
    def extract_stock_data(self):
        """Extract stock data from API"""
        logging.info("Starting stock data extraction...")
        stock_data = {}
        
        for symbol in self.symbols:
            try:
                url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={self.api_key}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    stock_data[symbol] = data.get("historical", [])[:30]  # Last 30 days
                    logging.info(f"Extracted data for {symbol}")
                else:
                    logging.warning(f"Failed to get data for {symbol}: {response.status_code}")
                
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logging.error(f"Error extracting data for {symbol}: {e}")
        
        return stock_data
    
    def extract_company_profiles(self):
        """Extract company profiles from web scraping"""
        logging.info("Starting company profile extraction...")
        profiles = []
        
        for symbol in self.symbols:
            try:
                url = f"https://finviz.com/quote.ashx?t={symbol}"
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract basic info
                    profile = {
                        "symbol": symbol,
                        "sector": "Technology",  # Simplified for demo
                        "industry": f"{symbol} Industry",
                        "extracted_at": datetime.now().isoformat()
                    }
                    profiles.append(profile)
                    logging.info(f"Extracted profile for {symbol}")
                
                time.sleep(2)  # Be respectful to the website
            except Exception as e:
                logging.error(f"Error extracting profile for {symbol}: {e}")
                # Fallback data
                profiles.append({
                    "symbol": symbol,
                    "sector": "Technology",
                    "industry": f"{symbol} Industry",
                    "extracted_at": datetime.now().isoformat()
                })
        
        return profiles
    
    def load_to_postgresql(self, stock_data):
        """Load stock data to PostgreSQL"""
        logging.info("Loading data to PostgreSQL...")
        
        try:
            cur = self.pg_conn.cursor()
            
            # Clear existing data (for demo purposes)
            cur.execute("DELETE FROM stock_quotes WHERE date >= CURRENT_DATE - INTERVAL '30 days'")
            
            # Insert new data
            for symbol, records in stock_data.items():
                for record in records:
                    cur.execute("""
                        INSERT INTO stock_quotes (
                            symbol, date, open, high, low, close, adj_close,
                            volume, unadjusted_volume, change, change_percent,
                            vwap, label, change_over_time
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (symbol, date) DO UPDATE SET
                            open = EXCLUDED.open,
                            high = EXCLUDED.high,
                            low = EXCLUDED.low,
                            close = EXCLUDED.close,
                            adj_close = EXCLUDED.adj_close,
                            volume = EXCLUDED.volume
                    """, (
                        symbol,
                        record.get("date"),
                        record.get("open"),
                        record.get("high"),
                        record.get("low"),
                        record.get("close"),
                        record.get("adjClose"),
                        record.get("volume"),
                        record.get("unadjustedVolume"),
                        record.get("change"),
                        record.get("changePercent"),
                        record.get("vwap"),
                        record.get("label"),
                        record.get("changeOverTime")
                    ))
            
            self.pg_conn.commit()
            cur.close()
            logging.info("PostgreSQL data loaded successfully")
            
        except Exception as e:
            logging.error(f"PostgreSQL loading failed: {e}")
            self.pg_conn.rollback()
    
    def load_to_mongodb(self, profiles):
        """Load company profiles to MongoDB"""
        logging.info("Loading data to MongoDB...")
        
        try:
            collection = self.mongo_db["profiles"]
            
            # Clear existing data
            collection.delete_many({})
            
            # Insert new data
            collection.insert_many(profiles)
            logging.info("MongoDB data loaded successfully")
            
        except Exception as e:
            logging.error(f"MongoDB loading failed: {e}")
    
    def load_to_elasticsearch(self, stock_data, profiles):
        """Simulate Elasticsearch loading"""
        logging.info("Simulating Elasticsearch loading...")
        
        try:
            # Convert stock data to flat format
            flat_stocks = []
            for symbol, records in stock_data.items():
                for record in records:
                    record["symbol"] = symbol
                    flat_stocks.append(record)
            
            # Save to JSON files (simulating Elasticsearch)
            with open("elasticsearch_stocks.json", "w") as f:
                json.dump(flat_stocks, f, indent=2)
            
            with open("elasticsearch_profiles.json", "w") as f:
                json.dump(profiles, f, indent=2)
            
            logging.info("Elasticsearch simulation completed")
            
        except Exception as e:
            logging.error(f"Elasticsearch simulation failed: {e}")
    
    def run_pipeline(self):
        """Run the complete ETL pipeline"""
        start_time = datetime.now()
        logging.info(f"ETL Pipeline started at {start_time}")
        
        try:
            # Extract
            stock_data = self.extract_stock_data()
            profiles = self.extract_company_profiles()
            
            # Transform (minimal for this demo)
            logging.info("Data transformation completed")
            
            # Load
            self.load_to_postgresql(stock_data)
            self.load_to_mongodb(profiles)
            self.load_to_elasticsearch(stock_data, profiles)
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logging.info(f"ETL Pipeline completed successfully in {duration.total_seconds():.2f} seconds")
            print(f"ETL Pipeline completed at {end_time}")
            print(f"Duration: {duration.total_seconds():.2f} seconds")
            print(f"Processed {len(stock_data)} symbols")
            print(f"Loaded {sum(len(records) for records in stock_data.values())} stock records")
            print(f"Loaded {len(profiles)} company profiles")
            
        except Exception as e:
            logging.error(f"ETL Pipeline failed: {e}")
            print(f"ETL Pipeline failed: {e}")
            raise
        
        finally:
            # Cleanup connections
            try:
                self.pg_conn.close()
                self.mongo_client.close()
            except:
                pass

if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run_pipeline()
