"""
Dataset Service
================
Business logic for loading and querying palmistry, tarot, and
dataset catalog data. Provides filtering, random selection,
catalog browsing, and statistics.
"""

import json
import random
from pathlib import Path
from typing import Optional
from functools import lru_cache


DATA_DIR = Path(__file__).parent.parent / "data"


@lru_cache(maxsize=1)
def _load_tarot_cards() -> list[dict]:
    """Load and cache the tarot cards dataset from JSON."""
    with open(DATA_DIR / "tarot_cards.json", "r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _load_palmistry_lines() -> list[dict]:
    """Load and cache the palmistry lines dataset from JSON."""
    with open(DATA_DIR / "palmistry_lines.json", "r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _load_dataset_catalog() -> dict:
    """Load and cache the 1000-image dataset catalog."""
    catalog_path = DATA_DIR / "dataset_catalog.json"
    if not catalog_path.exists():
        return {"images": [], "statistics": {}, "total_images": 0}
    with open(catalog_path, "r", encoding="utf-8") as f:
        return json.load(f)


class DatasetService:
    """Service layer for querying palmistry, tarot, and catalog datasets."""

    # ── Tarot Cards ──────────────────────────────────────────────

    @staticmethod
    def get_all_tarot_cards(
        arcana: Optional[str] = None,
        suit: Optional[str] = None,
        search: Optional[str] = None,
    ) -> list[dict]:
        """
        Get all tarot cards with optional filters.
        
        Args:
            arcana: Filter by 'major' or 'minor'
            suit: Filter by suit ('wands', 'cups', 'swords', 'pentacles')
            search: Search by card name or keywords
        """
        cards = list(_load_tarot_cards())

        if arcana:
            cards = [c for c in cards if c["arcana"] == arcana.lower()]

        if suit:
            cards = [c for c in cards if c.get("suit") == suit.lower()]

        if search:
            query = search.lower()
            cards = [
                c for c in cards
                if query in c["name"].lower()
                or any(query in kw.lower() for kw in c.get("keywords", []))
            ]

        return cards

    @staticmethod
    def get_tarot_card_by_id(card_id: str) -> Optional[dict]:
        """Get a single tarot card by its ID."""
        cards = _load_tarot_cards()
        for card in cards:
            if card["id"] == card_id:
                return card
        return None

    @staticmethod
    def draw_random_cards(count: int = 3) -> list[dict]:
        """
        Draw random tarot cards (simulating a reading spread).
        
        Args:
            count: Number of cards to draw (1-10)
        """
        cards = list(_load_tarot_cards())
        count = max(1, min(count, 10))  # Clamp between 1-10
        drawn = random.sample(cards, count)

        # Add random orientation (upright or reversed) for each drawn card
        for card in drawn:
            card["orientation"] = random.choice(["upright", "reversed"])

        return drawn

    # ── Palmistry Lines ──────────────────────────────────────────

    @staticmethod
    def get_all_palmistry_lines() -> list[dict]:
        """Get all palmistry line references."""
        return list(_load_palmistry_lines())

    @staticmethod
    def get_palmistry_line_by_id(line_id: str) -> Optional[dict]:
        """Get a single palmistry line by its ID."""
        lines = _load_palmistry_lines()
        for line in lines:
            if line["id"] == line_id:
                return line
        return None

    # ── Dataset Catalog (1000 Images) ────────────────────────────

    @staticmethod
    def get_dataset_catalog(
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        quality: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> dict:
        """
        Get the 1000-image dataset catalog with optional filtering and pagination.
        
        Args:
            category: Filter by 'palm' or 'tarot'
            subcategory: Filter by subcategory (hand type or arcana type)
            quality: Filter by quality level ('high', 'medium', 'low')
            search: Search by description, tags, or filename
            skip: Pagination offset
            limit: Pagination page size (max 100)
        """
        catalog = _load_dataset_catalog()
        images = list(catalog.get("images", []))

        if category:
            images = [i for i in images if i["category"] == category.lower()]

        if subcategory:
            query = subcategory.lower()
            images = [i for i in images if query in i.get("subcategory", "").lower()]

        if quality:
            images = [i for i in images if i.get("quality_level") == quality.lower()]

        if search:
            query = search.lower()
            images = [
                i for i in images
                if query in i.get("description", "").lower()
                or query in i.get("filename", "").lower()
                or any(query in t.lower() for t in i.get("tags", []))
            ]

        total = len(images)
        limit = min(limit, 100)
        paginated = images[skip:skip + limit]

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "catalog_name": catalog.get("catalog_name", ""),
            "catalog_version": catalog.get("version", ""),
            "images": paginated,
        }

    @staticmethod
    def get_catalog_stats() -> dict:
        """Get statistics about the 1000-image dataset catalog."""
        catalog = _load_dataset_catalog()
        stats = catalog.get("statistics", {})
        return {
            "catalog_name": catalog.get("catalog_name", ""),
            "version": catalog.get("version", ""),
            "created_date": catalog.get("created_date", ""),
            "description": catalog.get("description", ""),
            "total_images": catalog.get("total_images", 0),
            "statistics": stats,
        }

    # ── General Statistics ────────────────────────────────────────

    @staticmethod
    def get_dataset_stats() -> dict:
        """Get statistics about all loaded datasets including catalog."""
        cards = _load_tarot_cards()
        lines = _load_palmistry_lines()
        catalog = _load_dataset_catalog()

        major = [c for c in cards if c["arcana"] == "major"]
        minor = [c for c in cards if c["arcana"] == "minor"]

        suits = {}
        for card in minor:
            s = card.get("suit", "unknown")
            suits[s] = suits.get(s, 0) + 1

        return {
            "tarot": {
                "total_cards": len(cards),
                "major_arcana": len(major),
                "minor_arcana": len(minor),
                "suits": suits,
            },
            "palmistry": {
                "total_lines": len(lines),
                "line_names": [l["name"] for l in lines],
            },
            "catalog": {
                "total_images": catalog.get("total_images", 0),
                "categories": catalog.get("categories", {}),
            },
            "status": "datasets_loaded",
        }
