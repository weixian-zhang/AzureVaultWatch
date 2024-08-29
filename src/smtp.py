import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import AppConfig

class SMTPSender:

    def __init__(self, appconfig: AppConfig) -> None:
        self.appconfig = appconfig

    def send(self, content: str):
        # Create an SMTP object and establish a connection to the SMTP server
        smtpObj = smtplib.SMTP(self.appconfig.smtp_config.host, self.appconfig.smtp_config.port)

        # Identify yourself to an ESMTP server using EHLO
        smtpObj.ehlo()

        # Secure the SMTP connection
        smtpObj.starttls()

        # Login to the server (if required)
        smtpObj.login(self.appconfig.smtp_config.username, self.appconfig.smtp_config.password)

        html_mime = MIMEText(content, 'html')

        msg = MIMEMultipart('alternative') #EmailMessage()
        msg.attach(html_mime)
        msg['Subject'] = self.appconfig.smtp_config.subject
        msg['From'] = self.appconfig.smtp_config.senderAddress
        msg['To'] = self.appconfig.smtp_config.to
        msg['Cc'] = self.appconfig.smtp_config.cc

        smtpObj.sendmail( self.appconfig.smtp_config.senderAddress, self.appconfig.smtp_config.to, msg.as_string())
        #smtpObj.send_message(msg)

        # Quit the SMTP session
        smtpObj.quit()