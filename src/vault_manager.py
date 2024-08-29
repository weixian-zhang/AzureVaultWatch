from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.certificates import CertificateClient, CertificatePolicy
from azure.keyvault.secrets import SecretClient
from config import AppConfig
from model import ExpiringItem, ExpiringVersion
from datetime import  datetime, timedelta
from pytz import timezone

class VaultManager:

    def __init__(self, vault_url, appconfig: AppConfig) -> None:
        self.appconfig = appconfig
        dcred = DefaultAzureCredential()
        self.key_client = KeyClient(vault_url, dcred)
        self.cert_client = CertificateClient(vault_url, dcred)
        self.secret_client = SecretClient(vault_url, dcred)


    def list_expiring_secrets(self):
        
        expiring_items = []

        for secret in self.secret_client.list_properties_of_secrets():

            # ignore disabled and secret that is private key belonging to Certificate
            if not secret.enabled or secret.content_type == 'application/x-pkcs12':
                continue

            ei = ExpiringItem(secret.id, secret.name)

            for version in self.secret_client.list_properties_of_secret_versions(secret.name):

                if not version.enabled:
                    continue

                if self.is_expiring(version.expires_on):
                    ev = ExpiringVersion(version.version, version.expires_on, version.created_on)
                    ei.versions.append(ev)

            if ei.versions:
                ei.set_latest_version()
                expiring_items.append(ei)

        
        return expiring_items
    

    def list_expiring_certs(self):
        
        expiring_items = []

        for cert in self.cert_client.list_properties_of_certificates():

            if not cert.enabled:
                continue

            ei = ExpiringItem(cert.id, cert.name)

            for version in self.cert_client.list_properties_of_certificate_versions(cert.name):

                if not version.enabled:
                    continue

                if self.is_expiring(version.expires_on):
                    ev = ExpiringVersion(version.version, version.expires_on, version.created_on)
                    ei.versions.append(ev)

            if ei.versions:
                ei.set_latest_version()
                expiring_items.append(ei)
        
        return expiring_items
    
    
    def list_expiring_keys(self):
        
        expiring_items = []

        for key in self.key_client.list_properties_of_keys():

            if not key.enabled:
                continue

            ei = ExpiringItem(key.id, key.name)

            for version in self.key_client.list_properties_of_key_versions(key.name):

                if not version.enabled:
                    continue

                if self.is_expiring(version.expires_on):    
                    ev = ExpiringVersion(version.version, version.expires_on, version.created_on)
                    ei.versions.append(ev)

            if ei.versions:
                ei.set_latest_version()
                expiring_items.append(ei)
        
        return expiring_items
    

    def is_expiring(self, expires_on: datetime) -> bool:
        
        if not expires_on: # Secret may not have expiry date set
            return False

        expiring_on = expires_on - timedelta(days= self.appconfig.num_of_days_notify_before_expiry)

        if datetime.today().astimezone(timezone('Asia/Kuala_lumpur')) >= expiring_on.astimezone(timezone('Asia/Kuala_lumpur')):
                return True
        
        return False