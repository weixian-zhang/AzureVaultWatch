
from expiry_scanner import ExpiryScanner
from config import AppConfig
from model import ScanContext
from template.template_renderer import TemplateRenderer
from smtp import SMTPSender
from db import VaultObjectTableGateway
from filterer import ObjectNotificationFilterer
from opentelemetry.trace import Tracer

class WatchManager:

    def __init__(self, appconfig: AppConfig, otel_tracer: Tracer) -> None:
        self.otel_tracer = otel_tracer
        self.expiry_scanner = ExpiryScanner(appconfig, otel_tracer)
        self.tpl_renderer = TemplateRenderer(otel_tracer)
        self.smtp_sender = SMTPSender(appconfig, otel_tracer)
        self.version_table = VaultObjectTableGateway(appconfig)
        self.obj_notification_filterer = ObjectNotificationFilterer(appconfig, otel_tracer)

    def scan_expiring_items_and_notify(self):

        with self.otel_tracer.start_as_current_span('WatchManager.scan_expiring_items_and_notify') as cs:

            #cs.add_event('start WatchManager.scan_expiring_items_and_notify')

            #cs.add_event('start expiry_scanner')
            sc = self.expiry_scanner.scan()
            #cs.add_event('finish expiry_scanner')

            #cs.add_event('start determine_objects_to_renotify')
            notify, sc = self.obj_notification_filterer.determine_objects_to_renotify(sc)
            #cs.add_event('finish determine_objects_to_renotify')

            #cs.set_attribute('should_notify', notify)

            if notify:
                #cs.add_event('start render_html')
                html = self.tpl_renderer.render_html(sc.__dict__)
                #cs.add_event('finish render_html')

                #cs.add_event('start send email')
                self.smtp_sender.send(html)
                #cs.add_event('finish send email')

            cs.add_event('finish WatchManager.scan_expiring_items_and_notify')



    def scan_expiring_items(self) -> ScanContext:
        with self.otel_tracer.start_as_current_span('WatchManager.scan_expiring_items'):
            sc = self.expiry_scanner.scan()
            return sc
            

        
        

                