"""
Personality Intelligence Module
================================
Full personality profiling from combined palm + tarot data.
Generates Big Five trait mapping, strength/weakness analysis,
behavioral insights, and personal development recommendations.
"""

import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


# ============================================================================
# Big Five Personality Mapping
# ============================================================================

BIG_FIVE_TRAITS = {
    "openness": {
        "name": "Openness to Experience",
        "high_label": "Creative & Curious",
        "low_label": "Practical & Conventional",
        "description": "Reflects creativity, curiosity, and openness to new experiences.",
        "color": "from-violet-500 to-purple-500",
        "palm_sources": ["Creative Expression", "Intuitive Awareness"],
        "positive_indicators": ["long_and_curved", "forked_end", "multiple_lines"],
        "element_bonus": {"Water": 8, "Air": 5, "Fire": 3, "Earth": -3},
    },
    "conscientiousness": {
        "name": "Conscientiousness",
        "high_label": "Organized & Disciplined",
        "low_label": "Flexible & Spontaneous",
        "description": "Reflects self-discipline, organization, and goal-directed behavior.",
        "color": "from-blue-500 to-cyan-500",
        "palm_sources": ["Career Drive", "Analytical Thinking"],
        "positive_indicators": ["deep_and_clear", "long_and_straight"],
        "element_bonus": {"Earth": 8, "Fire": 3, "Air": 0, "Water": -3},
    },
    "extraversion": {
        "name": "Extraversion",
        "high_label": "Outgoing & Energetic",
        "low_label": "Reserved & Reflective",
        "description": "Reflects sociability, assertiveness, and positive emotions.",
        "color": "from-amber-500 to-orange-500",
        "palm_sources": ["Emotional Intelligence", "Vitality & Resilience"],
        "positive_indicators": ["curved_upward", "long_and_deep", "curving_widely"],
        "element_bonus": {"Fire": 10, "Air": 5, "Water": -3, "Earth": -5},
    },
    "agreeableness": {
        "name": "Agreeableness",
        "high_label": "Compassionate & Cooperative",
        "low_label": "Analytical & Competitive",
        "description": "Reflects compassion, trust, and concern for social harmony.",
        "color": "from-pink-500 to-rose-500",
        "palm_sources": ["Emotional Intelligence", "Intuitive Awareness"],
        "positive_indicators": ["long_and_curved", "deep_and_clear", "starts_under_index_finger"],
        "element_bonus": {"Water": 8, "Earth": 3, "Air": 0, "Fire": -5},
    },
    "neuroticism": {
        "name": "Emotional Sensitivity",
        "high_label": "Deeply Feeling & Perceptive",
        "low_label": "Calm & Resilient",
        "description": "Reflects emotional sensitivity, depth of feeling, and perceptiveness.",
        "color": "from-teal-500 to-emerald-500",
        "palm_sources": ["Emotional Intelligence", "Vitality & Resilience"],
        "positive_indicators": ["wavy", "broken", "chained", "faint_or_thin"],
        "element_bonus": {"Water": 5, "Fire": -3, "Earth": -5, "Air": 0},
    },
}

# Strength and weakness descriptions
STRENGTH_DESCRIPTIONS = {
    "high_openness": {
        "strength": "Creative Visionary",
        "description": "You possess an extraordinary ability to see possibilities where others see limitations. Your imagination and intellectual curiosity drive innovation and artistic expression.",
        "advice": "Channel your creativity into tangible projects. Your visionary nature is most powerful when grounded in action.",
    },
    "high_conscientiousness": {
        "strength": "Strategic Achiever",
        "description": "Your disciplined nature and goal-oriented mindset make you exceptionally effective at turning plans into reality. You are the architect of your own success.",
        "advice": "Remember to balance achievement with rest. Your drive is admirable, but sustainable success requires periods of recovery.",
    },
    "high_extraversion": {
        "strength": "Natural Connector",
        "description": "Your energy and warmth create instant rapport. You have a gift for bringing people together and creating community wherever you go.",
        "advice": "Use your social energy purposefully. Deep, meaningful connections often matter more than a wide network.",
    },
    "high_agreeableness": {
        "strength": "Empathic Leader",
        "description": "Your compassion and understanding create safe spaces for others. You lead through trust and genuine care, inspiring loyalty and collaboration.",
        "advice": "Protect your empathic gifts by maintaining strong boundaries. You cannot pour from an empty cup.",
    },
    "low_neuroticism": {
        "strength": "Emotional Anchor",
        "description": "Your emotional stability is a beacon for those around you. You navigate storms with grace and provide calm reassurance in challenging times.",
        "advice": "Continue cultivating your inner peace while remaining open to the full spectrum of human emotions.",
    },
}

WEAKNESS_DESCRIPTIONS = {
    "low_openness": {
        "area": "Comfort Zone Attachment",
        "description": "You may sometimes resist new experiences or unconventional approaches, potentially missing growth opportunities.",
        "growth_path": "Start small — try one new experience each week. Gradual exposure to novelty can expand your horizons without overwhelming you.",
    },
    "low_conscientiousness": {
        "area": "Structure & Follow-Through",
        "description": "Spontaneity is a gift, but it can sometimes lead to unfinished projects or missed commitments.",
        "growth_path": "Implement one simple organizational habit at a time. Even a small daily routine can create significant structure.",
    },
    "low_extraversion": {
        "area": "Social Visibility",
        "description": "Your reflective nature is valuable, but it may sometimes cause you to be overlooked or misunderstood.",
        "growth_path": "Practice expressing your ideas in low-pressure settings. Your insights are valuable and deserve to be heard.",
    },
    "low_agreeableness": {
        "area": "Interpersonal Warmth",
        "description": "Your analytical approach serves you well, but may sometimes create emotional distance in relationships.",
        "growth_path": "Practice active listening and expressing appreciation. Small gestures of warmth can strengthen your relationships significantly.",
    },
    "high_neuroticism": {
        "area": "Emotional Regulation",
        "description": "Your deep sensitivity makes you perceptive but may also lead to emotional overwhelm or anxiety.",
        "growth_path": "Develop grounding practices — meditation, breathwork, or journaling can help you process intense emotions constructively.",
    },
}

# Behavioral pattern templates
BEHAVIORAL_INSIGHTS = {
    "decision_making": {
        "analytical": "You approach decisions systematically, weighing evidence and considering multiple perspectives before committing.",
        "intuitive": "You trust your gut instincts when making decisions, often arriving at the right conclusion before you can articulate why.",
        "collaborative": "You prefer to make decisions in consultation with others, valuing diverse perspectives and collective wisdom.",
        "decisive": "You make decisions quickly and confidently, trusting your judgment and adapting as needed.",
    },
    "stress_response": {
        "resilient": "Under pressure, you remain calm and focused, drawing on inner reserves of strength and clarity.",
        "adaptive": "You respond to stress by seeking creative solutions and adapting your approach to changing circumstances.",
        "contemplative": "Stress drives you inward for reflection and processing, emerging with renewed clarity and purpose.",
        "active": "You channel stress into productive action, using the energy to fuel determination and progress.",
    },
    "communication_style": {
        "articulate": "You express yourself with clarity and precision, making complex ideas accessible to others.",
        "empathic": "Your communication is deeply attuned to others' emotions, creating genuine connection and understanding.",
        "strategic": "You communicate with purpose and intention, crafting your message for maximum impact and clarity.",
        "authentic": "Your communication style is genuine and transparent, building trust through honesty and vulnerability.",
    },
    "learning_style": {
        "experiential": "You learn best through hands-on experience and practical application of concepts.",
        "analytical": "You thrive on deep research, pattern recognition, and systematic understanding of complex topics.",
        "social": "You learn most effectively through discussion, collaboration, and sharing ideas with others.",
        "reflective": "You process information deeply through contemplation, journaling, and internal synthesis.",
    },
}


class PersonalityService:
    """Personality intelligence engine for comprehensive profiling."""

    @staticmethod
    def generate_personality_profile(
        palm_analysis: Dict[str, Any],
        tarot_reading: Optional[Dict[str, Any]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive personality profile from palm + tarot data.
        Returns Big Five traits, strengths, weaknesses, behavioral insights,
        and personal development recommendations.
        """
        personality_traits = palm_analysis.get("personality_traits", [])
        hand_shape = palm_analysis.get("hand_shape", {})
        lines = palm_analysis.get("lines", [])

        # Calculate Big Five scores
        big_five = _calculate_big_five(personality_traits, hand_shape, lines)

        # Determine strengths and weaknesses
        strengths = _identify_strengths(big_five)
        weaknesses = _identify_weaknesses(big_five)

        # Generate behavioral insights
        behavioral = _generate_behavioral_insights(big_five, hand_shape)

        # Generate development recommendations
        recommendations = _generate_development_recommendations(
            big_five, strengths, weaknesses, user_context
        )

        # Calculate overall personality archetype
        archetype = _determine_archetype(big_five, hand_shape)

        # Include tarot influence if available
        tarot_influence = None
        if tarot_reading:
            tarot_influence = _analyze_tarot_personality_influence(tarot_reading)

        return {
            "big_five_traits": big_five,
            "archetype": archetype,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "behavioral_insights": behavioral,
            "development_recommendations": recommendations,
            "tarot_personality_influence": tarot_influence,
            "hand_shape_influence": {
                "type": hand_shape.get("type", "Unknown"),
                "element": hand_shape.get("element", ""),
                "traits": hand_shape.get("traits", []),
            },
            "profile_confidence": round(
                palm_analysis.get("confidence_score", 0.75), 4
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def get_personality_summary(profile: Dict[str, Any]) -> Dict[str, str]:
        """Generate a concise personality summary from a full profile."""
        archetype = profile.get("archetype", {})
        big_five = profile.get("big_five_traits", {})

        # Find dominant and secondary traits
        sorted_traits = sorted(
            big_five.items(), key=lambda x: x[1]["score"], reverse=True
        )
        dominant = sorted_traits[0] if sorted_traits else ("unknown", {"name": "Unknown"})
        secondary = sorted_traits[1] if len(sorted_traits) > 1 else dominant

        return {
            "archetype_name": archetype.get("name", "The Seeker"),
            "archetype_description": archetype.get("description", ""),
            "dominant_trait": f"{dominant[1]['name']} ({dominant[1]['score']}%)",
            "secondary_trait": f"{secondary[1]['name']} ({secondary[1]['score']}%)",
            "one_liner": archetype.get("one_liner", "A unique soul on a journey of discovery."),
        }


# ============================================================================
# Private Helpers
# ============================================================================

def _calculate_big_five(
    personality_traits: List[Dict],
    hand_shape: Dict,
    lines: List[Dict],
) -> Dict[str, Any]:
    """Calculate Big Five personality scores from palm features."""
    trait_scores = {t["trait"]: t["score"] for t in personality_traits}
    element = hand_shape.get("element", "")

    big_five = {}
    for trait_id, trait_def in BIG_FIVE_TRAITS.items():
        # Base score from palm trait sources
        source_scores = [
            trait_scores.get(src, 60) for src in trait_def["palm_sources"]
        ]
        base_score = sum(source_scores) / max(len(source_scores), 1)

        # Element bonus
        element_bonus = trait_def["element_bonus"].get(element, 0)
        score = int(base_score + element_bonus)
        score = max(25, min(95, score))

        # Determine label
        label = trait_def["high_label"] if score >= 60 else trait_def["low_label"]

        big_five[trait_id] = {
            "name": trait_def["name"],
            "score": score,
            "label": label,
            "description": trait_def["description"],
            "color": trait_def["color"],
            "element_influence": f"{element} ({'+' if element_bonus >= 0 else ''}{element_bonus})",
        }

    return big_five


def _identify_strengths(big_five: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify top strengths from Big Five profile."""
    strengths = []
    sorted_traits = sorted(
        big_five.items(), key=lambda x: x[1]["score"], reverse=True
    )

    for trait_id, trait_data in sorted_traits[:3]:
        score = trait_data["score"]
        if score >= 65:
            key = f"high_{trait_id}"
            if trait_id == "neuroticism" and score < 50:
                key = "low_neuroticism"
            elif trait_id == "neuroticism":
                continue  # High neuroticism is not listed as strength

            strength_info = STRENGTH_DESCRIPTIONS.get(key)
            if strength_info:
                strengths.append({
                    "trait": trait_data["name"],
                    "score": score,
                    **strength_info,
                })

    # Ensure at least 2 strengths
    if len(strengths) < 2:
        for trait_id, trait_data in sorted_traits:
            if len(strengths) >= 2:
                break
            if not any(s["trait"] == trait_data["name"] for s in strengths):
                strengths.append({
                    "trait": trait_data["name"],
                    "score": trait_data["score"],
                    "strength": trait_data["label"],
                    "description": f"Your {trait_data['name'].lower()} score of {trait_data['score']}% reflects a notable quality that can be leveraged for personal growth.",
                    "advice": f"Continue developing your {trait_data['name'].lower()} through intentional practice and self-awareness.",
                })

    return strengths


def _identify_weaknesses(big_five: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify growth areas from Big Five profile."""
    weaknesses = []
    sorted_traits = sorted(
        big_five.items(), key=lambda x: x[1]["score"]
    )

    for trait_id, trait_data in sorted_traits[:2]:
        score = trait_data["score"]
        key = f"low_{trait_id}"
        if trait_id == "neuroticism" and score >= 70:
            key = "high_neuroticism"

        weakness_info = WEAKNESS_DESCRIPTIONS.get(key)
        if weakness_info:
            weaknesses.append({
                "trait": trait_data["name"],
                "score": score,
                **weakness_info,
            })

    return weaknesses


def _generate_behavioral_insights(
    big_five: Dict[str, Any], hand_shape: Dict
) -> Dict[str, Dict[str, str]]:
    """Generate behavioral pattern insights."""
    element = hand_shape.get("element", "Earth")
    scores = {k: v["score"] for k, v in big_five.items()}

    insights = {}

    # Decision making style
    if scores.get("conscientiousness", 50) > 70:
        insights["decision_making"] = {
            "style": "Analytical",
            **{"description": BEHAVIORAL_INSIGHTS["decision_making"]["analytical"]},
        }
    elif scores.get("openness", 50) > 70:
        insights["decision_making"] = {
            "style": "Intuitive",
            **{"description": BEHAVIORAL_INSIGHTS["decision_making"]["intuitive"]},
        }
    elif scores.get("agreeableness", 50) > 70:
        insights["decision_making"] = {
            "style": "Collaborative",
            **{"description": BEHAVIORAL_INSIGHTS["decision_making"]["collaborative"]},
        }
    else:
        insights["decision_making"] = {
            "style": "Decisive",
            **{"description": BEHAVIORAL_INSIGHTS["decision_making"]["decisive"]},
        }

    # Stress response
    neuroticism = scores.get("neuroticism", 50)
    extraversion = scores.get("extraversion", 50)
    if neuroticism < 40:
        insights["stress_response"] = {
            "style": "Resilient",
            **{"description": BEHAVIORAL_INSIGHTS["stress_response"]["resilient"]},
        }
    elif extraversion > 65:
        insights["stress_response"] = {
            "style": "Active",
            **{"description": BEHAVIORAL_INSIGHTS["stress_response"]["active"]},
        }
    elif scores.get("openness", 50) > 65:
        insights["stress_response"] = {
            "style": "Adaptive",
            **{"description": BEHAVIORAL_INSIGHTS["stress_response"]["adaptive"]},
        }
    else:
        insights["stress_response"] = {
            "style": "Contemplative",
            **{"description": BEHAVIORAL_INSIGHTS["stress_response"]["contemplative"]},
        }

    # Communication style
    if scores.get("agreeableness", 50) > 70:
        insights["communication_style"] = {
            "style": "Empathic",
            **{"description": BEHAVIORAL_INSIGHTS["communication_style"]["empathic"]},
        }
    elif scores.get("conscientiousness", 50) > 70:
        insights["communication_style"] = {
            "style": "Strategic",
            **{"description": BEHAVIORAL_INSIGHTS["communication_style"]["strategic"]},
        }
    elif scores.get("openness", 50) > 65:
        insights["communication_style"] = {
            "style": "Authentic",
            **{"description": BEHAVIORAL_INSIGHTS["communication_style"]["authentic"]},
        }
    else:
        insights["communication_style"] = {
            "style": "Articulate",
            **{"description": BEHAVIORAL_INSIGHTS["communication_style"]["articulate"]},
        }

    # Learning style
    if element == "Earth":
        insights["learning_style"] = {
            "style": "Experiential",
            **{"description": BEHAVIORAL_INSIGHTS["learning_style"]["experiential"]},
        }
    elif element == "Air":
        insights["learning_style"] = {
            "style": "Analytical",
            **{"description": BEHAVIORAL_INSIGHTS["learning_style"]["analytical"]},
        }
    elif element == "Fire":
        insights["learning_style"] = {
            "style": "Social",
            **{"description": BEHAVIORAL_INSIGHTS["learning_style"]["social"]},
        }
    else:
        insights["learning_style"] = {
            "style": "Reflective",
            **{"description": BEHAVIORAL_INSIGHTS["learning_style"]["reflective"]},
        }

    return insights


def _generate_development_recommendations(
    big_five: Dict,
    strengths: List[Dict],
    weaknesses: List[Dict],
    user_context: Optional[Dict],
) -> List[Dict[str, str]]:
    """Generate personalized development recommendations."""
    recommendations = []

    # Leverage strengths recommendations
    for s in strengths[:2]:
        recommendations.append({
            "type": "leverage_strength",
            "title": f"Amplify Your {s.get('strength', s['trait'])}",
            "description": s.get("advice", f"Continue developing your {s['trait']} through intentional practice."),
            "priority": "high",
            "category": "strength",
        })

    # Address growth areas
    for w in weaknesses[:2]:
        recommendations.append({
            "type": "growth_area",
            "title": f"Develop Your {w.get('area', w['trait'])}",
            "description": w.get("growth_path", f"Focus on developing your {w['trait']}."),
            "priority": "medium",
            "category": "growth",
        })

    # Context-aware recommendations
    if user_context:
        goals = user_context.get("spiritual_goals", [])
        if "career_guidance" in goals:
            recommendations.append({
                "type": "goal_aligned",
                "title": "Career Alignment Practice",
                "description": "Schedule weekly career reflection sessions. Review your professional trajectory against your deeper values and adjust course as needed.",
                "priority": "high",
                "category": "career",
            })
        if "self_discovery" in goals:
            recommendations.append({
                "type": "goal_aligned",
                "title": "Daily Self-Discovery Ritual",
                "description": "Begin each day with a 5-minute journaling practice, exploring one aspect of your personality or a question about your life direction.",
                "priority": "high",
                "category": "personal_growth",
            })

    # Universal recommendations
    recommendations.append({
        "type": "universal",
        "title": "Mindful Integration",
        "description": "Take 10 minutes daily to reflect on how your strengths and growth areas showed up in your interactions. This awareness practice accelerates personal development.",
        "priority": "low",
        "category": "wellness",
    })

    return recommendations


def _determine_archetype(big_five: Dict[str, Any], hand_shape: Dict) -> Dict[str, str]:
    """Determine a personality archetype from the profile."""
    scores = {k: v["score"] for k, v in big_five.items()}
    element = hand_shape.get("element", "Earth")

    # Find dominant traits
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dominant = sorted_scores[0][0]
    secondary = sorted_scores[1][0]

    archetypes = {
        ("openness", "extraversion"): {
            "name": "The Visionary Explorer",
            "one_liner": "A bold creative spirit who thrives on new horizons.",
            "description": "You combine boundless curiosity with magnetic social energy. Your path is one of innovation, connection, and inspiring others to see the world differently.",
        },
        ("openness", "agreeableness"): {
            "name": "The Empathic Artist",
            "one_liner": "A sensitive soul who creates beauty from understanding.",
            "description": "Your deep empathy and creative spirit merge to produce art, ideas, and connections that touch hearts. You see beauty in the human experience.",
        },
        ("conscientiousness", "extraversion"): {
            "name": "The Charismatic Leader",
            "one_liner": "A driven force who leads through energy and discipline.",
            "description": "You combine structured ambition with natural charisma. Others follow your lead because you embody both vision and the discipline to achieve it.",
        },
        ("conscientiousness", "agreeableness"): {
            "name": "The Devoted Guardian",
            "one_liner": "A reliable anchor who protects and nurtures with intention.",
            "description": "Your disciplined nature serves your deep caring for others. You build stable foundations and create safe spaces for growth.",
        },
        ("extraversion", "agreeableness"): {
            "name": "The Heart Connector",
            "one_liner": "A warm presence who builds bridges between souls.",
            "description": "Your combination of social energy and genuine compassion makes you a natural community builder. People feel seen and valued in your presence.",
        },
        ("openness", "conscientiousness"): {
            "name": "The Strategic Innovator",
            "one_liner": "A creative mind with the discipline to manifest ideas.",
            "description": "You bridge imagination and execution. Where others dream, you create actionable plans. Where others plan, you inject creative vision.",
        },
    }

    key = (dominant, secondary)
    reverse_key = (secondary, dominant)
    archetype = archetypes.get(key) or archetypes.get(reverse_key)

    if not archetype:
        # Default archetype based on element
        element_archetypes = {
            "Earth": {"name": "The Grounded Sage", "one_liner": "A practical wisdom-keeper rooted in reality.", "description": "Your pragmatic nature and steady presence make you a pillar of strength and wisdom."},
            "Air": {"name": "The Intellectual Seeker", "one_liner": "A curious mind that soars through ideas.", "description": "Your intellectual agility and communication skills open doors to understanding."},
            "Water": {"name": "The Intuitive Healer", "one_liner": "A deeply feeling soul who transforms through empathy.", "description": "Your emotional depth and intuitive wisdom guide healing and transformation."},
            "Fire": {"name": "The Passionate Pioneer", "one_liner": "An energetic force that blazes new trails.", "description": "Your boundless energy and enthusiasm inspire action and ignite passion in others."},
        }
        archetype = element_archetypes.get(element, element_archetypes["Earth"])

    return archetype


def _analyze_tarot_personality_influence(tarot_reading: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze how tarot cards reflect personality aspects."""
    cards = tarot_reading.get("cards", [])
    themes = tarot_reading.get("themes", [])

    major_arcana = [c for c in cards if c.get("arcana") == "major"]
    personality_cards = []

    for card in major_arcana[:3]:
        personality_cards.append({
            "card": card.get("card_name", "Unknown"),
            "orientation": card.get("orientation", "upright"),
            "influence": f"{card.get('card_name', 'This card')} ({card.get('orientation', 'upright')}) reflects key aspects of your personality that are currently active and evolving.",
        })

    return {
        "major_arcana_count": len(major_arcana),
        "personality_cards": personality_cards,
        "active_themes": themes[:5],
        "influence_summary": (
            f"The tarot reveals {len(major_arcana)} Major Arcana cards in your reading, "
            f"indicating significant personality themes at play. "
            f"Key themes emerging: {', '.join(themes[:3]) if themes else 'self-discovery and transformation'}."
        ),
    }
