import os
import json
from dotenv import load_dotenv
load_dotenv()



class SMTPConfig:
    def __init__(self) -> None:
        self.host = ''
        self.port = 587,
        self.username = ''
        self.password = ''
        self.subject = ''
        self.senderAddress = ''
        self.to = []
        self.cc = []
        
class AppConfig:

    def __init__(self) -> None:
        nod_before_exp = int(os.environ.get('NUM_OF_DAYS_NOTIFY_BEFORE_EXPIRY'))
        nod_resend_email  = int(os.environ.get('NUM_OF_DAYS_BEFORE_RESEND_EMAIL_AGAIN_FOR_EXPIRING_ITEMS'))

        self.num_of_days_notify_before_expiry = nod_before_exp if nod_before_exp else 60
        self.num_of_days_before_resend_email_for_expiring_items = nod_resend_email if nod_resend_email else 3
        self.smtp_config = self.get_smtp_config()
        

    def get_smtp_config(self):
        
        scj = os.environ.get('SMTP_CONFIG')

        if not scj:
            raise Exception('SMTP config is either malformed or missing')
        

        smtpc = SMTPConfig()

        sc = json.loads(scj)

        smtpc.host = sc['host']
        smtpc.port = int(sc['port'])
        smtpc.username = sc['username']
        smtpc.password = sc['password']
        smtpc.subject = sc['subject']
        smtpc.senderAddress = sc['senderAddress']
        smtpc.to = sc['to']
        smtpc.cc = sc['cc']

        return smtpc


