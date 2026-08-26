"""
Users API Router
================
Endpoints for fetching current user profile, listing users (Admin), and updating user roles.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.utils.dependencies import get_current_user, require_role
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get information for the currently authenticated user.
    """
    return {
        "status": "success",
        "data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "role": {
                "id": str(current_user.role.id),
                "name": current_user.role.name,
                "permissions": current_user.role.permissions
            },
            "is_verified": current_user.is_verified,
            "login_count": current_user.login_count,
            "last_login_at": current_user.last_login_at,
            "created_at": current_user.created_at
        }
    }


@router.get("", dependencies=[Depends(require_role(["admin"]))])
async def list_users(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """
    [Admin Only] List all users with pagination.
    """
    result = await db.execute(
        select(User).options(joinedload(User.role)).offset(skip).limit(limit)
    )
    users = result.scalars().all()

    return {
        "status": "success",
        "data": {
            "users": [
                {
                    "id": str(u.id),
                    "email": u.email,
                    "role": u.role.name,
                    "is_active": u.is_active,
                    "created_at": u.created_at
                } for u in users
            ],
            "skip": skip,
            "limit": limit
        }
    }
