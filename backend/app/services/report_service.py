"""
Reports & Export Service
=========================
Generates comprehensive reports for palmistry, tarot, personality,
and spiritual guidance readings. Supports PDF and CSV export.
"""

import csv
import io
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from app.services.palm_service import PalmService
from app.services.tarot_service import TarotService
from app.services.interpretation_service import InterpretationService
from app.services.personality_service import PersonalityService
from app.services.scoring_service import ScoringService


class ReportService:
    """Report generation and export service."""

    @staticmethod
    def generate_palm_report(palm_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive palmistry report."""
        hand_shape = palm_analysis.get("hand_shape", {})
        lines = palm_analysis.get("lines", [])
        personality = palm_analysis.get("personality_traits", [])
        narrative = palm_analysis.get("narrative", {})

        # Build report sections
        sections = []

        # Section 1: Hand Shape Analysis
        sections.append({
            "title": "Hand Shape Analysis",
            "content": {
                "type": hand_shape.get("type", "Unknown"),
                "description": hand_shape.get("description", ""),
                "element": hand_shape.get("element", ""),
                "traits": hand_shape.get("traits", []),
                "confidence": hand_shape.get("confidence", 0),
            },
            "narrative": f"Your hand is classified as a {hand_shape.get('type', 'unique')} hand — {hand_shape.get('description', '')}. This indicates a natural affinity with the {hand_shape.get('element', 'balanced')} element."
        })

        # Section 2: Palm Line Analysis
        line_details = []
        for line in lines:
            line_details.append({
                "name": line.get("line_name", ""),
                "detected": line.get("detected", False),
                "measurements": line.get("measurements", {}),
                "characteristics": line.get("characteristics", []),
                "confidence": line.get("confidence", 0),
            })

        sections.append({
            "title": "Palm Line Analysis",
            "content": {"lines": line_details, "total_detected": len([l for l in lines if l.get("detected")])},
            "narrative": narrative.get("detailed_analysis", ""),
        })

        # Section 3: Personality Traits
        sections.append({
            "title": "Personality Traits",
            "content": {"traits": personality},
            "narrative": f"Your palm reveals {len(personality)} key personality dimensions.",
        })

        # Section 4: Summary & Guidance
        sections.append({
            "title": "Summary & Guidance",
            "content": {},
            "narrative": f"{narrative.get('summary', '')} {narrative.get('advice', '')}",
        })

        return {
            "report_type": "palmistry",
            "title": "Comprehensive Palmistry Analysis Report",
            "subtitle": f"{hand_shape.get('type', 'Palm')} Analysis — {hand_shape.get('element', 'Balanced')} Element",
            "sections": sections,
            "confidence_score": palm_analysis.get("confidence_score", 0),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "analysis_method": palm_analysis.get("analysis_method", "simulated_cv"),
        }

    @staticmethod
    def generate_tarot_report(tarot_reading: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive tarot reading report."""
        cards = tarot_reading.get("cards", [])
        narrative = tarot_reading.get("narrative", {})
        themes = tarot_reading.get("themes", [])
        elemental = tarot_reading.get("elemental_balance", {})

        sections = []

        # Section 1: Spread Overview
        sections.append({
            "title": "Spread Overview",
            "content": {
                "spread_name": tarot_reading.get("spread_name", ""),
                "spread_description": tarot_reading.get("spread_description", ""),
                "card_count": len(cards),
                "question": tarot_reading.get("question", "General guidance"),
            },
            "narrative": narrative.get("summary", ""),
        })

        # Section 2: Card-by-Card Analysis
        card_analyses = []
        for card in cards:
            card_analyses.append({
                "position": card.get("position", ""),
                "card_name": card.get("card_name", ""),
                "orientation": card.get("orientation", ""),
                "arcana": card.get("arcana", ""),
                "suit": card.get("suit"),
                "element": card.get("element"),
                "keywords": card.get("keywords", []),
                "core_meaning": card.get("core_meaning", ""),
                "position_interpretation": card.get("position_interpretation", ""),
            })

        sections.append({
            "title": "Card-by-Card Analysis",
            "content": {"cards": card_analyses},
            "narrative": "Each card in your spread carries specific energy for its position.",
        })

        # Section 3: Themes & Elemental Balance
        sections.append({
            "title": "Themes & Elemental Balance",
            "content": {
                "themes": themes,
                "elemental_balance": elemental,
            },
            "narrative": f"Key themes: {', '.join(themes[:5]) if themes else 'general guidance'}. "
                        f"Elemental balance: Fire ({elemental.get('Fire', 0)}), Water ({elemental.get('Water', 0)}), "
                        f"Air ({elemental.get('Air', 0)}), Earth ({elemental.get('Earth', 0)}).",
        })

        # Section 4: Guidance & Advice
        sections.append({
            "title": "Guidance & Advice",
            "content": {"energy_tone": narrative.get("energy_tone", "balanced")},
            "narrative": narrative.get("advice", ""),
        })

        return {
            "report_type": "tarot",
            "title": f"{tarot_reading.get('spread_name', 'Tarot')} Reading Report",
            "subtitle": f"{len(cards)} Cards — {narrative.get('energy_tone', 'Balanced')} Energy",
            "sections": sections,
            "confidence_score": tarot_reading.get("confidence_score", 0),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def generate_personality_report(
        personality_profile: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate a personality analysis report."""
        big_five = personality_profile.get("big_five_traits", {})
        archetype = personality_profile.get("archetype", {})
        strengths = personality_profile.get("strengths", [])
        weaknesses = personality_profile.get("weaknesses", [])
        behavioral = personality_profile.get("behavioral_insights", {})
        recommendations = personality_profile.get("development_recommendations", [])

        sections = [
            {
                "title": "Your Personality Archetype",
                "content": archetype,
                "narrative": f"You are {archetype.get('name', 'The Seeker')} — {archetype.get('description', '')}",
            },
            {
                "title": "Big Five Personality Traits",
                "content": {k: {"name": v["name"], "score": v["score"], "label": v["label"]} for k, v in big_five.items()},
                "narrative": "Your Big Five personality profile reveals a unique combination of traits that shape your interactions, decisions, and life path.",
            },
            {
                "title": "Core Strengths",
                "content": {"strengths": strengths},
                "narrative": f"You possess {len(strengths)} identified core strengths that serve as foundations for growth.",
            },
            {
                "title": "Growth Opportunities",
                "content": {"growth_areas": weaknesses},
                "narrative": f"Your profile identifies {len(weaknesses)} areas where focused development can yield significant personal growth.",
            },
            {
                "title": "Behavioral Patterns",
                "content": behavioral,
                "narrative": "Understanding your behavioral patterns empowers conscious choice-making in daily life.",
            },
            {
                "title": "Development Recommendations",
                "content": {"recommendations": recommendations},
                "narrative": f"We've generated {len(recommendations)} personalized recommendations to support your growth journey.",
            },
        ]

        return {
            "report_type": "personality",
            "title": "Comprehensive Personality Intelligence Report",
            "subtitle": f"Archetype: {archetype.get('name', 'The Seeker')}",
            "sections": sections,
            "confidence_score": personality_profile.get("profile_confidence", 0),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def generate_spiritual_guidance_report(
        palm_analysis: Dict[str, Any],
        tarot_reading: Dict[str, Any],
        interpretation: Dict[str, Any],
        scoring: Dict[str, Any],
        recommendations: Dict[str, Any],
        trends: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate a comprehensive spiritual guidance report combining all modules."""
        sections = [
            {
                "title": "Executive Summary",
                "content": {
                    "insight_score": scoring.get("insight_score", 0),
                    "quality": scoring.get("quality", "good"),
                },
                "narrative": scoring.get("quality_description", ""),
            },
            {
                "title": "Insight Score Breakdown",
                "content": scoring.get("factors", {}),
                "narrative": "Your insight score is calculated using our 5-factor weighted model.",
            },
            {
                "title": "Life Trend Analysis",
                "content": {
                    "trajectory": trends.get("overall_trajectory", {}),
                    "opportunities": len(trends.get("opportunities", [])),
                    "challenges": len(trends.get("challenges", [])),
                },
                "narrative": trends.get("life_path_analysis", {}).get("summary", ""),
            },
            {
                "title": "Category Insights",
                "content": interpretation.get("insights", {}),
                "narrative": "Detailed insights across personality, relationships, career, finance, health, growth, and opportunities.",
            },
            {
                "title": "Top Recommendations",
                "content": {"recommendations": recommendations.get("top_recommendations", [])[:5]},
                "narrative": f"{recommendations.get('total_recommendations', 0)} personalized recommendations generated.",
            },
        ]

        return {
            "report_type": "spiritual_guidance",
            "title": "Complete Spiritual Guidance Report",
            "subtitle": f"Insight Score: {scoring.get('insight_score', 0):.1%} — {scoring.get('quality', 'Good').title()}",
            "sections": sections,
            "insight_score": scoring.get("insight_score", 0),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def export_to_csv(report: Dict[str, Any]) -> str:
        """Export report data to CSV format string."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["Report Type", report.get("report_type", "")])
        writer.writerow(["Title", report.get("title", "")])
        writer.writerow(["Generated At", report.get("generated_at", "")])
        writer.writerow(["Confidence Score", report.get("confidence_score", report.get("insight_score", ""))])
        writer.writerow([])

        # Sections
        for section in report.get("sections", []):
            writer.writerow(["--- " + section.get("title", "") + " ---"])
            writer.writerow(["Narrative", section.get("narrative", "")])

            content = section.get("content", {})
            if isinstance(content, dict):
                for key, value in content.items():
                    if isinstance(value, (str, int, float, bool)):
                        writer.writerow([key, str(value)])
                    elif isinstance(value, list):
                        writer.writerow([key, json.dumps(value, default=str)])
                    elif isinstance(value, dict):
                        writer.writerow([key, json.dumps(value, default=str)])
            writer.writerow([])

        return output.getvalue()

    @staticmethod
    def export_to_json(report: Dict[str, Any]) -> str:
        """Export report to formatted JSON string."""
        return json.dumps(report, indent=2, default=str)

    @staticmethod
    def generate_report_summary(report: Dict[str, Any]) -> Dict[str, str]:
        """Generate a brief summary of any report."""
        return {
            "type": report.get("report_type", "unknown"),
            "title": report.get("title", ""),
            "subtitle": report.get("subtitle", ""),
            "sections_count": len(report.get("sections", [])),
            "generated_at": report.get("generated_at", ""),
            "confidence": str(report.get("confidence_score", report.get("insight_score", "N/A"))),
        }
