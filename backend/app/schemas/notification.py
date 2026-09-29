"""
Notification Pydantic Schemas
==============================
Request and response schemas for the notification system.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class NotificationCreate(BaseModel):
    """Create a new notification."""
    type: str = Field(..., description="Notification type: daily_guidance, reading_reminder, growth_alert, announcement")
    title: str = Field(..., max_length=255)
    message: str
    priority: str = Field("normal", description="Priority: low, normal, high, urgent")
    metadata: Optional[Dict[str, Any]] = None


class NotificationResponse(BaseModel):
    """Single notification response."""
    id: str
    type: str
    title: str
    message: str
    priority: str
    is_read: bool
    is_dismissed: bool
    read_at: Optional[str] = None
    created_at: Optional[str] = None
    metadata: Dict[str, Any] = {}


class NotificationListResponse(BaseModel):
    """Response for notification list endpoints."""
    status: str = "success"
    count: int
    unread_count: int = 0
    data: List[NotificationResponse] = []


class AnnouncementRequest(BaseModel):
    """Request to create a platform announcement."""
    title: str = Field(..., max_length=255)
    message: str = Field(..., max_length=2000)
