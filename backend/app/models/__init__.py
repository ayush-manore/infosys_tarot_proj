"""
SQLAlchemy Models Package
========================
Export all models for easy imports and Alembic autogenerate discovery.
"""

from app.database import Base
from app.models.role import Role
from app.models.user import User
from app.models.profile import UserProfile
from app.models.reading import ReadingSession
from app.models.notification import Notification

__all__ = ["Base", "Role", "User", "UserProfile", "ReadingSession", "Notification"]
