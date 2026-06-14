import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from app.core.config import settings
from app.utils.logger import logger



class EmailProvider:

    def send(
        self,
        to_email: str,
        subject: str,
        body: str
    ) -> bool:

        try:
            message = MIMEMultipart()
            message["From"] = settings.SMTP_USERNAME
            message["To"] = to_email
            message["Subject"] = subject

            message.attach(
                MIMEText(body, "html")
            )

            with smtplib.SMTP(
                settings.SMTP_HOST,
                int(settings.SMTP_PORT),
                timeout=10
            ) as server:

                server.starttls()

                server.login(
                    settings.SMTP_USERNAME,
                    settings.SMTP_PASSWORD
                )

                server.send_message(message)

            return True

        except Exception as ex:
            logger.exception(f"Failed to send email: {str(ex)}")
            return False
        
email_provider = EmailProvider()