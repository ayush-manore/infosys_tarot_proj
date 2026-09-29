"""
Notification Model (SQLAlchemy)
================================
Stores user notifications including daily guidance,
reading reminders, growth alerts, and platform announcements.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Uuid, JSON, func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Notification content
    type = Column(String(50), nullable=False, index=True)  # 'daily_guidance', 'reading_reminder', 'growth_alert', 'announcement', 'insight_update'
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(String(20), default="normal")  # 'low', 'normal', 'high', 'urgent'

    # Status
    is_read = Column(Boolean, default=False, index=True)
    is_dismissed = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)

    # Extra data
    extra_data = Column(JSON, default=dict)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationship
    user = relationship("User", backref="notifications")

    def __repr__(self):
        return f"<Notification(id='{self.id}', type='{self.type}', read={self.is_read})>"
