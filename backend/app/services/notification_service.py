"""
Notification & Engagement System
==================================
Manages daily guidance notifications, reading reminders,
insight updates, spiritual growth alerts, and platform announcements.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from uuid import UUID
import random

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.notification import Notification


# ============================================================================
# Notification Templates
# ============================================================================

DAILY_GUIDANCE = [
    "🌟 Your daily energy aligns with introspection. Take a moment to reflect on your path today.",
    "🔮 The cosmos invite you to explore a new tarot spread. Consider a Career or Relationship reading.",
    "✨ Trust your intuition today — it's sharper than usual. Pay attention to recurring thoughts.",
    "🌙 A period of emotional clarity opens. This is an excellent time for a palm analysis session.",
    "🌅 New beginnings are favored today. Set an intention and take one small step toward it.",
    "💫 Your creative energy peaks today. Channel it into expression — art, writing, or meaningful conversation.",
    "🧘 Inner peace is your compass today. Practice mindful breathing between activities.",
    "🌈 Synchronicities are abundant. Stay alert for meaningful coincidences and patterns.",
    "⭐ Your natural charisma shines today. Use it to deepen connections and inspire others.",
    "🕯️ Quiet reflection yields profound insights today. Consider journaling about your spiritual journey.",
]

READING_REMINDERS = [
    "It's been a while since your last reading. The cards may have new wisdom to share.",
    "Your palm lines hold evolving stories. Schedule a new palm analysis to track your growth.",
    "A combined palm and tarot reading could offer deeper insights right now.",
    "Your spiritual journey benefits from regular check-ins. Time for a new reading?",
    "New energy patterns are emerging. A fresh tarot spread could illuminate your path forward.",
]

GROWTH_ALERTS = [
    "📈 Your personality profile shows growth in emotional intelligence. Keep nurturing this strength.",
    "🌱 Life trend analysis indicates an upcoming opportunity window. Stay prepared and open.",
    "💪 Your reading consistency is improving. Regular practice deepens insight quality.",
    "🎯 You're on track with your spiritual goals. Review your progress in the dashboard.",
    "🔄 Patterns in your readings suggest a transformative phase. Embrace the changes ahead.",
]


class NotificationService:
    """Notification and engagement management service."""

    @staticmethod
    async def create_notification(
        db: AsyncSession,
        user_id: UUID,
        notification_type: str,
        title: str,
        message: str,
        priority: str = "normal",
        metadata: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Create a new notification for a user."""
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
            priority=priority,
            extra_data=metadata or {},
        )
        db.add(notification)
        await db.flush()
        await db.refresh(notification)

        return _serialize_notification(notification)

    @staticmethod
    async def get_user_notifications(
        db: AsyncSession,
        user_id: UUID,
        unread_only: bool = False,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Get notifications for a user with optional filtering."""
        query = select(Notification).where(
            Notification.user_id == user_id,
            Notification.is_dismissed == False,
        )

        if unread_only:
            query = query.where(Notification.is_read == False)

        query = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        notifications = result.scalars().all()

        return [_serialize_notification(n) for n in notifications]

    @staticmethod
    async def mark_as_read(
        db: AsyncSession,
        notification_id: UUID,
        user_id: UUID,
    ) -> Optional[Dict[str, Any]]:
        """Mark a notification as read."""
        result = await db.execute(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
        )
        notification = result.scalar_one_or_none()
        if not notification:
            return None

        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)
        await db.commit()

        return _serialize_notification(notification)

    @staticmethod
    async def mark_all_read(db: AsyncSession, user_id: UUID) -> int:
        """Mark all notifications as read for a user."""
        result = await db.execute(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read == False,
            )
        )
        notifications = result.scalars().all()

        for n in notifications:
            n.is_read = True
            n.read_at = datetime.now(timezone.utc)

        await db.commit()
        return len(notifications)

    @staticmethod
    async def dismiss_notification(
        db: AsyncSession,
        notification_id: UUID,
        user_id: UUID,
    ) -> bool:
        """Dismiss (soft-delete) a notification."""
        result = await db.execute(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
        )
        notification = result.scalar_one_or_none()
        if not notification:
            return False

        notification.is_dismissed = True
        await db.commit()
        return True

    @staticmethod
    async def get_unread_count(db: AsyncSession, user_id: UUID) -> int:
        """Get count of unread notifications."""
        result = await db.execute(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read == False,
                Notification.is_dismissed == False,
            )
        )
        return len(result.scalars().all())

    @staticmethod
    async def generate_daily_guidance(
        db: AsyncSession,
        user_id: UUID,
    ) -> Dict[str, Any]:
        """Generate and store a daily guidance notification."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        seed = hash(f"{user_id}-{today}")
        rng = random.Random(seed)

        message = rng.choice(DAILY_GUIDANCE)

        return await NotificationService.create_notification(
            db=db,
            user_id=user_id,
            notification_type="daily_guidance",
            title="Daily Spiritual Guidance",
            message=message,
            priority="normal",
            metadata={"date": today, "type": "daily"},
        )

    @staticmethod
    async def generate_reading_reminder(
        db: AsyncSession,
        user_id: UUID,
    ) -> Dict[str, Any]:
        """Generate a reading reminder notification."""
        rng = random.Random(hash(str(user_id)))
        message = rng.choice(READING_REMINDERS)

        return await NotificationService.create_notification(
            db=db,
            user_id=user_id,
            notification_type="reading_reminder",
            title="Reading Reminder",
            message=message,
            priority="low",
        )

    @staticmethod
    async def generate_growth_alert(
        db: AsyncSession,
        user_id: UUID,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a spiritual growth alert."""
        rng = random.Random(hash(str(user_id) + str(datetime.now(timezone.utc).date())))
        message = context or rng.choice(GROWTH_ALERTS)

        return await NotificationService.create_notification(
            db=db,
            user_id=user_id,
            notification_type="growth_alert",
            title="Spiritual Growth Update",
            message=message,
            priority="normal",
            metadata={"category": "growth"},
        )

    @staticmethod
    async def create_platform_announcement(
        db: AsyncSession,
        user_ids: List[UUID],
        title: str,
        message: str,
    ) -> int:
        """Create a platform announcement for multiple users."""
        count = 0
        for uid in user_ids:
            await NotificationService.create_notification(
                db=db,
                user_id=uid,
                notification_type="announcement",
                title=title,
                message=message,
                priority="high",
            )
            count += 1
        await db.commit()
        return count


def _serialize_notification(notification: Notification) -> Dict[str, Any]:
    """Serialize a notification model to dict."""
    return {
        "id": str(notification.id),
        "type": notification.type,
        "title": notification.title,
        "message": notification.message,
        "priority": notification.priority,
        "is_read": notification.is_read,
        "is_dismissed": notification.is_dismissed,
        "read_at": notification.read_at.isoformat() if notification.read_at else None,
        "created_at": notification.created_at.isoformat() if notification.created_at else None,
        "metadata": notification.extra_data or {},
    }
