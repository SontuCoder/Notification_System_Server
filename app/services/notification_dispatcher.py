from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import Notification_Channel
from app.providers.push_provider import push_provider
from app.providers.email_provider import email_provider
from app.providers.sms_provider import sms_provider
from app.repositories.notification_repository import notification_repo
from app.repositories.device_repository import user_device_repo

class NotificationDispatcher:

    def send_notification(
        self,
        db: Session,
        notification: Notification
    ) -> bool:
        try: 
            if notification.channel == Notification_Channel.Email:
                success = email_provider.send(...)
    
            elif notification.channel == Notification_Channel.SMS:
                success = sms_provider.send(...)
    
            elif notification.channel == Notification_Channel.Push:
                user_devices = user_device_repo.get_active_devices_by_user_id(db,notification.user_id)
                if not user_devices:
                    success = False
                else:
                    success = True
                    for device in user_devices:
                        sent = push_provider.send(device.device_token, notification.title or "", notification.body)
                        success = success and sent
            if success:
                notification_repo.mark_as_sent(db, notification.id)
            else:
                notification_repo.mark_as_failed(db, notification.id, f"Failed to send {notification.channel} notification")
            
            return success
        except Exception as ex:
            notification_repo.mark_as_failed(
                db,
                notification.id,
                str(ex)
            )
            return False


notification_dispatcher = NotificationDispatcher()
