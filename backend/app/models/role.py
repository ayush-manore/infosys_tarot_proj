"""
Role Model (SQLAlchemy)
======================
Represents system roles for Role-Based Access Control (RBAC).
Roles:
1. user (Default)
2. tarot_reader
3. spiritual_consultant
4. admin
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, Uuid, JSON, func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    permissions = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to User
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(name='{self.name}')>"
