"""
Users API Router
================
Endpoints for fetching current user profile, listing users (Admin), and updating user roles.
Includes admin-only endpoints for role management and platform analytics.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from pydantic import BaseModel, Field
from typing import Optional

from app.database import get_db
from app.utils.dependencies import get_current_user, require_role
from app.models.user import User
from app.models.role import Role
from app.models.reading import ReadingSession

router = APIRouter(prefix="/users", tags=["Users"])


# ═══════════════════════════════════════════════════════════════════
# Request Schemas (local to this router)
# ═══════════════════════════════════════════════════════════════════

class UpdateRoleRequest(BaseModel):
    role_name: str = Field(..., description="New role: user, tarot_reader, spiritual_consultant, admin")


# ═══════════════════════════════════════════════════════════════════
# User Self-Service Endpoints
# ═══════════════════════════════════════════════════════════════════

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
                "description": current_user.role.description,
                "permissions": current_user.role.permissions
            },
            "is_verified": current_user.is_verified,
            "login_count": current_user.login_count,
            "last_login_at": current_user.last_login_at,
            "created_at": current_user.created_at
        }
    }


# ═══════════════════════════════════════════════════════════════════
# Admin-Only Endpoints
# ═══════════════════════════════════════════════════════════════════

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
                    "role_description": u.role.description,
                    "permissions": u.role.permissions,
                    "is_active": u.is_active,
                    "is_verified": u.is_verified,
                    "login_count": u.login_count,
                    "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None,
                    "created_at": u.created_at.isoformat() if u.created_at else None,
                } for u in users
            ],
            "skip": skip,
            "limit": limit
        }
    }


@router.patch("/{user_id}/role", dependencies=[Depends(require_role(["admin"]))])
async def update_user_role(
    user_id: str,
    request: UpdateRoleRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    [Admin Only] Update a user's role.
    Available roles: user, tarot_reader, spiritual_consultant, admin
    """
    from uuid import UUID

    allowed_roles = ["user", "tarot_reader", "spiritual_consultant", "admin"]
    if request.role_name not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(allowed_roles)}"
        )

    try:
        uid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Find user
    user_result = await db.execute(
        select(User).options(joinedload(User.role)).where(User.id == uid)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Find target role
    role_result = await db.execute(
        select(Role).where(Role.name == request.role_name)
    )
    new_role = role_result.scalar_one_or_none()
    if not new_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role '{request.role_name}' not found in system"
        )

    old_role = user.role.name
    user.role_id = new_role.id
    await db.commit()

    return {
        "status": "success",
        "message": f"User role updated from '{old_role}' to '{request.role_name}'",
        "data": {
            "user_id": str(user.id),
            "email": user.email,
            "old_role": old_role,
            "new_role": request.role_name,
        }
    }


@router.get("/stats", dependencies=[Depends(require_role(["admin"]))])
async def get_platform_stats(db: AsyncSession = Depends(get_db)):
    """
    [Admin Only] Get platform-wide user and reading statistics.
    """
    # Total users
    user_result = await db.execute(select(User).options(joinedload(User.role)))
    all_users = user_result.scalars().all()

    # Role distribution
    role_counts = {}
    active_count = 0
    verified_count = 0
    for u in all_users:
        role_name = u.role.name if u.role else "unknown"
        role_counts[role_name] = role_counts.get(role_name, 0) + 1
        if u.is_active:
            active_count += 1
        if u.is_verified:
            verified_count += 1

    # Reading stats
    reading_result = await db.execute(select(ReadingSession))
    all_readings = reading_result.scalars().all()

    type_counts = {}
    status_counts = {}
    total_duration = 0
    rated_readings = 0
    total_rating = 0
    for r in all_readings:
        type_counts[r.reading_type] = type_counts.get(r.reading_type, 0) + 1
        status_counts[r.status] = status_counts.get(r.status, 0) + 1
        if r.duration_seconds:
            total_duration += r.duration_seconds
        if r.user_rating:
            rated_readings += 1
            total_rating += r.user_rating

    return {
        "status": "success",
        "data": {
            "users": {
                "total": len(all_users),
                "active": active_count,
                "verified": verified_count,
                "role_distribution": role_counts,
            },
            "readings": {
                "total": len(all_readings),
                "by_type": type_counts,
                "by_status": status_counts,
                "avg_duration_seconds": round(total_duration / len(all_readings), 1) if all_readings else 0,
                "avg_rating": round(total_rating / rated_readings, 2) if rated_readings else None,
                "rated_count": rated_readings,
            },
        }
    }


@router.get("/roles", dependencies=[Depends(require_role(["admin"]))])
async def list_roles(db: AsyncSession = Depends(get_db)):
    """
    [Admin Only] List all system roles with their permissions.
    """
    result = await db.execute(select(Role).order_by(Role.name))
    roles = result.scalars().all()

    return {
        "status": "success",
        "data": [
            {
                "id": str(r.id),
                "name": r.name,
                "description": r.description,
                "permissions": r.permissions,
                "is_active": r.is_active,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            } for r in roles
        ]
    }
