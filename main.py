from fastapi import FastAPI
from ingestion.scheduler import start

app = FastAPI()

@app.on_event("startup")
def startup_event():
    start()