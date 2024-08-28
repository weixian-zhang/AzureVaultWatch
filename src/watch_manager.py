
from expiry_scanner import ExpiryScanner
from app_config import AppConfig
from model import KeyVault, ScanContext

class WatchManager:

    def __init__(self, appconfig: AppConfig) -> None:
        self.expiry_scanner = ExpiryScanner(appconfig)


    def notify(self):

        vaults = self.expiry_scanner.scan()

    
    def scan_expiring_items(self) -> ScanContext:
        sc = self.expiry_scanner.scan()
        return sc