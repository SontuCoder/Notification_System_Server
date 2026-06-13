from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime



from app.models.notification import Notification
from app.schemas.notification import Notification_Status, Notification_Channel
from app.utils.logger import logger


class NotificationRepository:

    def _save(self, db: Session, notification: Notification) -> None:
        db.commit()
        db.refresh(notification)
    
    # ============= Create ==============
    def create_notification(self, db: Session, new_notification: Notification)-> Notification:
        try:
            db.add(new_notification)
            self._save(db, new_notification)
            logger.info(f"New notification created successfully for new notification_id={new_notification.id}")
            return new_notification
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to create notification : {str(ex)}")
            raise
    
    # ============= Get ==============

    def get_by_id(self, db: Session, record_id: UUID)-> Notification | None:
        return db.query(Notification).filter(Notification.id == record_id).first()

    def get_by_user_id(self, db: Session, user_id: UUID) -> list[Notification]:
        return  db.query(Notification).filter(Notification.user_id == user_id).all()
    
    def get_by_status(self, db: Session, status: Notification_Status) -> list[Notification]:
        return  db.query(Notification).filter(Notification.status == status).all()

    def get_by_channel(self, db: Session, channel: Notification_Channel) -> list[Notification]:
        return db.query(Notification).filter(Notification.channel == channel).all()
    
    def get_by_template_id(self, db: Session, template_id: UUID) -> list[Notification]:
        return (db.query(Notification).filter(Notification.notification_template_id == template_id).all())

    def get_by_scheduled_notification_id(self, db: Session, schedule_id: UUID) -> list[Notification]:
        return (db.query(Notification).filter(Notification.scheduled_notification_id == schedule_id).all())
    
    def get_pending_notifications(self, db: Session) -> list[Notification]:
        return db.query(Notification).filter(Notification.status == Notification_Status.Pending).all()

    def get_sent_notifications(self, db: Session) -> list[Notification]:
        return db.query(Notification).filter(Notification.status == Notification_Status.Sent).all()
    
    def get_delivered_notifications(self, db: Session) -> list[Notification]:
        return db.query(Notification).filter(Notification.status == Notification_Status.Delivered).all()
    
    def get_failed_notifications(self, db: Session) -> list[Notification]:
        return db.query(Notification).filter(Notification.status == Notification_Status.Failed).all()

    def exists_by_id(self, db: Session, record_id: UUID) -> bool:
        return bool(db.query(exists().where(Notification.id == record_id)).scalar())

    def count_sent_notifications(self, db: Session) -> int:
        return db.query(Notification).filter(Notification.status == Notification_Status.Sent).count()
    
    def count_pending_notifications(self, db: Session) -> int:
        return db.query(Notification).filter(Notification.status == Notification_Status.Pending).count()
    
    def count_failed_notifications(self, db: Session) -> int:
        return db.query(Notification).filter(Notification.status == Notification_Status.Failed).count()
    
    def count_delivered_notifications(self, db: Session) -> int:
        return db.query(Notification).filter(Notification.status == Notification_Status.Delivered).count()
    
    def get_notifications_for_retry(self, db: Session, max_retry_count: int = 3) -> list[Notification]:
        return db.query(Notification).filter(Notification.status == Notification_Status.Failed, Notification.retry_count < max_retry_count).all()
    # ============= Update ==============

    def update_status(self, db:Session, record_id: UUID, new_status: Notification_Status)-> Notification | None:
        try:
            notification = self.get_by_id(db, record_id)
            if not notification:
                return None
            if notification.status == new_status:
                return notification
            notification.status = new_status
            self._save(db, notification)
            logger.info(f"Notification status updated successfully for notification {str(notification.id)}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update notification status due {str(ex)}")
            raise

    def increment_retry_count(self, db:Session, record_id: UUID)-> Notification | None:
        try:
            notification = self.get_by_id(db, record_id)
            if not notification:
                return None
            notification.retry_count +=1
            self._save(db, notification)
            logger.info(f"Notification retry count updated successfully for notification {str(notification.id)}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update notification retry count due {str(ex)}")
            raise

    def mark_as_sent(self, db:Session, notification_id: UUID)-> Notification | None:
        try:
            notification = self.get_by_id(db, notification_id)
            if not notification:
                return None
            if notification.status == Notification_Status.Sent:
                return notification
            notification.status = Notification_Status.Sent
            notification.sent_at = datetime.utcnow()
            self._save(db, notification)
            logger.info(f"Notification marked as 'Sent' successfully for notification {str(notification.id)}")
            return notification
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to mark as 'Sent' notification due {str(ex)}")
            raise

    def mark_as_failed(self, db:Session, notification_id: UUID, failure_reason: str)-> Notification | None:
        try:
            notification = self.get_by_id(db, notification_id)
            if not notification:
                return None
            if notification.status == Notification_Status.Failed:
                return notification
            notification.status = Notification_Status.Failed
            notification.failure_reason = failure_reason
            self._save(db, notification)
            logger.info(f"Notification marked as 'Failed' successfully for notification {str(notification.id)}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to mark as 'Failed' notification due {str(ex)}")
            raise

    def mark_as_delivered(self, db:Session, notification_id: UUID)-> Notification | None:
        try:
            notification = self.get_by_id(db, notification_id)
            if not notification:
                return None
            if notification.status == Notification_Status.Delivered:
                return notification
            if notification.sent_at is None:
                notification.sent_at = datetime.utcnow()
            notification.status = Notification_Status.Delivered
            notification.delivered_at = datetime.utcnow()
            self._save(db, notification)
            logger.info(f"Notification marked as 'Delivered' successfully for notification {str(notification.id)}")
            return notification
        
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to mark as 'Delivered' notification due {str(ex)}")
            raise

    def increment_retry_count_bulk(
        self,
        db: Session,
        notification_ids: list[UUID]
    ) -> int:
    
        try:
            updated_count = (
                db.query(Notification)
                .filter(Notification.id.in_(notification_ids))
                .update(
                    {
                        Notification.retry_count:
                        Notification.retry_count + 1
                    },
                    synchronize_session=False
                )
            )
        
            db.commit()
            logger.info(f"Notification retry count updated successfully for {str(updated_count)} notifications")
            return updated_count
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update notifications retry count due {str(ex)}")
            raise

    # ============= Delete ==============
    def delete_by_user_id(self, db: Session, user_id: UUID) -> bool:
        try:
            deleted_count = (db.query(Notification).filter(Notification.user_id == user_id).delete(synchronize_session=False))
            db.commit()
            logger.info(f"{deleted_count} notifications deleted for user {user_id}")
            return deleted_count > 0
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to delete notifications due {str(ex)}")
            raise

    def delete_by_id(self, db: Session, record_id: UUID) -> bool:
        try:
            notification  = self.get_by_id(db, record_id)
            
            if not notification :
                return False
            db.delete(notification )
            db.commit()
            logger.info(f"Notification deleted successfully for {notification .id}")
            return True
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to delete notification due {str(ex)}")
            raise

    def delete_old_notifications(self, db: Session, before_date: datetime) -> int:
        try:
            deleted_count = (db.query(Notification).filter(Notification.delivered_at.isnot(None),Notification.delivered_at < before_date).delete(synchronize_session=False))
            db.commit()
            logger.info(f"{deleted_count} notifications deleted")
            return deleted_count
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to delete notifications due {str(ex)}")
            raise

notification_repo = NotificationRepository()
