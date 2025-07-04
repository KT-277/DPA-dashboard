from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class ThreatIndicator(Base):
    __tablename__ = "threat_indicators"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True)
    type = Column(String, index=True)
    timestamp = Column(DateTime)
    is_anomaly = Column(String, default="False")

