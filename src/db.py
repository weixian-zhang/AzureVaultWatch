
from azure.data.tables import TableServiceClient, UpdateMode
from azure.identity import DefaultAzureCredential
from config import AppConfig
from model import ExpiringObject, TrackedExpiringObject
from util import DateUtil, LogicUtil
import json
from datetime import datetime

# Table Data Gateway architectural pattern
# singleton class
class VaultObjectTableGateway:

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
    

    def is_object_exists(self, vault_name, obj_type, obj_name) -> tuple[bool, TrackedExpiringObject]:

        try:
            rowKey = LogicUtil.create_db_row_key(obj_type, obj_name)

            existing_entity = self.tc.get_entity(partition_key=vault_name, row_key=rowKey)
   
            if not existing_entity:
                return False, None
            
            name = existing_entity['Name']
            type = existing_entity['Type']
            versions = json.loads(existing_entity['Versions'])
            
            teObj = TrackedExpiringObject(type, name)

            # converts from epoch timestamp
            for k, v in versions.items():
                teObj.versions[k] = datetime.fromtimestamp(v)
            
            return True, teObj
        
        except Exception as e:
            if hasattr(e, 'reason') and e.reason == 'Not Found':
                return False, None
            else:
                raise



    def insert_new_vault_object(self, vault_name, eo: ExpiringObject):

        version_last_notified_date = {}

        for v in eo.versions:
            version_last_notified_date[v.version] = DateUtil.now().timestamp()
        
        row_key = LogicUtil.create_db_row_key(eo.type, eo.name)
        entity = {
            u'PartitionKey': vault_name,
            u'RowKey': row_key,
            u'Name': eo.name,
            u'Type': eo.type,
            u'Versions': json.dumps(version_last_notified_date)
        }

        self.tc.upsert_entity(entity, mode=UpdateMode.REPLACE)

    
    def update_existing_vault_object(self, vault_name, teo: TrackedExpiringObject):

        row_key = LogicUtil.create_db_row_key(teo.type, teo.name)

        for k in teo.versions.keys():
            teo.versions[k] = teo.versions[k].timestamp()

        entity = {
            u'PartitionKey': vault_name,
            u'RowKey': row_key,
            u'Name': teo.name,
            u'Type': teo.type,
            u'Versions': json.dumps(teo.versions)
        }

        self.tc.upsert_entity(entity, mode=UpdateMode.REPLACE)


    