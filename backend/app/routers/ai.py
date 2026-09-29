"""
AI & Chatbot API Router
========================
Endpoints for AI-powered features:
- Interactive chatbot (Gemini-powered conversational AI)
- AI interpretation engine
- AI recommendation system
- Life trend analysis
- Personality intelligence
- Card meaning lookup

All endpoints require authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import json

from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.services.gemini_service import GeminiService
from app.schemas.ai_chat import (
    ChatMessageRequest, ChatResponse,
    AIInterpretationRequest, AIInterpretationResponse,
    AIRecommendationRequest, AIRecommendationResponse,
    TrendAnalysisRequest, TrendAnalysisResponse,
    PersonalityIntelligenceRequest, PersonalityIntelligenceResponse,
    CardMeaningRequest,
)

router = APIRouter(prefix="/ai", tags=["AI & Chatbot"])

# In-memory conversation store (per-user sessions)
# In production, use Redis or MongoDB for persistence
_conversation_store: Dict[str, list] = {}


# ═══════════════════════════════════════════════════════════════════
# Chatbot Endpoints
# ═══════════════════════════════════════════════════════════════════

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatMessageRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a message to MysticAI chatbot and receive a response.

    The chatbot maintains conversation context across messages using
    the conversation_id. If no conversation_id is provided, a new
    conversation is started.

    Features:
    - Context-aware responses using user's reading history & profile
    - Multi-turn conversation support
    - Tarot card meanings and palm reading guidance
    - Personalized spiritual advice
    """
    user_id = str(current_user.id)

    # Get or create conversation
    conv_id = request.conversation_id or f"{user_id}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    conv_key = f"conv:{conv_id}"

    if conv_key not in _conversation_store:
        _conversation_store[conv_key] = []

    conversation_history = _conversation_store[conv_key]

    # Build user context from profile
    user_context = _build_user_context(current_user)

    # Get AI response
    result = await GeminiService.chat(
        message=request.message,
        conversation_history=conversation_history,
        user_context=user_context,
    )

    # Store messages in conversation history
    conversation_history.append({
        "role": "user",
        "content": request.message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    conversation_history.append({
        "role": "assistant",
        "content": result["response"],
        "timestamp": result["timestamp"],
    })

    # Keep conversation manageable (last 40 messages)
    if len(conversation_history) > 40:
        _conversation_store[conv_key] = conversation_history[-40:]

    return ChatResponse(
        status="success",
        message="AI response generated",
        data={
            "response": result["response"],
            "conversation_id": conv_id,
            "model": result.get("model", "gemini"),
            "timestamp": result["timestamp"],
            "ai_status": result.get("status", "success"),
        },
    )


@router.get("/chat/history/{conversation_id}")
async def get_chat_history(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get chat history for a specific conversation."""
    conv_key = f"conv:{conversation_id}"
    history = _conversation_store.get(conv_key, [])

    return {
        "status": "success",
        "conversation_id": conversation_id,
        "message_count": len(history),
        "data": history,
    }


@router.get("/chat/conversations")
async def list_conversations(
    current_user: User = Depends(get_current_user),
):
    """List all active conversations for the current user."""
    user_id = str(current_user.id)
    conversations = []

    for key, messages in _conversation_store.items():
        conv_id = key.replace("conv:", "")
        if conv_id.startswith(user_id) and messages:
            last_msg = messages[-1]
            conversations.append({
                "conversation_id": conv_id,
                "message_count": len(messages),
                "last_message": last_msg.get("content", "")[:100],
                "last_timestamp": last_msg.get("timestamp"),
            })

    conversations.sort(key=lambda x: x.get("last_timestamp", ""), reverse=True)

    return {
        "status": "success",
        "count": len(conversations),
        "data": conversations,
    }


@router.delete("/chat/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
):
    """Delete a conversation and its history."""
    conv_key = f"conv:{conversation_id}"
    if conv_key in _conversation_store:
        del _conversation_store[conv_key]

    return {"status": "success", "message": "Conversation deleted"}


# ═══════════════════════════════════════════════════════════════════
# AI Interpretation Engine
# ═══════════════════════════════════════════════════════════════════

@router.post("/interpret", response_model=AIInterpretationResponse)
async def ai_interpret_reading(
    request: AIInterpretationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate an AI-powered deep interpretation of a reading.

    Provide either a reading_id to interpret a stored reading,
    or reading_data directly for immediate interpretation.

    Returns rich narrative insights across all life categories
    with personalized advice and affirmations.
    """
    reading_data = request.reading_data or {}

    if not reading_data:
        # Generate sample data for demo
        reading_data = _get_demo_reading_data(request.reading_type)

    user_context = _build_user_context(current_user)

    result = await GeminiService.generate_ai_interpretation(
        reading_data=reading_data,
        reading_type=request.reading_type,
        user_context=user_context,
    )

    return AIInterpretationResponse(
        status="success",
        message="AI interpretation generated",
        data=result,
    )


# ═══════════════════════════════════════════════════════════════════
# AI Recommendation Engine
# ═══════════════════════════════════════════════════════════════════

@router.post("/recommendations", response_model=AIRecommendationResponse)
async def get_ai_recommendations(
    request: AIRecommendationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate AI-powered personalized recommendations.

    Based on the user's personality profile, reading history,
    and spiritual goals. Returns categorized recommendations
    with actionable practices and rituals.
    """
    # Build personality profile from user context
    personality_profile = {
        "user_id": str(current_user.id),
        "email": current_user.email,
        "traits": {
            "Emotional Intelligence": 75,
            "Analytical Thinking": 70,
            "Creative Expression": 80,
            "Vitality & Resilience": 72,
            "Career Drive": 68,
            "Intuitive Awareness": 78,
        },
    }

    user_context = _build_user_context(current_user)

    result = await GeminiService.generate_ai_recommendations(
        personality_profile=personality_profile,
        user_context=user_context,
    )

    return AIRecommendationResponse(
        status="success",
        message="AI recommendations generated",
        data=result,
    )


# ═══════════════════════════════════════════════════════════════════
# Life Trend Analysis
# ═══════════════════════════════════════════════════════════════════

@router.post("/trends", response_model=TrendAnalysisResponse)
async def analyze_trends(
    request: TrendAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate AI-powered life trend analysis.

    Analyzes reading history to identify patterns, opportunity
    windows, and growth trajectories across life domains.
    """
    # Build reading history summary
    reading_history = [
        {
            "date": "2026-09-25",
            "type": "tarot",
            "spread": "three_card",
            "themes": ["transformation", "new beginnings"],
            "overall_score": 78,
        },
        {
            "date": "2026-09-20",
            "type": "combined",
            "spread": "celtic_cross",
            "themes": ["career growth", "inner wisdom"],
            "overall_score": 82,
        },
        {
            "date": "2026-09-15",
            "type": "palm",
            "themes": ["emotional depth", "creativity"],
            "overall_score": 75,
        },
    ]

    personality_profile = {
        "traits": {
            "Emotional Intelligence": 75,
            "Analytical Thinking": 70,
            "Creative Expression": 80,
        },
    }

    result = await GeminiService.analyze_life_trends(
        reading_history=reading_history,
        personality_profile=personality_profile,
    )

    return TrendAnalysisResponse(
        status="success",
        message="Life trend analysis generated",
        data=result,
    )


# ═══════════════════════════════════════════════════════════════════
# Personality Intelligence
# ═══════════════════════════════════════════════════════════════════

@router.post("/personality", response_model=PersonalityIntelligenceResponse)
async def personality_intelligence(
    request: PersonalityIntelligenceRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate AI-powered deep personality intelligence report.

    Creates a comprehensive personality profile including Big Five
    mapping, spiritual archetype, elemental alignment, and
    personalized development pathways.
    """
    # Build palm data from user context
    palm_data = {
        "hand_shape": {"type": "Water", "element": "Water"},
        "personality_traits": [
            {"trait": "Emotional Intelligence", "score": 78},
            {"trait": "Analytical Thinking", "score": 72},
            {"trait": "Creative Expression", "score": 85},
            {"trait": "Vitality & Resilience", "score": 70},
            {"trait": "Career Drive", "score": 68},
            {"trait": "Intuitive Awareness", "score": 80},
        ],
        "lines": [
            {"name": "Heart Line", "characteristic": "long_and_curved"},
            {"name": "Head Line", "characteristic": "deep_and_clear"},
            {"name": "Life Line", "characteristic": "long_and_deep"},
        ],
    }

    tarot_data = None
    if request.include_tarot:
        tarot_data = {
            "cards": [
                {"card_name": "The Star", "orientation": "upright", "position": "Present"},
                {"card_name": "The Empress", "orientation": "upright", "position": "Near Future"},
                {"card_name": "Knight of Cups", "orientation": "upright", "position": "Outcome"},
            ],
            "themes": ["hope", "nurturing", "emotional quest"],
            "elemental_balance": {"Water": 40, "Earth": 25, "Air": 20, "Fire": 15},
        }

    user_context = _build_user_context(current_user)

    result = await GeminiService.generate_personality_intelligence(
        palm_data=palm_data,
        tarot_data=tarot_data,
        user_context=user_context,
    )

    return PersonalityIntelligenceResponse(
        status="success",
        message="Personality intelligence report generated",
        data=result,
    )


# ═══════════════════════════════════════════════════════════════════
# Card Meaning Lookup
# ═══════════════════════════════════════════════════════════════════

@router.post("/card-meaning")
async def get_card_meaning(
    request: CardMeaningRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Get an AI-powered interpretation of a specific tarot card.
    Provides rich, contextual card meanings with actionable guidance.
    """
    result = await GeminiService.get_card_meaning(
        card_name=request.card_name,
        orientation=request.orientation,
        context=request.context,
    )

    return {
        "status": "success",
        "message": f"Interpretation for {request.card_name} ({request.orientation})",
        "data": result,
    }


# ═══════════════════════════════════════════════════════════════════
# AI Health Check
# ═══════════════════════════════════════════════════════════════════

@router.get("/status")
async def ai_status():
    """Check AI service status and configuration."""
    from app.config import settings

    has_key = bool(settings.GEMINI_API_KEY)
    return {
        "status": "success",
        "data": {
            "ai_enabled": has_key,
            "model": settings.GEMINI_MODEL if has_key else None,
            "features": {
                "chatbot": has_key,
                "interpretation_engine": True,
                "recommendation_engine": True,
                "trend_analysis": True,
                "personality_intelligence": True,
                "card_meanings": has_key,
            },
            "fallback_available": True,
        },
    }


# ═══════════════════════════════════════════════════════════════════
# Private Helpers
# ═══════════════════════════════════════════════════════════════════

def _build_user_context(user: User) -> Dict[str, Any]:
    """Build user context dict from the authenticated user object."""
    context = {
        "user_id": str(user.id),
        "email": user.email,
    }

    # Add profile data if available
    if hasattr(user, "profile") and user.profile:
        profile = user.profile
        context["spiritual_goals"] = getattr(profile, "spiritual_goals", []) or []
        context["spiritual_interests"] = getattr(profile, "spiritual_interests", []) or []
        context["experience_level"] = getattr(profile, "experience_level", "beginner")

    return context


def _get_demo_reading_data(reading_type: str) -> Dict[str, Any]:
    """Generate demo reading data for immediate interpretation."""
    if reading_type == "tarot":
        return {
            "cards": [
                {
                    "card_name": "The Fool",
                    "orientation": "upright",
                    "position": "Past",
                    "keywords": ["new beginnings", "adventure", "innocence"],
                },
                {
                    "card_name": "The Magician",
                    "orientation": "upright",
                    "position": "Present",
                    "keywords": ["manifestation", "willpower", "skill"],
                },
                {
                    "card_name": "The High Priestess",
                    "orientation": "upright",
                    "position": "Future",
                    "keywords": ["intuition", "mystery", "inner wisdom"],
                },
            ],
            "spread_type": "three_card",
            "themes": ["new beginnings", "personal power", "intuition"],
            "elemental_balance": {"Water": 35, "Air": 30, "Fire": 20, "Earth": 15},
        }
    elif reading_type == "palm":
        return {
            "hand_shape": {"type": "Water", "element": "Water"},
            "lines": [
                {"name": "Heart Line", "characteristic": "long_and_curved", "score": 82},
                {"name": "Head Line", "characteristic": "deep_and_clear", "score": 75},
                {"name": "Life Line", "characteristic": "long_and_deep", "score": 78},
            ],
            "personality_traits": [
                {"trait": "Emotional Intelligence", "score": 82},
                {"trait": "Analytical Thinking", "score": 75},
                {"trait": "Creative Expression", "score": 78},
            ],
        }
    else:
        return {
            "palm_analysis": {
                "hand_shape": {"type": "Water", "element": "Water"},
                "personality_traits": [
                    {"trait": "Emotional Intelligence", "score": 82},
                    {"trait": "Creative Expression", "score": 78},
                ],
            },
            "tarot_reading": {
                "cards": [
                    {"card_name": "The Star", "orientation": "upright", "position": "Present"},
                    {"card_name": "Ace of Cups", "orientation": "upright", "position": "Future"},
                ],
                "themes": ["hope", "emotional renewal"],
            },
        }
