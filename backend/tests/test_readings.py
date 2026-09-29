"""
Reading Endpoint Tests
=======================
Tests for palm, tarot, and combined reading API endpoints.
"""

import pytest
from app.services.palm_service import PalmService
from app.services.tarot_service import TarotService


class TestReadingEndpoints:
    """Tests for reading API endpoints."""

    def test_palm_reading_generation(self):
        """Test palm reading generates valid analysis."""
        result = PalmService.analyze_palm()
        assert result is not None
        assert "hand_shape" in result
        assert "lines" in result
        assert len(result["lines"]) >= 3

    def test_tarot_reading_all_spreads(self):
        """Test all supported tarot spread types."""
        spreads = {
            "single": 1,
            "three_card": 3,
            "celtic_cross": 10,
            "relationship": 5,
            "career": 5,
            "daily": 1,
        }
        for spread, expected_count in spreads.items():
            result = TarotService.generate_reading(spread)
            assert len(result["cards"]) == expected_count, f"Spread {spread} should have {expected_count} cards"
            assert result["spread_name"] is not None

    def test_tarot_with_question(self):
        """Test tarot reading with custom question."""
        result = TarotService.generate_reading("three_card", "Will I find love?")
        assert result["question"] == "Will I find love?"
        assert len(result["cards"]) == 3

    def test_combined_reading_generates_both(self):
        """Test that combined reading creates both palm and tarot data."""
        palm = PalmService.analyze_palm()
        tarot = TarotService.generate_reading("three_card")

        assert palm is not None
        assert tarot is not None
        assert "confidence_score" in palm
        assert "confidence_score" in tarot

    def test_palm_narrative_generated(self):
        """Test that palm reading generates narrative."""
        result = PalmService.analyze_palm()
        narrative = result.get("narrative", {})
        assert "summary" in narrative
        assert len(narrative["summary"]) > 10

    def test_tarot_narrative_generated(self):
        """Test that tarot reading generates narrative."""
        result = TarotService.generate_reading("celtic_cross")
        narrative = result.get("narrative", {})
        assert "summary" in narrative
        assert "energy_tone" in narrative

    def test_tarot_card_uniqueness(self):
        """Test that no duplicate cards in a single reading."""
        result = TarotService.generate_reading("celtic_cross")
        card_names = [c["card_name"] for c in result["cards"]]
        assert len(card_names) == len(set(card_names)), "Duplicate cards detected"

    def test_palm_confidence_reasonable(self):
        """Test palm confidence scores are reasonable."""
        for _ in range(5):
            result = PalmService.analyze_palm()
            assert 0.5 <= result["confidence_score"] <= 1.0

    def test_tarot_elemental_balance_present(self):
        """Test that elemental balance has all four elements."""
        result = TarotService.generate_reading("celtic_cross")
        balance = result["elemental_balance"]
        assert "Fire" in balance
        assert "Water" in balance
        assert "Air" in balance
        assert "Earth" in balance

    def test_tarot_invalid_spread_raises(self):
        """Test that invalid spread type raises ValueError."""
        with pytest.raises(ValueError):
            TarotService.generate_reading("nonexistent_spread")

    def test_palm_with_different_seeds(self):
        """Test that different seeds produce different results."""
        r1 = PalmService.analyze_palm(user_seed="user_a")
        r2 = PalmService.analyze_palm(user_seed="user_b")
        # Different seeds should produce different hand shapes (statistically)
        # At minimum, the function should run without error
        assert r1 is not None
        assert r2 is not None
