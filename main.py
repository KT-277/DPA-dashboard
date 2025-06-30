from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ThreatIndicator
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/threats")
def get_threats(db: Session = Depends(get_db)):
    threats = db.query(ThreatIndicator).all()
    return threats