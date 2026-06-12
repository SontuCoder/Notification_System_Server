# get_template()
# create_template()

# activate_template()
# deactivate_template()

# update_template()

# get_templates_by_channel()






from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.template_repository import (
    notification_template_repo
)
from app.models.template import (
    NotificationTemplate
)

from app.schemas.notification import (
    Notification_Template
)


class TemplateService:


    def create_template(self, db: Session, template_data:Notification_Template)-> NotificationTemplate:

        if notification_template_repo.exists_by_name(db, template_data.name):
            raise HTTPException(status_code=409, detail=f"Template '{template_data.name}' already exists")
        
        new_template = NotificationTemplate(**template_data.model_dump())
        return notification_template_repo.create_template(db, new_template)
