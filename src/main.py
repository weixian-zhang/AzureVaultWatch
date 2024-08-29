from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn
from config import AppConfig
from expiry_scanner import ExpiryScanner
from watch_manager import WatchManager

app = FastAPI()
scheduler = BackgroundScheduler()
appconfig = AppConfig()


# scan key vaults
#@scheduler.scheduled_job('interval', seconds=5)
def scheduled_job_1():
    print("scheduled_job_1")

@app.get("/api/ready", status_code=200)
async def is_ready():
    return 'ready'

@app.get("/api/objects/expire")
async def get_expired_items():

    # wm = WatchManager(appconfig)
    # sc = wm.scan_expiring_items()
    # return sc

    wm = WatchManager(appconfig)
    sc = wm.scan_expiring_items_and_notify()
    return sc

    


scheduler.start()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)