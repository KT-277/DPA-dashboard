from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class ThreatIndicator(Base):
    __tablename__ = "threat_indicators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime)

