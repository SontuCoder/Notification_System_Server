from time import sleep


from app.utils.logger import logger
from app.core.database import SessionLocal
from app.services.notification_dispatcher import notification_dispatcher
from app.services.notification_service import notification_service



while True:
    logger.info("Retry worker run start")
    db = SessionLocal()
    try:
        notifications = notification_service.retry_notification(db)
        for notification in notifications:
            try:  
                notification_dispatcher.send_notification(db, notification)
                logger.info(f"Retry worker processed {len(notifications)} notifications")
            except Exception as ex:
                logger.exception(f"Failed to send notification {notification.id} due {str(ex)}")
    finally:
        db.close()

    sleep(60)