from config import AppConfig
from model import ScanContext, ExpiringObject, TrackedExpiringObject
from db import VaultObjectTableGateway
from util import DateUtil, LogicUtil
class ObjectNotificationFilterer:

    def __init__(self, appconfig: AppConfig) -> None:
        self.appconfig = appconfig
        self.obj_db = VaultObjectTableGateway(appconfig)


    def determine_objects_to_renotify(self, sc: ScanContext) -> tuple[bool, ScanContext]:

        renotify = False
        
        for vault in sc.vaults:

            vault.expiring_certs = self.filter_objects(vault.name, vault.expiring_certs)

            vault.expiring_keys = self.filter_objects(vault.name, vault.expiring_keys)

            vault.expiring_secrets = self.filter_objects(vault.name, vault.expiring_secrets)

            if vault.expiring_certs or vault.expiring_keys or vault.expiring_secrets:
                renotify = True

        return renotify, sc


    # scenarios to filter objects from re-sending email notification until configured re-notify date is met
    # 1. object not tracked, begin tracking object
    # 2. objects are tracked - no new versions are created
    # 3. objects are tracked - # but a new version is created and this new version was not previously tracked.

    # *re-notify date = last notify date + NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS
    # 4. both object and version are tracked
        # last_notified_date does not meet re-notify date
    # 5. both object and version are tracked
        # last_notified_date meet re-noitfy-date
    def filter_objects(self, vault_name: str, expiring_objects: list[ExpiringObject]):

        for expiring_obj in expiring_objects:

            exists, tracked_obj = self.obj_db.is_object_exists(vault_name, expiring_obj.type, expiring_obj.name)

            if not exists:
                self.obj_db.insert_new_vault_object(vault_name, expiring_obj)
                continue

            self.filter_versions_in_expiring_object(vault_name, expiring_obj, tracked_obj)

        expiring_objects = [x for x in expiring_objects if x.versions]

        return expiring_objects
            
    
    def filter_versions_in_expiring_object(self, vault_name, expiring_obj: ExpiringObject, tracked_obj: TrackedExpiringObject):
            
            is_tracked_obj_dirty = False
            versions_to_notify = []

            for v in expiring_obj.versions:

                # version not exist in db
                if v.version not in tracked_obj.versions:

                    versions_to_notify.append(v) # contains version to notify user on expiry

                    tracked_obj.versions[v.version] = DateUtil.now()
                    is_tracked_obj_dirty = True
                    continue

                tracked_version_last_notify_date = tracked_obj.versions[v.version]
                
                # version exist in db and last_notify_date has past configured num of days to re-notify
                if LogicUtil.version_last_notify_date_over_config_num_of_days(
                    tracked_version_last_notify_date,
                    self.appconfig.num_of_days_to_renotify_expiring_objects
                    ):

                    versions_to_notify.append(v) # contains version to notify user on expiry

                    tracked_obj.versions[v.version] = DateUtil.now()
                    is_tracked_obj_dirty = True


            # update tracked cert versions in DB
            if is_tracked_obj_dirty:
                self.obj_db.update_existing_vault_object(vault_name, tracked_obj)


            expiring_obj.versions = versions_to_notify # will be empty if no version need to be notify or re-notify


            

