from datetime import datetime, timedelta
from util import Util

class ExpiringVersion:
    
    def __init__(self, id: str, version: str, expires_on: datetime, created_on: datetime) -> None:
        self.id = id
        self.version = version
        self.expires_on = Util.as_friendly_date_str(expires_on)
        self.days_to_expiry = Util.days_to_expiry(expires_on)
        self.created_on = created_on
        self.created_on_display = Util.as_friendly_date_str(created_on)
        self.is_latest = False
        self.key_last_rotation_days = -1 # -1 means not a key, this field only applicables to key

# type is either key, secret, cert
class ExpiringObject:
    def __init__(self, id, name, type) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.versions = []

    def set_latest_version(self):
        if not self.versions:
            return
        
        # sort latest created date first
        self.versions = sorted(self.versions, key= lambda v: v.created_on_display, reverse=True)
        self.versions[0].is_latest = True

        if self.type == 'key':

            now = Util.now()
            
            for i in range(len(self.versions) - 1, -1, -1):
                if i == 0:
                    self.versions[i].key_last_rotation_days = (now - Util.as_sing_kl_timezone(self.versions[i].created_on)).days
                    continue

                self.versions[i].key_last_rotation_days = (Util.as_sing_kl_timezone(self.versions[i - 1].created_on) - Util.as_sing_kl_timezone(self.versions[i].created_on)).days

        

        
class KeyVault:

    def __init__(self) -> None:
        self.name = ''
        self.url = ''
        self.subscription_id = ''
        self.resource_group = ''
        self.expiring_secrets : list[ExpiringObject] = []
        self.expiring_certs : list[ExpiringObject] = []
        self.expiring_keys : list[ExpiringObject] = []

class ScanContext:

    def __init__(self, num_of_days_notify_before_expiry: int) -> None:
        self.scan_date = Util.now_str()
        self.num_of_days_notify_before_expiry = num_of_days_notify_before_expiry
        self.date_to_notify = Util.as_friendly_date_str(datetime.now() - timedelta(self.num_of_days_notify_before_expiry))
        self.vaults = []