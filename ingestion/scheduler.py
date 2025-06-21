from apscheduler.schedulers.background import BackgroundScheduler
from otx_ingest import fetch_otx_data

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_otx_data, 'interval', minutes=10)
    scheduler.start()