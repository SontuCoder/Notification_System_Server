
# enable_push()
# disable_push()
# enable_email()
# disable_email()
# enable_sms()
# disable_sms()
# enable_promotion()
# disable_promotion()
# update_preferences()



from uuid import UUID
from sqlalchemy.orm import Session

from app.repositories.preference_repo import (
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
    ) -> UserNotificationPreference:
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

    def enable_push(self, db: Session, user_id: UUID)-> None:


