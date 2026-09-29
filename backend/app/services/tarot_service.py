"""
Tarot Intelligence Engine
=========================
Core tarot card reading service supporting:
- Randomized card shuffling with upright/reversed orientations
- 6 spread types (Single, Three Card, Celtic Cross, Career, Relationship, Daily)
- Position-specific interpretation generation
- Combined reading narrative synthesis
- Confidence scoring per reading
"""

import json
import random
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

# Load tarot card data
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def _load_tarot_deck() -> List[Dict]:
    """Load the full 78-card tarot deck from JSON data."""
    with open(os.path.join(DATA_DIR, "tarot_cards.json"), "r", encoding="utf-8") as f:
        return json.load(f)

TAROT_DECK = _load_tarot_deck()

# ============================================================================
# Spread Configurations
# ============================================================================

SPREAD_CONFIGS = {
    "single": {
        "name": "Single Card",
        "card_count": 1,
        "positions": ["Present Insight"],
        "description": "A focused single card pull for immediate guidance on a specific question.",
    },
    "three_card": {
        "name": "Three Card Spread",
        "card_count": 3,
        "positions": ["Past", "Present", "Future"],
        "description": "Classic past-present-future spread revealing the timeline of your situation.",
    },
    "celtic_cross": {
        "name": "Celtic Cross",
        "card_count": 10,
        "positions": [
            "Present Situation",
            "Immediate Challenge",
            "Distant Past / Root Cause",
            "Recent Past",
            "Best Possible Outcome",
            "Near Future",
            "Your Attitude",
            "External Influences",
            "Hopes & Fears",
            "Final Outcome",
        ],
        "description": "The most comprehensive spread revealing all aspects of your question — past influences, present challenges, and future possibilities.",
    },
    "career": {
        "name": "Career Spread",
        "card_count": 5,
        "positions": [
            "Current Career Energy",
            "Obstacles to Overcome",
            "Hidden Talents",
            "Recommended Action",
            "Career Outcome",
        ],
        "description": "Focused career guidance covering your professional energy, challenges, hidden strengths, and recommended path forward.",
    },
    "relationship": {
        "name": "Relationship Spread",
        "card_count": 5,
        "positions": [
            "Your Energy in the Relationship",
            "Partner's Energy",
            "Relationship Foundation",
            "Current Challenge",
            "Relationship Potential",
        ],
        "description": "Explore relationship dynamics, mutual energies, and the potential path forward together.",
    },
    "daily": {
        "name": "Daily Guidance",
        "card_count": 1,
        "positions": ["Today's Guiding Energy"],
        "description": "Your daily card for morning reflection and intention setting.",
    },
}


class TarotService:
    """Tarot reading intelligence engine."""

    @staticmethod
    def get_available_spreads() -> List[Dict[str, Any]]:
        """Return all available spread types with their configurations."""
        return [
            {
                "id": spread_id,
                "name": config["name"],
                "card_count": config["card_count"],
                "positions": config["positions"],
                "description": config["description"],
            }
            for spread_id, config in SPREAD_CONFIGS.items()
        ]

    @staticmethod
    def shuffle_and_deal(spread_type: str, seed: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Shuffle the full deck and deal cards for the specified spread.
        Each card gets a random upright/reversed orientation.
        """
        config = SPREAD_CONFIGS.get(spread_type)
        if not config:
            raise ValueError(f"Unknown spread type: {spread_type}. Available: {list(SPREAD_CONFIGS.keys())}")

        rng = random.Random(seed) if seed else random.Random()

        # Create a shuffled copy of the full deck
        deck = list(TAROT_DECK)
        rng.shuffle(deck)

        dealt_cards = []
        for i in range(config["card_count"]):
            card = deck[i].copy()
            is_reversed = rng.random() < 0.3  # 30% chance of reversed
            card["orientation"] = "reversed" if is_reversed else "upright"
            card["position"] = config["positions"][i]
            card["position_index"] = i
            dealt_cards.append(card)

        return dealt_cards

    @staticmethod
    def interpret_card(card: Dict[str, Any], question: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a detailed interpretation for a single card in its position.
        """
        is_reversed = card.get("orientation") == "reversed"
        meaning = card.get("reversed_meaning") if is_reversed else card.get("upright_meaning")
        position = card.get("position", "General")

        # Build position-specific context
        position_context = _get_position_context(position, card["name"], is_reversed)

        # Generate interpretation narrative
        interpretation = {
            "card_name": card["name"],
            "card_id": card["id"],
            "number": card.get("number"),
            "arcana": card.get("arcana"),
            "suit": card.get("suit"),
            "element": card.get("element"),
            "zodiac_sign": card.get("zodiac_sign"),
            "position": position,
            "position_index": card.get("position_index", 0),
            "orientation": card["orientation"],
            "keywords": card.get("keywords", []),
            "core_meaning": meaning,
            "description": card.get("description", ""),
            "position_interpretation": position_context,
            "image_key": card["id"],  # Used for frontend image lookup
        }

        # Add question-specific insight if provided
        if question:
            interpretation["question_insight"] = _generate_question_insight(
                card["name"], meaning, question, is_reversed
            )

        return interpretation

    @staticmethod
    def generate_reading(
        spread_type: str,
        question: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Perform a complete tarot reading:
        1. Shuffle & deal cards
        2. Interpret each card in position
        3. Synthesize overall narrative
        4. Calculate confidence score
        """
        config = SPREAD_CONFIGS.get(spread_type)
        if not config:
            raise ValueError(f"Unknown spread type: {spread_type}")

        # Deal cards
        dealt_cards = TarotService.shuffle_and_deal(spread_type, seed)

        # Interpret each card
        interpretations = []
        for card in dealt_cards:
            interpretation = TarotService.interpret_card(card, question)
            interpretations.append(interpretation)

        # Generate overall narrative
        narrative = _synthesize_narrative(interpretations, question, spread_type)

        # Calculate confidence score
        confidence = _calculate_confidence(interpretations)

        reading = {
            "spread_type": spread_type,
            "spread_name": config["name"],
            "spread_description": config["description"],
            "question": question,
            "card_count": len(interpretations),
            "cards": interpretations,
            "narrative": narrative,
            "confidence_score": confidence,
            "reading_timestamp": datetime.now(timezone.utc).isoformat(),
            "themes": _extract_themes(interpretations),
            "elemental_balance": _calculate_elemental_balance(interpretations),
        }

        return reading

    @staticmethod
    def get_daily_card(user_seed: Optional[str] = None) -> Dict[str, Any]:
        """Get a daily guidance card, optionally seeded by user ID for consistency."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        seed_str = f"{today}-{user_seed}" if user_seed else today
        seed = hash(seed_str) % (2**31)
        return TarotService.generate_reading("daily", "What energy should guide me today?", seed)


# ============================================================================
# Private Helper Functions
# ============================================================================

def _get_position_context(position: str, card_name: str, is_reversed: bool) -> str:
    """Generate position-specific interpretation context."""
    orientation = "reversed" if is_reversed else "upright"

    position_meanings = {
        "Present Insight": f"{card_name} ({orientation}) appears as your present insight, reflecting the energy currently surrounding your situation. This card asks you to look inward and acknowledge what is immediately present in your life.",
        "Today's Guiding Energy": f"{card_name} ({orientation}) is your guiding energy for today. Let this card's wisdom inform your decisions and interactions throughout the day.",
        "Past": f"In the past position, {card_name} ({orientation}) reveals the foundation of your current situation. These past experiences and energies have shaped where you are now.",
        "Present": f"{card_name} ({orientation}) in the present position shows the current energy at play. This is the central theme of what you are experiencing right now.",
        "Future": f"Looking ahead, {card_name} ({orientation}) suggests the direction things are moving. This is the likely outcome if current energies continue on their path.",
        "Present Situation": f"{card_name} ({orientation}) represents the heart of the matter — the core energy defining your current situation.",
        "Immediate Challenge": f"As the crossing card, {card_name} ({orientation}) reveals the immediate obstacle or energy that is either helping or hindering your progress.",
        "Distant Past / Root Cause": f"{card_name} ({orientation}) points to the deep root cause or distant past event that planted the seeds for your current situation.",
        "Recent Past": f"In the recent past, {card_name} ({orientation}) shows energies that are just beginning to fade but still influence your present.",
        "Best Possible Outcome": f"{card_name} ({orientation}) crowns your reading, showing the best possible outcome if you align with positive energies.",
        "Near Future": f"{card_name} ({orientation}) reveals what is coming into your life in the near future — events and energies on the immediate horizon.",
        "Your Attitude": f"{card_name} ({orientation}) reflects your own attitude and inner state regarding this situation. How you perceive and respond to challenges.",
        "External Influences": f"External forces represented by {card_name} ({orientation}) — people, environments, or circumstances beyond your control that affect the outcome.",
        "Hopes & Fears": f"{card_name} ({orientation}) in the hopes and fears position reveals your deepest wishes and anxieties about this situation.",
        "Final Outcome": f"The final outcome card, {card_name} ({orientation}), reveals the ultimate resolution and where all these energies converge.",
        "Current Career Energy": f"{card_name} ({orientation}) reflects the dominant energy in your professional life right now.",
        "Obstacles to Overcome": f"Career obstacles represented by {card_name} ({orientation}) — challenges to address for professional growth.",
        "Hidden Talents": f"{card_name} ({orientation}) reveals untapped professional strengths and hidden talents waiting to be leveraged.",
        "Recommended Action": f"The action card {card_name} ({orientation}) suggests the specific step or approach to take for career advancement.",
        "Career Outcome": f"{card_name} ({orientation}) reveals the projected career outcome based on current energies and actions.",
        "Your Energy in the Relationship": f"{card_name} ({orientation}) represents the energy you bring to this relationship.",
        "Partner's Energy": f"{card_name} ({orientation}) reveals the energy your partner or the other person brings to the dynamic.",
        "Relationship Foundation": f"The foundation of your relationship is represented by {card_name} ({orientation}) — the underlying bond and shared values.",
        "Current Challenge": f"{card_name} ({orientation}) highlights the current challenge or growth opportunity within the relationship.",
        "Relationship Potential": f"The potential card {card_name} ({orientation}) shows where this relationship can evolve if both parties grow together.",
    }

    return position_meanings.get(
        position,
        f"{card_name} ({orientation}) in the {position} position brings its unique energy to this aspect of your reading."
    )


def _generate_question_insight(card_name: str, meaning: str, question: str, is_reversed: bool) -> str:
    """Generate a question-specific insight blending the card's energy with the user's question."""
    orientation = "reversed" if is_reversed else "upright"
    return (
        f"Regarding your question — \"{question}\" — {card_name} ({orientation}) offers this insight: "
        f"{meaning} Consider how this energy directly relates to what you are asking. "
        f"The universe is guiding you to {'reconsider your approach and look for hidden factors' if is_reversed else 'trust the current flow and take confident action'}."
    )


def _synthesize_narrative(interpretations: List[Dict], question: Optional[str], spread_type: str) -> Dict[str, str]:
    """Synthesize an overall reading narrative from individual card interpretations."""
    card_names = [i["card_name"] for i in interpretations]
    orientations = [i["orientation"] for i in interpretations]
    reversed_count = orientations.count("reversed")
    total = len(interpretations)

    # Determine overall energy
    if reversed_count == 0:
        energy_tone = "strongly positive and forward-moving"
    elif reversed_count <= total * 0.3:
        energy_tone = "largely positive with minor areas requiring attention"
    elif reversed_count <= total * 0.6:
        energy_tone = "balanced between challenges and opportunities"
    else:
        energy_tone = "calling for deep reflection and internal transformation"

    # Check for major/minor arcana balance
    major_count = sum(1 for i in interpretations if i["arcana"] == "major")
    minor_count = total - major_count

    arcana_insight = ""
    if major_count > minor_count:
        arcana_insight = "The predominance of Major Arcana cards suggests significant life themes and karmic forces are at play. These are powerful, transformative energies."
    elif minor_count > major_count:
        arcana_insight = "The prevalence of Minor Arcana cards indicates that everyday actions and practical decisions are most important right now."
    else:
        arcana_insight = "A balanced mix of Major and Minor Arcana suggests both profound life themes and practical matters are intertwined."

    summary = (
        f"Your {SPREAD_CONFIGS[spread_type]['name']} reading reveals an energy that is {energy_tone}. "
        f"The cards drawn — {', '.join(card_names)} — weave together a story of your current journey. "
        f"{arcana_insight}"
    )

    advice = _generate_advice(interpretations)

    return {
        "summary": summary,
        "advice": advice,
        "energy_tone": energy_tone,
    }


def _generate_advice(interpretations: List[Dict]) -> str:
    """Generate actionable advice based on the reading."""
    # Collect all keywords
    all_keywords = []
    for interp in interpretations:
        all_keywords.extend(interp.get("keywords", []))

    # Find dominant themes
    positive_keywords = ["hope", "success", "abundance", "love", "growth", "renewal", "strength", "victory", "manifestation", "joy"]
    challenge_keywords = ["fear", "loss", "conflict", "deception", "stagnation", "control", "isolation", "destruction"]

    positive_count = sum(1 for k in all_keywords if k in positive_keywords)
    challenge_count = sum(1 for k in all_keywords if k in challenge_keywords)

    if positive_count > challenge_count:
        return (
            "The cards encourage you to move forward with confidence. The energies are aligned in your favor. "
            "Trust your instincts, take decisive action, and remain open to the opportunities unfolding before you. "
            "This is a time for growth and embracing new possibilities."
        )
    elif challenge_count > positive_count:
        return (
            "The reading suggests a period of introspection and careful consideration. "
            "Address challenges with patience rather than force. Look for hidden lessons in obstacles. "
            "This is a time for inner work, self-care, and strategic planning before taking major action."
        )
    else:
        return (
            "Balance is the key message of this reading. Neither rushing forward nor holding back will serve you best. "
            "Instead, find the middle path — act with intention, reflect with honesty, and remain adaptable. "
            "Trust that the right timing will reveal itself."
        )


def _extract_themes(interpretations: List[Dict]) -> List[str]:
    """Extract dominant themes from the reading."""
    all_keywords = []
    for interp in interpretations:
        all_keywords.extend(interp.get("keywords", []))

    # Count keyword frequency
    from collections import Counter
    keyword_counts = Counter(all_keywords)
    return [kw for kw, _ in keyword_counts.most_common(5)]


def _calculate_elemental_balance(interpretations: List[Dict]) -> Dict[str, int]:
    """Calculate the elemental balance of the reading."""
    elements = {"Fire": 0, "Water": 0, "Air": 0, "Earth": 0}
    for interp in interpretations:
        element = interp.get("element")
        if element in elements:
            elements[element] += 1
    return elements


def _calculate_confidence(interpretations: List[Dict]) -> float:
    """
    Calculate a confidence score (0.0 - 1.0) for the reading.
    Based on card harmony, elemental balance, and arcana distribution.
    """
    total = len(interpretations)
    if total == 0:
        return 0.5

    # Factor 1: Reversed ratio (fewer reversed = higher confidence in the reading's clarity)
    reversed_count = sum(1 for i in interpretations if i["orientation"] == "reversed")
    reversed_ratio = reversed_count / total
    clarity_score = 1.0 - (reversed_ratio * 0.3)

    # Factor 2: Elemental coherence
    elements = _calculate_elemental_balance(interpretations)
    non_zero = [v for v in elements.values() if v > 0]
    elemental_diversity = len(non_zero) / 4  # More elements = more balanced
    elemental_score = 0.5 + (elemental_diversity * 0.3)

    # Factor 3: Major arcana presence (more = more significant)
    major_count = sum(1 for i in interpretations if i["arcana"] == "major")
    significance_score = 0.6 + (major_count / total * 0.4) if total > 0 else 0.7

    # Weighted average
    confidence = (clarity_score * 0.4 + elemental_score * 0.3 + significance_score * 0.3)
    return round(min(max(confidence, 0.45), 0.98), 4)
