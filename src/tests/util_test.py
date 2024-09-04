from util import LogicUtil
import os 
import datetime
from freezegun import freeze_time

class TestLogicUtil:

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