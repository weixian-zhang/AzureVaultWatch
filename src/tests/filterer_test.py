
import pytest
from unittest.mock import Mock
from unittest.mock import patch
from filterer import ObjectNotificationFilterer
from config import AppConfig
from model import  TrackedExpiringObject, ExpiringObject, ExpiringVersion
from datetime import datetime
from freezegun import freeze_time



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


    def test_expiring_object_not_tracked_all_objects_will_be_returned(self):  
        """
        test case: 1. object not tracked, begin tracking object for the first time
         - Objects will not be filtered
         - unfiltered objects will have email notification sent
        """

        with patch("db.VaultObjectTableGateway.is_object_exists", return_value=(False, None)):
            with patch("db.VaultObjectTableGateway.insert_new_vault_object", return_value=None):
                with patch("db.VaultObjectTableGateway.update_existing_vault_object", return_value=None):

                    appconfig = self.get_appconfig()
                    filterer = ObjectNotificationFilterer(appconfig)

                    key1 = ExpiringObject('key-1','key')
                    key1.versions = [
                        ExpiringVersion('dasdada', datetime(2024,11,1), datetime(2023,11,1)),
                    ]

                    expiring_objs = [key1]

                    filtered_objs = filterer.filter_objects('vault_a', expiring_objs)

                    assert len(filtered_objs) == 1




    def test_expiring_object_are_tracked_and_no_new_version_is_created(self):
        """
        test case: 2. objects are tracked and no new versions are created
            - Objects will be filtered
            - Since all objects are filtered and no object will be returned, there will be no objects to send email notification.
              Hence, no notification sent
        test case: 4. last_notified_date does not meet re-notify date

            formula = 2024-9-5 (last notify date) + 2 (num_of_days_to_renotify_expiring_objects) <= 2024-09-6
            is False, filterer will filter away objects so nothing to re-notify
        """


        tracked_obj = TrackedExpiringObject('key', 'key-1')
        tracked_obj.versions['dasdada'] = datetime(2024,9,5)  # last notify date

        with patch("db.VaultObjectTableGateway.is_object_exists", return_value=(True, tracked_obj)):
            with patch("db.VaultObjectTableGateway.insert_new_vault_object", return_value=None):
                with patch("db.VaultObjectTableGateway.update_existing_vault_object", return_value=None):
                    with freeze_time('2024-09-6'): # represents datetime.now()

                        appconfig = self.get_appconfig()
                        appconfig.num_of_days_to_renotify_expiring_objects = 2

                        filterer = ObjectNotificationFilterer(appconfig)
                        

                        key1 = ExpiringObject('key-1','key')
                        key1.versions = [
                            ExpiringVersion('dasdada', datetime(2024,11,1), datetime(2023,11,1)),
                        ]
                        expiring_objs = [key1]

                        filtered_objs = filterer.filter_objects('vault_a', expiring_objs)

                        assert len(filtered_objs) == 0



    def test_expiring_object_are_tracked_with_new_version_created(self):
        """
        test case: 3. objects are tracked, but a new version is created and this new version was not previously tracked.
        """

        tracked_obj = TrackedExpiringObject('key', 'key-1')
        tracked_obj.versions['1'] = datetime(2024,9,5)  # last notify date

        with patch("db.VaultObjectTableGateway.is_object_exists", return_value=(True, tracked_obj)):
            with patch("db.VaultObjectTableGateway.insert_new_vault_object", return_value=None):
                with patch("db.VaultObjectTableGateway.update_existing_vault_object", return_value=None):
                    with freeze_time('2024-09-6'): # represents datetime.now()


                        appconfig = self.get_appconfig()
                        appconfig.num_of_days_to_renotify_expiring_objects = 2

                        filterer = ObjectNotificationFilterer(appconfig)
                        

                        key1 = ExpiringObject('key-1','key')
                        key1.versions = [
                            ExpiringVersion('1', datetime(2024,11,1), datetime(2023,11,1)),
                            ExpiringVersion('2', datetime(2025,11,1), datetime(2024,11,1)),
                        ]
                        expiring_objs = [key1]

                        filtered_objs = filterer.filter_objects('vault_a', expiring_objs)

                        assert len(filtered_objs) == 1
                        assert filtered_objs[0].versions[0].version == '2'

    def test_both_objects_andversions_are_tracked_and_last_notified_date_meets_renotify_date(self):
        """
        test case: 5. both object and version are tracked last_notified_date meets re-notify date

        formula = 2024-9-5 (last notify date) + 2 (num_of_days_to_renotify_expiring_objects) <= 2024-09-10
            is True, filterer will not filter away objects since last notify date + days meets
            re-notify date 2024-09-7.
        """

        tracked_obj = TrackedExpiringObject('key', 'key-1')
        tracked_obj.versions['1'] = datetime(2024,9,5)  # last notify date
        tracked_obj.versions['2'] = datetime(2024,9,5)

        with patch("db.VaultObjectTableGateway.is_object_exists", return_value=(True, tracked_obj)):
            with patch("db.VaultObjectTableGateway.insert_new_vault_object", return_value=None):
                with patch("db.VaultObjectTableGateway.update_existing_vault_object", return_value=None):
                    with freeze_time('2024-09-7'): # represents datetime.now()


                        appconfig = self.get_appconfig()
                        appconfig.num_of_days_to_renotify_expiring_objects = 2

                        filterer = ObjectNotificationFilterer(appconfig)
                        

                        key1 = ExpiringObject('key-1','key')
                        key1.versions = [
                            ExpiringVersion('1', datetime(2024,11,1), datetime(2023,11,1)),
                            ExpiringVersion('2', datetime(2025,11,1), datetime(2024,11,1)),
                        ]
                        expiring_objs = [key1]

                        filtered_objs = filterer.filter_objects('vault_a', expiring_objs)

                        assert len(filtered_objs) == 1
                        assert len(filtered_objs[0].versions) == 2