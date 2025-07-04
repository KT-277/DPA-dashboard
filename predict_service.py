from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime

app = FastAPI()

# Load trained model
model = joblib.load("anomaly_model.pkl")

# Input schema
class Threat(BaseModel):
    ip: str
    type: str
    timestamp: str

@app.post("/predict")
def predict(threat: Threat):
    try:
        # Parse timestamp to extract hour
        dt = datetime.fromisoformat(threat.timestamp)
        hour = dt.hour

        # Create input DataFrame
        df = pd.DataFrame([{
            "ip": threat.ip,
            "type": threat.type,
            "hour": hour
        }])

        # Encode features using same logic as model training
        df["ip_encoded"] = df["ip"].astype("category").cat.codes
        df["type_encoded"] = df["type"].astype("category").cat.codes

        # Final feature columns (must match training)
        features = df[["ip_encoded", "type_encoded", "hour"]]

        # Predict
        prediction = model.predict(features)
        is_anomaly = bool(prediction[0] == -1)

        return {"is_anomaly": is_anomaly}

    except Exception as e:
        return {"error": str(e)}

