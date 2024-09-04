from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.certificates import CertificateClient, CertificatePolicy
from azure.keyvault.secrets import SecretClient
from config import AppConfig
from model import ExpiringObject, ExpiringVersion
from util import LogicUtil
from pytz import timezone
from opentelemetry.trace import Tracer

class VaultManager:

    def __init__(self, vault_name, vault_url, appconfig: AppConfig, otel_tracer: Tracer) -> None:
        self.vault_name = vault_name
        self.otel_tracer = otel_tracer
        self.appconfig = appconfig
        dcred = DefaultAzureCredential()
        self.key_client = KeyClient(vault_url, dcred)
        self.cert_client = CertificateClient(vault_url, dcred)
        self.secret_client = SecretClient(vault_url, dcred)


    def list_expiring_secrets(self):

        with self.otel_tracer.start_as_current_span(f'VaultManager.list_expiring_secrets.{self.vault_name}') as cs:

            #cs.add_event(f'VaultManager.list_expiring_secrets.{self.vault_name}')
        
            expiring_items = []

            for secret in self.secret_client.list_properties_of_secrets():

                # ignore disabled and secret that is private key belonging to Certificate
                if not secret.enabled or secret.content_type == 'application/x-pkcs12':
                    continue

                ei = ExpiringObject(secret.name, 'secret')

                for version in self.secret_client.list_properties_of_secret_versions(secret.name):

                    if not version.enabled:
                        continue

                    if LogicUtil.is_expiring(version.expires_on, self.appconfig.num_of_days_notify_before_expiry):
                        ev = ExpiringVersion(version.version, version.expires_on, version.created_on)
                        ei.versions.append(ev)

                if ei.versions:
                    ei.set_latest_version()
                    expiring_items.append(ei)

            
            return expiring_items
    

    def list_expiring_certs(self):
        
        with self.otel_tracer.start_as_current_span(f'VaultManager.list_expiring_certs.{self.vault_name}') as cs:

            #cs.add_event(f'VaultManager.list_expiring_certs.{self.vault_name}')

            expiring_items = []

            for cert in self.cert_client.list_properties_of_certificates():

                if not cert.enabled:
                    continue

                ei = ExpiringObject(cert.name, 'cert')

                for version in self.cert_client.list_properties_of_certificate_versions(cert.name):

                    if not version.enabled:
                        continue

                    if LogicUtil.is_expiring(version.expires_on, self.appconfig.num_of_days_notify_before_expiry):
                        ev = ExpiringVersion(version.version, version.expires_on, version.created_on)
                        ei.versions.append(ev)

                if ei.versions:
                    ei.set_latest_version()
                    expiring_items.append(ei)
            
            return expiring_items
    
    
    def list_expiring_keys(self, cert_names: set):
        
        with self.otel_tracer.start_as_current_span(f'VaultManager.list_expiring_keys.{self.vault_name}') as cs:

            #cs.add_event(f'VaultManager.list_expiring_keys.{self.vault_name}')
        
            expiring_items = []

            for key in self.key_client.list_properties_of_keys():

                if not key.enabled or key.name in cert_names:
                    continue

                ei = ExpiringObject(key.name, 'key')

                for version in self.key_client.list_properties_of_key_versions(key.name):

                    if not version.enabled:
                        continue

                    if LogicUtil.is_expiring(version.expires_on, self.appconfig.num_of_days_notify_before_expiry):    
                        ev = ExpiringVersion(version.version, version.expires_on, version.created_on)
                        ei.versions.append(ev)

                if ei.versions:
                    ei.set_latest_version()
                    expiring_items.append(ei)
            
            return expiring_items
    

    