"""
Profile Service
================
Business logic for managing user profiles, preferences, and personal goals.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
import uuid

from app.models.profile import UserProfile
from app.schemas.profile import ProfileUpdate, GoalItem


class ProfileService:
    @staticmethod
    async def get_profile_by_user_id(db: AsyncSession, user_id: uuid.UUID) -> UserProfile:
        """Fetch profile for a specific user ID or create default if missing."""
        result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            profile = UserProfile(
                user_id=user_id,
                spiritual_interests=["palmistry", "tarot"],
                spiritual_goals=["self_discovery"]
            )
            db.add(profile)
            await db.commit()
            await db.refresh(profile)

        return profile

    @staticmethod
    async def update_profile(db: AsyncSession, user_id: uuid.UUID, data: ProfileUpdate) -> UserProfile:
        """Update user profile fields."""
        profile = await ProfileService.get_profile_by_user_id(db, user_id)

        update_dict = data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            if value is not None:
                setattr(profile, key, value)

        await db.commit()
        await db.refresh(profile)
        return profile

    @staticmethod
    async def add_goal(db: AsyncSession, user_id: uuid.UUID, goal_data: GoalItem) -> UserProfile:
        """Add a new personal goal to user profile."""
        profile = await ProfileService.get_profile_by_user_id(db, user_id)

        goals = list(profile.current_goals or [])
        new_goal = goal_data.model_dump()
        new_goal["id"] = str(uuid.uuid4())
        new_goal["created_at"] = datetime.utcnow().isoformat()
        goals.append(new_goal)

        profile.current_goals = goals
        await db.commit()
        await db.refresh(profile)
        return profile
