
from azure.identity import DefaultAzureCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from config import AppConfig
from model import KeyVault, ScanContext
from vault_manager import VaultManager
from opentelemetry.trace import Tracer
import json

class ExpiryScanner:

    def __init__(self, appconfig: AppConfig, otel_tracer: Tracer) -> None:
        self.otel_tracer = otel_tracer
        self.dcred = DefaultAzureCredential()
        self.appconfig = appconfig
        self.sub_client = SubscriptionClient(self.dcred)

    
    def scan(self) -> ScanContext:

        with self.otel_tracer.start_as_current_span('ExpiryScanner.scan') as cs:

            #cs.add_event('start ExpiryScanner.scan')

            scan_context = ScanContext(self.appconfig.num_of_days_notify_before_expiry)

            vaults = self.list_vaults()

            cs.add_event('ExpiryScanner.scan.for each vault')

            for vault in vaults:

                vm = VaultManager(vault.name, vault.url, self.appconfig, self.otel_tracer)
                vault.expiring_certs = vm.list_expiring_certs()

                # pass in cert names to ignore keys created by certificates
                vault.expiring_keys = vm.list_expiring_keys({c.name for c in vault.expiring_certs})

                vault.expiring_secrets = vm.list_expiring_secrets()

                if vault.expiring_certs or vault.expiring_keys or vault.expiring_secrets:
                    scan_context.vaults.append(vault)

            cs.add_event('finish ExpiryScanner.scan')

            return scan_context

        

    def list_vaults(self):

        with self.otel_tracer.start_as_current_span('ExpiryScanner.list_vaults') as cs:

            vaults = []

            for s in self.sub_client.subscriptions.list():

                subid = s.subscription_id
                akvc = KeyVaultManagementClient(self.dcred, subid)

                for v in akvc.vaults.list_by_subscription():
                    rid = v.id.split('/')
                    subid = rid[2]
                    rg = rid[4]

                    kv = KeyVault()
                    kv.subscription_id = subid
                    kv.resource_group = rg
                    kv.name = v.name
                    kv.url = f'https://{v.name}.vault.azure.net'
                    vaults.append(kv)

            return vaults                       
    
    # def list_subscription_ids(self):
    #     subids = []
    #     for s in self.sub_client.subscriptions.list():
    #         subids.append(s.subscription_id)
        
    #     return subids



