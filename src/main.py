from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn

app = FastAPI()

scheduler = BackgroundScheduler()

# scan key vaults
@scheduler.scheduled_job('interval', seconds=5)
def scheduled_job_1():
    print("scheduled_job_1")


@app.get("/expired")
async def read_root():
    return {"message": "Hello, World!"}


scheduler.start()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)