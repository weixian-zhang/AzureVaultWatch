
from azure.identity import DefaultAzureCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from config import AppConfig
from model import KeyVault, ScanContext
from vault_manager import VaultManager

class ExpiryScanner:

    def __init__(self, appconfig: AppConfig) -> None:
        self.dcred = DefaultAzureCredential()
        self.appconfig = appconfig
        self.sub_client = SubscriptionClient(self.dcred)

    
    def scan(self) -> ScanContext:

        scan_context = ScanContext(self.appconfig.num_of_days_notify_before_expiry)
        sub_ids = self.list_subscription_ids()
        vaults = self.list_vaults(sub_ids)

        for vault in vaults:
            vm = VaultManager(vault.url, self.appconfig)
            vault.expiring_certs = vm.list_expiring_certs()
            vault.expiring_keys = vm.list_expiring_keys()
            vault.expiring_secrets = vm.list_expiring_secrets()

            if vault.expiring_certs or vault.expiring_keys or vault.expiring_secrets:
                scan_context.vaults.append(vault)

        return scan_context

        

    def list_vaults(self, subscription_ids: list[KeyVault]):

        vaults = []

        for subid in subscription_ids:
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
    
    def list_subscription_ids(self):
        subids = []
        for s in self.sub_client.subscriptions.list():
            subids.append(s.subscription_id)
        
        return subids




