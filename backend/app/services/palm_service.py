"""
Palm Analysis Engine
====================
Simulated palm feature extraction and interpretation engine.
Architecture supports future drop-in replacement with real OpenCV + MediaPipe.

Features:
- Palm image acceptance (base64 or file upload)
- Simulated hand landmark detection & line classification
- Feature-to-interpretation mapping using palmistry_lines.json
- Personality trait scoring from palm features
- Combined palm reading narrative generation
"""

import json
import random
import os
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

# Load palmistry interpretation data
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def _load_palmistry_data() -> List[Dict]:
    """Load palmistry lines interpretation data."""
    with open(os.path.join(DATA_DIR, "palmistry_lines.json"), "r", encoding="utf-8") as f:
        return json.load(f)

PALMISTRY_LINES = _load_palmistry_data()

# Map line IDs to their data for quick lookup
LINES_MAP = {line["id"]: line for line in PALMISTRY_LINES}

# ============================================================================
# Simulated Feature Extraction
# ============================================================================

# Possible characteristics for each palm line
LINE_CHARACTERISTICS = {
    "heart_line": [
        "long_and_curved", "short_and_straight", "wavy", "broken",
        "deep_and_clear", "faint_or_thin", "curved_upward",
        "starts_under_index_finger", "starts_under_middle_finger",
        "starts_between_index_and_middle"
    ],
    "head_line": [
        "long_and_straight", "short", "curved_or_sloping",
        "deep_and_clear", "wavy", "broken", "forked_end",
        "separate_from_life_line", "joined_with_life_line", "chained"
    ],
    "life_line": [
        "long_and_deep", "short_and_shallow", "curving_widely",
        "close_to_thumb", "curved_semicircle",
        "straight_and_close_to_palm_edge", "broken",
        "multiple_lines", "chained", "absent"
    ],
    "fate_line": [
        "deep_and_clear", "faint", "broken",
        "starts_at_base_of_palm", "starts_at_head_line",
        "starts_at_heart_line", "forked", "absent"
    ],
    "sun_line": [
        "clear_and_strong", "faint_or_absent", "broken",
        "starts_at_wrist", "starts_at_head_line",
        "starts_at_heart_line", "multiple_lines", "wavy"
    ],
}

# Hand shape classifications
HAND_SHAPES = [
    {
        "type": "Earth Hand",
        "description": "Square palms with short fingers",
        "traits": ["practical", "grounded", "reliable", "hardworking"],
        "element": "Earth",
    },
    {
        "type": "Air Hand",
        "description": "Square or rectangular palms with long fingers",
        "traits": ["intellectual", "communicative", "curious", "analytical"],
        "element": "Air",
    },
    {
        "type": "Water Hand",
        "description": "Long or oval palms with long, flexible fingers",
        "traits": ["intuitive", "creative", "sensitive", "emotional"],
        "element": "Water",
    },
    {
        "type": "Fire Hand",
        "description": "Square or rectangular palms with short fingers",
        "traits": ["energetic", "passionate", "optimistic", "bold"],
        "element": "Fire",
    },
]


class PalmService:
    """Palm analysis intelligence engine."""

    @staticmethod
    def analyze_palm(
        image_data: Optional[str] = None,
        image_filename: Optional[str] = None,
        user_seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Perform a complete palm analysis.
        
        Currently uses simulated feature extraction that generates
        realistic, consistent results based on image hash or user seed.
        Architecture is designed for drop-in replacement with real
        OpenCV + MediaPipe pipeline.
        
        Args:
            image_data: Base64-encoded palm image (optional)
            image_filename: Filename of uploaded image (optional)
            user_seed: User ID or seed for consistent results
        
        Returns:
            Complete palm analysis with line interpretations,
            personality traits, and narrative.
        """
        # Generate a deterministic seed from the image or user
        seed = _generate_seed(image_data, image_filename, user_seed)
        rng = random.Random(seed)

        # Step 1: Detect hand shape
        hand_shape = _detect_hand_shape(rng)

        # Step 2: Extract line features (simulated)
        line_features = _extract_line_features(rng)

        # Step 3: Generate interpretations for each line
        line_interpretations = _interpret_lines(line_features)

        # Step 4: Calculate personality traits
        personality = _calculate_personality(line_features, hand_shape, rng)

        # Step 5: Generate overall narrative
        narrative = _generate_palm_narrative(hand_shape, line_interpretations, personality)

        # Step 6: Calculate confidence
        confidence = _calculate_palm_confidence(line_features, rng)

        analysis = {
            "hand_shape": hand_shape,
            "lines": line_interpretations,
            "personality_traits": personality,
            "narrative": narrative,
            "confidence_score": confidence,
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            "image_filename": image_filename,
            "analysis_method": "simulated_cv",  # Will change to "mediapipe" when real CV is added
            "landmarks_detected": _generate_landmark_data(rng),
        }

        return analysis

    @staticmethod
    def get_available_lines() -> List[Dict[str, Any]]:
        """Return information about all analyzable palm lines."""
        return [
            {
                "id": line["id"],
                "name": line["name"],
                "alternative_names": line.get("alternative_names", []),
                "location": line["location"],
                "element": line.get("element"),
                "description": line["description"],
                "traits": line.get("associated_traits", []),
            }
            for line in PALMISTRY_LINES
        ]


# ============================================================================
# Private Helper Functions
# ============================================================================

def _generate_seed(image_data: Optional[str], filename: Optional[str], user_seed: Optional[str]) -> int:
    """Generate a deterministic seed from available inputs."""
    seed_material = ""
    if image_data:
        seed_material = hashlib.md5(image_data[:200].encode()).hexdigest()
    elif filename:
        seed_material = hashlib.md5(filename.encode()).hexdigest()
    elif user_seed:
        seed_material = hashlib.md5(user_seed.encode()).hexdigest()
    else:
        seed_material = hashlib.md5(str(datetime.now(timezone.utc)).encode()).hexdigest()
    return int(seed_material[:8], 16)


def _detect_hand_shape(rng: random.Random) -> Dict[str, Any]:
    """Simulate hand shape detection."""
    shape = rng.choice(HAND_SHAPES)
    return {
        "type": shape["type"],
        "description": shape["description"],
        "traits": shape["traits"],
        "element": shape["element"],
        "confidence": round(rng.uniform(0.78, 0.95), 4),
    }


def _extract_line_features(rng: random.Random) -> Dict[str, Dict[str, Any]]:
    """
    Simulate palm line feature extraction.
    For each line, randomly select characteristics with realistic probabilities.
    """
    features = {}
    for line_id, characteristics in LINE_CHARACTERISTICS.items():
        # Each line gets 1-2 characteristics
        num_chars = rng.randint(1, 2)
        selected = rng.sample(characteristics, min(num_chars, len(characteristics)))

        # Generate realistic measurement data
        features[line_id] = {
            "detected": rng.random() > 0.05,  # 95% detection rate
            "characteristics": selected,
            "length_mm": round(rng.uniform(40, 120), 1),
            "depth": rng.choice(["shallow", "moderate", "deep"]),
            "clarity": rng.choice(["faint", "clear", "very_clear"]),
            "curvature_degrees": round(rng.uniform(5, 45), 1),
            "branch_count": rng.randint(0, 4),
            "confidence": round(rng.uniform(0.72, 0.96), 4),
        }

    return features


def _interpret_lines(line_features: Dict[str, Dict]) -> List[Dict[str, Any]]:
    """Map extracted line features to interpretations from palmistry data."""
    interpretations = []

    for line_id, features in line_features.items():
        line_data = LINES_MAP.get(line_id)
        if not line_data or not features.get("detected"):
            continue

        # Get interpretations for detected characteristics
        char_interpretations = []
        for char in features["characteristics"]:
            if char in line_data.get("interpretations", {}):
                char_interpretations.append({
                    "characteristic": char.replace("_", " ").title(),
                    "interpretation": line_data["interpretations"][char],
                })

        interpretations.append({
            "line_id": line_id,
            "line_name": line_data["name"],
            "alternative_names": line_data.get("alternative_names", []),
            "element": line_data.get("element"),
            "location": line_data["location"],
            "detected": features["detected"],
            "measurements": {
                "length_mm": features["length_mm"],
                "depth": features["depth"],
                "clarity": features["clarity"],
                "curvature": features["curvature_degrees"],
                "branches": features["branch_count"],
            },
            "characteristics": char_interpretations,
            "confidence": features["confidence"],
            "associated_traits": line_data.get("associated_traits", []),
        })

    return interpretations


def _calculate_personality(
    line_features: Dict, hand_shape: Dict, rng: random.Random
) -> List[Dict[str, Any]]:
    """Calculate personality trait scores based on palm features."""
    traits = [
        {
            "trait": "Emotional Intelligence",
            "score": _score_trait(line_features, "heart_line", rng),
            "description": "Your capacity for empathy, emotional awareness, and relationship depth.",
            "color": "from-pink-500 to-rose-500",
        },
        {
            "trait": "Analytical Thinking",
            "score": _score_trait(line_features, "head_line", rng),
            "description": "Your intellectual capacity, problem-solving style, and decision-making clarity.",
            "color": "from-cyan-500 to-blue-500",
        },
        {
            "trait": "Vitality & Resilience",
            "score": _score_trait(line_features, "life_line", rng),
            "description": "Your physical energy, life force, and ability to overcome challenges.",
            "color": "from-emerald-500 to-teal-500",
        },
        {
            "trait": "Career Drive",
            "score": _score_trait(line_features, "fate_line", rng),
            "description": "Your ambition, sense of purpose, and alignment with your destined career path.",
            "color": "from-amber-500 to-orange-500",
        },
        {
            "trait": "Creative Expression",
            "score": _score_trait(line_features, "sun_line", rng),
            "description": "Your artistic abilities, public recognition potential, and creative life force.",
            "color": "from-purple-500 to-indigo-500",
        },
        {
            "trait": "Intuitive Awareness",
            "score": min(95, int(
                (_score_trait(line_features, "heart_line", rng) +
                 _score_trait(line_features, "head_line", rng)) / 2 +
                rng.randint(-5, 10)
            )),
            "description": "Your natural intuition, spiritual sensitivity, and inner wisdom.",
            "color": "from-violet-500 to-fuchsia-500",
        },
    ]

    return traits


def _score_trait(line_features: Dict, line_id: str, rng: random.Random) -> int:
    """Score a personality trait based on line features."""
    features = line_features.get(line_id, {})
    if not features.get("detected"):
        return rng.randint(40, 60)

    base_score = 65
    depth = features.get("depth", "moderate")
    clarity = features.get("clarity", "clear")

    if depth == "deep":
        base_score += 15
    elif depth == "shallow":
        base_score -= 10

    if clarity == "very_clear":
        base_score += 10
    elif clarity == "faint":
        base_score -= 8

    # Add some variance
    base_score += rng.randint(-5, 10)
    return max(30, min(98, base_score))


def _generate_palm_narrative(
    hand_shape: Dict, line_interpretations: List[Dict], personality: List[Dict]
) -> Dict[str, str]:
    """Generate a comprehensive palm reading narrative."""
    shape_type = hand_shape["type"]
    shape_traits = ", ".join(hand_shape["traits"])

    # Find strongest and weakest traits
    sorted_traits = sorted(personality, key=lambda x: x["score"], reverse=True)
    strongest = sorted_traits[0]
    growth_area = sorted_traits[-1]

    summary = (
        f"Your palm reveals a {shape_type}, characterized by {hand_shape['description'].lower()}. "
        f"This hand shape is associated with being {shape_traits}. "
        f"Your palm's elemental alignment is {hand_shape['element']}, indicating a natural resonance "
        f"with {_element_description(hand_shape['element'])}."
    )

    # Compile line insights
    line_insights = []
    for line in line_interpretations:
        if line["characteristics"]:
            first_char = line["characteristics"][0]
            line_insights.append(
                f"Your {line['line_name']} ({', '.join(line.get('alternative_names', []))}) "
                f"shows a {first_char['characteristic'].lower()} pattern: {first_char['interpretation']}"
            )

    detailed = " ".join(line_insights) if line_insights else "Analysis of your palm lines reveals a complex and nuanced personality."

    advice = (
        f"Your strongest trait is {strongest['trait']} (score: {strongest['score']}%), "
        f"which is a powerful asset in your life journey. "
        f"An area for growth is {growth_area['trait']} (score: {growth_area['score']}%). "
        f"Focus on nurturing this aspect through mindful practice and self-awareness. "
        f"Your {shape_type} suggests that you thrive when you embrace your natural tendencies toward "
        f"being {shape_traits}."
    )

    return {
        "summary": summary,
        "detailed_analysis": detailed,
        "advice": advice,
    }


def _element_description(element: str) -> str:
    """Get a description for an element."""
    descriptions = {
        "Earth": "stability, practicality, and material success",
        "Air": "communication, intellectual pursuits, and social connections",
        "Water": "emotional depth, intuition, and creative expression",
        "Fire": "passion, energy, and bold action",
    }
    return descriptions.get(element, "balanced energies")


def _generate_landmark_data(rng: random.Random) -> Dict[str, Any]:
    """Generate simulated hand landmark detection data."""
    return {
        "total_landmarks": 21,
        "detected_landmarks": rng.randint(18, 21),
        "hand_detected": True,
        "dominant_hand": rng.choice(["left", "right"]),
        "palm_center": {"x": round(rng.uniform(0.4, 0.6), 3), "y": round(rng.uniform(0.4, 0.6), 3)},
        "finger_count": 5,
        "wrist_position": {"x": round(rng.uniform(0.4, 0.6), 3), "y": round(rng.uniform(0.8, 0.95), 3)},
    }


def _calculate_palm_confidence(line_features: Dict, rng: random.Random) -> float:
    """Calculate overall palm analysis confidence score."""
    detected_count = sum(1 for f in line_features.values() if f.get("detected"))
    total = len(line_features)

    detection_ratio = detected_count / total if total > 0 else 0.5
    avg_confidence = sum(f.get("confidence", 0.7) for f in line_features.values()) / total if total > 0 else 0.7

    confidence = (detection_ratio * 0.4 + avg_confidence * 0.6)
    return round(min(max(confidence, 0.50), 0.96), 4)
