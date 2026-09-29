"""
Notifications API Router
==========================
Endpoints for managing user notifications including daily guidance,
reading reminders, growth alerts, and platform announcements.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.utils.dependencies import get_current_user, require_role
from app.models.user import User
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("")
async def get_notifications(
    unread_only: bool = False,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get notifications for the authenticated user."""
    notifications = await NotificationService.get_user_notifications(
        db, current_user.id, unread_only, skip, limit
    )
    unread_count = await NotificationService.get_unread_count(db, current_user.id)

    return {
        "status": "success",
        "count": len(notifications),
        "unread_count": unread_count,
        "data": notifications,
    }


@router.get("/unread-count")
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get count of unread notifications."""
    count = await NotificationService.get_unread_count(db, current_user.id)
    return {"status": "success", "data": {"unread_count": count}}


@router.post("/daily-guidance")
async def generate_daily_guidance(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate today's daily spiritual guidance notification."""
    notification = await NotificationService.generate_daily_guidance(
        db, current_user.id
    )
    return {"status": "success", "message": "Daily guidance generated", "data": notification}


@router.post("/reading-reminder")
async def generate_reading_reminder(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a reading reminder notification."""
    notification = await NotificationService.generate_reading_reminder(
        db, current_user.id
    )
    return {"status": "success", "message": "Reading reminder created", "data": notification}


@router.post("/growth-alert")
async def generate_growth_alert(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a spiritual growth alert notification."""
    notification = await NotificationService.generate_growth_alert(
        db, current_user.id
    )
    return {"status": "success", "message": "Growth alert created", "data": notification}


@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark a notification as read."""
    try:
        nid = UUID(notification_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notification ID")

    result = await NotificationService.mark_as_read(db, nid, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Notification not found")

    return {"status": "success", "data": result}


@router.put("/mark-all-read")
async def mark_all_read(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark all notifications as read."""
    count = await NotificationService.mark_all_read(db, current_user.id)
    return {"status": "success", "message": f"{count} notifications marked as read"}


@router.delete("/{notification_id}")
async def dismiss_notification(
    notification_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Dismiss (soft-delete) a notification."""
    try:
        nid = UUID(notification_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notification ID")

    success = await NotificationService.dismiss_notification(db, nid, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")

    return {"status": "success", "message": "Notification dismissed"}
