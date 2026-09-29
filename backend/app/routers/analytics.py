"""
Analytics API Router
=====================
Endpoints for user-level and platform-wide analytics,
life trend analysis, personality profiling, and engagement metrics.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.utils.dependencies import get_current_user, require_role
from app.models.user import User
from app.services.analytics_service import AnalyticsService
from app.services.palm_service import PalmService
from app.services.tarot_service import TarotService
from app.services.interpretation_service import InterpretationService
from app.services.personality_service import PersonalityService
from app.services.trend_service import TrendService
from app.services.recommendation_service import RecommendationService
from app.services.scoring_service import ScoringService
from app.services.reading_service import ReadingService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# ═══════════════════════════════════════════════════════════════════
# User Analytics
# ═══════════════════════════════════════════════════════════════════

@router.get("/user")
async def get_user_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get comprehensive reading analytics for the authenticated user."""
    analytics = await AnalyticsService.get_user_analytics(db, current_user.id)
    return {"status": "success", "data": analytics}


@router.get("/engagement")
async def get_engagement_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get user engagement metrics including streak and level."""
    metrics = await AnalyticsService.get_engagement_metrics(db, current_user.id)
    return {"status": "success", "data": metrics}


@router.get("/statistics")
async def get_reading_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed reading statistics with charts-ready data."""
    stats = await AnalyticsService.get_reading_statistics(db, current_user.id)
    return {"status": "success", "data": stats}


# ═══════════════════════════════════════════════════════════════════
# AI Interpretation & Personality
# ═══════════════════════════════════════════════════════════════════

@router.get("/personality")
async def get_personality_profile(
    spread_type: str = "three_card",
    current_user: User = Depends(get_current_user),
):
    """
    Generate a full personality profile from simulated palm analysis.
    Returns Big Five traits, archetype, strengths, weaknesses, and recommendations.
    """
    palm = PalmService.analyze_palm(user_seed=str(current_user.id))
    tarot = TarotService.generate_reading(spread_type)
    profile = PersonalityService.generate_personality_profile(palm, tarot)
    summary = PersonalityService.get_personality_summary(profile)

    return {
        "status": "success",
        "data": {
            "profile": profile,
            "summary": summary,
        },
    }


@router.get("/interpretation")
async def get_combined_interpretation(
    spread_type: str = "three_card",
    question: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    """
    Generate AI-powered combined interpretation from palm + tarot.
    Returns 7-category insights with weighted scoring.
    """
    palm = PalmService.analyze_palm(user_seed=str(current_user.id))
    tarot = TarotService.generate_reading(spread_type, question)

    user_context = None
    if current_user.profile:
        user_context = {
            "spiritual_goals": current_user.profile.spiritual_goals or [],
            "spiritual_interests": current_user.profile.spiritual_interests or [],
            "experience_level": current_user.profile.experience_level or "beginner",
        }

    interpretation = InterpretationService.generate_combined_interpretation(
        palm, tarot, user_context
    )

    return {"status": "success", "data": interpretation}


@router.get("/trends")
async def get_life_trends(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze life trends from current readings and history.
    Returns trend trajectories, opportunities, challenges, and growth assessment.
    """
    palm = PalmService.analyze_palm(user_seed=str(current_user.id))
    tarot = TarotService.generate_reading("three_card")

    # Get reading history
    history = await ReadingService.get_reading_history(db, current_user.id)

    analysis = TrendService.analyze_life_trends(palm, tarot, history)
    summary = TrendService.get_trend_summary(analysis)

    return {
        "status": "success",
        "data": {
            "analysis": analysis,
            "summary": summary,
        },
    }


@router.get("/recommendations")
async def get_recommendations(
    current_user: User = Depends(get_current_user),
):
    """
    Generate personalized recommendations for growth, relationships,
    career, and spiritual development.
    """
    palm = PalmService.analyze_palm(user_seed=str(current_user.id))
    tarot = TarotService.generate_reading("three_card")

    user_context = None
    if current_user.profile:
        user_context = {
            "spiritual_goals": current_user.profile.spiritual_goals or [],
            "spiritual_interests": current_user.profile.spiritual_interests or [],
            "experience_level": current_user.profile.experience_level or "beginner",
        }

    recommendations = RecommendationService.generate_recommendations(
        palm, tarot, user_context
    )

    return {"status": "success", "data": recommendations}


@router.get("/insight-score")
async def get_insight_score(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Calculate the comprehensive 5-factor weighted insight score.
    """
    palm = PalmService.analyze_palm(user_seed=str(current_user.id))
    tarot = TarotService.generate_reading("three_card")
    personality = PersonalityService.generate_personality_profile(palm, tarot)

    user_context = None
    if current_user.profile:
        user_context = {
            "spiritual_goals": current_user.profile.spiritual_goals or [],
            "spiritual_interests": current_user.profile.spiritual_interests or [],
            "experience_level": current_user.profile.experience_level or "beginner",
        }

    history = await ReadingService.get_reading_history(db, current_user.id)

    score = ScoringService.calculate_insight_score(
        palm_analysis=palm,
        tarot_reading=tarot,
        personality_profile=personality,
        user_context=user_context,
        reading_history=history,
    )

    return {"status": "success", "data": score}


# ═══════════════════════════════════════════════════════════════════
# Platform Analytics (Admin only)
# ═══════════════════════════════════════════════════════════════════

@router.get("/platform")
async def get_platform_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """Get platform-wide analytics. Requires admin role."""
    analytics = await AnalyticsService.get_platform_analytics(db)
    return {"status": "success", "data": analytics}


@router.get("/platform/statistics")
async def get_platform_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """Get platform-wide reading statistics. Requires admin role."""
    stats = await AnalyticsService.get_reading_statistics(db)
    return {"status": "success", "data": stats}
