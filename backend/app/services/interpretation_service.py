"""
AI Interpretation Engine
========================
Context-aware insight generation across 7 categories:
Personality, Relationships, Career, Finance, Health & Wellness,
Personal Growth, Life Opportunities.

Synthesizes palm analysis + tarot reading data into unified,
weighted interpretations using the 5-factor scoring model.
"""

import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


# ============================================================================
# Insight Category Definitions
# ============================================================================

INSIGHT_CATEGORIES = {
    "personality": {
        "name": "Personality",
        "icon": "user",
        "color": "from-purple-500 to-indigo-500",
        "description": "Core personality traits, behavioral patterns, and self-understanding",
    },
    "relationships": {
        "name": "Relationships",
        "icon": "heart",
        "color": "from-pink-500 to-rose-500",
        "description": "Love, partnerships, family dynamics, and social connections",
    },
    "career": {
        "name": "Career",
        "icon": "briefcase",
        "color": "from-amber-500 to-orange-500",
        "description": "Professional growth, work satisfaction, and career direction",
    },
    "finance": {
        "name": "Finance",
        "icon": "dollar-sign",
        "color": "from-emerald-500 to-teal-500",
        "description": "Financial outlook, abundance mindset, and material stability",
    },
    "health_wellness": {
        "name": "Health & Wellness",
        "icon": "activity",
        "color": "from-cyan-500 to-blue-500",
        "description": "Physical vitality, mental health, and holistic well-being",
    },
    "personal_growth": {
        "name": "Personal Growth",
        "icon": "trending-up",
        "color": "from-violet-500 to-fuchsia-500",
        "description": "Self-improvement, spiritual development, and life lessons",
    },
    "life_opportunities": {
        "name": "Life Opportunities",
        "icon": "compass",
        "color": "from-yellow-500 to-amber-500",
        "description": "Upcoming opportunities, timing, and favorable conditions",
    },
}

# Interpretation templates keyed by category and sentiment
INTERPRETATION_TEMPLATES = {
    "personality": {
        "positive": [
            "Your inner light shines with remarkable clarity. The alignment of your palm features and tarot energies reveals a person of deep authenticity and self-awareness.",
            "A natural leader emerges from your reading — your confidence and emotional intelligence create a magnetic presence that others are drawn to.",
            "Your personality radiates warmth and intellectual curiosity. You possess a rare balance of heart and mind that serves you well in all endeavors.",
        ],
        "growth": [
            "There is an invitation to explore the deeper layers of your personality. Embrace vulnerability as a strength, not a weakness.",
            "Your reading suggests that self-reflection will unlock hidden potential. Take time to understand your shadow self — it holds keys to transformation.",
            "Growth awaits in the spaces between certainty and doubt. Trust the process of becoming who you are meant to be.",
        ],
    },
    "relationships": {
        "positive": [
            "Love and connection flow freely in your life. Your heart line and tarot cards suggest deep, meaningful bonds are strengthening around you.",
            "A period of emotional harmony is unfolding. Your relationships are built on foundations of mutual respect and genuine understanding.",
            "The universe supports your connections. Whether romantic, familial, or platonic, your relationships are sources of growth and joy.",
        ],
        "growth": [
            "Communication is the bridge to deeper connection. Express your needs clearly and listen with an open heart.",
            "Some relationships may need recalibration. Set healthy boundaries while remaining compassionate and available.",
            "Past patterns in relationships are asking to be healed. Approach this inner work with patience and self-compassion.",
        ],
    },
    "career": {
        "positive": [
            "Professional momentum is building. Your fate line and career-aligned cards indicate recognition and advancement are within reach.",
            "Your unique talents are being noticed. Trust your professional instincts — they are aligned with your true calling.",
            "A fertile period for career growth. New opportunities will test your skills and reward your dedication.",
        ],
        "growth": [
            "Consider whether your current path truly aligns with your deeper purpose. Small pivots can lead to significant transformation.",
            "Develop patience with career timing. The seeds you've planted are germinating beneath the surface.",
            "Expand your skill set and embrace learning opportunities. Professional growth requires stepping beyond comfort zones.",
        ],
    },
    "finance": {
        "positive": [
            "Financial stability is strengthening. Your practical nature and aligned energies support wise material decisions.",
            "Abundance consciousness is expanding. Trust that your efforts will be rewarded with material comfort and security.",
            "A favorable period for financial planning and investment. Your intuition about money matters is particularly sharp.",
        ],
        "growth": [
            "Examine your relationship with abundance. Scarcity thinking may be limiting your financial potential.",
            "Create a more structured approach to finances. Discipline now creates freedom later.",
            "Balance generosity with self-preservation. Ensure your financial boundaries protect your well-being.",
        ],
    },
    "health_wellness": {
        "positive": [
            "Vital energy courses through your being. Your life line and supportive cards indicate strong physical and emotional resilience.",
            "A period of renewed vitality. Your body and mind are in harmony, supporting wellness on all levels.",
            "Your commitment to self-care is paying dividends. Continue nurturing your physical, emotional, and spiritual health.",
        ],
        "growth": [
            "Listen to your body's subtle messages. Rest and restoration are not luxuries — they are necessities.",
            "Stress management deserves more attention. Explore mindfulness, meditation, or gentle movement practices.",
            "Nourish yourself holistically. What you consume — food, media, relationships — directly impacts your vitality.",
        ],
    },
    "personal_growth": {
        "positive": [
            "You are in a powerful phase of transformation. Old patterns are dissolving, making room for your authentic self to emerge.",
            "Spiritual awareness is deepening. Trust the wisdom that comes from within — it is your most reliable guide.",
            "Personal evolution is accelerating. The challenges you've faced have forged remarkable inner strength and wisdom.",
        ],
        "growth": [
            "Embrace discomfort as a catalyst for growth. The most profound transformations arise from the deepest challenges.",
            "Develop a daily practice of self-reflection. Journaling, meditation, or contemplation will accelerate your growth.",
            "Release the need for external validation. Your worth is inherent and unchanging, regardless of circumstances.",
        ],
    },
    "life_opportunities": {
        "positive": [
            "The cosmos align to present remarkable opportunities. Stay alert and ready to act when doors begin to open.",
            "Synchronicities are increasing — pay attention to recurring themes and unexpected connections. They are guideposts.",
            "A window of favorable timing is approaching. Prepare yourself to receive what the universe is arranging for you.",
        ],
        "growth": [
            "Opportunities may arrive disguised as challenges. Look beyond surface appearances to find hidden gifts.",
            "Patience is required as the right opportunities align. Focus on preparation rather than pursuit.",
            "Expand your vision of what's possible. Limiting beliefs may cause you to overlook promising pathways.",
        ],
    },
}


class InterpretationService:
    """AI-powered interpretation engine for palm and tarot readings."""

    @staticmethod
    def generate_palm_interpretation(palm_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate deep interpretation from palm analysis data.
        Maps palm features to insight categories with narratives.
        """
        hand_shape = palm_analysis.get("hand_shape", {})
        personality_traits = palm_analysis.get("personality_traits", [])
        lines = palm_analysis.get("lines", [])
        confidence = palm_analysis.get("confidence_score", 0.75)

        # Build category-level insights from palm data
        insights = {}

        # Map palm features to insight categories
        trait_scores = {t["trait"]: t["score"] for t in personality_traits}

        # Personality insights from overall traits
        avg_score = sum(trait_scores.values()) / max(len(trait_scores), 1)
        insights["personality"] = _build_category_insight(
            "personality", avg_score, hand_shape, personality_traits
        )

        # Relationships from heart line
        heart_score = trait_scores.get("Emotional Intelligence", 65)
        insights["relationships"] = _build_category_insight(
            "relationships", heart_score, hand_shape, personality_traits
        )

        # Career from fate line + career drive
        career_score = trait_scores.get("Career Drive", 60)
        insights["career"] = _build_category_insight(
            "career", career_score, hand_shape, personality_traits
        )

        # Health from life line
        vitality_score = trait_scores.get("Vitality & Resilience", 65)
        insights["health_wellness"] = _build_category_insight(
            "health_wellness", vitality_score, hand_shape, personality_traits
        )

        # Personal growth from intuitive awareness
        growth_score = trait_scores.get("Intuitive Awareness", 60)
        insights["personal_growth"] = _build_category_insight(
            "personal_growth", growth_score, hand_shape, personality_traits
        )

        # Creative expression mapped to life opportunities
        creative_score = trait_scores.get("Creative Expression", 60)
        insights["life_opportunities"] = _build_category_insight(
            "life_opportunities", creative_score, hand_shape, personality_traits
        )

        # Finance from analytical thinking + career drive
        analytical_score = trait_scores.get("Analytical Thinking", 65)
        finance_score = int((analytical_score + career_score) / 2)
        insights["finance"] = _build_category_insight(
            "finance", finance_score, hand_shape, personality_traits
        )

        return {
            "source": "palm",
            "insights": insights,
            "overall_confidence": confidence,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def generate_tarot_interpretation(tarot_reading: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate deep interpretation from tarot reading data.
        Analyzes card positions, elemental balance, and themes.
        """
        cards = tarot_reading.get("cards", [])
        themes = tarot_reading.get("themes", [])
        elemental_balance = tarot_reading.get("elemental_balance", {})
        confidence = tarot_reading.get("confidence_score", 0.75)
        narrative = tarot_reading.get("narrative", {})

        # Analyze card orientations
        reversed_count = sum(1 for c in cards if c.get("orientation") == "reversed")
        total_cards = len(cards)
        reversed_ratio = reversed_count / max(total_cards, 1)

        # Determine overall sentiment
        overall_score = int((1 - reversed_ratio * 0.5) * 100)

        insights = {}
        rng = random.Random(hash(str(themes) + str(total_cards)))

        for category in INSIGHT_CATEGORIES:
            # Vary score per category based on elemental and card alignment
            category_variance = rng.randint(-12, 12)
            cat_score = max(35, min(95, overall_score + category_variance))
            insights[category] = _build_tarot_category_insight(
                category, cat_score, cards, themes, elemental_balance
            )

        return {
            "source": "tarot",
            "insights": insights,
            "overall_confidence": confidence,
            "themes": themes,
            "elemental_balance": elemental_balance,
            "energy_tone": narrative.get("energy_tone", "balanced"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def generate_combined_interpretation(
        palm_analysis: Dict[str, Any],
        tarot_reading: Dict[str, Any],
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Synthesize palm + tarot interpretations into unified insights.
        Applies the 5-factor weighted scoring model.
        """
        palm_interp = InterpretationService.generate_palm_interpretation(palm_analysis)
        tarot_interp = InterpretationService.generate_tarot_interpretation(tarot_reading)

        combined_insights = {}

        for category in INSIGHT_CATEGORIES:
            palm_cat = palm_interp["insights"].get(category, {})
            tarot_cat = tarot_interp["insights"].get(category, {})

            palm_score = palm_cat.get("score", 60)
            tarot_score = tarot_cat.get("score", 60)

            # Weighted combination
            combined_score = int(palm_score * 0.45 + tarot_score * 0.55)

            sentiment = "positive" if combined_score >= 65 else "growth"
            rng = random.Random(hash(category + str(combined_score)))
            templates = INTERPRETATION_TEMPLATES[category][sentiment]
            narrative = rng.choice(templates)

            # Synthesize specific advice
            palm_narrative = palm_cat.get("narrative", "")
            tarot_narrative = tarot_cat.get("narrative", "")

            combined_insights[category] = {
                **INSIGHT_CATEGORIES[category],
                "score": combined_score,
                "sentiment": sentiment,
                "narrative": narrative,
                "palm_insight": palm_narrative,
                "tarot_insight": tarot_narrative,
                "synthesis": _synthesize_category(
                    category, palm_score, tarot_score, combined_score
                ),
            }

        # Calculate overall insight score using 5-factor model
        palm_confidence = palm_analysis.get("confidence_score", 0.75)
        tarot_confidence = tarot_reading.get("confidence_score", 0.75)

        avg_category_score = sum(
            c["score"] for c in combined_insights.values()
        ) / max(len(combined_insights), 1)

        # User context relevance (default if no user context)
        user_relevance = 0.75
        if user_context:
            goals = user_context.get("spiritual_goals", [])
            interests = user_context.get("spiritual_interests", [])
            user_relevance = min(0.95, 0.6 + len(goals) * 0.05 + len(interests) * 0.03)

        # Reading consistency (based on palm-tarot alignment)
        score_diffs = []
        for cat in INSIGHT_CATEGORIES:
            p = palm_interp["insights"].get(cat, {}).get("score", 60)
            t = tarot_interp["insights"].get(cat, {}).get("score", 60)
            score_diffs.append(abs(p - t))
        avg_diff = sum(score_diffs) / max(len(score_diffs), 1)
        consistency = max(0.4, 1.0 - avg_diff / 100)

        # 5-Factor Weighted Insight Score
        insight_score = (
            palm_confidence * 0.30
            + tarot_confidence * 0.25
            + (avg_category_score / 100) * 0.20
            + user_relevance * 0.15
            + consistency * 0.10
        )

        return {
            "source": "combined",
            "insights": combined_insights,
            "insight_score": round(insight_score, 4),
            "scoring_breakdown": {
                "palm_analysis_confidence": {"weight": "30%", "value": round(palm_confidence, 4)},
                "tarot_interpretation_relevance": {"weight": "25%", "value": round(tarot_confidence, 4)},
                "personality_alignment": {"weight": "20%", "value": round(avg_category_score / 100, 4)},
                "user_context_relevance": {"weight": "15%", "value": round(user_relevance, 4)},
                "reading_consistency": {"weight": "10%", "value": round(consistency, 4)},
            },
            "palm_source": palm_interp,
            "tarot_source": tarot_interp,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def get_insight_categories() -> List[Dict[str, Any]]:
        """Return all available insight categories with metadata."""
        return [
            {"id": cat_id, **cat_data}
            for cat_id, cat_data in INSIGHT_CATEGORIES.items()
        ]


# ============================================================================
# Private Helpers
# ============================================================================

def _build_category_insight(
    category: str,
    score: int,
    hand_shape: Dict,
    personality_traits: List[Dict],
) -> Dict[str, Any]:
    """Build a category-level insight from palm data."""
    sentiment = "positive" if score >= 65 else "growth"
    rng = random.Random(hash(category + str(score) + hand_shape.get("type", "")))
    templates = INTERPRETATION_TEMPLATES.get(category, {}).get(sentiment, [])
    narrative = rng.choice(templates) if templates else ""

    element = hand_shape.get("element", "")
    shape_type = hand_shape.get("type", "")

    # Add element-specific flavor
    element_suffix = ""
    if element:
        element_notes = {
            "Earth": "Your grounded nature provides stability in this area.",
            "Air": "Your intellectual approach brings clarity and insight here.",
            "Water": "Your emotional depth enriches this dimension of your life.",
            "Fire": "Your passionate energy drives powerful movement in this area.",
        }
        element_suffix = element_notes.get(element, "")

    return {
        **INSIGHT_CATEGORIES[category],
        "score": score,
        "sentiment": sentiment,
        "narrative": f"{narrative} {element_suffix}".strip(),
        "element_influence": element,
        "hand_shape_influence": shape_type,
    }


def _build_tarot_category_insight(
    category: str,
    score: int,
    cards: List[Dict],
    themes: List[str],
    elemental_balance: Dict,
) -> Dict[str, Any]:
    """Build a category-level insight from tarot data."""
    sentiment = "positive" if score >= 65 else "growth"
    rng = random.Random(hash(category + str(score) + str(themes)))
    templates = INTERPRETATION_TEMPLATES.get(category, {}).get(sentiment, [])
    narrative = rng.choice(templates) if templates else ""

    # Find dominant element
    dominant_element = max(elemental_balance, key=elemental_balance.get) if elemental_balance else None

    # Find relevant card for this category
    relevant_card = None
    category_positions = {
        "career": ["Current Career Energy", "Career Outcome", "Recommended Action"],
        "relationships": ["Your Energy in the Relationship", "Relationship Potential", "Partner's Energy"],
        "personality": ["Present Situation", "Your Attitude", "Present Insight"],
        "life_opportunities": ["Best Possible Outcome", "Near Future", "Future"],
        "health_wellness": ["Present", "Present Situation"],
        "finance": ["Obstacles to Overcome", "Hidden Talents"],
        "personal_growth": ["Hopes & Fears", "Final Outcome", "Immediate Challenge"],
    }

    target_positions = category_positions.get(category, [])
    for card in cards:
        if card.get("position") in target_positions:
            relevant_card = card
            break

    card_reference = ""
    if relevant_card:
        card_reference = (
            f"The {relevant_card['card_name']} ({relevant_card['orientation']}) "
            f"in the {relevant_card['position']} position particularly influences this area."
        )

    return {
        **INSIGHT_CATEGORIES[category],
        "score": score,
        "sentiment": sentiment,
        "narrative": f"{narrative} {card_reference}".strip(),
        "dominant_element": dominant_element,
        "themes": themes[:3] if themes else [],
        "relevant_card": relevant_card.get("card_name") if relevant_card else None,
    }


def _synthesize_category(
    category: str, palm_score: int, tarot_score: int, combined_score: int
) -> str:
    """Create a synthesis statement for a category combining both sources."""
    alignment = abs(palm_score - tarot_score)

    if alignment <= 10:
        harmony = "strong alignment"
        detail = "Both your palm's wisdom and the tarot's guidance point in the same direction, reinforcing this message."
    elif alignment <= 25:
        harmony = "complementary perspectives"
        detail = "Your palm analysis and tarot reading offer slightly different but complementary perspectives, creating a richer understanding."
    else:
        harmony = "dynamic tension"
        detail = "There is an interesting contrast between what your palm reveals and what the cards suggest. This tension itself is informative — explore both viewpoints."

    return (
        f"In the area of {INSIGHT_CATEGORIES[category]['name']}, your reading shows {harmony} "
        f"(palm: {palm_score}%, tarot: {tarot_score}%, combined: {combined_score}%). "
        f"{detail}"
    )
