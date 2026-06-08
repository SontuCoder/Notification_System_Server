from sqlalchemy.orm import Session
from sqlalchemy import exists
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError



from app.models.user_device import UserDevice
from app.utils.logger import logger
from app.schemas.notification import Device_Platform


class UserDeviceRepository:

    def _save(self, db: Session, device: UserDevice) -> None:
        db.commit()
        db.refresh(device)

    # ================= Create =================
    # Create a new device record
    def create_device_record(self, db: Session, user_device: UserDevice) -> UserDevice:

        try:
            db.add(user_device) 
            self._save(db, user_device)
            logger.info(f"Creating device record for user_id={user_device.user_id}")
            return user_device
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to create device record: {str(ex)}")
            raise
    
    # ================= Get =================
    # Get device by record ID
    def get_by_id(self, db: Session, record_id: UUID) -> UserDevice | None:
        return db.query(UserDevice).filter(UserDevice.id == record_id).first()
    
    # Get device by user ID
    def get_by_user_id(self, db: Session, user_id: UUID) -> list[UserDevice]:
        return db.query(UserDevice).filter(UserDevice.user_id == user_id).all()
    
    # Get device by device token
    def get_by_device_token(self, db: Session, device_token: str) -> UserDevice | None:
        return db.query(UserDevice).filter(UserDevice.device_token == device_token).first()
    
    # Get_active_devices_by_user_id
    def get_active_devices_by_user_id(self, db: Session, user_id: UUID) -> list[UserDevice]:
        return db.query(UserDevice).filter(UserDevice.user_id == user_id, UserDevice.is_active.is_(True)).all()
    
    # Check whether a device token exists
    def exists_by_device_token(self, db: Session, device_token: str) -> bool:
        return bool(db.query(exists().where(UserDevice.device_token == device_token)).scalar())
    
    def get_devices_for_users( self, db: Session, user_ids: list[UUID]) -> list[UserDevice]:
    
        return (
            db.query(UserDevice)
            .filter(
                UserDevice.user_id.in_(user_ids),
                UserDevice.is_active.is_(True),
                UserDevice.notifications_enabled.is_(True)
            ).all()
        )

    def get_inactive_devices(self, db: Session) -> list[UserDevice]:
        return (
            db.query(UserDevice).filter(UserDevice.is_active.is_(False)).all()
        )

    def get_all_push_enabled_devices(self, db: Session) -> list[UserDevice]:
        return(
            db.query(UserDevice).filter(
                UserDevice.notifications_enabled.is_(True),
                UserDevice.is_active.is_(True)
            ).all()
        ) 


    # ================= Update =================
    def update_device_token(self, db: Session, record_id: UUID, new_device_token: str) -> UserDevice | None:
        try:
            device = self.get_by_id(db,record_id)

            if not device:
                return None
            if device.device_token == new_device_token:
                return device
            
            device.device_token = new_device_token
            self._save(db, device)
            logger.info(f"Device token details successfully updated for {device.id}")
            return device
            
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update device token due {str(ex)}")
            raise

    def update_notification_device_status(self, db: Session, record_id: UUID, status: bool) -> UserDevice | None:
        try:
            device = self.get_by_id(db,record_id)
            if not device:
                return None
            
            if device.notifications_enabled == status:
                return device
            
            device.notifications_enabled = status
            self._save(db, device)
            logger.info(f"Notification status changed successfully updated for {device.id}")
            return device
            
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update notification status due {str(ex)}")
            raise

    def update_device_status(self, db: Session, record_id: UUID, enabled: bool) -> UserDevice | None:
        try:
            device = self.get_by_id(db,record_id)
            if not device:
                return None
            
            if device.is_active == enabled:
                return device
            
            device.is_active = enabled
            self._save(db, device)
            logger.info(f"Device status changed successfully updated for {device.id}")
            return device
            
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update device status due {str(ex)}")
            raise

    def update_device_platform(self, db: Session, record_id: UUID, new_platform: Device_Platform) -> UserDevice | None:
        try:
            device = self.get_by_id(db,record_id)
            if not device:
                return None
            
            if device.platform == new_platform:
                return device
            
            device.platform = new_platform
            self._save(db, device)
            logger.info(f"Device platform changed successfully updated for {device.id}")
            return device
            
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update device platform due {str(ex)}")
            raise
    

    def bulk_deactivate_devices_by_tokens(self, db: Session, device_tokens: list[str] ) -> int:
        try:
            devices = db.query(UserDevice).filter(UserDevice.device_token.in_(device_tokens)).update({"is_active": False},synchronize_session=False)
            db.commit()
            logger.info(f"Total {devices} devices deactivated successfully")
            return devices
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to deactivate devices due {str(ex)}")
            raise
    

    # ================= Delete =================
    def delete_device_by_id(self, db: Session, record_id: UUID) -> bool:
        try:
            device = self.get_by_id(db, record_id)
            
            if not device:
                return False
            db.delete(device)
            db.commit()
            logger.info(f"User device deleted successfully for {record_id}")
            return True
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to delete device due {str(ex)}")
            raise

    def delete_device_by_device_token(self, db: Session, device_token: str) -> bool:
        try:
            device = self.get_by_device_token(db, device_token)
            
            if not device:
                return False
            db.delete(device)
            db.commit()
            logger.info(f"User device deleted successfully for {device.id}")
            return True
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to delete device due {str(ex)}")
            raise




# get_by_user_id_and_platform()
# count_active_devices()
# exists_by_user_id_and_platform()


user_device_repo = UserDeviceRepository()