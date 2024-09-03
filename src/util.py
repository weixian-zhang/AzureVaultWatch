
from pytz import timezone
from datetime import datetime, timedelta

class LogicUtil:
    """
    contains utilities function that performs functional requirements
    """
    @staticmethod
    def should_notify_again(version_last_send_date: datetime, num_of_days_to_renotify_expiring_objects: int):
        last_send_with_nod = (DateUtil.as_utc8(version_last_send_date) + 
                              timedelta(days=num_of_days_to_renotify_expiring_objects))
        
        if last_send_with_nod <= DateUtil.now():
            return True
        
        return False
    
    @staticmethod
    def is_expiring(expires_on: datetime, num_of_days_notify_before_expiry: int) -> bool:
        
        if not expires_on: # Secret may not have expiry date set
            return False

        expiring_on = expires_on - timedelta(days= num_of_days_notify_before_expiry)

        if DateUtil.now() >= expiring_on.astimezone(timezone('Asia/Kuala_lumpur')):
                return True
        
        return False
    
    @staticmethod
    def create_db_row_key(type: str, name: str) -> bool:
        return f'{type}_{name}'
    

class DateUtil:

    @staticmethod
    def now():
        """
        Get current datetime with UTC+8 timezone
        """
        return DateUtil.as_utc8(datetime.now()) #.astimezone(timezone('Asia/Kuala_Lumpur'))
    
    @staticmethod
    def now_str():
        return DateUtil.as_utc8(datetime.now()) #.astimezone(timezone('Asia/Kuala_Lumpur')).ctime()
        
    
    @staticmethod
    def as_utc8(d: datetime):
        return d.astimezone(timezone('Asia/Kuala_Lumpur'))
    
    @staticmethod
    def as_friendly_date_str(d: datetime):
        if d:
            return d.astimezone(timezone('Asia/Kuala_Lumpur')).strftime("%a %b %d %Y %H:%M") #d.astimezone(timezone('Asia/Kuala_Lumpur')).ctime()
    
    @staticmethod
    def days_to_expiry(d:datetime):
        now = datetime.now().astimezone(timezone('Asia/Kuala_Lumpur'))
        dt = d.astimezone(timezone('Asia/Kuala_Lumpur'))
        return (dt - now).days