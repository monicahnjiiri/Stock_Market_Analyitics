import json
import matplotlib.pyplot as plt
from collections import Counter

print("🔍 Simulating Kibana Visualizations...")

# Load the data
with open("elasticsearch_profiles.json", "r") as f:
    company_profiles = json.load(f)

with open("elasticsearch_stocks.json", "r") as f:
    stock_sample = json.load(f)

# 1. Pie Chart: Sector Distribution
print("\n📊 Creating Pie Chart: Sector Distribution")
sectors = [profile['sector'] for profile in company_profiles]
sector_counts = Counter(sectors)

plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.pie(sector_counts.values(), labels=sector_counts.keys(), autopct='%1.1f%%')
plt.title('Sector Distribution')

# 2. Bar Chart: Companies by Sector
plt.subplot(1, 2, 2)
companies = [profile['symbol'] for profile in company_profiles]
plt.bar(companies, [1]*len(companies))
plt.title('Companies Overview')
plt.ylabel('Count')

plt.tight_layout()
plt.savefig('kibana_visualizations.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ Kibana Visualizations Created!")
print("📁 Chart saved as 'kibana_visualizations.png'")

# Display summary stats (simulating Kibana dashboard)
print("\n📈 Dashboard Summary:")
print(f"• Total Companies: {len(company_profiles)}")
print(f"• Technology Sector: {sum(1 for p in company_profiles if 'Technology' in p['sector'])}")
print(f"• Stock Records: {len(stock_sample)} (sample shown)")
print(f"• Date Range: {stock_sample[0]['date']} to {stock_sample[-1]['date']}")

print("\n🎯 This simulates what you would see in Kibana at http://localhost:5601")
