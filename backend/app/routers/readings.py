"""
Readings API Router
====================
Endpoints for performing palm analysis, tarot readings, combined readings,
reading history, and user feedback. All endpoints require authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import base64

from app.database import get_db
from app.utils.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.reading import (
    TarotReadingRequest, CombinedReadingRequest,
    ReadingFeedbackRequest, ReadingResponse,
)
from app.services.reading_service import ReadingService
from app.services.tarot_service import TarotService
from app.services.palm_service import PalmService

router = APIRouter(prefix="/readings", tags=["Readings"])

# Allowed image MIME types and max size
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB


# ═══════════════════════════════════════════════════════════════════
# Palm Reading Endpoints
# ═══════════════════════════════════════════════════════════════════

@router.post("/palm", response_model=ReadingResponse)
async def perform_palm_reading(
    file: Optional[UploadFile] = File(None),
    image_data: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Perform a palm analysis reading.

    Accepts either:
    - A multipart file upload (jpg, png, webp — max 10MB)
    - A base64-encoded image string in the `image_data` form field

    Returns complete palm analysis with hand shape, line interpretations,
    personality traits, narrative, and confidence score.
    """
    encoded_data = None
    filename = None

    if file:
        # Validate file type
        if file.content_type and file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid image type '{file.content_type}'. Allowed: jpg, png, webp"
            )

        # Read file content
        content = await file.read()

        # Validate size
        if len(content) > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Image exceeds maximum size of {MAX_IMAGE_SIZE // (1024*1024)}MB"
            )

        encoded_data = base64.b64encode(content).decode("utf-8")
        filename = file.filename

    elif image_data:
        encoded_data = image_data
        filename = "base64_upload.png"
    else:
        # No image provided — still perform analysis using user seed
        filename = None
        encoded_data = None

    try:
        result = await ReadingService.perform_palm_reading(
            db=db,
            user_id=current_user.id,
            image_data=encoded_data,
            image_filename=filename,
        )
        return ReadingResponse(
            status="success",
            message="Palm analysis completed successfully",
            data=result,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Palm analysis failed: {str(e)}"
        )


@router.get("/palm/lines")
async def get_palm_lines():
    """
    Get information about all analyzable palm lines.
    Returns line names, locations, elements, and associated traits.
    """
    lines = PalmService.get_available_lines()
    return {
        "status": "success",
        "count": len(lines),
        "data": lines,
    }


# ═══════════════════════════════════════════════════════════════════
# Tarot Reading Endpoints
# ═══════════════════════════════════════════════════════════════════

@router.post("/tarot", response_model=ReadingResponse)
async def perform_tarot_reading(
    request: TarotReadingRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Perform a tarot card reading.

    Select a spread type and optionally provide a guiding question.
    Returns dealt cards with position-specific interpretations,
    overall narrative, themes, and elemental balance.

    Spread types: single, three_card, celtic_cross, career, relationship, daily
    """
    try:
        result = await ReadingService.perform_tarot_reading(
            db=db,
            user_id=current_user.id,
            spread_type=request.spread_type,
            question=request.question,
        )
        return ReadingResponse(
            status="success",
            message="Tarot reading completed successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tarot reading failed: {str(e)}"
        )


@router.get("/tarot/spreads")
async def list_spreads():
    """
    List all available tarot spread types with their configurations.
    Returns spread names, card counts, position labels, and descriptions.
    """
    spreads = TarotService.get_available_spreads()
    return {
        "status": "success",
        "count": len(spreads),
        "data": spreads,
    }


@router.get("/tarot/daily", response_model=ReadingResponse)
async def daily_card(
    current_user: User = Depends(get_current_user),
):
    """
    Get today's daily guidance card.
    Consistent for each user per day (seeded by user ID + date).
    """
    reading = TarotService.get_daily_card(user_seed=str(current_user.id))
    return ReadingResponse(
        status="success",
        message="Daily guidance card drawn",
        data=reading,
    )


# ═══════════════════════════════════════════════════════════════════
# Combined Reading Endpoints
# ═══════════════════════════════════════════════════════════════════

@router.post("/combined", response_model=ReadingResponse)
async def perform_combined_reading(
    request: CombinedReadingRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Perform a combined palm + tarot reading.

    Synthesizes insights from both the palm analysis engine and tarot
    reading engine into a unified narrative and guidance report.
    """
    try:
        result = await ReadingService.perform_combined_reading(
            db=db,
            user_id=current_user.id,
            spread_type=request.spread_type,
            question=request.question,
            image_data=request.image_data,
            image_filename=request.image_filename,
        )
        return ReadingResponse(
            status="success",
            message="Combined reading completed successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Combined reading failed: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════
# Reading History & Feedback
# ═══════════════════════════════════════════════════════════════════

@router.get("/history")
async def get_reading_history(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the authenticated user's reading history with pagination.
    Returns a list of past reading sessions ordered by most recent.
    """
    history = await ReadingService.get_reading_history(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return {
        "status": "success",
        "count": len(history),
        "data": history,
    }


@router.get("/{reading_id}")
async def get_reading(
    reading_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get details of a specific reading session by ID.
    Users can only access their own readings.
    """
    from uuid import UUID
    try:
        rid = UUID(reading_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reading ID format"
        )

    result = await ReadingService.get_reading(db=db, reading_id=rid, user_id=current_user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading not found"
        )

    return {
        "status": "success",
        "data": result,
    }


@router.post("/{reading_id}/feedback", response_model=ReadingResponse)
async def submit_feedback(
    reading_id: str,
    request: ReadingFeedbackRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit rating and optional feedback for a completed reading.
    Rating: 1 (poor) to 5 (excellent).
    """
    from uuid import UUID
    try:
        rid = UUID(reading_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reading ID format"
        )

    result = await ReadingService.submit_feedback(
        db=db,
        reading_id=rid,
        user_id=current_user.id,
        rating=request.rating,
        feedback=request.feedback,
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading not found"
        )

    return ReadingResponse(
        status="success",
        message="Feedback submitted successfully",
        data=result,
    )
