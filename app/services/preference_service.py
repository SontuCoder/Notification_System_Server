from uuid import UUID
from sqlalchemy.orm import Session

from app.repositories.preference_repository import (
    user_notification_preference_repo
)
from app.models.user_notification_preference import (
    UserNotificationPreference
)


class PreferenceService:

    def get_user_preferences(
        self,
        db: Session,
        user_id: UUID
    ) -> UserNotificationPreference | None:
        return user_notification_preference_repo.get_by_user_id(
            db,
            user_id
        )

    def create_default_preferences(
        self,
        db: Session,
        user_id: UUID
    ) -> UserNotificationPreference:
        pref = user_notification_preference_repo.get_by_user_id(
            db,
            user_id
        )

        if pref:
            return pref

        new_preference = UserNotificationPreference(
            user_id=user_id,
            push_enabled=True,
            email_enabled=True,
            sms_enabled=True,
            promotion_enabled=True
        )

        return (
            user_notification_preference_repo
            .create_preference(
                db,
                new_preference
            )
        )

    def enable_push(self, db: Session, user_id: UUID)-> UserNotificationPreference | None:
        return user_notification_preference_repo.update_push_enabled_by_user_id(db, True, user_id)
    
    def disable_push(self, db: Session, user_id: UUID)-> UserNotificationPreference | None:
        return user_notification_preference_repo.update_push_enabled_by_user_id(db, False, user_id)
    
    def enable_email(self, db: Session, user_id: UUID)-> UserNotificationPreference | None:
        return user_notification_preference_repo.update_email_enabled_by_user_id(db, True, user_id)
    
    def disable_email(self, db: Session, user_id: UUID)-> UserNotificationPreference | None:
        return user_notification_preference_repo.update_email_enabled_by_user_id(db, False, user_id)

    def enable_sms(self, db: Session, user_id: UUID)-> UserNotificationPreference | None:
        return user_notification_preference_repo.update_sms_enabled_by_user_id(db, True, user_id)
    
    def disable_sms(self, db: Session, user_id: UUID)-> UserNotificationPreference | None:
        return user_notification_preference_repo.update_sms_enabled_by_user_id(db, False, user_id)
    
    def enable_promotion(self, db: Session, user_id: UUID)-> UserNotificationPreference | None:
        return user_notification_preference_repo.update_promotion_enabled_by_user_id(db, True, user_id)
    
    def disable_promotion(self, db: Session, user_id: UUID)-> UserNotificationPreference | None:
        return user_notification_preference_repo.update_promotion_enabled_by_user_id(db, False, user_id)
    
    def update_preferences(
        self,
        db: Session,
        user_id: UUID,
        email_enabled: bool,
        push_enabled: bool,
        sms_enabled: bool,
        promotion_enabled: bool
    ) -> UserNotificationPreference | None:
    
        return (
            user_notification_preference_repo
            .update_all_preferences_by_user_id(
                db,
                email_enabled,
                push_enabled,
                sms_enabled,
                promotion_enabled,
                user_id
            )
        )