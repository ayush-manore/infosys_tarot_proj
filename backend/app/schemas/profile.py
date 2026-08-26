"""
Profile Pydantic Schemas
========================
Data validation and serialization for User Profiles and Goal Management.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import date, datetime
from uuid import UUID


class GoalItem(BaseModel):
    id: Optional[str] = None
    title: str
    category: str = "personal_growth"  # 'personal_growth', 'spiritual', 'career', 'relationship'
    description: Optional[str] = None
    status: str = "active"             # 'active', 'completed', 'paused'
    target_date: Optional[str] = None
    created_at: Optional[str] = None


class ProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    display_name: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[date] = None
    age_group: Optional[str] = Field(None, description="'18-25', '26-35', '36-45', '46-55', '55+'")
    gender: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = "UTC"
    spiritual_interests: Optional[List[str]] = Field(default_factory=list)
    spiritual_goals: Optional[List[str]] = Field(default_factory=list)
    experience_level: Optional[str] = "beginner"
    preferred_spread: Optional[str] = "three_card"
    preferred_reading_time: Optional[str] = "evening"
    notification_enabled: Optional[bool] = True
    bio: Optional[str] = None


class ProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    age_group: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = "UTC"
    spiritual_interests: List[str] = []
    spiritual_goals: List[str] = []
    experience_level: str = "beginner"
    preferred_spread: str = "three_card"
    preferred_reading_time: str = "evening"
    notification_enabled: bool = True
    current_goals: List[dict] = []
    bio: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
