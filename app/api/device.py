
# GET    /devices
# GET    /devices/user/{user_id}
# PUT    /devices/{device_id}
# DELETE /devices/{device_id}

from uuid import UUID

from fastapi import ( APIRouter, Depends, HTTPException) # type: ignore[import]
from sqlalchemy.orm import Session


from app.clients.Auth_client import auth_client
from app.schemas.notification import (
    Device_Create,
    Device_Response
)
from app.services.user_device_service import user_device_service
from app.core.database import get_db


router = APIRouter(
    prefix="/devices",
    tags=["Notification_User_Device"]
)


def require_admin(
    is_admin: bool = Depends(auth_client.is_admin)
)-> None:
    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )




@router.post("", response_model=Device_Response, status_code=201)
def create_device(device_data: Device_Create, db:Session = Depends(get_db)):
    return user_device_service.create_device(db, device_data)

@router.get("/{device_id}", response_model=Device_Response)
def get_device(device_id: UUID, db:Session = Depends(get_db)):
    return user_device_service.get_device_by_id(db, device_id)


