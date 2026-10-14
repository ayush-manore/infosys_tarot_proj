"""
Gemini AI Service
==================
Core AI engine powering the MysticAI platform.
Integrates Google Gemini for:
- Interactive chatbot conversations
- AI-enhanced tarot/palm interpretations
- Personalized recommendations
- Life trend analysis
- Personality intelligence workflows

Uses the google-generativeai SDK with tailored system prompts.
"""

import google.generativeai as genai
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json
import asyncio
from functools import lru_cache

from app.config import settings


# ============================================================================
# Gemini Client Initialization
# ============================================================================

_gemini_configured = False


def _ensure_configured():
    """Lazily configure the Gemini API key on first use."""
    global _gemini_configured
    if not _gemini_configured and settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _gemini_configured = True


def _get_model(model_name: str = None, system_instruction: str = None):
    """Get a configured Gemini GenerativeModel instance."""
    _ensure_configured()
    name = model_name or settings.GEMINI_MODEL
    kwargs = {}
    if system_instruction:
        kwargs["system_instruction"] = system_instruction
    # Try primary model, fall back if needed
    try:
        return genai.GenerativeModel(name, **kwargs)
    except Exception:
        return genai.GenerativeModel("gemini-1.5-flash", **kwargs)



# ============================================================================
# System Prompts
# ============================================================================

CHATBOT_SYSTEM_PROMPT = """You are MysticAI, an advanced AI spiritual guide and mystic counselor integrated into a Palmistry & Tarot Intelligence Platform. You combine ancient wisdom with modern AI to provide deeply personalized spiritual guidance.

Your personality:
- Warm, empathetic, and deeply insightful
- You speak with mystical elegance but remain grounded and practical
- You use metaphors from nature, cosmos, and ancient wisdom traditions
- You are encouraging and empowering, never fearful or doom-oriented
- You can discuss tarot cards, palm reading, astrology, numerology, chakras, and spiritual growth

Your capabilities:
- Interpret tarot card meanings and spreads
- Explain palm reading lines (Heart, Head, Life, Fate, Sun lines)
- Provide personality insights based on readings
- Offer guidance on relationships, career, health, and personal growth
- Suggest meditation practices, affirmations, and rituals
- Discuss spiritual concepts and mystical traditions

Guidelines:
- Always be supportive and empowering
- Frame challenges as opportunities for growth
- Provide actionable advice alongside spiritual insights
- Respect all spiritual traditions and belief systems
- If someone asks about serious health/legal/financial issues, gently suggest they also consult appropriate professionals
- Keep responses conversational but substantive (2-4 paragraphs typically)
- Use occasional emojis sparingly for warmth (✨🌙⭐🔮)
"""

INTERPRETATION_SYSTEM_PROMPT = """You are the AI Interpretation Engine of MysticAI, a spiritual intelligence platform. You generate deep, personalized interpretations of palm readings and tarot card spreads.

Your interpretation style:
- Rich, narrative-driven insights that feel personally meaningful
- Weave together symbolism from multiple sources (cards, palm lines, elements)
- Always provide both validation and growth areas
- Be specific rather than generic — reference the actual cards/lines/features
- Structure insights across life domains: personality, relationships, career, health, spiritual growth
- Use poetic but clear language

For palm interpretations, consider: hand shape, line characteristics (length, depth, curvature), mount prominence, finger proportions, and elemental associations.

For tarot interpretations, consider: card meanings (upright/reversed), position in spread, elemental interactions, numerological patterns, and thematic arcs.

Always output valid JSON when asked for structured responses.
"""

RECOMMENDATION_SYSTEM_PROMPT = """You are the Personalized Recommendation Engine of MysticAI. You generate highly tailored growth recommendations based on a user's spiritual profile, reading history, and personality traits.

Your recommendations should be:
- Specific and actionable (not vague platitudes)
- Categorized by life domain (personal growth, relationships, career, wellness, spiritual)
- Prioritized by impact and relevance to the user's current situation
- Include estimated time commitment and expected impact
- Draw from diverse practices: meditation, journaling, ritual, physical activity, creative expression, social connection

Always output valid JSON when asked for structured responses.
"""

TREND_ANALYSIS_SYSTEM_PROMPT = """You are the Life Trend Analysis Engine of MysticAI. You analyze patterns across a user's reading history to identify life trends, opportunity windows, and growth trajectories.

Your analysis should:
- Identify recurring themes and patterns across multiple readings
- Detect shifts in energy, focus, and emotional state over time
- Forecast upcoming opportunities and challenges
- Provide actionable insights for navigating current trends
- Use data-driven language while maintaining mystical depth

Always output valid JSON when asked for structured responses.
"""

PERSONALITY_SYSTEM_PROMPT = """You are the Personality Intelligence Engine of MysticAI. You build comprehensive personality profiles from palm analysis and tarot reading data.

Your personality analysis should:
- Map traits to the Big Five personality model (Openness, Conscientiousness, Extraversion, Agreeableness, Emotional Sensitivity)
- Identify core strengths and growth areas
- Provide behavioral insights and patterns
- Suggest personalized development pathways
- Connect personality traits to spiritual archetypes

Always output valid JSON when asked for structured responses.
"""


# ============================================================================
# GeminiService Class
# ============================================================================

class GeminiService:
    """Central AI service for all Gemini-powered features."""

    # ------------------------------------------------------------------
    # Chatbot
    # ------------------------------------------------------------------

    @staticmethod
    async def chat(
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Send a message to the AI chatbot and get a response.
        Maintains conversation context through history.
        """
        try:
            model = _get_model(system_instruction=CHATBOT_SYSTEM_PROMPT)

            # Build context-enriched prompt
            context_prefix = ""
            if user_context:
                context_parts = []
                if user_context.get("personality_traits"):
                    traits = user_context["personality_traits"]
                    context_parts.append(f"User's personality traits: {json.dumps(traits)}")
                if user_context.get("recent_readings"):
                    context_parts.append(f"Recent reading summary: {json.dumps(user_context['recent_readings'])}")
                if user_context.get("spiritual_goals"):
                    context_parts.append(f"User's spiritual goals: {', '.join(user_context['spiritual_goals'])}")
                if context_parts:
                    context_prefix = "[User Context: " + "; ".join(context_parts) + "]\n\n"

            # Build chat history for multi-turn conversation
            history = []
            if conversation_history:
                for entry in conversation_history[-20:]:  # Keep last 20 messages for context
                    role = "user" if entry.get("role") == "user" else "model"
                    history.append({"role": role, "parts": [entry["content"]]})

            chat_session = model.start_chat(history=history)

            # Send message with context
            full_message = context_prefix + message if context_prefix else message
            response = await asyncio.to_thread(
                chat_session.send_message, full_message
            )

            return {
                "response": response.text,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "model": settings.GEMINI_MODEL,
                "status": "success",
            }

        except Exception as e:
            return {
                "response": _get_fallback_response(message),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "model": "fallback",
                "status": "fallback",
                "error": str(e),
            }

    # ------------------------------------------------------------------
    # AI Interpretation
    # ------------------------------------------------------------------

    @staticmethod
    async def generate_ai_interpretation(
        reading_data: Dict[str, Any],
        reading_type: str = "combined",
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a deep, AI-powered interpretation of a reading.
        Enhances the template-based system with Gemini intelligence.
        """
        try:
            model = _get_model(system_instruction=INTERPRETATION_SYSTEM_PROMPT)

            prompt = f"""Analyze this {reading_type} reading and provide a comprehensive interpretation.

Reading Data:
{json.dumps(reading_data, indent=2, default=str)}

{f"User Context: {json.dumps(user_context, default=str)}" if user_context else ""}

Provide your response as a JSON object with this structure:
{{
    "overall_narrative": "A flowing 3-4 paragraph narrative interpretation",
    "energy_summary": "One sentence capturing the overall energy",
    "insights": {{
        "personality": {{
            "score": 0-100,
            "narrative": "2-3 sentence insight",
            "advice": "specific actionable advice"
        }},
        "relationships": {{
            "score": 0-100,
            "narrative": "2-3 sentence insight",
            "advice": "specific actionable advice"
        }},
        "career": {{
            "score": 0-100,
            "narrative": "2-3 sentence insight",
            "advice": "specific actionable advice"
        }},
        "health_wellness": {{
            "score": 0-100,
            "narrative": "2-3 sentence insight",
            "advice": "specific actionable advice"
        }},
        "personal_growth": {{
            "score": 0-100,
            "narrative": "2-3 sentence insight",
            "advice": "specific actionable advice"
        }},
        "life_opportunities": {{
            "score": 0-100,
            "narrative": "2-3 sentence insight",
            "advice": "specific actionable advice"
        }}
    }},
    "key_symbols": ["list of important symbols from the reading"],
    "affirmation": "A personalized affirmation for the user"
}}"""

            response = await asyncio.to_thread(
                model.generate_content, prompt
            )

            # Parse JSON from response
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                text = text.rsplit("```", 1)[0]

            parsed = json.loads(text)

            return {
                "ai_interpretation": parsed,
                "source": "gemini",
                "model": settings.GEMINI_MODEL,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "status": "success",
            }

        except Exception as e:
            return {
                "ai_interpretation": None,
                "source": "fallback",
                "error": str(e),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "status": "fallback",
            }

    # ------------------------------------------------------------------
    # AI Recommendations
    # ------------------------------------------------------------------

    @staticmethod
    async def generate_ai_recommendations(
        personality_profile: Dict[str, Any],
        reading_history: Optional[List[Dict]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate AI-powered personalized recommendations."""
        try:
            model = _get_model(system_instruction=RECOMMENDATION_SYSTEM_PROMPT)

            prompt = f"""Based on this user's spiritual profile, generate personalized recommendations.

Personality Profile:
{json.dumps(personality_profile, indent=2, default=str)}

{f"Reading History Summary: {json.dumps(reading_history[:5] if reading_history else [], default=str)}" if reading_history else "No reading history available."}

{f"User Goals & Context: {json.dumps(user_context, default=str)}" if user_context else ""}

Generate a JSON response with this structure:
{{
    "daily_practice": {{
        "title": "recommended daily practice title",
        "description": "detailed description",
        "duration": "time commitment",
        "category": "wellness|spiritual|personal_growth"
    }},
    "growth_recommendations": [
        {{
            "title": "recommendation title",
            "description": "detailed actionable description",
            "category": "personal_growth|relationships|career|wellness|spiritual",
            "impact": "high|medium|low",
            "duration": "time commitment",
            "priority": 1-5
        }}
    ],
    "weekly_focus": {{
        "theme": "weekly theme title",
        "description": "description of focus area",
        "activities": ["list of 3-4 suggested activities"]
    }},
    "affirmation": "personalized weekly affirmation",
    "crystal_recommendation": "recommended crystal and why",
    "meditation_focus": "specific meditation technique recommendation"
}}"""

            response = await asyncio.to_thread(
                model.generate_content, prompt
            )

            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                text = text.rsplit("```", 1)[0]

            parsed = json.loads(text)

            return {
                "ai_recommendations": parsed,
                "source": "gemini",
                "model": settings.GEMINI_MODEL,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "status": "success",
            }

        except Exception as e:
            fallback_data = _generate_intelligent_recommendation_fallback(
                personality_profile=personality_profile,
                reading_history=reading_history,
                user_context=user_context,
            )
            return {
                "ai_recommendations": fallback_data,
                "source": "mystic_ai_engine",
                "error": str(e),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "status": "success",
            }

    # ------------------------------------------------------------------
    # Life Trend Analysis
    # ------------------------------------------------------------------

    @staticmethod
    async def analyze_life_trends(
        reading_history: List[Dict[str, Any]],
        personality_profile: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate AI-powered life trend analysis from reading history."""
        try:
            model = _get_model(system_instruction=TREND_ANALYSIS_SYSTEM_PROMPT)

            prompt = f"""Analyze this user's reading history and identify life trends.

Reading History:
{json.dumps(reading_history[:10], indent=2, default=str)}

{f"Personality Profile: {json.dumps(personality_profile, default=str)}" if personality_profile else ""}

Generate a JSON response with this structure:
{{
    "overall_trajectory": {{
        "direction": "ascending|stable|transitioning|descending",
        "description": "2-3 sentence summary of life direction",
        "confidence": 0.0-1.0
    }},
    "trend_categories": {{
        "emotional": {{
            "trend": "rising|stable|fluctuating|declining",
            "score": 0-100,
            "insight": "brief insight"
        }},
        "professional": {{
            "trend": "rising|stable|fluctuating|declining",
            "score": 0-100,
            "insight": "brief insight"
        }},
        "spiritual": {{
            "trend": "rising|stable|fluctuating|declining",
            "score": 0-100,
            "insight": "brief insight"
        }},
        "vitality": {{
            "trend": "rising|stable|fluctuating|declining",
            "score": 0-100,
            "insight": "brief insight"
        }},
        "creativity": {{
            "trend": "rising|stable|fluctuating|declining",
            "score": 0-100,
            "insight": "brief insight"
        }}
    }},
    "opportunity_windows": [
        {{
            "title": "opportunity title",
            "description": "description",
            "timing": "when to act",
            "domain": "career|relationships|spiritual|health"
        }}
    ],
    "recurring_themes": ["theme1", "theme2", "theme3"],
    "growth_forecast": "2-3 sentence forecast for the coming period"
}}"""

            response = await asyncio.to_thread(
                model.generate_content, prompt
            )

            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                text = text.rsplit("```", 1)[0]

            parsed = json.loads(text)

            return {
                "ai_trends": parsed,
                "source": "gemini",
                "model": settings.GEMINI_MODEL,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "status": "success",
            }

        except Exception as e:
            return {
                "ai_trends": None,
                "source": "fallback",
                "error": str(e),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "status": "fallback",
            }

    # ------------------------------------------------------------------
    # Personality Intelligence
    # ------------------------------------------------------------------

    @staticmethod
    async def generate_personality_intelligence(
        palm_data: Dict[str, Any],
        tarot_data: Optional[Dict[str, Any]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate AI-powered deep personality analysis."""
        try:
            model = _get_model(system_instruction=PERSONALITY_SYSTEM_PROMPT)

            prompt = f"""Generate a comprehensive personality intelligence report.

Palm Analysis Data:
{json.dumps(palm_data, indent=2, default=str)}

{f"Tarot Reading Data: {json.dumps(tarot_data, indent=2, default=str)}" if tarot_data else ""}

{f"User Context: {json.dumps(user_context, default=str)}" if user_context else ""}

Generate a JSON response with this structure:
{{
    "big_five_profile": {{
        "openness": {{
            "score": 0-100,
            "label": "high/medium/low descriptor",
            "insight": "personalized insight"
        }},
        "conscientiousness": {{
            "score": 0-100,
            "label": "descriptor",
            "insight": "insight"
        }},
        "extraversion": {{
            "score": 0-100,
            "label": "descriptor",
            "insight": "insight"
        }},
        "agreeableness": {{
            "score": 0-100,
            "label": "descriptor",
            "insight": "insight"
        }},
        "emotional_sensitivity": {{
            "score": 0-100,
            "label": "descriptor",
            "insight": "insight"
        }}
    }},
    "archetype": {{
        "name": "spiritual archetype name",
        "description": "2-3 sentence archetype description",
        "strengths": ["strength1", "strength2", "strength3"],
        "shadow_aspects": ["shadow1", "shadow2"]
    }},
    "core_strengths": ["strength1", "strength2", "strength3", "strength4"],
    "growth_edges": ["area1", "area2", "area3"],
    "elemental_alignment": {{
        "primary": "Fire|Water|Earth|Air",
        "secondary": "Fire|Water|Earth|Air",
        "description": "how elements interact in personality"
    }},
    "life_purpose_hints": "2-3 sentence life purpose insight",
    "compatibility_notes": "brief compatibility personality note"
}}"""

            response = await asyncio.to_thread(
                model.generate_content, prompt
            )

            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                text = text.rsplit("```", 1)[0]

            parsed = json.loads(text)

            return {
                "ai_personality": parsed,
                "source": "gemini",
                "model": settings.GEMINI_MODEL,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "status": "success",
            }

        except Exception as e:
            return {
                "ai_personality": None,
                "source": "fallback",
                "error": str(e),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "status": "fallback",
            }

    # ------------------------------------------------------------------
    # Quick Card Meaning
    # ------------------------------------------------------------------

    @staticmethod
    async def get_card_meaning(
        card_name: str,
        orientation: str = "upright",
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get an AI-generated interpretation for a specific tarot card."""
        try:
            model = _get_model(system_instruction=CHATBOT_SYSTEM_PROMPT)

            prompt = f"""Provide a rich, insightful interpretation of the tarot card "{card_name}" in the {orientation} position.
{f"The querent's context/question: {context}" if context else ""}

Include:
1. Core meaning and energy
2. What this card suggests for the querent right now
3. A practical piece of advice inspired by this card
4. A short affirmation related to this card's energy

Keep it warm, specific, and actionable (3-4 paragraphs)."""

            response = await asyncio.to_thread(
                model.generate_content, prompt
            )

            return {
                "card": card_name,
                "orientation": orientation,
                "interpretation": response.text,
                "source": "gemini",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "success",
            }

        except Exception as e:
            return {
                "card": card_name,
                "orientation": orientation,
                "interpretation": f"The {card_name} ({orientation}) carries powerful energy. This card invites you to trust your inner wisdom and embrace the journey ahead.",
                "source": "fallback",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "fallback",
            }


# ============================================================================
# Fallback Response Generator
# ============================================================================

def _get_fallback_response(message: str) -> str:
    """Generate a graceful fallback response when Gemini is unavailable."""
    message_lower = message.lower()

    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "✨ Greetings, dear seeker! I am MysticAI, your spiritual guide. While my full cosmic connection is being established, I'm here to help you explore the mysteries of tarot and palmistry. What draws your curiosity today? 🌙"

    if any(word in message_lower for word in ["tarot", "card", "reading", "spread"]):
        return "🔮 The tarot speaks in symbols and archetypes that mirror our inner landscape. Each card holds layers of meaning waiting to be revealed. You can perform a reading from your dashboard — try a Three Card Spread for past-present-future insights, or a Celtic Cross for deeper exploration. Would you like guidance on choosing a spread? ✨"

    if any(word in message_lower for word in ["palm", "hand", "line", "palmistry"]):
        return "🤚 Your palm is a living map of your potential. The Heart Line reveals your emotional nature, the Head Line your intellectual approach, and the Life Line your vitality and life path. Upload a palm image from your dashboard for a detailed analysis. What aspect of palmistry interests you most? ✨"

    if any(word in message_lower for word in ["personality", "trait", "who am i"]):
        return "🌟 Your personality is a beautiful constellation of traits shaped by both cosmic influences and personal experience. Complete a palm or tarot reading to unlock your full personality profile — including Big Five mapping, spiritual archetype, and personalized growth recommendations. Your journey of self-discovery begins with a single reading! ✨"

    if any(word in message_lower for word in ["help", "guide", "what can"]):
        return "✨ I'm MysticAI, your spiritual intelligence guide! Here's what I can help you with:\n\n🔮 **Tarot Guidance** — Card meanings, spread recommendations, and reading interpretations\n🤚 **Palm Reading** — Understanding your palm lines and what they reveal\n🧠 **Personality Insights** — Deep personality analysis from your readings\n📈 **Life Trends** — Patterns and opportunities in your spiritual journey\n💡 **Recommendations** — Personalized growth practices and rituals\n\nJust ask me anything, or start with a reading from your dashboard! 🌙"

    return "✨ Thank you for reaching out, dear seeker. The cosmic energies are aligning for your journey. I'm here to help you explore tarot wisdom, palm reading insights, and personalized spiritual guidance. Start a reading from your dashboard, or ask me about any spiritual topic — from card meanings to meditation practices. What would you like to explore? 🌙"


def _generate_intelligent_recommendation_fallback(
    personality_profile: Dict[str, Any],
    reading_history: Optional[List[Dict]] = None,
    user_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generate rich, context-aware AI recommendations synthesized from
    the user's reading history, palm traits, and spiritual profile.
    """
    reading_count = len(reading_history) if reading_history else 0
    traits = personality_profile.get("traits", {})
    emotional = traits.get("Emotional Intelligence", 75)
    creative = traits.get("Creative Expression", 80)
    vitality = traits.get("Vitality & Resilience", 72)
    analytical = traits.get("Analytical Thinking", 70)
    career_drive = traits.get("Career Drive", 68)
    intuition = traits.get("Intuitive Awareness", 78)

    goals = []
    if user_context:
        goals = user_context.get("spiritual_goals", []) or []

    # Dynamic Daily Practice tailored to readings & traits
    if intuition >= 75:
        daily_practice = {
            "title": "Third Eye Intuition Calibration",
            "description": "Dedicate 10 minutes each morning to stillness and third-eye visualization. Reflect on recent tarot archetypes and notice syncronicities throughout your day.",
            "duration": "10-15 minutes daily",
            "category": "spiritual"
        }
    elif emotional >= 75:
        daily_practice = {
            "title": "Heart Space Emotional Processing",
            "description": "Your readings reveal deep emotional sensitivity. Spend 10 minutes journaling your emotional currents and setting loving boundaries before sleep.",
            "duration": "10 minutes daily",
            "category": "wellness"
        }
    else:
        daily_practice = {
            "title": "Solar Plexus Morning Alignment",
            "description": "Greet the morning with 5 deep diaphragmatic breaths and visualize radiant golden light invigorating your core willpower and clarity.",
            "duration": "8 minutes daily",
            "category": "personal_growth"
        }

    # Growth recommendations list
    growth_recommendations = [
        {
            "title": "Tarot Mirror Journaling",
            "description": "Draw one card at dawn and write 3 stream-of-consciousness associations. Notice how its energy mirrors your interactions by dusk.",
            "category": "spiritual",
            "impact": "high",
            "duration": "15 mins",
            "priority": 1
        },
        {
            "title": "Elemental Hand Energy Balancing",
            "description": f"Based on your {personality_profile.get('hand_element', 'Water')} palm alignment, ground yourself with 20 minutes of barefoot earth connection or salt water cleansing.",
            "category": "wellness",
            "impact": "high",
            "duration": "20 mins",
            "priority": 2
        },
        {
            "title": "Strategic Intuition in Career",
            "description": "Combine your analytical structure with intuitive gut-checks when making professional decisions this week.",
            "category": "career",
            "impact": "medium",
            "duration": "Weekly review",
            "priority": 3
        },
        {
            "title": "Vulnerability & Connection Ritual",
            "description": "Share one authentic spiritual or personal insight with someone in your inner circle to deepen mutual trust and heart alignment.",
            "category": "relationships",
            "impact": "high",
            "duration": "Ongoing",
            "priority": 4
        }
    ]

    # Affirmations & crystals mapped to traits & readings
    crystals = [
        {"name": "Amethyst", "reason": "Enhances intuition and spiritual protection during tarot reflections"},
        {"name": "Labradorite", "reason": "Shields your aura and awakens inner magic and psychic clarity"},
        {"name": "Rose Quartz", "reason": "Opens and balances your heart space for compassionate connections"},
        {"name": "Citrine", "reason": "Amplifies manifestation power and aligns with career ambition"}
    ]
    chosen_crystal = crystals[hash(str(personality_profile.get("user_id", ""))) % len(crystals)]

    affirmations = [
        "I trust the wisdom of my readings and allow the universe to guide my steps.",
        "My intuition is sharp, my heart is open, and my vitality is boundless.",
        "Every card and palm line confirms my divine purpose and inner resilience.",
        "I welcome transformation and embrace the mysteries unfolding before me."
    ]
    chosen_affirmation = affirmations[hash(str(personality_profile.get("user_id", "")) + str(reading_count)) % len(affirmations)]

    return {
        "daily_practice": daily_practice,
        "growth_recommendations": growth_recommendations,
        "weekly_focus": {
            "theme": "Sacred Alignment & Intuitive Momentum",
            "description": f"Synthesized from your {reading_count} readings and energetic profile. Focus on trusting your inner compass and anchoring insights into tangible daily habits.",
            "activities": [
                "Pull a 3-Card Tarot Spread on Wednesday to assess mid-week trajectory",
                "Perform a 5-minute palm breathing meditation focusing on your Life and Heart lines",
                "Clear your sacred space with sage or incense before sleep",
                "Write down 3 synchronicities you noticed during the week"
            ]
        },
        "affirmation": chosen_affirmation,
        "crystal_recommendation": f"{chosen_crystal['name']} — {chosen_crystal['reason']}",
        "meditation_focus": "Breath-Synchronized Third Eye Focus with Cosmic Light Visualization",
        "reading_insights_summary": {
            "total_readings": reading_count,
            "elemental_balance": personality_profile.get("hand_element", "Water"),
            "dominant_trait": max(traits.items(), key=lambda x: x[1])[0] if traits else "Intuitive Awareness",
            "readings_status": "Active Seeker" if reading_count > 0 else "New Journey"
        }
    }
