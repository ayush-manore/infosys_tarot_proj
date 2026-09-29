"""
Reading Session Model (SQLAlchemy)
=================================
Tracks palm and tarot reading sessions for users.
Acts as a relational link to detailed MongoDB document stores.
"""

from sqlalchemy import Column, String, Text, Integer, Numeric, DateTime, ForeignKey, Uuid, func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class ReadingSession(Base):
    __tablename__ = "reading_sessions"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Session Metadata
    reading_type = Column(String(20), nullable=False)  # 'palm', 'tarot', 'combined'
    spread_type = Column(String(50), nullable=True)    # 'single', 'three_card', etc.
    status = Column(String(20), default="initiated")   # 'initiated', 'processing', 'completed', 'failed'

    # Mongo Document References
    analysis_ref = Column(String(100), nullable=True)
    interpretation_ref = Column(String(100), nullable=True)

    # Performance & Feedback
    duration_seconds = Column(Integer, nullable=True)
    confidence_score = Column(Numeric(5, 4), nullable=True)
    user_rating = Column(Integer, nullable=True)
    user_feedback = Column(Text, nullable=True)

    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationship
    user = relationship("User", back_populates="reading_sessions")

    def __repr__(self):
        return f"<ReadingSession(id='{self.id}', type='{self.reading_type}', status='{self.status}')>"
