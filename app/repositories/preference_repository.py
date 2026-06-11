from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError



from app.models.user_notification_preference import UserNotificationPreference
from app.utils.logger import logger


class UserNotificationPreferenceRepo:

    def _save(self, db: Session, user_pref: UserNotificationPreference) -> None:
        db.commit()
        db.refresh(user_pref)
    
    
    # ============= Create =============
    def create_preference(self, db: Session, user_preference: UserNotificationPreference ) -> UserNotificationPreference:
        try:
            db.add(user_preference)
            self._save(db, user_preference)
            logger.info(f"User preference record created successfully for user_id={user_preference.user_id}")
            return user_preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to create user preference record: {str(ex)}")
            raise

        
    # ============= Get =============

    def get_by_id(self, db: Session, record_id: UUID)-> UserNotificationPreference | None:
        return db.query(UserNotificationPreference).filter(UserNotificationPreference.id == record_id).first()

    def get_by_user_id(self, db: Session, user_id: UUID) -> UserNotificationPreference | None:
        return  db.query(UserNotificationPreference).filter(UserNotificationPreference.user_id == user_id).first()
    
    def get_push_enabled_users(self, db: Session) -> list[UserNotificationPreference]:
        return  db.query(UserNotificationPreference).filter(UserNotificationPreference.push_enabled.is_(True)).all()
    
    def get_email_enabled_users(self, db: Session) -> list[UserNotificationPreference]:
        return  db.query(UserNotificationPreference).filter(UserNotificationPreference.email_enabled.is_(True)).all()

    def get_sms_enabled_users(self, db: Session) -> list[UserNotificationPreference]:
        return  db.query(UserNotificationPreference).filter(UserNotificationPreference.sms_enabled.is_(True)).all()
    
    def get_promotion_enabled_users(self, db: Session) -> list[UserNotificationPreference]:
        return  db.query(UserNotificationPreference).filter(UserNotificationPreference.promotion_enabled.is_(True)).all()
    
    def count_push_enabled_users(self, db: Session) -> int:
        return  db.query(UserNotificationPreference).filter(UserNotificationPreference.push_enabled.is_(True)).count()
    
    def count_email_enabled_users(self, db: Session) -> int:
        return  db.query(UserNotificationPreference).filter(UserNotificationPreference.email_enabled.is_(True)).count()

    def count_sms_enabled_users(self, db: Session) -> int:
        return  db.query(UserNotificationPreference).filter(UserNotificationPreference.sms_enabled.is_(True)).count()
    
    def count_promotion_enabled_users(self, db: Session) -> int:
        return  db.query(UserNotificationPreference).filter(UserNotificationPreference.promotion_enabled.is_(True)).count()
    
    def exists_by_user_id(self, db: Session, user_id: UUID) -> bool:
        return bool(db.query(exists().where(UserNotificationPreference.user_id == user_id)).scalar())

    # ============= Update =============

    def update_push_enabled(self, db: Session, status: bool, record_id: UUID)-> UserNotificationPreference | None:
        try:
            preference = self.get_by_id(db, record_id)
            if not preference:
                return None
            
            if preference.push_enabled == status:
                return preference
            preference.push_enabled = status
            self._save(db, preference)
            logger.info(f"User push notification preference updated successfully for user {preference.user_id}")
            return preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update user push notification preference due {str(ex)}")
            raise

    def update_email_enabled(self, db: Session, status: bool, record_id: UUID)-> UserNotificationPreference | None:
        try:
            preference = self.get_by_id(db, record_id)
            if not preference:
                return None
            
            if preference.email_enabled == status:
                return preference
            preference.email_enabled = status
            self._save(db, preference)
            logger.info(f"User email notification preference updated successfully for user {preference.user_id}")
            return preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update user email notification preference due {str(ex)}")
            raise

    def update_sms_enabled(self, db: Session, status: bool, record_id: UUID)-> UserNotificationPreference | None:
        try:
            preference = self.get_by_id(db, record_id)
            if not preference:
                return None
            
            if preference.sms_enabled == status:
                return preference
            preference.sms_enabled = status
            self._save(db, preference)
            logger.info(f"User sms notification preference updated successfully for user {preference.user_id}")
            return preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update user sms notification preference due {str(ex)}")
            raise

    def update_promotion_enabled(self, db: Session, status: bool, record_id: UUID)-> UserNotificationPreference | None:
        try:
            preference = self.get_by_id(db, record_id)
            if not preference:
                return None
            
            if preference.promotion_enabled == status:
                return preference
            preference.promotion_enabled = status
            self._save(db, preference)
            logger.info(f"User promotional notification preference updated successfully for user {preference.user_id}")
            return preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update user promotion notification preference due {str(ex)}")
            raise

    def update_all_preferences(self, db: Session, email_status: bool, push_status: bool, sms_status: bool, promotion_status: bool, record_id: UUID)-> UserNotificationPreference | None:
        try:
            preference = self.get_by_id(db, record_id)
            if not preference:
                return None
            
            if preference.email_enabled == email_status and preference.push_enabled == push_status and preference.sms_enabled == sms_status and preference.promotion_enabled == promotion_status:
                return preference
            
            preference.email_enabled = email_status
            preference.push_enabled = push_status
            preference.sms_enabled = sms_status
            preference.promotion_enabled = promotion_status
            self._save(db, preference)
            logger.info(f"User all notification preference updated successfully for user {preference.user_id}")
            return preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update user notification preference due {str(ex)}")
            raise
    
    def update_push_enabled_by_user_id( self, db: Session, status: bool, user_id: UUID) -> UserNotificationPreference | None:
    
        try:
            preference = self.get_by_user_id(db, user_id)
            if not preference:
                return None
        
            if preference.push_enabled == status:
                return preference
            preference.push_enabled = status
            self._save(db, preference)
            logger.info(f"User push notification preference updated successfully for user {preference.user_id}")
            return preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update user push notification preference due {str(ex)}")
            raise
    
    def update_email_enabled_by_user_id(self, db: Session, status: bool, user_id: UUID)-> UserNotificationPreference | None:
        try:
            preference = self.get_by_user_id(db, user_id)
            if not preference:
                return None
            
            if preference.email_enabled == status:
                return preference
            preference.email_enabled = status
            self._save(db, preference)
            logger.info(f"User email notification preference updated successfully for user {preference.user_id}")
            return preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update user email notification preference due {str(ex)}")
            raise

    def update_sms_enabled_by_user_id(self, db: Session, status: bool, user_id: UUID)-> UserNotificationPreference | None:
        try:
            preference = self.get_by_user_id(db, user_id)
            if not preference:
                return None
            
            if preference.sms_enabled == status:
                return preference
            preference.sms_enabled = status
            self._save(db, preference)
            logger.info(f"User sms notification preference updated successfully for user {preference.user_id}")
            return preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update user sms notification preference due {str(ex)}")
            raise

    def update_promotion_enabled_by_user_id(self, db: Session, status: bool, user_id: UUID)-> UserNotificationPreference | None:
        try:
            preference = self.get_by_user_id(db, user_id)
            if not preference:
                return None
            
            if preference.promotion_enabled == status:
                return preference
            preference.promotion_enabled = status
            self._save(db, preference)
            logger.info(f"User promotional notification preference updated successfully for user {preference.user_id}")
            return preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update user promotion notification preference due {str(ex)}")
            raise

    def update_all_preferences_by_user_id(self, db: Session, email_status: bool, push_status: bool, sms_status: bool, promotion_status: bool, user_id: UUID)-> UserNotificationPreference | None:
        try:
            preference = self.get_by_user_id(db, user_id)
            if not preference:
                return None
            
            if preference.email_enabled == email_status and preference.push_enabled == push_status and preference.sms_enabled == sms_status and preference.promotion_enabled == promotion_status:
                return preference
            
            preference.email_enabled = email_status
            preference.push_enabled = push_status
            preference.sms_enabled = sms_status
            preference.promotion_enabled = promotion_status
            self._save(db, preference)
            logger.info(f"User all notification preference updated successfully for user {preference.user_id}")
            return preference
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update user notification preference due {str(ex)}")
            raise



    # ============= Delete =============

    def delete_by_id(self, db: Session, record_id: UUID) -> bool:
        try:
            preference = self.get_by_id(db, record_id)
            
            if not preference:
                return False
            db.delete(preference)
            db.commit()
            logger.info(f"User notification preference deleted successfully for {record_id}")
            return True
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to delete notification preference due {str(ex)}")
            raise

    def delete_by_user_id(self, db: Session, user_id: UUID) -> bool:
        try:
            preference = self.get_by_user_id(db, user_id)
            
            if not preference:
                return False
            db.delete(preference)
            db.commit()
            logger.info(f"User notification preference deleted successfully for {user_id}")
            return True
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to delete notification preference due {str(ex)}")
            raise



user_notification_preference_repo = UserNotificationPreferenceRepo()
