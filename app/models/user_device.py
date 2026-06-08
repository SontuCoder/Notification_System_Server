from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4

from app.core.database import Base

class UserDevice(Base):
    __tablename__ = "user_devices"

    id : Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),

    )
    device_token
    platform
    notifications_enabled
    is_active
    created_at
    updated_at