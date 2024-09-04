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
        nod_renotify  = int(os.environ.get('NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS'))

        self.storage_account_name = os.environ.get('STORAGE_ACCOUNT_NAME')
        self.storage_table_name = os.environ.get('STORAGE_TABLE_NAME')
        self.num_of_days_notify_before_expiry = nod_before_exp
        self.num_of_days_to_renotify_expiring_objects = nod_renotify
        self.smtp_config = self.get_smtp_config()
        self.appinsights_connection_string = os.environ.get('APP_INSIGHTS_CONN_STRIN')
        

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


