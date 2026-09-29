"""
Datasets API Router
====================
Endpoints for browsing, querying, and drawing from the
integrated palmistry, tarot card, and image catalog datasets.
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional

from app.services.dataset_service import DatasetService

router = APIRouter(prefix="/datasets", tags=["Datasets"])


# ═══════════════════════════════════════════════════════════════════
# Tarot Card Endpoints
# ═══════════════════════════════════════════════════════════════════

@router.get("/tarot/cards")
async def list_tarot_cards(
    arcana: Optional[str] = Query(None, description="Filter by arcana type: 'major' or 'minor'"),
    suit: Optional[str] = Query(None, description="Filter by suit: 'wands', 'cups', 'swords', 'pentacles'"),
    search: Optional[str] = Query(None, description="Search by card name or keywords"),
):
    """
    List all tarot cards with optional filtering.
    
    - **arcana**: Filter by 'major' (22 cards) or 'minor' (56 cards)
    - **suit**: Filter minor arcana by suit (wands, cups, swords, pentacles)
    - **search**: Search by card name or keywords
    """
    cards = DatasetService.get_all_tarot_cards(arcana=arcana, suit=suit, search=search)
    return {
        "status": "success",
        "count": len(cards),
        "data": cards
    }


@router.get("/tarot/cards/random")
async def draw_random_cards(
    count: int = Query(3, ge=1, le=10, description="Number of cards to draw (1-10)")
):
    """
    Draw random tarot cards for a reading simulation.
    Each card receives a random orientation (upright or reversed).
    
    - **count**: Number of cards to draw (default: 3 for a classic three-card spread)
    """
    drawn = DatasetService.draw_random_cards(count=count)
    return {
        "status": "success",
        "spread_type": _get_spread_name(count),
        "count": len(drawn),
        "data": drawn
    }


@router.get("/tarot/cards/{card_id}")
async def get_tarot_card(card_id: str):
    """
    Get detailed information for a specific tarot card by ID.
    
    Example IDs: 'major_00' (The Fool), 'cups_01' (Ace of Cups)
    """
    card = DatasetService.get_tarot_card_by_id(card_id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarot card with id '{card_id}' not found"
        )
    return {
        "status": "success",
        "data": card
    }


# ═══════════════════════════════════════════════════════════════════
# Palmistry Line Endpoints
# ═══════════════════════════════════════════════════════════════════

@router.get("/palmistry/lines")
async def list_palmistry_lines():
    """
    List all palmistry line references with interpretations.
    Returns 7 major palm lines with detailed meaning guides.
    """
    lines = DatasetService.get_all_palmistry_lines()
    return {
        "status": "success",
        "count": len(lines),
        "data": lines
    }


@router.get("/palmistry/lines/{line_id}")
async def get_palmistry_line(line_id: str):
    """
    Get detailed information for a specific palm line by ID.
    
    Example IDs: 'heart_line', 'head_line', 'life_line', 'fate_line'
    """
    line = DatasetService.get_palmistry_line_by_id(line_id)
    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Palmistry line with id '{line_id}' not found"
        )
    return {
        "status": "success",
        "data": line
    }


# ═══════════════════════════════════════════════════════════════════
# Dataset Catalog (1000 Images)
# ═══════════════════════════════════════════════════════════════════

@router.get("/catalog")
async def get_catalog(
    category: Optional[str] = Query(None, description="Filter: 'palm' or 'tarot'"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory (e.g. hand type, arcana type)"),
    quality: Optional[str] = Query(None, description="Filter: 'high', 'medium', 'low'"),
    search: Optional[str] = Query(None, description="Search by description, tags, or filename"),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(50, ge=1, le=100, description="Page size (max 100)"),
):
    """
    Browse the 1000-image dataset catalog with filtering and pagination.

    The catalog contains 500 palm images (labeled by hand type, lines, quality)
    and 500 tarot card images (covering all 78 cards in multiple art styles).
    
    - **category**: Filter by 'palm' or 'tarot'
    - **subcategory**: E.g. 'Earth Hand', 'major', 'minor'
    - **quality**: 'high', 'medium', 'low'
    - **search**: Free-text search across descriptions, tags, and filenames
    """
    result = DatasetService.get_dataset_catalog(
        category=category,
        subcategory=subcategory,
        quality=quality,
        search=search,
        skip=skip,
        limit=limit,
    )
    return {
        "status": "success",
        **result,
    }


@router.get("/catalog/stats")
async def get_catalog_stats():
    """
    Get comprehensive statistics about the 1000-image dataset catalog.
    Returns breakdowns by category, hand type, art style, quality, and more.
    """
    stats = DatasetService.get_catalog_stats()
    return {
        "status": "success",
        "data": stats,
    }


# ═══════════════════════════════════════════════════════════════════
# Combined Dataset Statistics
# ═══════════════════════════════════════════════════════════════════

@router.get("/stats")
async def get_dataset_stats():
    """
    Get overview statistics of all integrated datasets.
    Returns counts of tarot cards (by arcana/suit), palmistry lines,
    and the 1000-image catalog summary.
    """
    stats = DatasetService.get_dataset_stats()
    return {
        "status": "success",
        "data": stats
    }


# ═══════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════

def _get_spread_name(count: int) -> str:
    """Map card count to a spread name."""
    spreads = {
        1: "single_card",
        2: "two_card",
        3: "three_card_spread",
        5: "cross_spread",
        7: "horseshoe_spread",
        10: "celtic_cross",
    }
    return spreads.get(count, f"custom_{count}_card")
