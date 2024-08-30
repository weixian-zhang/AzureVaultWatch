
from expiry_scanner import ExpiryScanner
from config import AppConfig
from model import ScanContext
from template.template_renderer import TemplateRenderer
from smtp import SMTPSender
class WatchManager:

    def __init__(self, appconfig: AppConfig) -> None:
        self.expiry_scanner = ExpiryScanner(appconfig)
        self.tpl_renderer = TemplateRenderer()
        self.smtp_sender = SMTPSender(appconfig)

    def scan_expiring_items_and_notify(self):
        sc = self.expiry_scanner.scan()
        html = self.tpl_renderer.render_html(sc.__dict__)
        self.smtp_sender.send(html)

    def scan_expiring_items(self) -> ScanContext:
        sc = self.expiry_scanner.scan()
        return sc