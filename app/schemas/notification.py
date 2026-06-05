from pydantic import BaseModel, Field
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
    id: UUID
    name: str
    channel: Notification_Channel
    title: Optional[str] = None
    body: str
    variables: Optional[Dict[str, Any]] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User_Device(BaseModel): # for only Ph, Tab, not for web
    id: UUID
    user_id: UUID
    device_token: str
    platform: Device_Platform
    notification_enabled: bool = True
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class User_Notification_Preferences(BaseModel):
    id: UUID
    user_id: UUID
    push_enabled: bool = True
    email_enabled: bool = True
    sms_enabled: bool = True
    promotion_enabled: bool = True


class Scheduled_Notification(BaseModel):
    id: UUID
    channel: Notification_Channel
    scheduled_at: datetime
    target_type: str
    target_data: Optional[Dict[str, Any]] = None
    notification_template_id: UUID
    status: Scheduled_Notification_Status = Scheduled_Notification_Status.Pending
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None

class Notification(BaseModel):
    id: UUID
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
    failure_reason: Optional[str] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)






