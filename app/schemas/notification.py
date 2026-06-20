from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from enum import Enum
from uuid import UUID
from datetime import datetime


# ========================================
# ========== Define Data stucture ========
# ========================================

class Notification_Status(str, Enum):
    Pending = "pending"
    Queued = "queued"
    Sent = "sent"
    Delivered = "delivered"
    Failed = "failed"

class NotificationTargetType(str, Enum):
    User = "user"
    Users = "users"
    AllUsers = "all_users"

class Notification_Priority(str, Enum):
    Low = "low"
    Medium = "medium"
    High = "high"
    Critical = "critical"

class Notification_Channel(str, Enum):
    SMS = "sms"
    Email = "email"
    Push = "push"

class Scheduled_Notification_Status(str, Enum):
    Pending = "pending"
    Sent = "sent"
    Cancelled = "cancelled"
    Failed = "failed"

class Notification_Category(str, Enum):
    OTP = "otp"
    Security = "security"
    Order = "order"
    Payment = "payment"
    Promotion = "promotion"
    System = "system"


class Device_Platform(str, Enum):
    Android = "android"
    IOS = "ios"
    Web = "web"


# ========================================
# ========== Tables ======================
# ========================================
class Notification_Template(BaseModel):
    name: str
    channel: Notification_Channel
    title: Optional[str] = None
    body: str
    variables: Optional[Dict[str, Any]] = None
    is_active: bool = True

class User_Device(BaseModel): # for only Ph, Tab, not for web
    user_id: UUID
    device_token: str
    platform: Device_Platform
    notification_enabled: bool = True
    is_active: bool = True


class User_Notification_Preferences(BaseModel):
    user_id: UUID
    push_enabled: bool = True
    email_enabled: bool = True
    sms_enabled: bool = True
    promotion_enabled: bool = True


class Scheduled_Notification(BaseModel):
    channel: Notification_Channel
    scheduled_at: datetime
    target_type: NotificationTargetType = NotificationTargetType.AllUsers
    target_data: Optional[Dict[str, Any]] = None
    notification_template_id: UUID
    status: Scheduled_Notification_Status = Scheduled_Notification_Status.Pending
    category: Notification_Category = Notification_Category.Promotion
    is_active: bool = True

class Notification(BaseModel):
    user_id: UUID
    channel: Notification_Channel
    notification_template_id: Optional[UUID] = None
    scheduled_notification_id: Optional[UUID] = None
    title: Optional[str] = None
    body: str
    status: Notification_Status = Notification_Status.Pending
    retry_count: int = 0
    category: Notification_Category
    priority: Notification_Priority = Notification_Priority.Medium

class Notification_Create(BaseModel):
    user_id: UUID
    channel: Notification_Channel
    category: Notification_Category
    title: str | None = None
    body: str
    priority: Notification_Priority = (
        Notification_Priority.Medium
    )
    notification_template_id: UUID | None = None
    scheduled_notification_id: UUID | None = None


class Notification_Response(BaseModel):
    id: UUID
    user_id: UUID
    channel: Notification_Channel
    category: Notification_Category
    status: Notification_Status
    priority: Notification_Priority
    title: str | None
    body: str
    retry_count: int
    failure_reason: str | None
    notification_template_id: UUID | None
    scheduled_notification_id: UUID | None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class Template_Create(BaseModel):
    name: str
    channel: Notification_Channel
    title: Optional[str] | None
    body: str
    variables: Optional[Dict[str, Any]] | None


class Template_Response(BaseModel):
    id: UUID
    name: str
    channel: Notification_Channel
    title: str | None
    body: str
    variables: dict[str, Any] | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class Template_Update(BaseModel):
    name: str | None = None
    channel: Notification_Channel | None = None
    title: str | None = None
    body: str | None = None
    variables: dict[str, Any] | None = None
    is_active: bool | None = None

