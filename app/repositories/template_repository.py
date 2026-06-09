from sqlalchemy.orm import Session
from typing import Any
from uuid import UUID
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError



from app.models.template import NotificationTemplate
from app.schemas.notification import Notification_Channel
from app.utils.logger import logger


class NotificationTemplateRepository:

    def _save(self, db: Session, notification_template: NotificationTemplate) -> None:
        db.commit()
        db.refresh(notification_template)
    
    # ============= Create ==============
    def create_template(self, db: Session, new_template: NotificationTemplate)-> NotificationTemplate:
        try:
            db.add(new_template)
            self._save(db, new_template)
            logger.info(f"New notification template created successfully for new template_id={new_template.id}")
            return new_template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to create notification template: {str(ex)}")
            raise
    
    # ============= Get ==============

    def get_by_id(self, db: Session, record_id: UUID)-> NotificationTemplate | None:
        return db.query(NotificationTemplate).filter(NotificationTemplate.id == record_id).first()

    def get_by_name(self, db: Session, name: str) -> NotificationTemplate | None:
        return  db.query(NotificationTemplate).filter(NotificationTemplate.name == name).first()
    
    def get_by_channel(self, db: Session, channel: Notification_Channel) -> list[NotificationTemplate]:
        return  db.query(NotificationTemplate).filter(NotificationTemplate.channel == channel).all()
    
    def get_active_templates(self, db: Session) -> list[NotificationTemplate]:
        return  db.query(NotificationTemplate).filter(NotificationTemplate.is_active.is_(True)).all()

    def get_all_templates(self, db: Session) -> list[NotificationTemplate]:
        return  db.query(NotificationTemplate).all()
    
    def exists_by_name(self, db: Session, name: str) -> bool:
        return  bool(db.query(exists().where(NotificationTemplate.name == name)).scalar())
    
    def count_active_templates(self, db: Session)-> int:
        return  db.query(NotificationTemplate).filter(NotificationTemplate.is_active.is_(True)).count()
    
    def count_templates_by_channel(self, db: Session, channel: Notification_Channel)-> int:
        return  db.query(NotificationTemplate).filter( NotificationTemplate.channel == channel).count()
    
    def exists_by_id(self, db: Session, temp_id: UUID) -> bool:
        return bool(db.query(exists().where(NotificationTemplate.id == temp_id)).scalar())  

    # ============= Update ==============

    def update_name(self, db:Session, temp_id: UUID, new_name: str)-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if template.name == new_name:
                return template
            template.name = new_name
            self._save(db, template)
            logger.info(f"Template name updated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update template name due {str(ex)}")
            raise

    def update_title(self, db:Session, temp_id: UUID, new_title: str)-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if template.title == new_title:
                return template
            template.title = new_title
            self._save(db, template)
            logger.info(f"Template title updated successfully for template {template.id}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update template title due {str(ex)}")
            raise

    def update_body(self, db:Session, temp_id: UUID, new_body: str)-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if template.body == new_body:
                return template
            template.body = new_body
            self._save(db, template)
            logger.info(f"Template body updated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update template body due {str(ex)}")
            raise

    def update_channel(self, db:Session, temp_id: UUID, new_channel: Notification_Channel)-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if template.channel == new_channel:
                return template
            template.channel = new_channel
            self._save(db, template)
            logger.info(f"Template channel updated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update template channel due {str(ex)}")
            raise

    def update_variables(self, db:Session, temp_id: UUID, new_variable:dict[str, Any])-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if template.variables == new_variable:
                return template
            template.variables = new_variable
            self._save(db, template)
            logger.info(f"Template variables updated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update template variables due {str(ex)}")
            raise

    def activate_template(self, db:Session, temp_id: UUID)-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if template.is_active:
                return template
            template.is_active = True
            self._save(db, template)
            logger.info(f"Template activated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to activate template due {str(ex)}")
            raise

    def deactivate_template(self, db:Session, temp_id: UUID)-> NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            if not template.is_active:
                return template
            template.is_active = False
            self._save(db, template)
            logger.info(f"Template deactivated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to deactivate template due {str(ex)}")
            raise

    def update_template( self, db: Session, temp_id: UUID, title: str | None, body: str, variables: dict[str, Any] | None ) ->NotificationTemplate | None:
        try:
            template = self.get_by_id(db, temp_id)
            if not template:
                return None
            
            if template.title == title and template.body == body and template.variables == variables:
                return template
            template.title = title
            template.body = body
            template.variables = variables
            self._save(db, template)
            logger.info(f"Template updated successfully for template {str(template.id)}")
            return template
        except SQLAlchemyError as ex:
            db.rollback()
            logger.exception(f"Failed to update template due {str(ex)}")
            raise


notification_template_repo = NotificationTemplateRepository()


