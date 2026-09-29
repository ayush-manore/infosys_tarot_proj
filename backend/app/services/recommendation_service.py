"""
Recommendation Engine
======================
Generates personalized recommendations for personal growth,
relationships, career, goal alignment, and spiritual development
based on palm analysis, tarot readings, and user context.
"""

import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


# ============================================================================
# Recommendation Templates
# ============================================================================

GROWTH_RECOMMENDATIONS = {
    "high_emotional": [
        {
            "title": "Emotional Leadership Practice",
            "description": "Your high emotional intelligence is a superpower. Practice leading with empathy in one interaction daily — actively listen without judgment and reflect back what you hear.",
            "category": "personal_growth",
            "duration": "Daily, 10 minutes",
            "impact": "high",
        },
        {
            "title": "Emotional Journaling Ritual",
            "description": "Dedicate 15 minutes each evening to emotional processing through journaling. Write about three feelings you experienced and what triggered them.",
            "category": "wellness",
            "duration": "Daily, 15 minutes",
            "impact": "high",
        },
    ],
    "low_emotional": [
        {
            "title": "Empathy Building Exercise",
            "description": "Practice perspective-taking by imagining yourself in someone else's situation for 5 minutes daily. This builds emotional muscle over time.",
            "category": "personal_growth",
            "duration": "Daily, 5 minutes",
            "impact": "medium",
        },
    ],
    "high_analytical": [
        {
            "title": "Strategic Life Review",
            "description": "Apply your analytical strengths to life planning. Create a quarterly life review covering goals, relationships, career, and spiritual growth.",
            "category": "career",
            "duration": "Quarterly, 2 hours",
            "impact": "high",
        },
    ],
    "low_analytical": [
        {
            "title": "Decision Framework Practice",
            "description": "Build analytical confidence by using a simple pros/cons framework for daily decisions. Start small and gradually apply to bigger choices.",
            "category": "personal_growth",
            "duration": "As needed",
            "impact": "medium",
        },
    ],
    "high_vitality": [
        {
            "title": "Energy Channel Mastery",
            "description": "Your abundant energy is best directed with intention. Create a morning ritual that channels your vitality into your highest priorities.",
            "category": "wellness",
            "duration": "Daily, 20 minutes",
            "impact": "high",
        },
    ],
    "low_vitality": [
        {
            "title": "Gentle Restoration Protocol",
            "description": "Prioritize restorative practices: quality sleep, gentle movement like yoga or walking, and nourishing whole foods. Your body is asking for care.",
            "category": "wellness",
            "duration": "Daily, ongoing",
            "impact": "high",
        },
    ],
    "high_career": [
        {
            "title": "Professional Vision Mapping",
            "description": "Your strong career drive is ready for the next level. Create a 12-month professional development roadmap with specific milestones and skill targets.",
            "category": "career",
            "duration": "Monthly review",
            "impact": "high",
        },
    ],
    "low_career": [
        {
            "title": "Career Alignment Discovery",
            "description": "Explore what truly motivates you professionally. Try the Ikigai exercise — map the intersection of what you love, what you're good at, what the world needs, and what you can be paid for.",
            "category": "career",
            "duration": "One-time, 1 hour",
            "impact": "high",
        },
    ],
    "high_creative": [
        {
            "title": "Creative Expression Commitment",
            "description": "Your creative energy is peaking. Commit to one creative project — writing, art, music, or innovation — and dedicate focused time to it weekly.",
            "category": "personal_growth",
            "duration": "Weekly, 2 hours",
            "impact": "high",
        },
    ],
    "low_creative": [
        {
            "title": "Creativity Unblocking Practice",
            "description": "Engage in 'morning pages' — write three pages of stream-of-consciousness writing each morning. This bypasses your inner critic and awakens creative flow.",
            "category": "personal_growth",
            "duration": "Daily, 20 minutes",
            "impact": "medium",
        },
    ],
}

RELATIONSHIP_GUIDANCE = [
    {
        "title": "Conscious Communication Practice",
        "description": "Implement the 'three before me' rule — ask three genuine questions about the other person before sharing about yourself in conversations.",
        "category": "relationships",
        "applicable_when": "high_emotional",
    },
    {
        "title": "Vulnerability Window",
        "description": "Share one authentic feeling or experience with a trusted person each week. Vulnerability deepens connection and builds trust.",
        "category": "relationships",
        "applicable_when": "any",
    },
    {
        "title": "Relationship Energy Audit",
        "description": "Review your key relationships. Identify which energize you and which drain you. Invest more in nourishing connections and set boundaries with depleting ones.",
        "category": "relationships",
        "applicable_when": "any",
    },
    {
        "title": "Gratitude Expression Habit",
        "description": "Express specific, genuine appreciation to one person daily. This practice transforms relationship quality over time.",
        "category": "relationships",
        "applicable_when": "any",
    },
]

CAREER_SUGGESTIONS = [
    {
        "title": "Skill Gap Analysis",
        "description": "Identify three skills that would accelerate your career and create a learning plan for each. Focus on one skill per month.",
        "category": "career",
        "applicable_when": "any",
    },
    {
        "title": "Network Cultivation Strategy",
        "description": "Reach out to one professional contact per week for a meaningful conversation. Relationships drive opportunity.",
        "category": "career",
        "applicable_when": "high_career",
    },
    {
        "title": "Passion Project Initiative",
        "description": "Start a side project that aligns with your deeper interests. This creates optionality and may reveal your true calling.",
        "category": "career",
        "applicable_when": "low_career",
    },
]

SPIRITUAL_INSIGHTS = [
    {
        "title": "Daily Meditation Practice",
        "description": "Begin with 5 minutes of silent meditation each morning. Focus on breath awareness and gradually extend the duration as comfort grows.",
        "category": "spiritual",
        "type": "foundational",
    },
    {
        "title": "Tarot Reflection Ritual",
        "description": "Pull a daily tarot card each morning and journal about its meaning throughout the day. Notice how its themes manifest in your experiences.",
        "category": "spiritual",
        "type": "practice",
    },
    {
        "title": "Moon Phase Alignment",
        "description": "Align your intentions with lunar cycles — set new intentions at the new moon and release what no longer serves you at the full moon.",
        "category": "spiritual",
        "type": "advanced",
    },
    {
        "title": "Gratitude Moonlight Journal",
        "description": "Each evening, write three things you're grateful for and one insight you gained today. This practice builds spiritual awareness over time.",
        "category": "spiritual",
        "type": "foundational",
    },
    {
        "title": "Nature Connection Practice",
        "description": "Spend at least 20 minutes in nature weekly without devices. Observe natural patterns and reflect on what they mirror in your life.",
        "category": "spiritual",
        "type": "practice",
    },
]


class RecommendationService:
    """Personalized recommendation engine for growth and guidance."""

    @staticmethod
    def generate_recommendations(
        palm_analysis: Dict[str, Any],
        tarot_reading: Optional[Dict[str, Any]] = None,
        user_context: Optional[Dict[str, Any]] = None,
        personality_profile: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate comprehensive personalized recommendations across all categories.
        """
        personality_traits = palm_analysis.get("personality_traits", [])
        trait_scores = {t["trait"]: t["score"] for t in personality_traits}

        # Personal growth recommendations
        growth = _generate_growth_recommendations(trait_scores)

        # Relationship guidance
        relationships = _generate_relationship_guidance(trait_scores, user_context)

        # Career suggestions
        career = _generate_career_suggestions(trait_scores, user_context)

        # Goal alignment
        goal_alignment = _generate_goal_recommendations(user_context, trait_scores)

        # Spiritual development
        spiritual = _generate_spiritual_recommendations(
            trait_scores, tarot_reading, user_context
        )

        # Priority ranking
        all_recommendations = growth + relationships + career + goal_alignment + spiritual
        prioritized = _prioritize_recommendations(all_recommendations, trait_scores, user_context)

        return {
            "personal_growth": growth,
            "relationship_guidance": relationships,
            "career_suggestions": career,
            "goal_alignment": goal_alignment,
            "spiritual_development": spiritual,
            "top_recommendations": prioritized[:5],
            "total_recommendations": len(all_recommendations),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def get_daily_recommendation(
        trait_scores: Dict[str, int],
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Get a single daily recommendation."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        seed = hash(today + str(trait_scores))
        rng = random.Random(seed)

        # Collect all possible recommendations
        all_recs = []
        for key, recs in GROWTH_RECOMMENDATIONS.items():
            all_recs.extend(recs)
        all_recs.extend(RELATIONSHIP_GUIDANCE)
        all_recs.extend(SPIRITUAL_INSIGHTS)

        daily = rng.choice(all_recs)
        return {
            "recommendation": daily,
            "date": today,
            "message": "Your daily guidance for spiritual growth and personal development.",
        }


# ============================================================================
# Private Helpers
# ============================================================================

def _generate_growth_recommendations(
    trait_scores: Dict[str, int],
) -> List[Dict[str, Any]]:
    """Generate personal growth recommendations based on traits."""
    recommendations = []

    trait_mapping = {
        "Emotional Intelligence": ("high_emotional", "low_emotional"),
        "Analytical Thinking": ("high_analytical", "low_analytical"),
        "Vitality & Resilience": ("high_vitality", "low_vitality"),
        "Career Drive": ("high_career", "low_career"),
        "Creative Expression": ("high_creative", "low_creative"),
    }

    for trait, (high_key, low_key) in trait_mapping.items():
        score = trait_scores.get(trait, 60)
        if score >= 70:
            recs = GROWTH_RECOMMENDATIONS.get(high_key, [])
        elif score <= 45:
            recs = GROWTH_RECOMMENDATIONS.get(low_key, [])
        else:
            continue  # Balanced — no specific recommendation needed

        for rec in recs[:1]:  # Take top recommendation per trait
            recommendations.append({
                **rec,
                "source_trait": trait,
                "trait_score": score,
                "relevance": "high" if abs(score - 60) > 20 else "medium",
            })

    return recommendations


def _generate_relationship_guidance(
    trait_scores: Dict[str, int],
    user_context: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Generate relationship-specific guidance."""
    emotional_score = trait_scores.get("Emotional Intelligence", 60)
    guidance = []

    for item in RELATIONSHIP_GUIDANCE:
        when = item.get("applicable_when", "any")
        if when == "any":
            guidance.append({**item, "relevance_score": emotional_score})
        elif when == "high_emotional" and emotional_score >= 70:
            guidance.append({**item, "relevance_score": emotional_score})
        elif when == "low_emotional" and emotional_score < 50:
            guidance.append({**item, "relevance_score": 100 - emotional_score})

    # Sort by relevance and return top 3
    guidance.sort(key=lambda x: x.get("relevance_score", 50), reverse=True)
    return guidance[:3]


def _generate_career_suggestions(
    trait_scores: Dict[str, int],
    user_context: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Generate career-specific suggestions."""
    career_score = trait_scores.get("Career Drive", 60)
    suggestions = []

    for item in CAREER_SUGGESTIONS:
        when = item.get("applicable_when", "any")
        if when == "any":
            suggestions.append({**item, "relevance_score": career_score})
        elif when == "high_career" and career_score >= 70:
            suggestions.append({**item, "relevance_score": career_score})
        elif when == "low_career" and career_score < 50:
            suggestions.append({**item, "relevance_score": 100 - career_score})

    return suggestions[:3]


def _generate_goal_recommendations(
    user_context: Optional[Dict[str, Any]],
    trait_scores: Dict[str, int],
) -> List[Dict[str, Any]]:
    """Generate goal-aligned recommendations from user profile."""
    if not user_context:
        return [{
            "title": "Define Your Spiritual Goals",
            "description": "Visit your profile to set spiritual goals and interests. This enables personalized goal-aligned recommendations.",
            "category": "setup",
            "priority": "high",
        }]

    goals = user_context.get("spiritual_goals", [])
    recommendations = []

    goal_recommendations = {
        "self_discovery": {
            "title": "Self-Discovery Acceleration",
            "description": "Your goal of self-discovery aligns with regular palm and tarot readings. Schedule weekly sessions and track your evolving insights.",
            "action": "Schedule a weekly combined reading session",
        },
        "career_guidance": {
            "title": "Career Path Illumination",
            "description": "Use career-focused tarot spreads monthly to gain clarity on professional decisions. Track patterns across readings.",
            "action": "Perform a Career Spread tarot reading this week",
        },
        "relationship_healing": {
            "title": "Relationship Renewal Focus",
            "description": "Relationship spreads combined with heart line analysis can illuminate partnership dynamics. Focus on understanding before action.",
            "action": "Explore a Relationship Spread reading",
        },
        "spiritual_growth": {
            "title": "Deepening Spiritual Practice",
            "description": "Your spiritual growth journey is supported by daily card pulls and regular palm analysis. Build a consistent practice.",
            "action": "Begin daily single-card guidance readings",
        },
        "stress_management": {
            "title": "Stress Alchemy Practice",
            "description": "Transform stress into fuel by using your readings as mirrors for understanding tension patterns and their deeper meanings.",
            "action": "Use readings to identify stress patterns",
        },
    }

    for goal in goals:
        rec = goal_recommendations.get(goal)
        if rec:
            recommendations.append({
                **rec,
                "category": "goal_alignment",
                "goal": goal,
                "priority": "high",
            })

    return recommendations[:4]


def _generate_spiritual_recommendations(
    trait_scores: Dict[str, int],
    tarot_reading: Optional[Dict[str, Any]],
    user_context: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Generate spiritual development recommendations."""
    intuitive_score = trait_scores.get("Intuitive Awareness", 60)

    # Determine experience level
    experience = "beginner"
    if user_context:
        experience = user_context.get("experience_level", "beginner")

    recommendations = []
    for insight in SPIRITUAL_INSIGHTS:
        insight_type = insight.get("type", "foundational")
        if experience == "beginner" and insight_type == "advanced":
            continue
        if experience == "advanced" and insight_type == "foundational":
            continue
        recommendations.append({
            **insight,
            "relevance_score": intuitive_score,
        })

    return recommendations[:3]


def _prioritize_recommendations(
    all_recommendations: List[Dict],
    trait_scores: Dict[str, int],
    user_context: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Prioritize and rank all recommendations."""

    def score_recommendation(rec):
        base = 50
        if rec.get("priority") == "high" or rec.get("impact") == "high":
            base += 20
        if rec.get("relevance") == "high":
            base += 15
        if rec.get("category") == "goal_alignment":
            base += 10
        return base

    scored = [(score_recommendation(r), r) for r in all_recommendations]
    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        {**rec, "priority_score": score, "rank": i + 1}
        for i, (score, rec) in enumerate(scored)
    ]
