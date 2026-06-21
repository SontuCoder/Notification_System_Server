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


class TemplateService:


    def create_template(self, db: Session, template_data:Notification_Template)-> NotificationTemplate:

        if notification_template_repo.exists_by_name(db, template_data.name):
            raise HTTPException(status_code=409, detail=f"Template '{template_data.name}' already exists")
        
        new_template = NotificationTemplate(**template_data.model_dump())
        return notification_template_repo.create_template(db, new_template)
    
    def get_template(self, db:Session, temp_id: UUID) -> NotificationTemplate | None:
        return notification_template_repo.get_by_id(db, temp_id)
    
    def activate_template(self, db: Session, temp_id: UUID) -> NotificationTemplate | None:
        return notification_template_repo.activate_template(db, temp_id)

    def deactivate_template(self, db: Session, temp_id: UUID) -> NotificationTemplate | None:
        return notification_template_repo.deactivate_template(db, temp_id)
    

    def update_template( self, db: Session, temp_id: UUID, name: str | None, 
                        channel: Notification_Channel | None, 
                        title: str | None, body: str | None, 
                        variables: dict[str, Any] | None) -> NotificationTemplate | None:
        template = notification_template_repo.get_by_id(db, temp_id)
        if not template:
            raise HTTPException(status_code=404, detail=f"Template '{temp_id}' is not exist.")
        
        if name and name != template.name and notification_template_repo.exists_by_name(db, name):
            raise HTTPException(status_code=409, detail=f"Template with this '{name}' already exists.")
        
        return notification_template_repo.update_template(db, temp_id, name if name is not None else template.name,
                                                        channel if channel is not None else template.channel,
                                                        title if title is not None else template.title,
                                                        body if body is not None else template.body,
                                                        variables if variables is not None else template.variables)
    
    def get_templates_by_channel(self, db: Session, channel: Notification_Channel)-> list[NotificationTemplate]:
        return notification_template_repo.get_by_channel(db, channel)
    
    def get_templates(self, db: Session) -> list[NotificationTemplate]:
        return notification_template_repo.get_all_templates(db)

template_service = TemplateService()