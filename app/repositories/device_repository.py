from sqlalchemy.orm import Session
from sqlalchemy import exists
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError



from app.models.user_device import UserDevice
from app.utils.logger import logger

class UserDeviceRepository:

    # ================= Create =================
    # Create a new device record
    def create_device_record(self, db: Session, user_device: UserDevice) -> UserDevice:

        try:
            db.add(user_device) 
            db.commit()
            db.refresh(user_device)
            logger.info(f"Creating device record for user_id={user_device.user_id}")
            return user_device
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to create device record: {str(ex)}")
            raise
    
    # ================= Get =================
    # Get device by record ID
    def get_by_id(self, db: Session, record_id:UUID) -> UserDevice | None:
        return db.query(UserDevice).filter(UserDevice.id == record_id).first()
    
    # Get device by user ID
    def get_by_user_id(self, db: Session, user_id:UUID) -> list[UserDevice]:
        return db.query(UserDevice).filter(UserDevice.user_id == user_id).all()
    
    # Get device by device token
    def get_by_device_token(self, db: Session, device_token:str) -> UserDevice | None:
        return db.query(UserDevice).filter(UserDevice.device_token == device_token).first()
    
    # Get_active_devices_by_user_id
    def get_active_devices_by_user_id(self, db: Session, user_id:UUID) -> list[UserDevice]:
        return db.query(UserDevice).filter(UserDevice.user_id == user_id, UserDevice.is_active == True).all()
    
    # Check whether a device token exists
    def exists_by_device_token(self, db: Session, device_token:str) -> bool:
        return db.query(exists().where(UserDevice.device_token == device_token)).scalar()
    

    # ================= Update =================
    def update_device_token(self, db: Session, record_id: UUID, new_device_token: str) -> UserDevice | None:
        try:
            device = self.get_by_id(db,record_id)

            if not device:
                return None
            
            device.device_token = new_device_token
            db.commit()
            db.refresh(device)
            logger.info(f"Device token details successfully updated for {device.id}")
            return device
            
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update device token for {device.id}")
            raise






# │
# ├── update_notification_status()
# │     Enable/Disable notifications for a device
# │
# ├── activate_device()
# │     Set is_active = True
# │
# ├── deactivate_device()
# │     Set is_active = False
# │
# ├── update_platform()
# │     Update device platform (android/ios/web)
# │
# ├── delete_by_id()
# │     Delete device by record ID
# │
# ├── delete_by_device_token()
# │     Delete device by token
# │
# ├── get_all_push_enabled_devices()
# │     Get all devices where:
# │         notifications_enabled = True
# │         is_active = True
# │
# ├── get_devices_for_users()
# │     Get devices for multiple users
# │
# ├── get_inactive_devices()
# │     Get all inactive devices
# │
# └── bulk_deactivate_invalid_tokens()
#       Mark invalid tokens as inactive
