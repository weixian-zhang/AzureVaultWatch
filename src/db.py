
from azure.data.tables import TableServiceClient, UpdateMode
from azure.identity import DefaultAzureCredential
from config import AppConfig
from model import ExpiringVersion
from util import Util

# Table Data Gateway architectural pattern
# singleton class
class VersionTableGateway:

    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance of class already exits
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, appconfig: AppConfig) -> None:

        if self._initialized:
            return
        
        dcred = DefaultAzureCredential()
        self.appconfig = appconfig
        self.table_name = self.appconfig.storage_table_name
        self.tsc = TableServiceClient(endpoint=f"https://{appconfig.storage_account_name}.table.core.windows.net/", credential=dcred)
        self.tsc.create_table_if_not_exists(self.table_name)
        self.tc = self.tsc.get_table_client(self.table_name)

        if self._initialized:
            return
        

    def is_version_exists(self, version_id):

        version = self.tc.get_entity(version_id)
        
        if not version:
            return False, None
        
        return True, version
    

    def _add_version(self, v: ExpiringVersion):
        entity = {
            u'PartitionKey': v.id,
            u'RowKey': '',
            u'LastNotifiedOn': Util.now(),
        }

        self.tc.create_entity(entity)


    def update_last_notfied_on(self, v: ExpiringVersion):
        
        entity = {
            u'PartitionKey': v.id,
            u'RowKey': '',
            u'LastNotifiedOn': Util.now(),
        }


        self.tc.upsert_entity(entity, mode=UpdateMode.REPLACE)


    