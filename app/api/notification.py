from uuid import UUID

from fastapi import ( APIRouter, Depends, HTTPException, Query) # type: ignore[import]
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.notification_service import (
    notification_service
)
from app.schemas.notification import (
    Notification_Create,
    Notification_Response,
    Notification_Channel,
    Notification_Status,
)
from app.clients.Auth_client import auth_client

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

def require_admin(
    is_admin: bool = Depends(auth_client.is_admin)
)-> None:
    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


@router.post(
    "",
    response_model=Notification_Response,
    status_code=201
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

@router.get(
    "",
    response_model=list[Notification_Response]
)
def get_notifications(
    user_id: UUID | None = None,
    status: Notification_Status | None = None,
    channel: Notification_Channel | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: None = Depends(require_admin)
):
    return notification_service.get_notifications(
        db=db,
        user_id=user_id,
        status=status,
        channel=channel,
        skip=skip,
        limit=limit
    )