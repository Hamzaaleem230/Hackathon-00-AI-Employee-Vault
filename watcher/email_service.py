import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from watcher.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_FROM


class EmailService:

    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_FROM
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)


            return True

        except Exception as e:
            print(f"[EMAIL ERROR]: {e}")
            return False
