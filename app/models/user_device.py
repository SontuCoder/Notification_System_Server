from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String, Boolean, DateTime, Index, Text
from uuid import UUID, uuid4
from datetime import datetime

from app.core.database import Base
from app.schemas.notification import DevicePlatform


class UserDevice(Base):

    __tablename__ = "user_devices"

    __table_args__ = (
        Index("idx_user_devices_user_id", "user_id")
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False
    )

    device_token: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    platform: Mapped[DevicePlatform] = mapped_column(
        String(20),
        nullable=False
    )

    notifications_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
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

