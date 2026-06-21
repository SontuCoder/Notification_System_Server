from uuid import UUID
from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException  #  type: ignore[import]

from app.repositories.template_repository import (
    notification_template_repo
)

from app.models.template import (
    NotificationTemplate
)

from app.schemas.notification import (
    Notification_Template, Notification_Channel
)


class UserDeviceService:
    def 
    
user_device_service = UserDeviceService()