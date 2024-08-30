
from pytz import timezone
from datetime import datetime

class Util:

    @staticmethod
    def now_str():
        return datetime.now().astimezone(timezone('Asia/Kuala_Lumpur')).ctime()
    
    def as_friendly_date_str(d: datetime):
        if d:
            return d.astimezone(timezone('Asia/Kuala_Lumpur')).strftime("%a %b %d %Y %H:%M") #d.astimezone(timezone('Asia/Kuala_Lumpur')).ctime()
    
    def days_to_expiry(d:datetime):
        now = datetime.now().astimezone(timezone('Asia/Kuala_Lumpur'))
        dt = d.astimezone(timezone('Asia/Kuala_Lumpur'))
        return (dt - now).days