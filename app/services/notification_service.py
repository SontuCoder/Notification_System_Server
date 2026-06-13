
# send_notification()
# send_email()
# send_sms()
# send_push()
# process_failed_notification()


from sqlalchemy.orm import Session
from uuid import UUID

from app.models.notification import Notification as Notification_Model
from app.schemas.notification import Notification as Notification_Schema

from app.repositories.notification_repository import (
    notification_repo
)


class NotificationService:

    def create_notification(
        self,
        db: Session,
        notification_data: Notification_Schema
    ) -> Notification_Model:

        notification = Notification_Model(
            **notification_data.model_dump()
        )

        return notification_repo.create_notification(
            db,
            notification
        )
    
    def get_notification(
        self,
        db: Session,
        notification_id: UUID
    ) -> Notification_Model | None:
    
        return notification_repo.get_by_id(
            db,
            notification_id
        )

    def get_user_notifications(
        self,
        db: Session,
        user_id: UUID
    ) -> list[Notification_Model]:
    
        return notification_repo.get_by_user_id(
            db,
            user_id
        )
    
    def mark_sent(self, db: Session, notification_id: UUID)-> Notification_Model | None:
        return notification_repo.mark_as_sent(db, notification_id)
    
    def mark_failed(self, db: Session, notification_id: UUID, reason: str)-> Notification_Model | None:
        return notification_repo.mark_as_failed(db, notification_id, reason)
    
    def mark_delivered(self, db: Session, notification_id: UUID)-> Notification_Model | None:
        return notification_repo.mark_as_delivered(db, notification_id)
    
    def retry_notification(self, db: Session, max_retry: int = 3) -> list[Notification_Model]:
        lst_notification = notification_repo.get_notifications_for_retry(db, max_retry)
        ids = [n.id for n in lst_notification]
    
        if ids:
            notification_repo.increment_retry_count_bulk(
                db,
                ids
            )
    
        return lst_notification
        
    def get_failed_notifications(
        self,
        db: Session
    ) -> list[Notification_Model]:
    
        return notification_repo.get_failed_notifications(db)
    
    def get_pending_notifications(
        self,
        db: Session
    ) -> list[Notification_Model]:
    
        return notification_repo.get_pending_notifications(db)
    
notification_service = NotificationService()