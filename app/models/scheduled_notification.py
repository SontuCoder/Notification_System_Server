from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy import Boolean, String, DateTime, Enum as SQLEnum, ForeignKey,Index
from uuid import UUID, uuid4
from datetime import datetime
from typing import Any

from app.core.database import Base
from app.schemas.notification import Notification_Channel, Scheduled_Notification_Status


class ScheduledNotification(Base):
    __tablename__ = "scheduled_notifications"
    __table_args__ = (
        Index(
        "idx_scheduled_notifications_status_scheduled_at",
        "status",
        "scheduled_at")
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    channel: Mapped[Notification_Channel] = mapped_column(
        SQLEnum(Notification_Channel),
        nullable=False
    )

    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    target_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    target_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True
    )

    notification_template_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("notification_templates.id"),
        nullable=False
    )

    status: Mapped[Scheduled_Notification_Status] = mapped_column(
        SQLEnum(Scheduled_Notification_Status),
        nullable=False,
        default=Scheduled_Notification_Status.Pending
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
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

    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
