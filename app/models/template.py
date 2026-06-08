
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy import Boolean, String, DateTime, Enum as SQLEnum,Text
from uuid import UUID, uuid4
from datetime import datetime
from typing import Any

from app.core.database import Base
from app.schemas.notification import Notification_Channel


class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    channel: Mapped[Notification_Channel] = mapped_column(
        SQLEnum(Notification_Channel),
        nullable=False
    )

    title: Mapped[str|None] = mapped_column(
        Text,
        nullable=True
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    variables: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True
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
