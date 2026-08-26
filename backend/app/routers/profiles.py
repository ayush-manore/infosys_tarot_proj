"""
Profiles API Router
===================
Endpoints for viewing & updating user profile, preferences, and goals.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.profile import ProfileUpdate, GoalItem
from app.services.profile_service import ProfileService
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/profiles", tags=["User Profiles"])


@router.get("/me")
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user profile data including spiritual interests and preferences.
    """
    profile = await ProfileService.get_profile_by_user_id(db, current_user.id)
    return {
        "status": "success",
        "data": profile
    }


@router.put("/me")
async def update_my_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update profile details (name, interests, preferences, bio).
    """
    profile = await ProfileService.update_profile(db, current_user.id, data)
    return {
        "status": "success",
        "message": "Profile updated successfully",
        "data": profile
    }


@router.post("/me/goals", status_code=status.HTTP_201_CREATED)
async def add_personal_goal(
    goal: GoalItem,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a new personal/spiritual goal to user profile.
    """
    profile = await ProfileService.add_goal(db, current_user.id, goal)
    return {
        "status": "success",
        "message": "Goal added successfully",
        "data": profile.current_goals
    }
