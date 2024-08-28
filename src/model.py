from datetime import datetime, timedelta
from util import Util

class ExpiringVersion:
    
    def __init__(self, version: str, expires_on: datetime) -> None:
        self.version = version
        self.expires_on = Util.as_date_str(expires_on)
        self.days_to_expiry = Util.days_to_expiry(expires_on)

class ExpiringItem:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.versions = []
        
class KeyVault:

    def __init__(self) -> None:
        self.name = ''
        self.url = ''
        self.subscription_id = ''
        self.resource_group = ''
        self.expiring_secrets : list[ExpiringItem] = []
        self.expiring_certs : list[ExpiringItem] = []
        self.expiring_keys : list[ExpiringItem] = []

class ScanContext:

    def __init__(self, num_of_days_notify_before_expiry: int) -> None:
        self.scan_date = Util.now_str()
        self.num_of_days_notify_before_expiry = num_of_days_notify_before_expiry
        self.date_to_notify = Util.as_date_str(datetime.now() - timedelta(self.num_of_days_notify_before_expiry))
        self.vaults = []