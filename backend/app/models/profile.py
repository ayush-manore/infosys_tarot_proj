"""
User Profile Model (SQLAlchemy)
==============================
Stores user details, spiritual interests, goals, and reading preferences.
"""

from sqlalchemy import Column, String, Text, Date, Boolean, DateTime, ForeignKey, Uuid, JSON, func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    # Personal Data
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    age_group = Column(String(20), nullable=True)  # '18-25', '26-35', '36-45', '46-55', '55+'
    gender = Column(String(20), nullable=True)

    # Location
    country = Column(String(100), nullable=True)
    timezone = Column(String(50), nullable=True, default="UTC")

    # Spiritual Profile & Goals
    spiritual_interests = Column(JSON, default=list)  # ['palmistry', 'tarot', 'astrology']
    spiritual_goals = Column(JSON, default=list)      # ['self_discovery', 'career_guidance']
    experience_level = Column(String(20), default="beginner")

    # Preferences & Customization
    preferred_spread = Column(String(50), default="three_card")
    preferred_reading_time = Column(String(20), default="evening")
    notification_enabled = Column(Boolean, default=True)

    # Personal Goal Objects
    current_goals = Column(JSON, default=list)
    bio = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(user_id='{self.user_id}', display_name='{self.display_name}')>"
