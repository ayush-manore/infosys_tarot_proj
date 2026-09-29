"""
Reports API Router
===================
Endpoints for generating and exporting palmistry, tarot,
personality, and spiritual guidance reports.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.services.report_service import ReportService
from app.services.palm_service import PalmService
from app.services.tarot_service import TarotService
from app.services.interpretation_service import InterpretationService
from app.services.personality_service import PersonalityService
from app.services.trend_service import TrendService
from app.services.recommendation_service import RecommendationService
from app.services.scoring_service import ScoringService
from app.services.reading_service import ReadingService

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/palm")
async def generate_palm_report(
    current_user: User = Depends(get_current_user),
):
    """Generate a comprehensive palmistry analysis report."""
    palm = PalmService.analyze_palm(user_seed=str(current_user.id))
    report = ReportService.generate_palm_report(palm)
    return {"status": "success", "data": report}


@router.get("/tarot")
async def generate_tarot_report(
    spread_type: str = "three_card",
    question: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    """Generate a comprehensive tarot reading report."""
    tarot = TarotService.generate_reading(spread_type, question)
    report = ReportService.generate_tarot_report(tarot)
    return {"status": "success", "data": report}


@router.get("/personality")
async def generate_personality_report(
    current_user: User = Depends(get_current_user),
):
    """Generate a comprehensive personality analysis report."""
    palm = PalmService.analyze_palm(user_seed=str(current_user.id))
    tarot = TarotService.generate_reading("three_card")
    profile = PersonalityService.generate_personality_profile(palm, tarot)
    report = ReportService.generate_personality_report(profile)
    return {"status": "success", "data": report}


@router.get("/spiritual-guidance")
async def generate_spiritual_guidance_report(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a complete spiritual guidance report combining all modules."""
    palm = PalmService.analyze_palm(user_seed=str(current_user.id))
    tarot = TarotService.generate_reading("three_card")

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

    history = await ReadingService.get_reading_history(db, current_user.id)

    scoring = ScoringService.calculate_insight_score(
        palm_analysis=palm,
        tarot_reading=tarot,
        user_context=user_context,
        reading_history=history,
    )

    recommendations = RecommendationService.generate_recommendations(
        palm, tarot, user_context
    )

    trends = TrendService.analyze_life_trends(palm, tarot, history)

    report = ReportService.generate_spiritual_guidance_report(
        palm, tarot, interpretation, scoring, recommendations, trends
    )

    return {"status": "success", "data": report}


@router.get("/export/csv")
async def export_report_csv(
    report_type: str = "palm",
    current_user: User = Depends(get_current_user),
):
    """Export a report as CSV. Types: palm, tarot, personality."""
    palm = PalmService.analyze_palm(user_seed=str(current_user.id))

    if report_type == "palm":
        report = ReportService.generate_palm_report(palm)
    elif report_type == "tarot":
        tarot = TarotService.generate_reading("three_card")
        report = ReportService.generate_tarot_report(tarot)
    elif report_type == "personality":
        tarot = TarotService.generate_reading("three_card")
        profile = PersonalityService.generate_personality_profile(palm, tarot)
        report = ReportService.generate_personality_report(profile)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown report type: {report_type}. Valid: palm, tarot, personality",
        )

    csv_content = ReportService.export_to_csv(report)
    return PlainTextResponse(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{report_type}_report.csv"'
        },
    )


@router.get("/export/json")
async def export_report_json(
    report_type: str = "palm",
    current_user: User = Depends(get_current_user),
):
    """Export a report as formatted JSON. Types: palm, tarot, personality."""
    palm = PalmService.analyze_palm(user_seed=str(current_user.id))

    if report_type == "palm":
        report = ReportService.generate_palm_report(palm)
    elif report_type == "tarot":
        tarot = TarotService.generate_reading("three_card")
        report = ReportService.generate_tarot_report(tarot)
    elif report_type == "personality":
        tarot = TarotService.generate_reading("three_card")
        profile = PersonalityService.generate_personality_profile(palm, tarot)
        report = ReportService.generate_personality_report(profile)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown report type: {report_type}",
        )

    json_content = ReportService.export_to_json(report)
    return PlainTextResponse(
        content=json_content,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="{report_type}_report.json"'
        },
    )


@router.get("/insight-categories")
async def get_insight_categories():
    """Get all available insight categories for interpretation."""
    categories = InterpretationService.get_insight_categories()
    return {"status": "success", "count": len(categories), "data": categories}
