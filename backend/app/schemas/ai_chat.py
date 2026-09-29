"""
AI Chat Schemas
================
Request and response schemas for the AI chatbot and intelligence endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ==========================================
# Chat Schemas
# ==========================================

class ChatMessageRequest(BaseModel):
    """Request body for sending a chat message."""
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's message to the AI chatbot"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation ID for context continuity"
    )


class ChatMessage(BaseModel):
    """A single chat message."""
    role: str = Field(..., description="Message sender: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = None


class ChatResponse(BaseModel):
    """Response from the AI chatbot."""
    status: str = "success"
    message: str = ""
    data: Dict[str, Any] = {}


# ==========================================
# AI Interpretation Schemas
# ==========================================

class AIInterpretationRequest(BaseModel):
    """Request for AI-powered interpretation of a reading."""
    reading_id: Optional[str] = Field(None, description="Reading session ID to interpret")
    reading_type: str = Field("combined", description="Type: palm, tarot, or combined")
    reading_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Direct reading data if no reading_id provided"
    )


class AIInterpretationResponse(BaseModel):
    """Response with AI interpretation."""
    status: str = "success"
    message: str = ""
    data: Dict[str, Any] = {}


# ==========================================
# AI Recommendation Schemas
# ==========================================

class AIRecommendationRequest(BaseModel):
    """Request for AI-powered recommendations."""
    include_reading_history: bool = Field(
        True,
        description="Whether to include reading history for context"
    )


class AIRecommendationResponse(BaseModel):
    """Response with AI recommendations."""
    status: str = "success"
    message: str = ""
    data: Dict[str, Any] = {}


# ==========================================
# Trend Analysis Schemas
# ==========================================

class TrendAnalysisRequest(BaseModel):
    """Request for AI life trend analysis."""
    time_period: str = Field(
        "all",
        description="Time period: 'week', 'month', 'quarter', 'all'"
    )


class TrendAnalysisResponse(BaseModel):
    """Response with trend analysis."""
    status: str = "success"
    message: str = ""
    data: Dict[str, Any] = {}


# ==========================================
# Personality Intelligence Schemas
# ==========================================

class PersonalityIntelligenceRequest(BaseModel):
    """Request for AI personality intelligence."""
    include_tarot: bool = Field(True, description="Include tarot data in analysis")


class PersonalityIntelligenceResponse(BaseModel):
    """Response with personality intelligence."""
    status: str = "success"
    message: str = ""
    data: Dict[str, Any] = {}


# ==========================================
# Card Meaning Schema
# ==========================================

class CardMeaningRequest(BaseModel):
    """Request for an AI interpretation of a specific card."""
    card_name: str = Field(..., description="Name of the tarot card")
    orientation: str = Field("upright", description="Card orientation: upright or reversed")
    context: Optional[str] = Field(None, max_length=500, description="Optional context/question")
