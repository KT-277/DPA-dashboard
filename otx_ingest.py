import requests
import json
from datetime import datetime
from database import SessionLocal
from models import ThreatIndicator
from pymongo import MongoClient

# OTX API Setup
API_KEY = '7f4aa8c51b6b7e017fbfeb3d136dd7b9205b076e38e355e325dcde2b551148f5'
headers = {'X-OTX-API-KEY': API_KEY}
url = 'https://otx.alienvault.com/api/v1/indicators/export'

# MongoDB Setup
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client.threat_intel
mongo_collection = mongo_db.raw_indicators

def fetch_otx_data():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.text.splitlines()
        session = SessionLocal()
        saved_count = 0

        for line in data:
            if line.strip():
                try:
                    # Convert line to JSON safely
                    item = json.loads(line)

                    # Save raw line in MongoDB
                    mongo_collection.insert_one(item)

                    # Save structured fields to PostgreSQL
                    ip = item.get("indicator")
                    threat_type = item.get("type")
                    timestamp = datetime.now()

                    if ip and threat_type:
                        indicator = ThreatIndicator(
                            ip=ip,
                            threat_type=threat_type,
                            source="OTX",
                            timestamp=timestamp
                        )
                        session.add(indicator)
                        saved_count += 1
                except Exception as e:
                    print("Error:", e)

        session.commit()
        session.close()
        print(f"{saved_count} indicators saved to PostgreSQL.")
    else:
        print("Failed to fetch data. Status Code:", response.status_code)

# Run manually
if __name__ == "__main__":
    fetch_otx_data()
