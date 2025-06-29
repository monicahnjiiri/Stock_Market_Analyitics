import json

# Load stock data from JSON file
with open("full_stock_history.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert to flat list
stock_data = []
for symbol, history in data.items():
    for record in history:
        record["symbol"] = symbol
        stock_data.append(record)

# Company profiles
company_profiles = [
    {"symbol": "AAPL", "sector": "Technology", "industry": "Consumer Electronics"},
    {"symbol": "MSFT", "sector": "Technology", "industry": "Software"},
    {"symbol": "GOOG", "sector": "Technology", "industry": "Internet Content & Information"},
    {"symbol": "AMZN", "sector": "Consumer Discretionary", "industry": "Internet & Direct Marketing Retail"},
    {"symbol": "META", "sector": "Technology", "industry": "Internet Content & Information"}
]

print("Simulating Elasticsearch indexing...")
print(f"Would index {len(stock_data)} stock records to 'stocks' index")
print(f"Would index {len(company_profiles)} company profiles to 'profiles' index")

# Save to files to simulate indexing
with open("elasticsearch_stocks.json", "w") as f:
    json.dump(stock_data[:10], f, indent=2)  # Save first 10 records as sample

with open("elasticsearch_profiles.json", "w") as f:
    json.dump(company_profiles, f, indent=2)

print("Data successfully 'indexed' to Elasticsearch! (simulated)")
print("Sample data saved to elasticsearch_stocks.json and elasticsearch_profiles.json")
