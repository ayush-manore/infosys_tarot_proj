"""
User Model (SQLAlchemy)
======================
Core user authentication and identity record.
Supports local email/password auth and OAuth2 (Google).
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, UniqueConstraint, Uuid, func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Nullable for OAuth-only users
    role_id = Column(Uuid, ForeignKey("roles.id"), nullable=False, index=True)

    # OAuth2 Fields
    oauth_provider = Column(String(50), nullable=True)  # e.g., 'google'
    oauth_id = Column(String(255), nullable=True)

    # Status Flags
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    login_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Constraints
    __table_args__ = (
        UniqueConstraint('oauth_provider', 'oauth_id', name='uq_oauth_provider_id'),
    )

    # Relationships
    role = relationship("Role", back_populates="users")
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    reading_sessions = relationship("ReadingSession", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role.name if self.role else None}')>"
