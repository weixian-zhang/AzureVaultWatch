from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn
from config import AppConfig
from expiry_scanner import ExpiryScanner
from watch_manager import WatchManager
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

app = FastAPI()
scheduler = BackgroundScheduler()
appconfig = AppConfig()

# init open telemetry tracer exporting traces to App Insights
app_insights_exporter = AzureMonitorTraceExporter(
    connection_string=appconfig.appinsights_connection_string
)
provider = TracerProvider()
processor = BatchSpanProcessor(app_insights_exporter)
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)

wm = WatchManager(appconfig, tracer)


@scheduler.scheduled_job('interval', seconds=900)
def background_scan_and_notify():
    with tracer.start_as_current_span('background_scan_and_notify') as cs:
        cs.add_event('start main.background_scan_and_notify')
        
        wm.scan_expiring_items_and_notify()
        
        cs.add_event('finish main.background_scan_and_notify')


@app.get("/api/ready/v1", status_code=200)
async def is_ready():
    return 'ready'

@app.get("/api/objects/expire/v1", status_code=200)
async def get_expired_items():
    with tracer.start_as_current_span('fastapi.get_expired_items'):
        sc = wm.scan_expiring_items()
        return sc

    
scheduler.start()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)