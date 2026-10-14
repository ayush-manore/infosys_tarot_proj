"""
Notifications API Router
==========================
Endpoints for managing user notifications including daily guidance,
reading reminders, growth alerts, and platform announcements.
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.database import get_db
from app.utils.dependencies import get_current_user, require_role
from app.models.user import User
from app.services.notification_service import NotificationService
from app.services import email_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# ── Email request schemas ────────────────────────────────────────────────────

class EmailReminderRequest(BaseModel):
    email: Optional[str] = None          # override; defaults to current user's email
    reading_type: str = "tarot"          # tarot | palm | combined
    custom_message: Optional[str] = None

class DailyGuidanceRequest(BaseModel):
    email: Optional[str] = None
    affirmation: Optional[str] = None
    crystal: Optional[str] = None

class MonthlyReportRequest(BaseModel):
    email: Optional[str] = None
    total_readings: int = 0
    streak_days: int = 0
    top_insight: Optional[str] = None
    growth_score: int = 78
    dominant_element: str = "Fire"


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


# ============================================================================
# Email Notification Endpoints
# ============================================================================

@router.post("/email/reminder")
async def send_reading_reminder_email(
    req: EmailReminderRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """Send a reading reminder email to the current user (or a specified email)."""
    to_email = req.email or current_user.email
    user_name = getattr(current_user, "full_name", None) or current_user.email.split("@")[0].title()

    background_tasks.add_task(
        email_service.send_reading_reminder,
        to_email, user_name, req.reading_type, req.custom_message or ""
    )
    return {
        "status": "success",
        "message": f"Reading reminder email queued for {to_email}",
        "data": {"to": to_email, "type": req.reading_type}
    }


@router.post("/email/daily-guidance")
async def send_daily_guidance_email(
    req: DailyGuidanceRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """Send today's daily spiritual guidance email."""
    to_email = req.email or current_user.email
    user_name = getattr(current_user, "full_name", None) or current_user.email.split("@")[0].title()

    background_tasks.add_task(
        email_service.send_daily_guidance,
        to_email, user_name, req.affirmation or "", req.crystal or ""
    )
    return {
        "status": "success",
        "message": f"Daily guidance email queued for {to_email}",
        "data": {"to": to_email}
    }


@router.post("/email/monthly-report")
async def send_monthly_report_email(
    req: MonthlyReportRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """Send the monthly spiritual journey report email."""
    to_email = req.email or current_user.email
    user_name = getattr(current_user, "full_name", None) or current_user.email.split("@")[0].title()

    stats = {
        "total_readings": req.total_readings,
        "streak_days": req.streak_days,
        "top_insight": req.top_insight or "Your spiritual journey is progressing beautifully",
        "growth_score": req.growth_score,
        "dominant_element": req.dominant_element,
    }

    background_tasks.add_task(
        email_service.send_monthly_report,
        to_email, user_name, stats
    )
    return {
        "status": "success",
        "message": f"Monthly report email queued for {to_email}",
        "data": {"to": to_email, "stats": stats}
    }


@router.post("/email/test")
async def send_test_email(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """Send a test welcome email to verify Gmail SMTP is configured correctly."""
    to_email = current_user.email
    user_name = getattr(current_user, "full_name", None) or current_user.email.split("@")[0].title()

    background_tasks.add_task(
        email_service.send_welcome_email,
        to_email, user_name
    )
    return {
        "status": "success",
        "message": f"Test email queued for {to_email}. Check inbox in ~30 seconds.",
        "data": {"to": to_email}
    }
