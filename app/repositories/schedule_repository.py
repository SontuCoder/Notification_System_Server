from sqlalchemy.orm import Session
from typing import Any
from uuid import UUID
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime



from app.models.scheduled_notification import ScheduledNotification
from app.schemas.notification import Notification_Channel, Scheduled_Notification_Status
from app.utils.logger import logger


class ScheduledNotificationRepository:

    def _save(self, db: Session, scheduled_notification: ScheduledNotification) -> None:
        db.commit()
        db.refresh(scheduled_notification)
    
    # ============= Create ==============
    def create_scheduled_notification(self, db: Session, new_schedule: ScheduledNotification)-> ScheduledNotification:
        try:
            db.add(new_schedule)
            self._save(db, new_schedule)
            logger.info(f"New notification scheduled successfully for new schedule_id={new_schedule.id}")
            return new_schedule
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to schedule notification : {str(ex)}")
            raise
    
    # ============= Get ==============

    def get_by_id(self, db: Session, record_id: UUID)-> ScheduledNotification | None:
        return db.query(ScheduledNotification).filter(ScheduledNotification.id == record_id).first()

    def get_by_status(self, db: Session, status: Scheduled_Notification_Status) -> list[ScheduledNotification]:
        return  db.query(ScheduledNotification).filter(ScheduledNotification.status == status).all()
    
    def get_by_template_id(self, db: Session, template_id: UUID) -> list[ScheduledNotification]:
        return  db.query(ScheduledNotification).filter(ScheduledNotification.notification_template_id == template_id).all()
    
    def exists_by_id(self, db: Session, record_id: UUID) -> bool:
        return bool(db.query(exists().where(ScheduledNotification.id == record_id)).scalar()) 
    
    def get_due_notifications(self, db: Session) -> list[ScheduledNotification]:
        return (db.query(ScheduledNotification).filter(ScheduledNotification.status == Scheduled_Notification_Status.Pending,
            ScheduledNotification.is_active.is_(True),
            ScheduledNotification.scheduled_at <= datetime.utcnow()).all())

    def get_pending_notifications(self, db: Session) -> list[ScheduledNotification]:
        return db.query(ScheduledNotification).filter(ScheduledNotification.status == Scheduled_Notification_Status.Pending).all()
    
    def count_pending_notifications(self, db: Session) -> list[ScheduledNotification]:
        return db.query(ScheduledNotification).filter(ScheduledNotification.status == Scheduled_Notification_Status.Pending).count()

    def count_completed_notifications(self, db: Session) -> list[ScheduledNotification]:
        return db.query(ScheduledNotification).filter(ScheduledNotification.status == Scheduled_Notification_Status.Sent).count()
    

    # ============= Update ==============

    def update_status(self, db:Session, record_id: UUID, new_status: Scheduled_Notification_Status)-> ScheduledNotification | None:
        try:
            notification = self.get_by_id(db, record_id)
            if not notification:
                return None
            if notification.status == new_status:
                return notification
            notification.status = new_status
            self._save(db, notification)
            logger.info(f"Schedule notification status updated successfully for notification {str(notification.id)}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update Schedule notification status due {str(ex)}")
            raise

    def update_schedule_time(self, db:Session, record_id: UUID, scheduled_at: datetime)-> ScheduledNotification | None:
        try:
            notification = self.get_by_id(db, record_id)
            if not notification:
                return None
            if notification.scheduled_at == scheduled_at:
                return notification
            notification.scheduled_at = scheduled_at
            self._save(db, notification)
            logger.info(f"Notification schedule updated successfully for notification {notification.id}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update notification schedule due {str(ex)}")
            raise

    def update_target_data(self, db:Session, record_id: UUID, new_body: str)-> ScheduledNotification | None:
        try:
            notification = self.get_by_id(db, record_id)
            if not notification:
                return None
            if notification.body == new_body:
                return notification
            notification.body = new_body
            self._save(db, notification)
            logger.info(f"Template body updated successfully for template {str(notification.id)}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update template body due {str(ex)}")
            raise



    def update_channel(self, db:Session, temp_id: UUID, new_channel: Notification_Channel)-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if template.channel == new_channel:
                return template
            template.channel = new_channel
            self._save(db, template)
            logger.info(f"Template channel updated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update template channel due {str(ex)}")
            raise

    def update_variables(self, db:Session, temp_id: UUID, new_variable:dict[str, Any])-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if template.variables == new_variable:
                return template
            template.variables = new_variable
            self._save(db, template)
            logger.info(f"Template variables updated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update template variables due {str(ex)}")
            raise

    def activate_template(self, db:Session, temp_id: UUID)-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if template.is_active:
                return template
            template.is_active = True
            self._save(db, template)
            logger.info(f"Template activated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to activate template due {str(ex)}")
            raise

    def deactivate_template(self, db:Session, temp_id: UUID)-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if not template.is_active:
                return template
            template.is_active = False
            self._save(db, template)
            logger.info(f"Template deactivated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to deactivate template due {str(ex)}")
            raise

    def update_template( self, db: Session, temp_id: UUID, title: str | None, body: str, variables: dict[str, Any] | None ) ->NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            
            if template.title == title and template.body == body and template.variables == variables:
                return template
            template.title = title
            template.body = body
            template.variables = variables
            self._save(db, template)
            logger.info(f"Template updated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update template due {str(ex)}")
            raise


notification_template_repo = NotificationTemplateRepository()


# ScheduledNotificationRepository
# │
# ├── mark_as_sent()
# ├── mark_as_failed()
# │
# ├── activate_schedule()
# └── deactivate_schedule()
