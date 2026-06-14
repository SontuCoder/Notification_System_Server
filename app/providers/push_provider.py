from firebase_admin import messaging  # type: ignore[import]
from app.utils.logger import logger


class PushProvider:

    def send(
        self,
        device_token: str,
        title: str | None,
        body: str
    ) -> bool:

        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title or "",
                    body=body
                ),
                token=device_token
            )

            messaging.send(message)
            return True

        except Exception as ex:
            logger.exception(
                f"Failed to send push notification: {ex}"
            )
            return False


push_provider = PushProvider()