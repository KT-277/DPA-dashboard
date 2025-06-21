from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class ThreatIndicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True)
    threat_type = Column(String)
    source = Column(String)
    timestamp = Column(DateTime)