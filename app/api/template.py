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

def require_admin(
    is_admin: bool = Depends(auth_client.is_admin)
)-> None:
    if not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

@router.get("", response_model=list[Template_Response])
def get_templates(db: Session = Depends(get_db), _: None = Depends(require_admin)):
    return template_service.get_templates(db)

@router.post("", response_model=Template_Response, status_code=201)
def create_template(template: Template_Create, db: Session = Depends(get_db),  _: None = Depends(require_admin)):

    return template_service.create_template(db, template)

@router.get("/{template_id}", response_model=Template_Response)
def get_template(template_id: UUID, db: Session = Depends(get_db)):
    template = template_service.get_template(db, template_id)

    if not template:
        raise HTTPException(
            status_code=404,
            detail="Notification template not found"
        )
    
    return template

@router.put("/{template_id}", response_model=Template_Response)
def update_template(template_id: UUID, template_data: Template_Update, db: Session = Depends(get_db),  _: None = Depends(require_admin)):
    template = template_service.update_template(db, template_id, template_data.name, 
                                                template_data.channel, template_data.title,
                                                template_data.body, template_data.variables)
    
    if not template:
        raise HTTPException(
            status_code=404,
            detail="Notification template not found"
        )
    
    return template

@router.delete("/{template_id}", response_model=Template_Response, status_code=200)
def delete_template(template_id: UUID, db: Session = Depends(get_db),  _: None = Depends(require_admin)):

    template = template_service.deactivate_template(db, template_id)
    
    if not template:
        raise HTTPException(
            status_code=404,
            detail="Notification template not found"
        )
    
    return template

@router.patch("/{template_id}/activate", response_model=Template_Response)
def activate_template(
    template_id: UUID,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin)
):
    template = template_service.activate_template(db, template_id)
    
    if not template:
        raise HTTPException(
            status_code=404,
            detail="Notification template not found"
        )
    
    return template


