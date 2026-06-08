from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Text, Integer
from uuid import UUID, uuid4
from datetime import datetime

from app.core.database import Base
from app.schemas.notification import Notification_Channel, Notification_Status, Notification_Category, Notification_Priority


class Notification(Base):
    __tablename__ = "notifications"
    

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False
    )

    channel: Mapped[Notification_Channel] = mapped_column(
        SQLEnum(Notification_Channel),
        nullable=False
    )

    notification_template_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("notification_templates.id"),
        nullable=True
    )

    scheduled_notification_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("scheduled_notifications.id"),
        nullable=True
    )

    title: Mapped[str|None] = mapped_column(
        Text,
        nullable=True
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[Notification_Status] = mapped_column(
        SQLEnum(Notification_Status),
        nullable=False,
        default=Notification_Status.Pending
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    category: Mapped[Notification_Category] = mapped_column(
        SQLEnum(Notification_Category),
        nullable=False
    )

    priority: Mapped[Notification_Priority] = mapped_column(
        SQLEnum(Notification_Priority),
        nullable=False,
        default=Notification_Priority.Medium
    )

    failure_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    delivered_at: Mapped[datetime|None] = mapped_column(
        DateTime,
        nullable= True
    )    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


