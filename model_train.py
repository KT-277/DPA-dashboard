import pandas as pd
from sqlalchemy import create_engine
import joblib
from datetime import datetime
from sklearn.ensemble import IsolationForest

# Connect to the database
engine = create_engine("postgresql://postgres:admin123@localhost:5432/threatdb")

# Load data
df = pd.read_sql("SELECT ip, type, timestamp FROM threat_indicators", engine)

# Basic preprocessing
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['ip_encoded'] = df['ip'].astype('category').cat.codes
df['type_encoded'] = df['type'].astype('category').cat.codes

# Train model
features = df[['ip_encoded', 'type_encoded', 'hour']]
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(features)

# Save model
joblib.dump(model, 'anomaly_model.pkl')
print("✅ Model trained and saved as anomaly_model.pkl")

