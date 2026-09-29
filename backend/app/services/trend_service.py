"""
Life Trend Analysis Engine
===========================
Analyzes reading history to identify life path patterns,
opportunity windows, challenge forecasting, and growth potential.
"""

import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from collections import Counter


# ============================================================================
# Trend Categories & Pattern Definitions
# ============================================================================

TREND_CATEGORIES = {
    "emotional": {
        "name": "Emotional Trajectory",
        "icon": "heart",
        "color": "from-pink-500 to-rose-500",
        "description": "Patterns in emotional well-being, relationships, and inner harmony",
    },
    "professional": {
        "name": "Professional Momentum",
        "icon": "briefcase",
        "color": "from-amber-500 to-orange-500",
        "description": "Career trajectory, professional growth, and work satisfaction trends",
    },
    "spiritual": {
        "name": "Spiritual Evolution",
        "icon": "sparkles",
        "color": "from-violet-500 to-purple-500",
        "description": "Spiritual awareness, intuitive development, and inner wisdom growth",
    },
    "vitality": {
        "name": "Life Vitality",
        "icon": "zap",
        "color": "from-emerald-500 to-teal-500",
        "description": "Energy levels, physical well-being, and overall life force",
    },
    "creativity": {
        "name": "Creative Flow",
        "icon": "palette",
        "color": "from-cyan-500 to-blue-500",
        "description": "Creative expression, artistic potential, and innovative thinking",
    },
}

OPPORTUNITY_TYPES = [
    {
        "type": "career_pivot",
        "title": "Career Transition Window",
        "description": "Conditions are favorable for professional changes or new ventures.",
        "triggers": ["Career Drive", "Analytical Thinking"],
        "threshold": 75,
    },
    {
        "type": "relationship_deepening",
        "title": "Relationship Deepening Period",
        "description": "Emotional energies support deeper connections and relationship growth.",
        "triggers": ["Emotional Intelligence", "Intuitive Awareness"],
        "threshold": 70,
    },
    {
        "type": "creative_breakthrough",
        "title": "Creative Breakthrough Phase",
        "description": "Heightened creative energy indicates potential for artistic or innovative achievements.",
        "triggers": ["Creative Expression", "Intuitive Awareness"],
        "threshold": 72,
    },
    {
        "type": "self_discovery",
        "title": "Self-Discovery Journey",
        "description": "A period of profound self-understanding and personal revelation is unfolding.",
        "triggers": ["Intuitive Awareness", "Emotional Intelligence"],
        "threshold": 68,
    },
    {
        "type": "leadership_emergence",
        "title": "Leadership Opportunity",
        "description": "Your qualities are aligning for leadership roles and increased influence.",
        "triggers": ["Career Drive", "Vitality & Resilience"],
        "threshold": 75,
    },
]

CHALLENGE_TYPES = [
    {
        "type": "emotional_turbulence",
        "title": "Emotional Processing Phase",
        "description": "A period of emotional intensity that requires patience and self-compassion.",
        "mitigation": "Practice grounding techniques: meditation, journaling, or spending time in nature. These emotions carry wisdom.",
        "triggers": ["Emotional Intelligence"],
        "threshold": 45,
    },
    {
        "type": "career_uncertainty",
        "title": "Professional Crossroads",
        "description": "Career direction may feel unclear. This is a normal phase of professional evolution.",
        "mitigation": "Focus on skill development and network building rather than forcing decisions. Clarity will emerge.",
        "triggers": ["Career Drive"],
        "threshold": 45,
    },
    {
        "type": "energy_depletion",
        "title": "Energy Restoration Needed",
        "description": "Vital energy reserves may be running low. Prioritize rest and regeneration.",
        "mitigation": "Implement non-negotiable self-care routines. Quality sleep, nutrition, and gentle movement are your allies.",
        "triggers": ["Vitality & Resilience"],
        "threshold": 45,
    },
    {
        "type": "creative_block",
        "title": "Creative Gestation Period",
        "description": "Creative flow may feel blocked, but this is often a period of subconscious preparation.",
        "mitigation": "Change your environment, consume inspiring content, and release the pressure to produce. Creativity will return naturally.",
        "triggers": ["Creative Expression"],
        "threshold": 40,
    },
]


class TrendService:
    """Life trend analysis engine for pattern recognition and forecasting."""

    @staticmethod
    def analyze_life_trends(
        palm_analysis: Dict[str, Any],
        tarot_reading: Optional[Dict[str, Any]] = None,
        reading_history: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze life trends from current readings and historical data.
        Returns trend trajectories, opportunities, challenges, and growth assessment.
        """
        personality_traits = palm_analysis.get("personality_traits", [])
        trait_scores = {t["trait"]: t["score"] for t in personality_traits}
        hand_shape = palm_analysis.get("hand_shape", {})

        # Calculate trend scores
        trends = _calculate_trend_scores(trait_scores, hand_shape, tarot_reading)

        # Identify opportunities
        opportunities = _identify_opportunities(trait_scores)

        # Forecast challenges
        challenges = _forecast_challenges(trait_scores)

        # Calculate growth potential
        growth_potential = _assess_growth_potential(
            trait_scores, trends, reading_history
        )

        # Generate life path narrative
        life_path = _generate_life_path_analysis(
            trends, opportunities, challenges, hand_shape
        )

        # Historical trend comparison (if history available)
        historical = _analyze_historical_trends(reading_history)

        return {
            "trends": trends,
            "opportunities": opportunities,
            "challenges": challenges,
            "growth_potential": growth_potential,
            "life_path_analysis": life_path,
            "historical_trends": historical,
            "overall_trajectory": _calculate_overall_trajectory(trends),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def get_trend_summary(analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Get a concise trend summary for dashboard display."""
        trends = analysis.get("trends", {})
        trajectory = analysis.get("overall_trajectory", {})
        opportunities = analysis.get("opportunities", [])
        challenges = analysis.get("challenges", [])

        return {
            "overall_direction": trajectory.get("direction", "stable"),
            "momentum_score": trajectory.get("score", 65),
            "top_trend": max(trends.values(), key=lambda t: t.get("score", 0)) if trends else None,
            "active_opportunities": len(opportunities),
            "active_challenges": len(challenges),
            "key_message": trajectory.get("message", "Your life trajectory shows balanced momentum."),
        }


# ============================================================================
# Private Helpers
# ============================================================================

def _calculate_trend_scores(
    trait_scores: Dict[str, int],
    hand_shape: Dict,
    tarot_reading: Optional[Dict],
) -> Dict[str, Dict[str, Any]]:
    """Calculate trend scores across all categories."""
    element = hand_shape.get("element", "Earth")
    trends = {}

    # Map traits to trend categories
    trait_to_trend = {
        "emotional": ["Emotional Intelligence", "Intuitive Awareness"],
        "professional": ["Career Drive", "Analytical Thinking"],
        "spiritual": ["Intuitive Awareness", "Creative Expression"],
        "vitality": ["Vitality & Resilience", "Career Drive"],
        "creativity": ["Creative Expression", "Intuitive Awareness"],
    }

    element_modifiers = {
        "emotional": {"Water": 8, "Fire": 3, "Air": 0, "Earth": -3},
        "professional": {"Earth": 8, "Fire": 5, "Air": 3, "Water": -3},
        "spiritual": {"Water": 10, "Air": 5, "Fire": 3, "Earth": -5},
        "vitality": {"Fire": 8, "Earth": 5, "Air": 0, "Water": -3},
        "creativity": {"Water": 8, "Air": 5, "Fire": 3, "Earth": -5},
    }

    rng = random.Random(hash(str(trait_scores) + element))

    for trend_id, trend_def in TREND_CATEGORIES.items():
        source_traits = trait_to_trend.get(trend_id, [])
        scores = [trait_scores.get(t, 60) for t in source_traits]
        base_score = sum(scores) / max(len(scores), 1)

        # Apply element modifier
        elem_mod = element_modifiers.get(trend_id, {}).get(element, 0)
        score = int(base_score + elem_mod + rng.randint(-5, 5))
        score = max(25, min(95, score))

        # Determine direction
        if score >= 75:
            direction = "ascending"
            momentum = "strong"
        elif score >= 60:
            direction = "stable"
            momentum = "steady"
        elif score >= 45:
            direction = "transitioning"
            momentum = "shifting"
        else:
            direction = "resting"
            momentum = "gathering"

        # Tarot influence
        tarot_modifier = 0
        if tarot_reading:
            themes = tarot_reading.get("themes", [])
            energy = tarot_reading.get("narrative", {}).get("energy_tone", "balanced")
            if "positive" in energy:
                tarot_modifier = rng.randint(3, 8)
            elif "reflection" in energy or "challenge" in energy:
                tarot_modifier = rng.randint(-5, 0)

        final_score = max(25, min(95, score + tarot_modifier))

        trends[trend_id] = {
            **trend_def,
            "score": final_score,
            "direction": direction,
            "momentum": momentum,
            "element_influence": element,
            "tarot_influence": tarot_modifier,
        }

    return trends


def _identify_opportunities(trait_scores: Dict[str, int]) -> List[Dict[str, Any]]:
    """Identify current life opportunities based on trait scores."""
    opportunities = []

    for opp in OPPORTUNITY_TYPES:
        trigger_scores = [trait_scores.get(t, 60) for t in opp["triggers"]]
        avg_score = sum(trigger_scores) / max(len(trigger_scores), 1)

        if avg_score >= opp["threshold"]:
            strength = "strong" if avg_score >= 80 else "emerging"
            opportunities.append({
                "type": opp["type"],
                "title": opp["title"],
                "description": opp["description"],
                "strength": strength,
                "alignment_score": int(avg_score),
                "timing": "current" if avg_score >= 80 else "approaching",
            })

    return opportunities


def _forecast_challenges(trait_scores: Dict[str, int]) -> List[Dict[str, Any]]:
    """Forecast potential challenges based on trait scores."""
    challenges = []

    for challenge in CHALLENGE_TYPES:
        trigger_scores = [trait_scores.get(t, 60) for t in challenge["triggers"]]
        avg_score = sum(trigger_scores) / max(len(trigger_scores), 1)

        if avg_score <= challenge["threshold"]:
            severity = "significant" if avg_score <= 35 else "mild"
            challenges.append({
                "type": challenge["type"],
                "title": challenge["title"],
                "description": challenge["description"],
                "mitigation": challenge["mitigation"],
                "severity": severity,
                "awareness_score": int(avg_score),
            })

    return challenges


def _assess_growth_potential(
    trait_scores: Dict[str, int],
    trends: Dict[str, Dict],
    reading_history: Optional[List[Dict]],
) -> Dict[str, Any]:
    """Assess overall growth potential."""
    avg_trait = sum(trait_scores.values()) / max(len(trait_scores), 1)
    ascending_count = sum(
        1 for t in trends.values() if t.get("direction") == "ascending"
    )
    total_trends = len(trends)

    growth_score = int(
        avg_trait * 0.5
        + (ascending_count / max(total_trends, 1)) * 50
    )
    growth_score = max(30, min(95, growth_score))

    # Determine growth phase
    if growth_score >= 80:
        phase = "Expansion"
        message = "You are in a powerful expansion phase. Multiple areas of life are growing simultaneously. Embrace the momentum."
    elif growth_score >= 65:
        phase = "Cultivation"
        message = "Seeds of growth are taking root. Continue nurturing your development with patience and consistency."
    elif growth_score >= 50:
        phase = "Preparation"
        message = "You are in a preparation phase, building the foundation for future growth. This groundwork is essential."
    else:
        phase = "Gestation"
        message = "A period of quiet gestation. Important transformations are happening beneath the surface. Trust the process."

    # Areas of highest growth potential
    potential_areas = []
    for trait, score in sorted(trait_scores.items(), key=lambda x: x[1]):
        if score < 70:  # Room for growth
            potential_areas.append({
                "area": trait,
                "current_score": score,
                "growth_room": 95 - score,
                "priority": "high" if score < 50 else "medium",
            })

    return {
        "overall_score": growth_score,
        "phase": phase,
        "message": message,
        "potential_areas": potential_areas[:5],
        "reading_count": len(reading_history) if reading_history else 0,
    }


def _generate_life_path_analysis(
    trends: Dict,
    opportunities: List[Dict],
    challenges: List[Dict],
    hand_shape: Dict,
) -> Dict[str, str]:
    """Generate a narrative life path analysis."""
    element = hand_shape.get("element", "Earth")
    shape_type = hand_shape.get("type", "Unknown Hand")

    ascending = [t for t in trends.values() if t.get("direction") == "ascending"]
    resting = [t for t in trends.values() if t.get("direction") == "resting"]

    summary = f"Your life path, shaped by your {shape_type} and {element} elemental nature, reveals a journey of "

    if len(ascending) >= 3:
        summary += "remarkable momentum and multi-dimensional growth. Several key life areas are experiencing upward movement simultaneously."
    elif len(ascending) >= 1:
        summary += "focused growth and selective development. Key areas of your life are advancing while others provide stable support."
    elif resting:
        summary += "contemplation and preparation. This is a period of inner work that will fuel future expansion."
    else:
        summary += "steady navigation and balanced progress across life dimensions."

    # Opportunity summary
    opp_text = ""
    if opportunities:
        opp_names = [o["title"] for o in opportunities[:3]]
        opp_text = f" Active opportunities include: {', '.join(opp_names)}. Stay alert and ready to act."

    # Challenge summary
    challenge_text = ""
    if challenges:
        challenge_names = [c["title"] for c in challenges[:2]]
        challenge_text = f" Areas requiring attention: {', '.join(challenge_names)}. Approach these with patience and self-compassion."

    return {
        "summary": summary + opp_text + challenge_text,
        "element_influence": f"As a {element} dominant personality, you naturally align with {_element_path_description(element)}.",
        "guidance": _generate_path_guidance(element, ascending, opportunities),
    }


def _element_path_description(element: str) -> str:
    """Get element-specific path description."""
    descriptions = {
        "Earth": "steady, practical progress. Your path unfolds through consistent effort and reliable growth",
        "Air": "intellectual discovery and social connection. Your path unfolds through ideas, communication, and mental exploration",
        "Water": "emotional depth and intuitive flow. Your path unfolds through feeling, empathy, and creative expression",
        "Fire": "passionate action and bold initiative. Your path unfolds through courage, energy, and enthusiastic pursuit",
    }
    return descriptions.get(element, "balanced multi-dimensional growth")


def _generate_path_guidance(
    element: str, ascending: List[Dict], opportunities: List[Dict]
) -> str:
    """Generate personalized path guidance."""
    if ascending and opportunities:
        return (
            "The alignment of ascending trends and active opportunities suggests this is a pivotal moment. "
            "Take decisive action where opportunities call to you, while maintaining the momentum in your growing areas."
        )
    elif ascending:
        return (
            "Your ascending trends indicate positive movement. Focus on sustaining this momentum through consistent effort "
            "and remain open to opportunities that may emerge from this growth."
        )
    elif opportunities:
        return (
            "Opportunities are presenting themselves even during a quieter phase. Evaluate them carefully and choose "
            "those that align with your deepest values and long-term vision."
        )
    else:
        return (
            "This is a period of quiet preparation. Use this time for reflection, skill development, and self-care. "
            "The next wave of growth is building beneath the surface."
        )


def _analyze_historical_trends(
    reading_history: Optional[List[Dict]],
) -> Dict[str, Any]:
    """Analyze trends from reading history."""
    if not reading_history:
        return {
            "available": False,
            "message": "Complete more readings to unlock historical trend analysis.",
            "readings_needed": 3,
        }

    total_readings = len(reading_history)
    completed = [r for r in reading_history if r.get("status") == "completed"]
    avg_confidence = (
        sum(r.get("confidence_score", 0.7) for r in completed) / max(len(completed), 1)
    )

    reading_types = Counter(r.get("reading_type", "unknown") for r in reading_history)

    return {
        "available": True,
        "total_readings": total_readings,
        "completed_readings": len(completed),
        "average_confidence": round(avg_confidence, 4),
        "reading_type_distribution": dict(reading_types),
        "engagement_level": "high" if total_readings >= 10 else "moderate" if total_readings >= 5 else "growing",
    }


def _calculate_overall_trajectory(trends: Dict[str, Dict]) -> Dict[str, Any]:
    """Calculate the overall life trajectory from all trends."""
    if not trends:
        return {"direction": "stable", "score": 60, "message": "Balanced life trajectory."}

    scores = [t.get("score", 60) for t in trends.values()]
    avg_score = sum(scores) / len(scores)

    ascending = sum(1 for t in trends.values() if t.get("direction") == "ascending")
    resting = sum(1 for t in trends.values() if t.get("direction") == "resting")

    if avg_score >= 75 and ascending >= 3:
        direction = "strongly_ascending"
        message = "Your life trajectory shows powerful upward momentum across multiple dimensions. This is a remarkable period of growth and opportunity."
    elif avg_score >= 65:
        direction = "ascending"
        message = "Positive momentum is building in your life. Key areas are growing while others provide stable foundation."
    elif avg_score >= 50:
        direction = "stable"
        message = "Your life trajectory is stable and balanced. This is a period of consolidation and preparation for future growth."
    elif resting >= 3:
        direction = "restorative"
        message = "Multiple life areas are in a restorative phase. Honor this period of rest — it fuels future expansion."
    else:
        direction = "transitioning"
        message = "You are in a transition period. Old patterns are dissolving to make room for new ones. Embrace the change."

    return {
        "direction": direction,
        "score": int(avg_score),
        "message": message,
        "ascending_count": ascending,
        "total_dimensions": len(trends),
    }
