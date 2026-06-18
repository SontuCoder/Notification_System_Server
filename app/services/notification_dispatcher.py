from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import Notification_Channel, Notification_Category
from app.providers.push_provider import push_provider
from app.providers.email_provider import email_provider
from app.providers.sms_provider import sms_provider
from app.repositories.notification_repository import notification_repo
from app.repositories.device_repository import user_device_repo
from app.clients.Auth_client import auth_client
from app.services.preference_service import preference_service

class NotificationDispatcher:

    def send_notification(
        self,
        db: Session,
        notification: Notification
    ) -> bool:
        try: 
            email_preference = False
            sms_preference = False
            push_preference = False
            promotion_preference = False

            if notification.category not in (Notification_Category.Order, Notification_Category.Promotion):
                email_preference = True
                sms_preference = True
                push_preference = True
            else:
                preference = preference_service.get_user_preferences(db, notification.user_id)
                if not preference:
                    email_preference = True
                    sms_preference = True
                    push_preference = True
                    promotion_preference = True
                else:
                    email_preference = preference.email_enabled
                    sms_preference = preference.sms_enabled
                    push_preference = preference.push_enabled
                    promotion_preference = preference.promotion_enabled

            if notification.channel == Notification_Channel.Email:
                if not email_preference:
                    return False
                email = auth_client.get_email_by_id(notification.user_id)
                if not email:
                    success = False
                else:
                    success = email_provider.send(email, notification.title, notification.body)
    
            elif notification.channel == Notification_Channel.SMS:
                if not sms_preference:
                    return False
                phone = auth_client.get_phone_by_id(notification.user_id)
                if not phone:
                    success = False
                else:
                    success = sms_provider.send(phone, notification.body)
    
            elif notification.channel == Notification_Channel.Push:
                if not push_preference:
                    return False
                if notification.category == Notification_Category.Promotion and not promotion_preference:
                    return False
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
