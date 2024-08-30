
from pytz import timezone
from datetime import datetime

class Util:

    @staticmethod
    def now():
        """
        Get current datetime with UTC+8 timezone
        """
        return datetime.now().astimezone(timezone('Asia/Kuala_Lumpur'))
    
    @staticmethod
    def now_str():
        return datetime.now().astimezone(timezone('Asia/Kuala_Lumpur')).ctime()
    
    @staticmethod
    def as_sing_kl_timezone(d: datetime):
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