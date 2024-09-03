from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn
from config import AppConfig
from expiry_scanner import ExpiryScanner
from watch_manager import WatchManager

app = FastAPI()
scheduler = BackgroundScheduler()
appconfig = AppConfig()
wm = WatchManager(appconfig)

#@scheduler.scheduled_job('interval', seconds=900)
def background_scan_and_notify():
    sc = wm.scan_expiring_items_and_notify()
    return sc

@app.get("/api/ready/v1", status_code=200)
async def is_ready():
    return 'ready'

@app.get("/api/objects/expire/v1", status_code=200)
async def get_expired_items():
    sc = wm.scan_expiring_items()
    return sc

    
scheduler.start()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)