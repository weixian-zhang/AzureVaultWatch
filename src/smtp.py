import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.generator import Generator
from io import StringIO
from config import AppConfig
from opentelemetry.trace import Tracer

class SMTPSender:

    def __init__(self, appconfig: AppConfig, otel_tracer: Tracer) -> None:
        self.appconfig = appconfig
        self.otel_tracer = otel_tracer

    def send(self, content: str):

        with self.otel_tracer.start_as_current_span('SMTPSender.send') as cs:

            # Create an SMTP object and establish a connection to the SMTP server
            smtpObj = smtplib.SMTP(self.appconfig.smtp_config.host, self.appconfig.smtp_config.port)

            # Identify yourself to an ESMTP server using EHLO
            smtpObj.ehlo()

            # Secure the SMTP connection
            smtpObj.starttls()

            smtpObj.login(self.appconfig.smtp_config.username, self.appconfig.smtp_config.password)

            html_mime = MIMEText(content, 'html', 'UTF-8')

            msg = MIMEMultipart('alternative') #EmailMessage()
            msg.attach(html_mime)
            msg['Subject'] = self.appconfig.smtp_config.subject
            msg['From'] = self.appconfig.smtp_config.senderAddress
            msg['To'] = ', '.join(self.appconfig.smtp_config.to)
            msg['Cc'] = ', '.join(self.appconfig.smtp_config.cc)

            # Create a generator and flatten message object to 'file’
            str_io = StringIO()
            g = Generator(str_io, False)
            g.flatten(msg)

            smtpObj.sendmail( self.appconfig.smtp_config.senderAddress, self.appconfig.smtp_config.to, msg.as_string())

            smtpObj.quit()

            cs.add_event('finish SMTPSender.send')