from twilio.rest import Client  # type: ignore[import]

from app.core.config import settings
from app.utils.logger import logger


class SMSProvider:

    def __init__(self) -> None:
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

    def send(
        self,
        phone_number: str,
        message: str
    ) -> bool:

        try:
            self.client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )

            return True

        except Exception as ex:
            logger.exception(
                f"Failed to send SMS: {str(ex)}"
            )
            return False


sms_provider = SMSProvider()