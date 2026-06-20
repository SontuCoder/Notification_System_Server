from uuid import UUID

from fastapi import ( APIRouter, Depends, HTTPException) # type: ignore[import]
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.notification_service import (
    notification_service
)
from app.schemas.notification import (
    Notification_Create,
    Notification_Response
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.post(
    "",
    response_model=Notification_Response
)
def create_notification(
    notification: Notification_Create,
    db: Session = Depends(get_db)
):

    return notification_service.create_notification(
        db,
        notification
    )


@router.get(
    "/{notification_id}",
    response_model=Notification_Response
)
def get_notification(
    notification_id: UUID,
    db: Session = Depends(get_db)
):

    notification = (
        notification_service.get_notification(
            db,
            notification_id
        )
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return notification


@router.get(
    "/user/{user_id}",
    response_model=list[Notification_Response]
)
def get_user_notifications(
    user_id: UUID,
    db: Session = Depends(get_db)
):

    return (
        notification_service
        .get_user_notifications(
            db,
            user_id
        )
    )