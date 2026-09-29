"""
Service Unit Tests
===================
Tests for PalmService, TarotService, InterpretationService,
PersonalityService, ScoringService, TrendService, and RecommendationService.
"""

import pytest
from app.services.palm_service import PalmService
from app.services.tarot_service import TarotService
from app.services.interpretation_service import InterpretationService
from app.services.personality_service import PersonalityService
from app.services.scoring_service import ScoringService
from app.services.trend_service import TrendService
from app.services.recommendation_service import RecommendationService
from app.services.report_service import ReportService


# ============================================================================
# PalmService Tests
# ============================================================================

class TestPalmService:
    """Tests for the palm analysis service."""

    def test_analyze_palm_returns_valid_structure(self):
        result = PalmService.analyze_palm()
        assert "hand_shape" in result
        assert "lines" in result
        assert "personality_traits" in result
        assert "confidence_score" in result
        assert "narrative" in result

    def test_analyze_palm_hand_shape(self):
        result = PalmService.analyze_palm()
        hand_shape = result["hand_shape"]
        assert "type" in hand_shape
        assert "element" in hand_shape
        assert hand_shape["element"] in ["Earth", "Air", "Water", "Fire"]

    def test_analyze_palm_detects_lines(self):
        result = PalmService.analyze_palm()
        lines = result["lines"]
        assert len(lines) >= 3  # At least heart, head, life
        for line in lines:
            assert "line_name" in line
            assert "detected" in line
            assert "confidence" in line

    def test_analyze_palm_personality_traits(self):
        result = PalmService.analyze_palm()
        traits = result["personality_traits"]
        assert len(traits) >= 4
        for trait in traits:
            assert "trait" in trait
            assert "score" in trait
            assert 0 <= trait["score"] <= 100

    def test_analyze_palm_with_seed_deterministic(self):
        r1 = PalmService.analyze_palm(user_seed="test123")
        r2 = PalmService.analyze_palm(user_seed="test123")
        assert r1["hand_shape"]["type"] == r2["hand_shape"]["type"]

    def test_confidence_score_in_range(self):
        result = PalmService.analyze_palm()
        assert 0 < result["confidence_score"] <= 1.0


# ============================================================================
# TarotService Tests
# ============================================================================

class TestTarotService:
    """Tests for the tarot reading service."""

    def test_generate_reading_three_card(self):
        result = TarotService.generate_reading("three_card")
        assert "cards" in result
        assert len(result["cards"]) == 3
        assert "themes" in result
        assert "elemental_balance" in result

    def test_generate_reading_celtic_cross(self):
        result = TarotService.generate_reading("celtic_cross")
        assert len(result["cards"]) == 10

    def test_generate_reading_single_card(self):
        result = TarotService.generate_reading("single")
        assert len(result["cards"]) == 1

    def test_card_structure(self):
        result = TarotService.generate_reading("three_card")
        for card in result["cards"]:
            assert "card_name" in card
            assert "orientation" in card
            assert card["orientation"] in ["upright", "reversed"]
            assert "position" in card
            assert "arcana" in card

    def test_elemental_balance(self):
        result = TarotService.generate_reading("three_card")
        balance = result["elemental_balance"]
        assert "Fire" in balance
        assert "Water" in balance
        assert "Air" in balance
        assert "Earth" in balance

    def test_confidence_score_present(self):
        result = TarotService.generate_reading("three_card")
        assert "confidence_score" in result
        assert 0 < result["confidence_score"] <= 1.0

    def test_themes_generated(self):
        result = TarotService.generate_reading("celtic_cross")
        assert isinstance(result["themes"], list)
        assert len(result["themes"]) > 0


# ============================================================================
# InterpretationService Tests
# ============================================================================

class TestInterpretationService:
    """Tests for the AI interpretation engine."""

    def test_generate_palm_interpretation(self, sample_palm_analysis):
        result = InterpretationService.generate_palm_interpretation(sample_palm_analysis)
        assert result["source"] == "palm"
        assert "insights" in result
        assert len(result["insights"]) == 7

    def test_generate_tarot_interpretation(self, sample_tarot_reading):
        result = InterpretationService.generate_tarot_interpretation(sample_tarot_reading)
        assert result["source"] == "tarot"
        assert "insights" in result
        assert "themes" in result

    def test_generate_combined_interpretation(self, sample_palm_analysis, sample_tarot_reading):
        result = InterpretationService.generate_combined_interpretation(
            sample_palm_analysis, sample_tarot_reading
        )
        assert result["source"] == "combined"
        assert "insight_score" in result
        assert "scoring_breakdown" in result
        assert 0 < result["insight_score"] <= 1.0

    def test_insight_categories(self, sample_palm_analysis, sample_tarot_reading):
        result = InterpretationService.generate_combined_interpretation(
            sample_palm_analysis, sample_tarot_reading
        )
        expected_categories = [
            "personality", "relationships", "career", "finance",
            "health_wellness", "personal_growth", "life_opportunities",
        ]
        for cat in expected_categories:
            assert cat in result["insights"]
            insight = result["insights"][cat]
            assert "score" in insight
            assert "sentiment" in insight
            assert "narrative" in insight

    def test_scoring_breakdown_weights(self, sample_palm_analysis, sample_tarot_reading):
        result = InterpretationService.generate_combined_interpretation(
            sample_palm_analysis, sample_tarot_reading
        )
        breakdown = result["scoring_breakdown"]
        assert breakdown["palm_analysis_confidence"]["weight"] == "30%"
        assert breakdown["tarot_interpretation_relevance"]["weight"] == "25%"
        assert breakdown["personality_alignment"]["weight"] == "20%"
        assert breakdown["user_context_relevance"]["weight"] == "15%"
        assert breakdown["reading_consistency"]["weight"] == "10%"

    def test_get_insight_categories(self):
        categories = InterpretationService.get_insight_categories()
        assert len(categories) == 7


# ============================================================================
# PersonalityService Tests
# ============================================================================

class TestPersonalityService:
    """Tests for the personality intelligence module."""

    def test_generate_personality_profile(self, sample_palm_analysis):
        result = PersonalityService.generate_personality_profile(sample_palm_analysis)
        assert "big_five_traits" in result
        assert "archetype" in result
        assert "strengths" in result
        assert "weaknesses" in result
        assert "behavioral_insights" in result

    def test_big_five_traits_present(self, sample_palm_analysis):
        result = PersonalityService.generate_personality_profile(sample_palm_analysis)
        big_five = result["big_five_traits"]
        expected = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        for trait in expected:
            assert trait in big_five
            assert "score" in big_five[trait]
            assert 25 <= big_five[trait]["score"] <= 95

    def test_archetype_has_name(self, sample_palm_analysis):
        result = PersonalityService.generate_personality_profile(sample_palm_analysis)
        archetype = result["archetype"]
        assert "name" in archetype
        assert "description" in archetype

    def test_strengths_identified(self, sample_palm_analysis):
        result = PersonalityService.generate_personality_profile(sample_palm_analysis)
        assert len(result["strengths"]) >= 2

    def test_behavioral_insights_structure(self, sample_palm_analysis):
        result = PersonalityService.generate_personality_profile(sample_palm_analysis)
        behavioral = result["behavioral_insights"]
        expected_keys = ["decision_making", "stress_response", "communication_style", "learning_style"]
        for key in expected_keys:
            assert key in behavioral
            assert "style" in behavioral[key]

    def test_personality_summary(self, sample_palm_analysis):
        profile = PersonalityService.generate_personality_profile(sample_palm_analysis)
        summary = PersonalityService.get_personality_summary(profile)
        assert "archetype_name" in summary
        assert "dominant_trait" in summary

    def test_with_tarot_influence(self, sample_palm_analysis, sample_tarot_reading):
        result = PersonalityService.generate_personality_profile(
            sample_palm_analysis, sample_tarot_reading
        )
        assert result["tarot_personality_influence"] is not None
        assert "major_arcana_count" in result["tarot_personality_influence"]


# ============================================================================
# ScoringService Tests
# ============================================================================

class TestScoringService:
    """Tests for the spiritual guidance scoring engine."""

    def test_calculate_insight_score(self, sample_palm_analysis, sample_tarot_reading):
        result = ScoringService.calculate_insight_score(
            palm_analysis=sample_palm_analysis,
            tarot_reading=sample_tarot_reading,
        )
        assert "insight_score" in result
        assert "quality" in result
        assert "factors" in result
        assert 0 < result["insight_score"] <= 1.0

    def test_five_factors_present(self, sample_palm_analysis, sample_tarot_reading):
        result = ScoringService.calculate_insight_score(
            palm_analysis=sample_palm_analysis,
            tarot_reading=sample_tarot_reading,
        )
        factors = result["factors"]
        expected = [
            "palm_analysis_confidence",
            "tarot_interpretation_relevance",
            "personality_alignment",
            "user_context_relevance",
            "reading_consistency",
        ]
        for factor in expected:
            assert factor in factors
            assert "weight" in factors[factor]
            assert "raw_score" in factors[factor]
            assert "grade" in factors[factor]

    def test_quality_tiers(self, sample_palm_analysis, sample_tarot_reading):
        result = ScoringService.calculate_insight_score(
            palm_analysis=sample_palm_analysis,
            tarot_reading=sample_tarot_reading,
        )
        assert result["quality"] in ["exceptional", "strong", "good", "moderate", "developing"]

    def test_self_development_score(self, sample_palm_analysis):
        profile = PersonalityService.generate_personality_profile(sample_palm_analysis)
        recommendations = RecommendationService.generate_recommendations(sample_palm_analysis)
        result = ScoringService.calculate_self_development_score(
            profile, recommendations.get("top_recommendations", [])
        )
        assert "overall_score" in result
        assert "level" in result
        assert "next_steps" in result

    def test_guidance_relevance(self):
        recommendations = [
            {"category": "goal_alignment", "priority": "high"},
            {"category": "personal_growth", "priority": "medium"},
        ]
        result = ScoringService.calculate_guidance_relevance(recommendations)
        assert "score" in result
        assert "level" in result


# ============================================================================
# TrendService Tests
# ============================================================================

class TestTrendService:
    """Tests for the life trend analysis engine."""

    def test_analyze_life_trends(self, sample_palm_analysis):
        result = TrendService.analyze_life_trends(sample_palm_analysis)
        assert "trends" in result
        assert "opportunities" in result
        assert "challenges" in result
        assert "growth_potential" in result
        assert "overall_trajectory" in result

    def test_trend_categories(self, sample_palm_analysis):
        result = TrendService.analyze_life_trends(sample_palm_analysis)
        expected = ["emotional", "professional", "spiritual", "vitality", "creativity"]
        for cat in expected:
            assert cat in result["trends"]
            trend = result["trends"][cat]
            assert "score" in trend
            assert "direction" in trend
            assert trend["direction"] in ["ascending", "stable", "transitioning", "resting"]

    def test_growth_potential(self, sample_palm_analysis):
        result = TrendService.analyze_life_trends(sample_palm_analysis)
        growth = result["growth_potential"]
        assert "overall_score" in growth
        assert "phase" in growth
        assert growth["phase"] in ["Expansion", "Cultivation", "Preparation", "Gestation"]

    def test_overall_trajectory(self, sample_palm_analysis):
        result = TrendService.analyze_life_trends(sample_palm_analysis)
        trajectory = result["overall_trajectory"]
        assert "direction" in trajectory
        assert "score" in trajectory
        assert "message" in trajectory

    def test_trend_summary(self, sample_palm_analysis):
        analysis = TrendService.analyze_life_trends(sample_palm_analysis)
        summary = TrendService.get_trend_summary(analysis)
        assert "overall_direction" in summary
        assert "momentum_score" in summary


# ============================================================================
# RecommendationService Tests
# ============================================================================

class TestRecommendationService:
    """Tests for the recommendation engine."""

    def test_generate_recommendations(self, sample_palm_analysis):
        result = RecommendationService.generate_recommendations(sample_palm_analysis)
        assert "personal_growth" in result
        assert "relationship_guidance" in result
        assert "career_suggestions" in result
        assert "spiritual_development" in result
        assert "top_recommendations" in result

    def test_top_recommendations_ranked(self, sample_palm_analysis):
        result = RecommendationService.generate_recommendations(sample_palm_analysis)
        top = result["top_recommendations"]
        assert len(top) <= 5
        for i, rec in enumerate(top):
            assert rec["rank"] == i + 1

    def test_goal_alignment_with_context(self, sample_palm_analysis, sample_user_context):
        result = RecommendationService.generate_recommendations(
            sample_palm_analysis, user_context=sample_user_context
        )
        goal_recs = result["goal_alignment"]
        assert len(goal_recs) >= 1  # At least one from the goals

    def test_daily_recommendation(self):
        trait_scores = {"Emotional Intelligence": 75, "Career Drive": 60}
        result = RecommendationService.get_daily_recommendation(trait_scores)
        assert "recommendation" in result
        assert "date" in result


# ============================================================================
# ReportService Tests
# ============================================================================

class TestReportService:
    """Tests for the report generation service."""

    def test_generate_palm_report(self, sample_palm_analysis):
        report = ReportService.generate_palm_report(sample_palm_analysis)
        assert report["report_type"] == "palmistry"
        assert "title" in report
        assert "sections" in report
        assert len(report["sections"]) >= 3

    def test_generate_tarot_report(self, sample_tarot_reading):
        report = ReportService.generate_tarot_report(sample_tarot_reading)
        assert report["report_type"] == "tarot"
        assert "sections" in report

    def test_generate_personality_report(self, sample_palm_analysis):
        profile = PersonalityService.generate_personality_profile(sample_palm_analysis)
        report = ReportService.generate_personality_report(profile)
        assert report["report_type"] == "personality"
        assert len(report["sections"]) >= 5

    def test_export_to_csv(self, sample_palm_analysis):
        report = ReportService.generate_palm_report(sample_palm_analysis)
        csv = ReportService.export_to_csv(report)
        assert isinstance(csv, str)
        assert "palmistry" in csv.lower()

    def test_export_to_json(self, sample_palm_analysis):
        report = ReportService.generate_palm_report(sample_palm_analysis)
        json_str = ReportService.export_to_json(report)
        assert isinstance(json_str, str)
        assert "palmistry" in json_str

    def test_report_summary(self, sample_palm_analysis):
        report = ReportService.generate_palm_report(sample_palm_analysis)
        summary = ReportService.generate_report_summary(report)
        assert "type" in summary
        assert "title" in summary
