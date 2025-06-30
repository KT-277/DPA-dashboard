import requests
import json
from datetime import datetime
from database import SessionLocal
from models import ThreatIndicator
from pymongo import MongoClient

# --------------------
# Configuration
# --------------------
OTX_API_KEY = '7f4aa8c51b6b7e017fbfeb3d136dd7b9205b076e38e355e325dcde2b551148f5'
OTX_URL = 'https://otx.alienvault.com/api/v1/indicators/export'
PREDICT_URL = 'http://localhost:8001/predict'  

# --------------------
# Headers
# --------------------
headers = {'X-OTX-API-KEY': OTX_API_KEY}

# --------------------
# MongoDB Setup
# --------------------
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client.threat_intel
mongo_collection = mongo_db.raw_indicators

# --------------------
# Anomaly Detection Call
# --------------------
def is_anomaly(ip, threat_type, timestamp):
    payload = {
        "ip": ip,
        "type": threat_type,
        "timestamp": str(timestamp)
    }
    try:
        response = requests.post(PREDICT_URL, json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            return result.get("is_anomaly", False)
    except Exception as e:
        print("Prediction error:", e)
    return False  # Default fallback

# --------------------
# Main Ingestion Function
# --------------------
def fetch_otx_data():
    print("Fetching threat data from OTX...")
    response = requests.get(OTX_URL, headers=headers)
    if response.status_code == 200:
        data = response.text.splitlines()
        session = SessionLocal()
        saved_count = 0

        for line in data:
            if line.strip():
                try:
                    item = json.loads(line)
                    mongo_collection.insert_one(item)

                    ip = item.get("indicator")
                    threat_type = item.get("type")
                    timestamp = datetime.now()

                    if ip and threat_type:
                        anomaly = is_anomaly(ip, threat_type, timestamp)

                        indicator = ThreatIndicator(
                            ip=ip,
                            threat_type=threat_type,
                            source="OTX",
                            timestamp=timestamp,
                            is_anomaly=anomaly
                        )
                        session.add(indicator)
                        saved_count += 1

                except Exception as e:
                    print("Error parsing line:", e)

        session.commit()
        session.close()
        print(f"✅ {saved_count} indicators saved to PostgreSQL.")
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")

# --------------------
# Run
# --------------------
if __name__ == "__main__":
    fetch_otx_data()
