
import pytest
from unittest.mock import Mock
from unittest.mock import patch
from filterer import ObjectNotificationFilterer
from config import AppConfig
from model import ScanContext, TrackedExpiringObject, ExpiringObject, ExpiringVersion
from datetime import datetime




# scenarios to filter objects from re-sending email notification until configured re-notify date is met
# 1. object not tracked, begin tracking object
# 2. objects are tracked - no new versions are created
# 3. objects are tracked - # but a new version is created and this new version was not previously tracked.

# *re-notify date = last notify date + NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS
# 4. both object and version are tracked
    # last_notified_date does not meet re-notify date
# 5. both object and version are tracked
    # last_notified_date meet re-noitfy-date
class TestFilterer:

    def get_appconfig(self):
        appconfig = AppConfig()
        appconfig.num_of_days_notify_before_expiry = 30
        appconfig.num_of_days_to_renotify_expiring_objects = 5
        return appconfig

    @patch('db.VaultObjectTableGateway')
    #@patch('filterer.ObjectNotificationFilterer')
    @patch('db.VaultObjectTableGateway.insert_new_vault_object')
    @patch('db.VaultObjectTableGateway.update_existing_vault_object')
    def test_expiring_object_not_tracked_all_objects_will_be_returned(self, 
                                                                      mock_VaultObjectTableGateway, 
                                                                      #mock_ObjectNotificationFilterer,
                                                                      mock_insert_new_vault_object,
                                                                      mock_update_existing_vault_object) -> None:
        """
        1. object not tracked, begin tracking object
        """

        #mock_ObjectNotificationFilterer.obj_db = Mock()

        mock_VaultObjectTableGateway.is_object_exists.return_value = (False, None)

        appconfig = self.get_appconfig()

        filterer = ObjectNotificationFilterer(appconfig)
        
        #sc = ScanContext(appconfig.num_of_days_notify_before_expiry)

        # tracked_obj = TrackedExpiringObject('key', 'key-1')
        # tracked_obj.versions = {
        #     'version_sdaas222', datetime(2024,9,1),
        #     'version_sdaasdas', datetime(2024,8,1)  
        # }

        #mock_ObjectNotificationFilterer.obj_db.return_value = (True, [])

        key1 = ExpiringObject('key-1','key')
        key1.versions = [
            ExpiringVersion('dasdada', datetime(2024,11,1), datetime(2023,11,1)),
        ]

        eos = [
            key1
        ]

        filtered_objs = filterer.filter_objects('vault_a', eos)

        assert len(filtered_objs) == 1