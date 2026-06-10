from sqlalchemy.orm import Session
from typing import Any
from uuid import UUID
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime



from app.models.scheduled_notification import ScheduledNotification
from app.schemas.notification import Scheduled_Notification_Status
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
    
    def get_due_notifications(self, db: Session, limit: int = 100) -> list[ScheduledNotification]:
        return (db.query(ScheduledNotification).filter(ScheduledNotification.status == Scheduled_Notification_Status.Pending,
            ScheduledNotification.is_active.is_(True),
            ScheduledNotification.scheduled_at <= datetime.utcnow()).limit(limit).all())

    def get_pending_notifications(self, db: Session) -> list[ScheduledNotification]:
        return db.query(ScheduledNotification).filter(ScheduledNotification.status == Scheduled_Notification_Status.Pending).all()
    
    def count_pending_notifications(self, db: Session) -> int:
        return db.query(ScheduledNotification).filter(ScheduledNotification.status == Scheduled_Notification_Status.Pending).count()

    def count_completed_notifications(self, db: Session) -> int:
        return db.query(ScheduledNotification).filter(ScheduledNotification.status == Scheduled_Notification_Status.Sent).count()
    
    def get_failed_notifications(self, db: Session) -> list[ScheduledNotification]:
        return (db.query(ScheduledNotification).filter(ScheduledNotification.status ==Scheduled_Notification_Status.Failed).all())
    
    def get_active_schedules(self,db: Session) -> list[ScheduledNotification]:
        return (db.query(ScheduledNotification).filter(ScheduledNotification.is_active.is_(True)).all())

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

    def update_target_data(self, db:Session, record_id: UUID, target_data: dict[str, Any])-> ScheduledNotification | None:
        try:
            notification = self.get_by_id(db, record_id)
            if not notification:
                return None
            if notification.target_data == target_data:
                return notification
            notification.target_data = target_data
            self._save(db, notification)
            logger.info(f"Notification target data updated successfully for notification {str(notification.id)}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update Notification target data due {str(ex)}")
            raise

    def update_template_id(self, db:Session, record_id: UUID, template_id: UUID)-> ScheduledNotification | None:
        try:
            notification = self.get_by_id(db, record_id)
            if not notification:
                return None
            if notification.notification_template_id == template_id:
                return notification
            notification.notification_template_id = template_id
            self._save(db, notification)
            logger.info(f"Notification template id updated successfully for notification {str(notification.id)}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update Notification template id due {str(ex)}")
            raise

    def mark_as_sent(self, db:Session, notification_id: UUID)-> ScheduledNotification | None:
        try:
            notification = self.get_by_id(db, notification_id)
            if not notification:
                return None
            if notification.status == Scheduled_Notification_Status.Sent:
                return notification
            notification.status = Scheduled_Notification_Status.Sent
            notification.sent_at = datetime.utcnow()
            self._save(db, notification)
            logger.info(f"Notification marked as 'Sent' successfully for notification {str(notification.id)}")
            return notification
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to mark as 'Sent' notification due {str(ex)}")
            raise

    def mark_as_failed(self, db:Session, notification_id: UUID)-> ScheduledNotification | None:
        try:
            notification = self.get_by_id(db, notification_id)
            if not notification:
                return None
            if notification.status == Scheduled_Notification_Status.Failed:
                return notification
            notification.status = Scheduled_Notification_Status.Failed
            self._save(db, notification)
            logger.info(f"Notification marked as 'Failed' successfully for notification {str(notification.id)}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to mark as 'Failed' notification due {str(ex)}")
            raise

    def activate_schedule(self, db:Session, notification_id: UUID)-> ScheduledNotification | None:
        try:
            notification = self.get_by_id(db, notification_id)
            if not notification:
                return None
            if notification.is_active:
                return notification
            notification.is_active = True
            self._save(db, notification)
            logger.info(f"Notification schedule activated successfully for notification {str(notification.id)}")
            return notification
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to activate Notification schedule due {str(ex)}")
            raise

    def deactivate_schedule(self, db:Session, notification_id: UUID)-> ScheduledNotification | None:
        try:
            notification = self.get_by_id(db, notification_id)
            if not notification:
                return None
            if not notification.is_active:
                return notification
            notification.is_active = False
            self._save(db, notification)
            logger.info(f"Notification schedule deactivated successfully for notification {str(notification.id)}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to deactivate notification schedule due {str(ex)}")
            raise


scheduled_notification_repo = ScheduledNotificationRepository()
