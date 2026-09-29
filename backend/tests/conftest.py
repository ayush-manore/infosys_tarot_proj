"""
Test Configuration & Fixtures
==============================
Shared pytest fixtures for async database sessions, test clients,
and authentication helpers.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4


@pytest.fixture(scope="session")
def event_loop():
    """Create a persistent event loop for all async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_db():
    """Create a mock async database session."""
    db = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(
        scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))
    ))
    db.commit = AsyncMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    return db


@pytest.fixture
def sample_user():
    """Create a sample user dict for testing."""
    return {
        "id": uuid4(),
        "email": "test@mystic.ai",
        "full_name": "Test Seeker",
        "role": {
            "name": "user",
            "permissions": {
                "can_create_readings": True,
                "can_view_own_data": True,
            },
        },
    }


@pytest.fixture
def sample_palm_analysis():
    """Create sample palm analysis data for testing."""
    return {
        "hand_shape": {
            "type": "Water Hand",
            "element": "Water",
            "description": "Long palm with long, slender fingers",
            "traits": ["Sensitive", "Intuitive", "Empathic"],
            "confidence": 0.87,
        },
        "lines": [
            {"line_name": "Heart Line", "detected": True, "confidence": 0.92,
             "measurements": {"depth": "deep", "clarity": "clear", "length_mm": 98}},
            {"line_name": "Head Line", "detected": True, "confidence": 0.88,
             "measurements": {"depth": "moderate", "clarity": "clear", "length_mm": 85}},
            {"line_name": "Life Line", "detected": True, "confidence": 0.90,
             "measurements": {"depth": "deep", "clarity": "clear", "length_mm": 105}},
            {"line_name": "Fate Line", "detected": True, "confidence": 0.78,
             "measurements": {"depth": "moderate", "clarity": "faint", "length_mm": 72}},
            {"line_name": "Sun Line", "detected": True, "confidence": 0.65,
             "measurements": {"depth": "faint", "clarity": "faint", "length_mm": 45}},
        ],
        "personality_traits": [
            {"trait": "Emotional Intelligence", "score": 82},
            {"trait": "Analytical Thinking", "score": 71},
            {"trait": "Creative Expression", "score": 78},
            {"trait": "Career Drive", "score": 68},
            {"trait": "Intuitive Awareness", "score": 85},
            {"trait": "Vitality & Resilience", "score": 73},
        ],
        "confidence_score": 0.847,
        "landmarks_detected": {"hand_detected": True},
        "narrative": {
            "summary": "Your palm reveals a deeply intuitive nature.",
            "detailed_analysis": "Full analysis of palm features.",
            "advice": "Trust your intuition.",
        },
        "analysis_method": "simulated_cv",
    }


@pytest.fixture
def sample_tarot_reading():
    """Create sample tarot reading data for testing."""
    return {
        "spread_name": "Three Card Spread",
        "spread_description": "Past, Present, Future layout",
        "question": "What does the future hold?",
        "cards": [
            {"card_name": "The Fool", "orientation": "upright", "position": "Past",
             "arcana": "major", "suit": None, "element": "Air",
             "keywords": ["beginnings", "innocence", "spontaneity"],
             "core_meaning": "New beginnings and infinite possibilities.",
             "position_interpretation": "Your past was marked by fresh starts."},
            {"card_name": "The Magician", "orientation": "upright", "position": "Present",
             "arcana": "major", "suit": None, "element": "Air",
             "keywords": ["manifestation", "power", "action"],
             "core_meaning": "You have the tools for creation.",
             "position_interpretation": "You currently hold tremendous creative power."},
            {"card_name": "The Star", "orientation": "upright", "position": "Future",
             "arcana": "major", "suit": None, "element": "Air",
             "keywords": ["hope", "renewal", "serenity"],
             "core_meaning": "Hope and inspiration guide you forward.",
             "position_interpretation": "Your future shines with hope and renewal."},
        ],
        "themes": ["transformation", "hope", "new beginnings", "spiritual growth"],
        "elemental_balance": {"Fire": 10, "Water": 25, "Air": 45, "Earth": 20},
        "confidence_score": 0.82,
        "narrative": {
            "summary": "A reading filled with major arcana energy.",
            "energy_tone": "positive and transformative",
            "advice": "Trust the process and embrace new beginnings.",
        },
    }


@pytest.fixture
def sample_user_context():
    """Create sample user profile context."""
    return {
        "spiritual_goals": ["self_discovery", "career_guidance"],
        "spiritual_interests": ["tarot", "palmistry", "meditation"],
        "experience_level": "intermediate",
    }
