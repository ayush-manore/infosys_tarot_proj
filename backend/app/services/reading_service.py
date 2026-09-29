"""
Reading Session Orchestrator Service
=====================================
Coordinates tarot readings, palm analyses, and combined readings.
Manages ReadingSession database records and generates reading reports.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from uuid import UUID
import time

from app.models.reading import ReadingSession
from app.services.tarot_service import TarotService
from app.services.palm_service import PalmService


class ReadingService:
    """Orchestrates reading sessions and manages persistence."""

    @staticmethod
    async def perform_tarot_reading(
        db: AsyncSession,
        user_id: UUID,
        spread_type: str,
        question: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Perform a complete tarot reading session:
        1. Create session record
        2. Execute tarot engine
        3. Update session with results
        """
        start_time = time.time()

        # Create reading session
        session = ReadingSession(
            user_id=user_id,
            reading_type="tarot",
            spread_type=spread_type,
            status="processing",
        )
        db.add(session)
        await db.flush()

        try:
            # Execute tarot engine
            reading = TarotService.generate_reading(spread_type, question)

            # Update session
            duration = int(time.time() - start_time)
            session.status = "completed"
            session.duration_seconds = duration
            session.confidence_score = reading["confidence_score"]
            session.completed_at = datetime.now(timezone.utc)
            await db.commit()

            # Refresh to get updated fields
            await db.refresh(session)

            return {
                "session_id": str(session.id),
                "reading_type": "tarot",
                "status": "completed",
                "reading": reading,
                "duration_seconds": duration,
                "created_at": session.created_at.isoformat() if session.created_at else None,
            }

        except Exception as e:
            session.status = "failed"
            await db.commit()
            raise e

    @staticmethod
    async def perform_palm_reading(
        db: AsyncSession,
        user_id: UUID,
        image_data: Optional[str] = None,
        image_filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Perform a complete palm analysis session:
        1. Create session record
        2. Execute palm analysis engine
        3. Update session with results
        """
        start_time = time.time()

        session = ReadingSession(
            user_id=user_id,
            reading_type="palm",
            spread_type="full_palm_scan",
            status="processing",
        )
        db.add(session)
        await db.flush()

        try:
            # Execute palm engine
            analysis = PalmService.analyze_palm(
                image_data=image_data,
                image_filename=image_filename,
                user_seed=str(user_id),
            )

            duration = int(time.time() - start_time)
            session.status = "completed"
            session.duration_seconds = duration
            session.confidence_score = analysis["confidence_score"]
            session.completed_at = datetime.now(timezone.utc)
            await db.commit()

            await db.refresh(session)

            return {
                "session_id": str(session.id),
                "reading_type": "palm",
                "status": "completed",
                "analysis": analysis,
                "duration_seconds": duration,
                "created_at": session.created_at.isoformat() if session.created_at else None,
            }

        except Exception as e:
            session.status = "failed"
            await db.commit()
            raise e

    @staticmethod
    async def perform_combined_reading(
        db: AsyncSession,
        user_id: UUID,
        spread_type: str = "three_card",
        question: Optional[str] = None,
        image_data: Optional[str] = None,
        image_filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Perform a combined palm + tarot reading session.
        Synthesizes insights from both engines into a unified report.
        """
        start_time = time.time()

        session = ReadingSession(
            user_id=user_id,
            reading_type="combined",
            spread_type=spread_type,
            status="processing",
        )
        db.add(session)
        await db.flush()

        try:
            # Run both engines
            tarot_reading = TarotService.generate_reading(spread_type, question)
            palm_analysis = PalmService.analyze_palm(
                image_data=image_data,
                image_filename=image_filename,
                user_seed=str(user_id),
            )

            # Synthesize combined insights
            combined_narrative = _synthesize_combined(tarot_reading, palm_analysis, question)

            # Average confidence
            combined_confidence = round(
                (tarot_reading["confidence_score"] + palm_analysis["confidence_score"]) / 2,
                4,
            )

            duration = int(time.time() - start_time)
            session.status = "completed"
            session.duration_seconds = duration
            session.confidence_score = combined_confidence
            session.completed_at = datetime.now(timezone.utc)
            await db.commit()

            await db.refresh(session)

            return {
                "session_id": str(session.id),
                "reading_type": "combined",
                "status": "completed",
                "tarot_reading": tarot_reading,
                "palm_analysis": palm_analysis,
                "combined_narrative": combined_narrative,
                "confidence_score": combined_confidence,
                "duration_seconds": duration,
                "created_at": session.created_at.isoformat() if session.created_at else None,
            }

        except Exception as e:
            session.status = "failed"
            await db.commit()
            raise e

    @staticmethod
    async def get_reading(db: AsyncSession, reading_id: UUID, user_id: UUID) -> Optional[Dict]:
        """Get a specific reading session by ID."""
        result = await db.execute(
            select(ReadingSession).where(
                ReadingSession.id == reading_id,
                ReadingSession.user_id == user_id,
            )
        )
        session = result.scalar_one_or_none()
        if not session:
            return None

        return {
            "session_id": str(session.id),
            "reading_type": session.reading_type,
            "spread_type": session.spread_type,
            "status": session.status,
            "confidence_score": float(session.confidence_score) if session.confidence_score else None,
            "duration_seconds": session.duration_seconds,
            "user_rating": session.user_rating,
            "user_feedback": session.user_feedback,
            "started_at": session.started_at.isoformat() if session.started_at else None,
            "completed_at": session.completed_at.isoformat() if session.completed_at else None,
            "created_at": session.created_at.isoformat() if session.created_at else None,
        }

    @staticmethod
    async def get_reading_history(
        db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 20
    ) -> List[Dict]:
        """Get reading history for a user with pagination."""
        result = await db.execute(
            select(ReadingSession)
            .where(ReadingSession.user_id == user_id)
            .order_by(ReadingSession.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        sessions = result.scalars().all()

        return [
            {
                "session_id": str(s.id),
                "reading_type": s.reading_type,
                "spread_type": s.spread_type,
                "status": s.status,
                "confidence_score": float(s.confidence_score) if s.confidence_score else None,
                "duration_seconds": s.duration_seconds,
                "user_rating": s.user_rating,
                "started_at": s.started_at.isoformat() if s.started_at else None,
                "completed_at": s.completed_at.isoformat() if s.completed_at else None,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in sessions
        ]

    @staticmethod
    async def submit_feedback(
        db: AsyncSession, reading_id: UUID, user_id: UUID, rating: int, feedback: Optional[str]
    ) -> Optional[Dict]:
        """Submit user feedback for a reading session."""
        result = await db.execute(
            select(ReadingSession).where(
                ReadingSession.id == reading_id,
                ReadingSession.user_id == user_id,
            )
        )
        session = result.scalar_one_or_none()
        if not session:
            return None

        session.user_rating = rating
        session.user_feedback = feedback
        await db.commit()

        return {
            "session_id": str(session.id),
            "rating": rating,
            "feedback": feedback,
            "message": "Feedback submitted successfully",
        }


# ============================================================================
# Private Helpers
# ============================================================================

def _synthesize_combined(tarot: Dict, palm: Dict, question: Optional[str]) -> Dict[str, str]:
    """Synthesize a unified narrative from tarot and palm analyses."""
    hand_type = palm.get("hand_shape", {}).get("type", "Unknown")
    hand_element = palm.get("hand_shape", {}).get("element", "")
    tarot_energy = tarot.get("narrative", {}).get("energy_tone", "balanced")
    tarot_themes = tarot.get("themes", [])

    # Find alignment between palm traits and tarot themes
    palm_traits = []
    for trait in palm.get("personality_traits", []):
        if trait["score"] >= 75:
            palm_traits.append(trait["trait"])

    summary = (
        f"Your combined reading reveals a fascinating alignment between your palm's story and the tarot's guidance. "
        f"Your {hand_type} (element: {hand_element}) resonates with the tarot's {tarot_energy} energy. "
        f"The cards and your palm lines together suggest that your strongest qualities — "
        f"{', '.join(palm_traits[:3]) if palm_traits else 'your innate talents'} — "
        f"are being called upon at this time."
    )

    if tarot_themes:
        theme_text = ", ".join(tarot_themes[:3])
        summary += f" Key themes emerging from both readings: {theme_text}."

    advice = (
        f"The synthesis of your palm analysis and tarot reading suggests a period of "
        f"{'growth and opportunity' if 'positive' in tarot_energy else 'reflection and transformation'}. "
        f"Trust your {hand_element.lower()} nature and let it guide your decisions. "
        f"{'The cards confirm what your palm reveals — you are on the right path.' if 'positive' in tarot_energy else 'The cards urge patience; your palm shows the resilience needed to navigate this phase.'}"
    )

    return {
        "summary": summary,
        "advice": advice,
    }
