"""
Reading Pydantic Schemas
========================
Request and response schemas for palm analysis, tarot readings,
combined readings, and user feedback.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# ==========================================
# Palm Reading Schemas
# ==========================================

class PalmReadingRequest(BaseModel):
    """Request body for base64-encoded palm image analysis."""
    image_data: Optional[str] = Field(None, description="Base64-encoded palm image data")
    image_filename: Optional[str] = Field(None, description="Original filename of the uploaded image")


# ==========================================
# Tarot Reading Schemas
# ==========================================

class TarotReadingRequest(BaseModel):
    """Request body for tarot card reading."""
    spread_type: str = Field(
        "three_card",
        description="Spread type: single, three_card, celtic_cross, career, relationship, daily"
    )
    question: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional question to guide the reading"
    )


# ==========================================
# Combined Reading Schemas
# ==========================================

class CombinedReadingRequest(BaseModel):
    """Request body for combined palm + tarot reading."""
    spread_type: str = Field("three_card", description="Tarot spread type for the combined reading")
    question: Optional[str] = Field(None, max_length=500, description="Optional guiding question")
    image_data: Optional[str] = Field(None, description="Base64-encoded palm image data")
    image_filename: Optional[str] = Field(None, description="Original filename of the palm image")


# ==========================================
# Feedback Schemas
# ==========================================

class ReadingFeedbackRequest(BaseModel):
    """Request body for submitting reading feedback."""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 (poor) to 5 (excellent)")
    feedback: Optional[str] = Field(None, max_length=1000, description="Optional text feedback")


# ==========================================
# Response Schemas
# ==========================================

class ReadingResponse(BaseModel):
    """Standard reading API response wrapper."""
    status: str = "success"
    message: str = ""
    data: Dict[str, Any] = {}


class ReadingHistoryItem(BaseModel):
    """Single item in reading history."""
    session_id: str
    reading_type: str
    spread_type: Optional[str] = None
    status: str
    confidence_score: Optional[float] = None
    duration_seconds: Optional[int] = None
    user_rating: Optional[int] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: Optional[str] = None


class ReadingHistoryResponse(BaseModel):
    """Response for reading history endpoint."""
    status: str = "success"
    count: int
    data: List[ReadingHistoryItem] = []
