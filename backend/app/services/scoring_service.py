"""
Spiritual Guidance Scoring Engine
==================================
Implements the 5-factor weighted scoring model:
  - Palm Analysis Confidence: 30%
  - Tarot Interpretation Relevance: 25%
  - Personality Alignment: 20%
  - User Context Relevance: 15%
  - Reading Consistency: 10%

Provides personality alignment, reading confidence, guidance relevance,
self-development, and overall insight scoring.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import math


class ScoringService:
    """Spiritual guidance scoring engine with weighted multi-factor model."""

    @staticmethod
    def calculate_insight_score(
        palm_analysis: Optional[Dict[str, Any]] = None,
        tarot_reading: Optional[Dict[str, Any]] = None,
        personality_profile: Optional[Dict[str, Any]] = None,
        user_context: Optional[Dict[str, Any]] = None,
        reading_history: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Calculate the comprehensive 5-factor weighted insight score.
        """
        # Factor 1: Palm Analysis Confidence (30%)
        palm_confidence = _calculate_palm_confidence(palm_analysis)

        # Factor 2: Tarot Interpretation Relevance (25%)
        tarot_relevance = _calculate_tarot_relevance(tarot_reading)

        # Factor 3: Personality Alignment (20%)
        personality_alignment = _calculate_personality_alignment(
            palm_analysis, tarot_reading, personality_profile
        )

        # Factor 4: User Context Relevance (15%)
        context_relevance = _calculate_context_relevance(
            user_context, palm_analysis, tarot_reading
        )

        # Factor 5: Reading Consistency (10%)
        reading_consistency = _calculate_reading_consistency(
            palm_analysis, tarot_reading, reading_history
        )

        # Weighted composite score
        insight_score = (
            palm_confidence["score"] * 0.30
            + tarot_relevance["score"] * 0.25
            + personality_alignment["score"] * 0.20
            + context_relevance["score"] * 0.15
            + reading_consistency["score"] * 0.10
        )

        # Determine quality tier
        if insight_score >= 0.85:
            quality = "exceptional"
            quality_description = "This reading achieves exceptional clarity and alignment across all dimensions."
        elif insight_score >= 0.70:
            quality = "strong"
            quality_description = "This reading provides strong, reliable guidance with high confidence."
        elif insight_score >= 0.55:
            quality = "good"
            quality_description = "This reading offers solid insights with room for deeper exploration."
        elif insight_score >= 0.40:
            quality = "moderate"
            quality_description = "This reading provides useful directional guidance. Consider additional readings for clarity."
        else:
            quality = "developing"
            quality_description = "This reading offers initial insights. More data will strengthen future readings."

        return {
            "insight_score": round(insight_score, 4),
            "quality": quality,
            "quality_description": quality_description,
            "factors": {
                "palm_analysis_confidence": {
                    "weight": "30%",
                    "raw_score": round(palm_confidence["score"], 4),
                    "weighted_contribution": round(palm_confidence["score"] * 0.30, 4),
                    "details": palm_confidence["details"],
                    "grade": _score_to_grade(palm_confidence["score"]),
                },
                "tarot_interpretation_relevance": {
                    "weight": "25%",
                    "raw_score": round(tarot_relevance["score"], 4),
                    "weighted_contribution": round(tarot_relevance["score"] * 0.25, 4),
                    "details": tarot_relevance["details"],
                    "grade": _score_to_grade(tarot_relevance["score"]),
                },
                "personality_alignment": {
                    "weight": "20%",
                    "raw_score": round(personality_alignment["score"], 4),
                    "weighted_contribution": round(personality_alignment["score"] * 0.20, 4),
                    "details": personality_alignment["details"],
                    "grade": _score_to_grade(personality_alignment["score"]),
                },
                "user_context_relevance": {
                    "weight": "15%",
                    "raw_score": round(context_relevance["score"], 4),
                    "weighted_contribution": round(context_relevance["score"] * 0.15, 4),
                    "details": context_relevance["details"],
                    "grade": _score_to_grade(context_relevance["score"]),
                },
                "reading_consistency": {
                    "weight": "10%",
                    "raw_score": round(reading_consistency["score"], 4),
                    "weighted_contribution": round(reading_consistency["score"] * 0.10, 4),
                    "details": reading_consistency["details"],
                    "grade": _score_to_grade(reading_consistency["score"]),
                },
            },
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def calculate_self_development_score(
        personality_profile: Dict[str, Any],
        recommendations: List[Dict],
        reading_history: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """Calculate a self-development readiness and progress score."""
        big_five = personality_profile.get("big_five_traits", {})
        strengths = personality_profile.get("strengths", [])
        weaknesses = personality_profile.get("weaknesses", [])

        # Trait balance score (how balanced are the Big Five)
        scores = [t.get("score", 50) for t in big_five.values()]
        avg = sum(scores) / max(len(scores), 1)
        variance = sum((s - avg) ** 2 for s in scores) / max(len(scores), 1)
        balance_score = max(0.3, 1.0 - math.sqrt(variance) / 100)

        # Strength leverage potential
        strength_score = min(
            1.0, sum(s.get("score", 60) for s in strengths) / max(len(strengths) * 100, 1)
        )

        # Growth awareness (having identified weaknesses is positive)
        growth_awareness = min(1.0, 0.5 + len(weaknesses) * 0.15)

        # Action readiness (based on recommendation count)
        action_readiness = min(1.0, len(recommendations) * 0.1 + 0.3)

        # Historical engagement
        engagement = 0.5
        if reading_history:
            engagement = min(1.0, len(reading_history) * 0.05 + 0.3)

        overall = (
            balance_score * 0.25
            + strength_score * 0.25
            + growth_awareness * 0.20
            + action_readiness * 0.15
            + engagement * 0.15
        )

        return {
            "overall_score": round(overall, 4),
            "breakdown": {
                "trait_balance": round(balance_score, 4),
                "strength_leverage": round(strength_score, 4),
                "growth_awareness": round(growth_awareness, 4),
                "action_readiness": round(action_readiness, 4),
                "historical_engagement": round(engagement, 4),
            },
            "level": (
                "Advanced" if overall >= 0.75 else
                "Intermediate" if overall >= 0.55 else
                "Developing" if overall >= 0.35 else
                "Beginning"
            ),
            "next_steps": _generate_development_next_steps(overall, weaknesses),
        }

    @staticmethod
    def calculate_guidance_relevance(
        recommendations: List[Dict],
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Calculate how relevant the generated guidance is to the user."""
        if not recommendations:
            return {"score": 0.5, "level": "moderate", "message": "Generate recommendations to assess relevance."}

        # Check goal alignment
        goal_aligned = sum(1 for r in recommendations if r.get("category") == "goal_alignment")
        high_priority = sum(1 for r in recommendations if r.get("priority") == "high")
        total = len(recommendations)

        goal_ratio = goal_aligned / max(total, 1)
        priority_ratio = high_priority / max(total, 1)

        relevance = goal_ratio * 0.4 + priority_ratio * 0.3 + min(total / 10, 1.0) * 0.3

        return {
            "score": round(relevance, 4),
            "level": "high" if relevance >= 0.7 else "moderate" if relevance >= 0.4 else "developing",
            "goal_aligned_count": goal_aligned,
            "high_priority_count": high_priority,
            "total_recommendations": total,
            "message": (
                "Guidance is highly relevant to your stated goals and current needs."
                if relevance >= 0.7 else
                "Guidance provides useful direction. Setting more goals in your profile will increase relevance."
            ),
        }


# ============================================================================
# Private Factor Calculators
# ============================================================================

def _calculate_palm_confidence(palm_analysis: Optional[Dict]) -> Dict[str, Any]:
    """Factor 1: Palm Analysis Confidence."""
    if not palm_analysis:
        return {"score": 0.5, "details": "No palm analysis data available."}

    confidence = palm_analysis.get("confidence_score", 0.7)
    lines = palm_analysis.get("lines", [])
    detected_lines = sum(1 for l in lines if l.get("detected", True))
    total_lines = max(len(lines), 1)
    detection_ratio = detected_lines / total_lines

    hand_detected = palm_analysis.get("landmarks_detected", {}).get("hand_detected", True)

    score = confidence * 0.5 + detection_ratio * 0.3 + (0.2 if hand_detected else 0.0)

    details = (
        f"Palm confidence: {confidence:.2%}, "
        f"Lines detected: {detected_lines}/{total_lines}, "
        f"Hand landmark: {'detected' if hand_detected else 'not detected'}"
    )

    return {"score": min(max(score, 0.3), 0.98), "details": details}


def _calculate_tarot_relevance(tarot_reading: Optional[Dict]) -> Dict[str, Any]:
    """Factor 2: Tarot Interpretation Relevance."""
    if not tarot_reading:
        return {"score": 0.5, "details": "No tarot reading data available."}

    confidence = tarot_reading.get("confidence_score", 0.7)
    cards = tarot_reading.get("cards", [])
    themes = tarot_reading.get("themes", [])
    elemental = tarot_reading.get("elemental_balance", {})

    # Card quality factors
    major_count = sum(1 for c in cards if c.get("arcana") == "major")
    total = max(len(cards), 1)
    major_ratio = major_count / total

    # Theme richness
    theme_richness = min(1.0, len(themes) / 5)

    # Elemental diversity
    non_zero_elements = sum(1 for v in elemental.values() if v > 0)
    element_diversity = non_zero_elements / 4

    score = (
        confidence * 0.4
        + major_ratio * 0.2
        + theme_richness * 0.2
        + element_diversity * 0.2
    )

    details = (
        f"Tarot confidence: {confidence:.2%}, "
        f"Major Arcana: {major_count}/{total}, "
        f"Themes: {len(themes)}, "
        f"Elemental diversity: {non_zero_elements}/4"
    )

    return {"score": min(max(score, 0.3), 0.98), "details": details}


def _calculate_personality_alignment(
    palm_analysis: Optional[Dict],
    tarot_reading: Optional[Dict],
    personality_profile: Optional[Dict],
) -> Dict[str, Any]:
    """Factor 3: Personality Alignment between sources."""
    if not palm_analysis:
        return {"score": 0.6, "details": "Insufficient data for alignment calculation."}

    traits = palm_analysis.get("personality_traits", [])
    trait_scores = [t.get("score", 50) for t in traits]

    if not trait_scores:
        return {"score": 0.6, "details": "No personality trait data."}

    avg_score = sum(trait_scores) / len(trait_scores)
    # Higher average score = better alignment
    alignment = avg_score / 100

    # Check internal consistency (low variance = more aligned)
    variance = sum((s - avg_score) ** 2 for s in trait_scores) / len(trait_scores)
    consistency = max(0.3, 1.0 - math.sqrt(variance) / 50)

    score = alignment * 0.6 + consistency * 0.4

    details = (
        f"Average trait score: {avg_score:.1f}%, "
        f"Internal consistency: {consistency:.2%}"
    )

    return {"score": min(max(score, 0.3), 0.98), "details": details}


def _calculate_context_relevance(
    user_context: Optional[Dict],
    palm_analysis: Optional[Dict],
    tarot_reading: Optional[Dict],
) -> Dict[str, Any]:
    """Factor 4: User Context Relevance."""
    if not user_context:
        return {
            "score": 0.5,
            "details": "No user profile context. Set goals and interests to improve relevance.",
        }

    goals = user_context.get("spiritual_goals", [])
    interests = user_context.get("spiritual_interests", [])
    experience = user_context.get("experience_level", "beginner")

    # Goal coverage
    goal_score = min(1.0, len(goals) * 0.15 + 0.3)

    # Interest alignment
    interest_score = min(1.0, len(interests) * 0.1 + 0.3)

    # Experience factor (more experienced = better context)
    exp_scores = {"beginner": 0.5, "intermediate": 0.7, "advanced": 0.9}
    exp_score = exp_scores.get(experience, 0.5)

    score = goal_score * 0.4 + interest_score * 0.3 + exp_score * 0.3

    details = (
        f"Goals set: {len(goals)}, "
        f"Interests: {len(interests)}, "
        f"Experience: {experience}"
    )

    return {"score": min(max(score, 0.3), 0.98), "details": details}


def _calculate_reading_consistency(
    palm_analysis: Optional[Dict],
    tarot_reading: Optional[Dict],
    reading_history: Optional[List[Dict]],
) -> Dict[str, Any]:
    """Factor 5: Reading Consistency across sessions."""
    if not reading_history or len(reading_history) < 2:
        return {
            "score": 0.6,
            "details": "Insufficient reading history for consistency analysis. Complete 3+ readings.",
        }

    completed = [r for r in reading_history if r.get("status") == "completed"]
    if not completed:
        return {"score": 0.5, "details": "No completed readings in history."}

    # Confidence consistency
    confidences = [r.get("confidence_score", 0.7) for r in completed if r.get("confidence_score")]
    if confidences:
        avg_conf = sum(confidences) / len(confidences)
        conf_variance = sum((c - avg_conf) ** 2 for c in confidences) / len(confidences)
        consistency = max(0.3, 1.0 - math.sqrt(conf_variance) * 2)
    else:
        consistency = 0.6

    # Engagement consistency (regular readings)
    engagement = min(1.0, len(completed) * 0.08 + 0.3)

    score = consistency * 0.6 + engagement * 0.4

    details = (
        f"Completed readings: {len(completed)}, "
        f"Confidence consistency: {consistency:.2%}, "
        f"Engagement: {engagement:.2%}"
    )

    return {"score": min(max(score, 0.3), 0.98), "details": details}


def _score_to_grade(score: float) -> str:
    """Convert a score to a letter grade."""
    if score >= 0.9:
        return "A+"
    elif score >= 0.8:
        return "A"
    elif score >= 0.7:
        return "B+"
    elif score >= 0.6:
        return "B"
    elif score >= 0.5:
        return "C+"
    elif score >= 0.4:
        return "C"
    else:
        return "D"


def _generate_development_next_steps(
    overall: float, weaknesses: List[Dict]
) -> List[str]:
    """Generate next steps for self-development."""
    steps = []

    if overall < 0.4:
        steps.append("Complete your user profile with spiritual goals and interests.")
        steps.append("Perform at least 3 readings to build your insight baseline.")
    elif overall < 0.6:
        steps.append("Focus on your identified growth areas with daily practice.")
        steps.append("Try different reading types (palm, tarot, combined) for broader insights.")
    else:
        steps.append("Deepen your practice by exploring advanced tarot spreads.")
        steps.append("Track your progress by reviewing reading history trends monthly.")

    for w in weaknesses[:2]:
        area = w.get("area", w.get("trait", ""))
        growth_path = w.get("growth_path", "")
        if area and growth_path:
            steps.append(f"Growth area — {area}: {growth_path}")

    return steps[:5]
