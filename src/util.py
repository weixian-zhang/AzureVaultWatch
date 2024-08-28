
from pytz import timezone
from datetime import datetime

class Util:

    @staticmethod
    def now_str():
        return datetime.now().astimezone(timezone('Asia/Kuala_Lumpur')).ctime()
    
    def as_date_str(d: datetime):
        return d.astimezone(timezone('Asia/Kuala_Lumpur')).ctime() #d.astimezone(timezone('Asia/Kuala_Lumpur')).strftime("%d-%m-%Y %H:%M:%S")
    
    def days_to_expiry(d:datetime):
        now = datetime.now().astimezone(timezone('Asia/Kuala_Lumpur'))
        dt = d.astimezone(timezone('Asia/Kuala_Lumpur'))
        return (dt - now).days