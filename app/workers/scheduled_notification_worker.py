from uuid import UUID

from app.services.schedule_service import schedule_service
from app.core.database import SessionLocal
from app.services.notification_dispatcher import notification_dispatcher
from app.services.template_service import template_service
from time import sleep
from app.models.notification import Notification
from app.schemas.notification import Notification_Category, Notification_Priority, Notification_Status, NotificationTargetType
from app.services.notification_service import (notification_service)
from app.repositories.device_repository import user_device_repo
from app.utils.logger import logger


def create_notification_from_schedule(
    schedule,
    user_id,
    template
):
    return Notification(
        user_id=user_id,
        channel=schedule.channel,
        notification_template_id=
            schedule.notification_template_id,
        scheduled_notification_id=
            schedule.id,
        title=template.title,
        body=template.body,
        status=Notification_Status.Pending,
        retry_count=0,
        category=schedule.category,
        priority=Notification_Priority.Medium,
    )


while True:
    logger.info("Schedule worker run start")
    db = SessionLocal()

    try:
        due_schedules = (schedule_service.process_due_notifications(db))
        for schedule in due_schedules:
            try:
                notification_template =  template_service.get_template(db, schedule.notification_template_id)
                if not notification_template:
                    logger.warning(f"Template {schedule.notification_template_id} not found")
                    schedule_service.mark_failed(db,schedule.id)
    
                all_success = True
    
                if schedule.target_type == NotificationTargetType.User:
                    if schedule.category in (Notification_Category.Promotion,Notification_Category.System):
                        notification = create_notification_from_schedule(schedule, UUID(schedule.target_data["user_id"]),notification_template)
                
                        notification = notification_service.create_notification(db,notification)
                
                        # Send
                        sent = notification_dispatcher.send_notification(db,notification)
                        all_success = all_success and sent
                elif schedule.target_type == NotificationTargetType.Users:
                    if schedule.category in (Notification_Category.Promotion,Notification_Category.System):
                        for user_id in schedule.target_data["user_ids"]:
    
                            notification = create_notification_from_schedule(schedule, UUID(user_id),notification_template)
                    
                            notification = notification_service.create_notification(db,notification)
                    
                            # Send
                            sent = notification_dispatcher.send_notification(db,notification)
                            all_success = all_success and sent
    
                elif schedule.target_type == NotificationTargetType.AllUsers:
                    if schedule.category in (Notification_Category.Promotion,Notification_Category.System):
                        users_devices = user_device_repo.get_all_push_enabled_devices(db)
                        if not users_devices:
                            all_success = False
                        for user_device in users_devices:
                            notification = create_notification_from_schedule(schedule, user_device.user_id, notification_template)
                    
                            notification = notification_service.create_notification(db,notification)
                    
                            # Send
                            sent = notification_dispatcher.send_notification(db,notification)
                            all_success = all_success and sent
    
                # Mark schedule as sent
                if all_success:
                    schedule_service.mark_sent(db,schedule.id)
    
                else: 
                    schedule_service.mark_failed(db, schedule.id)
            except Exception as ex:
                logger.exception(f"Failed to send schedule notification {schedule.id} due {str(ex)}")
                schedule_service.mark_failed(db, schedule.id)
    finally:
        db.close()
        logger.info(f"Schedule worker processed {len(due_schedules)} schedules")
    sleep(10)
