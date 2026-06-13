from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime


from app.repositories.schedule_repository import scheduled_notification_repo
from app.models.scheduled_notification import ScheduledNotification as schedule_model
from app.schemas.notification import Scheduled_Notification, Scheduled_Notification_Status

class ScheduleService:

    def schedule_notification(self, db: Session, schedule_notification: Scheduled_Notification)-> schedule_model:
        new_schedule = schedule_model(**schedule_notification.model_dump())
        return scheduled_notification_repo.create_scheduled_notification(db, new_schedule)
    
    def get_schedule(self, db: Session, notification_id: UUID)-> schedule_model | None:
        return scheduled_notification_repo.get_by_id(db, notification_id)
    
    def activate_schedule(self, db: Session, notification_id: UUID)-> schedule_model | None:
        return scheduled_notification_repo.activate_schedule(db, notification_id)
    
    def deactivate_schedule(self, db: Session, notification_id: UUID)-> schedule_model | None:
        return scheduled_notification_repo.deactivate_schedule(db, notification_id)

    def reschedule_notification(self, db: Session, notification_id: UUID, schedule_at: datetime)-> schedule_model | None:
        if schedule_at <= datetime.utcnow():
            raise ValueError(
                "scheduled_at must be in the future"
            )
        return scheduled_notification_repo.update_schedule_time(db, notification_id, schedule_at)
    
    def cancel_schedule(self, db: Session, notification_id: UUID)-> schedule_model | None:
        return scheduled_notification_repo.update_status(db, notification_id, new_status= Scheduled_Notification_Status.Cancelled)
    
    def process_due_notifications(self, db: Session, limit: int = 100)-> list[schedule_model]:
        return scheduled_notification_repo.get_due_notifications(db, limit)
    

schedule_service = ScheduleService()