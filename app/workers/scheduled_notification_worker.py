from uuid import UUID

from app.services.schedule_service import schedule_service
from app.core.database import get_db
from app.services.notification_dispatcher import notification_dispatcher
from app.services.template_service import template_service
from time import sleep
from app.models.notification import Notification
from app.schemas.notification import Notification_Category, Notification_Priority, Notification_Status, NotificationTargetType
from app.services.notification_service import (notification_service)

db = get_db()

while True:

    due_schedules = (schedule_service.process_due_notifications(db))

    for schedule in due_schedules:
        notification_template =  template_service.get_template(db, schedule.notification_template_id)

        if schedule.target_type != NotificationTargetType.User:
            if schedule.category == Notification_Category.Promotion or schedule.category == Notification_Category.System:
                notification = Notification(
                    user_id=UUID(schedule.target_data["user_id"]),
                    channel=schedule.channel,
                    notification_template_id=schedule.notification_template_id,
                    scheduled_notification_id=schedule.id,
                    title=notification_template.title,
                    body=notification_template.body,
                    status=Notification_Status.Pending,
                    retry_count=0,
                    category=schedule.category,
                    priority=Notification_Priority.Medium,
                )
        
                notification = (notification_service.create_notification(db,notification))
        
                # Send
                notification_dispatcher.send_notification(db,notification)
        elif schedule.target_type != NotificationTargetType.Users:
            if schedule.category == Notification_Category.Promotion or schedule.category == Notification_Category.System:
                for user_id in list(schedule.target_data["user_id"]):
                    notification = Notification(
                        user_id=UUID(user_id),
                        channel=schedule.channel,
                        notification_template_id=schedule.notification_template_id,
                        scheduled_notification_id=schedule.id,
                        title=notification_template.title,
                        body=notification_template.body,
                        status=Notification_Status.Pending,
                        retry_count=0,
                        category=schedule.category,
                        priority=Notification_Priority.Medium,
                    )
            
                    notification = (notification_service.create_notification(db,notification))
            
                    # Send
                    notification_dispatcher.send_notification(db,notification)
        # Mark schedule as sent
        schedule_service.mark_sent(
            db,
            schedule.id
        )

    sleep(10)