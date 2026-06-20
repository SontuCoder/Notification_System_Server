# POST   /templates
# GET    /templates/{template_id}
# GET    /templates
# PUT    /templates/{template_id}
# DELETE /templates/{template_id}


from uuid import UUID

from fastapi import ( APIRouter, Depends, HTTPException) # type: ignore[import]
from sqlalchemy.orm import Session


from app.clients.Auth_client import auth_client
from app.schemas.notification import (
    Template_Create,
    Template_Response,
    Template_Update
)
from app.services.template_service import template_service
from app.core.database import get_db


router = APIRouter(
    prefix="/templates",
    tags=["Notification_Template"]
)


@router.post("", response_model=Template_Response)
def create_template(template: Template_Create, db: Session = Depends(get_db), is_admin: bool = Depends(auth_client.is_admin())):
    
    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    
    return template_service.create_template(db, template)


@router.get("/{template_id}", response_model=Template_Response)
def

