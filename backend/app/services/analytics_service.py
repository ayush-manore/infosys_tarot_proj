"""
Analytics Service
==================
Provides user-level and platform-wide analytics for reading sessions,
engagement metrics, satisfaction scores, and system performance.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from collections import Counter
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func as sa_func

from app.models.reading import ReadingSession
from app.models.user import User
from app.models.notification import Notification


class AnalyticsService:
    """Analytics and metrics engine for dashboards."""

    @staticmethod
    async def get_user_analytics(
        db: AsyncSession,
        user_id: UUID,
    ) -> Dict[str, Any]:
        """Get comprehensive analytics for a single user."""
        # Fetch all user readings
        result = await db.execute(
            select(ReadingSession)
            .where(ReadingSession.user_id == user_id)
            .order_by(ReadingSession.created_at.desc())
        )
        readings = result.scalars().all()

        total = len(readings)
        completed = [r for r in readings if r.status == "completed"]
        failed = [r for r in readings if r.status == "failed"]

        # Type distribution
        type_dist = Counter(r.reading_type for r in readings)

        # Spread distribution
        spread_dist = Counter(r.spread_type for r in readings if r.spread_type)

        # Confidence stats
        confidences = [
            float(r.confidence_score) for r in completed if r.confidence_score
        ]
        avg_confidence = sum(confidences) / max(len(confidences), 1)
        max_confidence = max(confidences) if confidences else 0
        min_confidence = min(confidences) if confidences else 0

        # Duration stats
        durations = [r.duration_seconds for r in completed if r.duration_seconds]
        avg_duration = sum(durations) / max(len(durations), 1)

        # Rating stats
        ratings = [r.user_rating for r in completed if r.user_rating]
        avg_rating = sum(ratings) / max(len(ratings), 1)

        # Activity timeline (last 30 days)
        now = datetime.now(timezone.utc)
        thirty_days_ago = now - timedelta(days=30)
        recent = [r for r in readings if r.created_at and r.created_at >= thirty_days_ago]

        # Daily activity count for charts
        daily_activity = Counter()
        for r in recent:
            if r.created_at:
                day = r.created_at.strftime("%Y-%m-%d")
                daily_activity[day] += 1

        return {
            "overview": {
                "total_readings": total,
                "completed_readings": len(completed),
                "failed_readings": len(failed),
                "completion_rate": round(len(completed) / max(total, 1), 4),
            },
            "type_distribution": dict(type_dist),
            "spread_distribution": dict(spread_dist),
            "confidence_metrics": {
                "average": round(avg_confidence, 4),
                "highest": round(max_confidence, 4),
                "lowest": round(min_confidence, 4),
                "total_readings_with_score": len(confidences),
            },
            "performance": {
                "average_duration_seconds": round(avg_duration, 1),
                "average_user_rating": round(avg_rating, 2) if ratings else None,
                "ratings_submitted": len(ratings),
            },
            "activity": {
                "readings_last_30_days": len(recent),
                "daily_activity": dict(sorted(daily_activity.items())),
            },
            "engagement": {
                "level": (
                    "highly_engaged" if total >= 20 else
                    "engaged" if total >= 10 else
                    "active" if total >= 5 else
                    "new"
                ),
                "total_feedback_given": len(ratings),
            },
        }

    @staticmethod
    async def get_platform_analytics(db: AsyncSession) -> Dict[str, Any]:
        """Get platform-wide analytics (admin only)."""
        # Total users
        user_result = await db.execute(select(sa_func.count(User.id)))
        total_users = user_result.scalar() or 0

        # Active users (logged in within 30 days)
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        active_result = await db.execute(
            select(sa_func.count(User.id)).where(
                User.last_login_at >= thirty_days_ago
            )
        )
        active_users = active_result.scalar() or 0

        # Total readings
        reading_result = await db.execute(select(sa_func.count(ReadingSession.id)))
        total_readings = reading_result.scalar() or 0

        # Completed readings
        completed_result = await db.execute(
            select(sa_func.count(ReadingSession.id)).where(
                ReadingSession.status == "completed"
            )
        )
        completed_readings = completed_result.scalar() or 0

        # All readings for type distribution
        all_readings_result = await db.execute(select(ReadingSession))
        all_readings = all_readings_result.scalars().all()

        type_dist = Counter(r.reading_type for r in all_readings)
        spread_dist = Counter(r.spread_type for r in all_readings if r.spread_type)

        # Average confidence
        confidences = [
            float(r.confidence_score)
            for r in all_readings
            if r.confidence_score and r.status == "completed"
        ]
        avg_confidence = sum(confidences) / max(len(confidences), 1)

        # Average rating
        ratings = [r.user_rating for r in all_readings if r.user_rating]
        avg_rating = sum(ratings) / max(len(ratings), 1) if ratings else None

        # Readings per day (last 30 days)
        recent_readings = [
            r for r in all_readings
            if r.created_at and r.created_at >= thirty_days_ago
        ]
        daily_readings = Counter()
        for r in recent_readings:
            if r.created_at:
                day = r.created_at.strftime("%Y-%m-%d")
                daily_readings[day] += 1

        return {
            "users": {
                "total": total_users,
                "active_30d": active_users,
                "retention_rate": round(active_users / max(total_users, 1), 4),
            },
            "readings": {
                "total": total_readings,
                "completed": completed_readings,
                "completion_rate": round(completed_readings / max(total_readings, 1), 4),
                "type_distribution": dict(type_dist),
                "spread_distribution": dict(spread_dist),
            },
            "quality": {
                "average_confidence": round(avg_confidence, 4),
                "average_rating": round(avg_rating, 2) if avg_rating else None,
                "feedback_count": len(ratings),
            },
            "activity": {
                "readings_last_30_days": len(recent_readings),
                "daily_readings": dict(sorted(daily_readings.items())),
                "avg_daily_readings": round(len(recent_readings) / 30, 2),
            },
            "system": {
                "platform_health": "healthy",
                "database": "operational",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        }

    @staticmethod
    async def get_reading_statistics(
        db: AsyncSession,
        user_id: Optional[UUID] = None,
    ) -> Dict[str, Any]:
        """Get detailed reading statistics with charts-ready data."""
        query = select(ReadingSession)
        if user_id:
            query = query.where(ReadingSession.user_id == user_id)
        query = query.order_by(ReadingSession.created_at.desc())

        result = await db.execute(query)
        readings = result.scalars().all()

        # Build chart data
        confidence_over_time = []
        for r in readings:
            if r.confidence_score and r.created_at:
                confidence_over_time.append({
                    "date": r.created_at.strftime("%Y-%m-%d"),
                    "confidence": float(r.confidence_score),
                    "type": r.reading_type,
                })

        # Rating distribution
        rating_dist = Counter(r.user_rating for r in readings if r.user_rating)

        # Weekly trend
        now = datetime.now(timezone.utc)
        weekly_data = {}
        for i in range(4):
            week_start = now - timedelta(weeks=i + 1)
            week_end = now - timedelta(weeks=i)
            week_readings = [
                r for r in readings
                if r.created_at and week_start <= r.created_at <= week_end
            ]
            weekly_data[f"week_{i + 1}"] = {
                "count": len(week_readings),
                "period": f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d')}",
            }

        return {
            "total_readings": len(readings),
            "confidence_timeline": confidence_over_time[:50],
            "rating_distribution": dict(rating_dist),
            "weekly_trend": weekly_data,
        }

    @staticmethod
    async def get_engagement_metrics(
        db: AsyncSession,
        user_id: UUID,
    ) -> Dict[str, Any]:
        """Get user engagement metrics."""
        # Readings
        result = await db.execute(
            select(ReadingSession).where(ReadingSession.user_id == user_id)
        )
        readings = result.scalars().all()

        # Notifications
        notif_result = await db.execute(
            select(Notification).where(Notification.user_id == user_id)
        )
        notifications = notif_result.scalars().all()

        read_notifs = sum(1 for n in notifications if n.is_read)

        # Calculate engagement score
        reading_score = min(100, len(readings) * 5)
        feedback_score = min(100, sum(1 for r in readings if r.user_rating) * 10)
        notif_engagement = (
            round(read_notifs / max(len(notifications), 1) * 100, 1)
            if notifications else 0
        )

        engagement_score = int(
            reading_score * 0.4 + feedback_score * 0.3 + notif_engagement * 0.3
        )

        return {
            "engagement_score": engagement_score,
            "total_readings": len(readings),
            "feedback_given": sum(1 for r in readings if r.user_rating),
            "notification_engagement": notif_engagement,
            "reading_streak": _calculate_streak(readings),
            "level": (
                "Champion" if engagement_score >= 80 else
                "Dedicated" if engagement_score >= 60 else
                "Regular" if engagement_score >= 40 else
                "Newcomer"
            ),
        }


def _calculate_streak(readings: list) -> int:
    """Calculate current reading streak (consecutive days with readings)."""
    if not readings:
        return 0

    dates = set()
    for r in readings:
        if r.created_at:
            dates.add(r.created_at.date())

    if not dates:
        return 0

    today = datetime.now(timezone.utc).date()
    streak = 0
    current = today

    while current in dates:
        streak += 1
        current -= timedelta(days=1)

    return streak
