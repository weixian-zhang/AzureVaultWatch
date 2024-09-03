from util import LogicUtil
import pytest
import os 
import datetime
from unittest.mock import patch, Mock
from unittest import mock
from freezegun import freeze_time

cwd = os.path.dirname(os.path.realpath(__file__))
scan_context = None

# @pytest.fixture()
# def resource():
#     with open(os.path.join(cwd, 'scan_context.json')) as f:
#         sc_str = f.read()
#         sc = json.loads(sc_str)

#         yield sc
#         print("teardown")

class TestLogicUtil:
 # scenarios to filter objects from re-sending email notification until configured re-notify date is met
    # 1. object not tracked, begin tracking object
    # 2. objects are tracked - no new versions are created
    # 3. objects are tracked - # but a new version is created and this new version was not previously tracked.

    # *re-notify date = last notify date + NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS
    # 4. both object and version are tracked
        # last_notified_date does not meet re-notify date
    # 5. both object and version are tracked
        # last_notified_date meet re-noitfy-date


    """
    freezetime is use to mock datetime.now() in LogicUtil functions
    """
    def test_version_previously_notify_should_renotify_as_renotify_date_met(self) -> None:
        """
        last_notify_date + NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS <= datetime.now()
        """

        with freeze_time("2024-08-03"):
           
            last_notify_date = datetime.datetime(2024, 8, 1)

            NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS = 2

            should_notify_again = LogicUtil.should_notify_again(last_notify_date, NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS)

            assert should_notify_again


    def test_version_previously_notify_should_renotify_as_renotify_date_met_2(self) -> None:
        """
        last_notify_date + NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS <= datetime.now()
        """
         
        with freeze_time("2024-08-11"): 

            last_notify_date = datetime.datetime(2024, 8, 1)

            NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS = 10

            should_notify_again = LogicUtil.should_notify_again(last_notify_date, NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS)

            assert should_notify_again

    def test_version_previously_notify_should_not_renotify_as_renotify_date_met_1(self) -> None:
        """
        last_notify_date + NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS <= datetime.now()
        """

        with freeze_time("2024-08-03"): 

            last_notify_date = datetime.datetime(2024, 8, 2)

            NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS = 2

            should_notify_again = LogicUtil.should_notify_again(last_notify_date, NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS)

            assert not should_notify_again

    # test version expiring

    def test_version_is_expiring(self) -> None:
        """
        formula: datetime.now() >= version_expires_on - NUM_OF_DAYS_NOTIFY_BEFORE_EXPIRY
        """

        with freeze_time("2024-09-01"): 

            version_expires_on = datetime.datetime(2024, 10, 1)

            NUM_OF_DAYS_NOTIFY_BEFORE_EXPIRY = 30

            is_expiring = LogicUtil.is_expiring(version_expires_on, NUM_OF_DAYS_NOTIFY_BEFORE_EXPIRY)

            assert is_expiring

    def test_version_is_not_expiring(self) -> None:
        """
        formula: datetime.now() >= version_expires_on - NUM_OF_DAYS_NOTIFY_BEFORE_EXPIRY
        """

        with freeze_time("2024-08-01"): 

            version_expires_on = datetime.datetime(2024, 10, 1)

            NUM_OF_DAYS_NOTIFY_BEFORE_EXPIRY = 30

            is_expiring = LogicUtil.is_expiring(version_expires_on, NUM_OF_DAYS_NOTIFY_BEFORE_EXPIRY)

            assert not is_expiring