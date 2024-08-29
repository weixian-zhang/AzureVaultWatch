
from expiry_scanner import ExpiryScanner
from app_config import AppConfig
from model import ScanContext
from jinja_template.template_renderer import TemplateRenderer
class WatchManager:

    def __init__(self, appconfig: AppConfig) -> None:
        self.expiry_scanner = ExpiryScanner(appconfig)
        self.tpl_renderer = TemplateRenderer()


    def scan_expiring_items_and_notify(self):

        sc = self.expiry_scanner.scan()
        
        html = self.tpl_renderer.render_email(sc.__dict__)
        pass

    
    def scan_expiring_items(self) -> ScanContext:
        sc = self.expiry_scanner.scan()
        return sc