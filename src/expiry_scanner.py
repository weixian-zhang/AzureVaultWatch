
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
        #sub_ids = self.list_subscription_ids()
        vaults = self.list_vaults()

        for vault in vaults:
            vm = VaultManager(vault.url, self.appconfig)
            vault.expiring_certs = vm.list_expiring_certs()

            # pass in cert names to ignore keys created by certificates
            vault.expiring_keys = vm.list_expiring_keys({c.name for c in vault.expiring_certs})

            vault.expiring_secrets = vm.list_expiring_secrets()

            if vault.expiring_certs or vault.expiring_keys or vault.expiring_secrets:
                scan_context.vaults.append(vault)

        # testing only
        # import os, json, datetime
        # with open('C:\\Users\\weixzha\\Desktop\\sc.json', 'w') as f:
        #     scan_context.scan_date = scan_context.scan_date.timestamp()
        #     for vault in scan_context.vaults:
        #         for x in vault.expiring_certs:
        #             for version in x.versions:
        #                 version.created_on = version.created_on.timestamp()
        #                 version.expires_on = version.expires_on.timestamp()
        #         for x in vault.expiring_keys:
        #             for version in x.versions:
        #                 version.created_on = version.created_on.timestamp()
        #                 version.expires_on = version.expires_on.timestamp()
        #         for x in vault.expiring_secrets:
        #             for version in x.versions:
        #                 version.created_on = version.created_on.timestamp()
        #                 version.expires_on = version.expires_on.timestamp()
        #     sc_json = json.dumps(scan_context, indent=4, default=lambda o: o.__dict__)
        #     f.write(sc_json)


        return scan_context

        

    def list_vaults(self):

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



