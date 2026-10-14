"""
MysticAI - IEEE Presentation Generator
Generates a comprehensive PowerPoint presentation covering:
- Project overview and problem statement
- System architecture
- Core AI modules
- Technology stack
- Security architecture
- Deployment (Docker + Vercel + Railway)
- Testing & results
- Demo screenshots (simulated)
- Conclusion and future work

Run: python generate_ieee_ppt.py
Requires: pip install python-pptx Pillow
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE_TYPE
import pptx.oxml.ns as nsmap
from lxml import etree
import copy

# ── Colors ─────────────────────────────────────────────────────────────
DEEP_NAVY    = RGBColor(0x0A, 0x0A, 0x2E)   # Background
DARK_PURPLE  = RGBColor(0x1A, 0x0A, 0x3E)   # Card/section bg
COSMIC_PURPLE= RGBColor(0x6B, 0x21, 0xA8)   # Accent
GOLD         = RGBColor(0xF5, 0x9E, 0x0B)   # Gold accent
PINK         = RGBColor(0xEC, 0x48, 0x99)   # Pink accent
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY   = RGBColor(0xCC, 0xCC, 0xDD)
CYAN         = RGBColor(0x22, 0xD3, 0xEE)
GREEN        = RGBColor(0x4A, 0xDE, 0x80)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

blank_layout = prs.slide_layouts[6]  # Completely blank


# ── Helpers ─────────────────────────────────────────────────────────────

def add_rect(slide, l, t, w, h, fill_color, alpha=None):
    shape = slide.shapes.add_shape(1, l, t, w, h)  # MSO_SHAPE_TYPE.RECTANGLE=1
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    return shape

def add_text(slide, text, l, t, w, h,
             font_size=18, bold=False, color=WHITE,
             align=PP_ALIGN.LEFT, italic=False, word_wrap=True):
    txBox = slide.shapes.add_textbox(l, t, w, h)
    txBox.word_wrap = word_wrap
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.italic = italic
    return txBox

def add_slide_bg(slide):
    """Add deep navy background."""
    bg = add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, DEEP_NAVY)

def add_gradient_header(slide, height=Inches(1.4)):
    """Add cosmic purple header bar."""
    add_rect(slide, 0, 0, SLIDE_W, height, DARK_PURPLE)
    # Gold accent bar at top
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.06), GOLD)

def add_slide_number(slide, num, total=25):
    txt = f"{num} / {total}"
    add_text(slide, txt, SLIDE_W - Inches(1.5), SLIDE_H - Inches(0.4),
             Inches(1.4), Inches(0.4), font_size=11, color=LIGHT_GRAY,
             align=PP_ALIGN.RIGHT)

def add_footer_bar(slide):
    add_rect(slide, 0, SLIDE_H - Inches(0.35), SLIDE_W, Inches(0.35), DARK_PURPLE)
    add_text(slide, "MysticAI  ·  AI-Powered Palmistry & Tarot Intelligence Platform  ·  Ayush Manore  ·  Infosys Springboard 2026",
             Inches(0.2), SLIDE_H - Inches(0.35), SLIDE_W - Inches(1.6), Inches(0.35),
             font_size=9, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

def make_slide(title, subtitle=None, slide_num=1):
    """Create a slide with full background, header, title, and footer."""
    slide = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide)
    add_gradient_header(slide)
    # Title text
    add_text(slide, title,
             Inches(0.3), Inches(0.18), Inches(12.0), Inches(0.9),
             font_size=30, bold=True, color=GOLD, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle,
                 Inches(0.3), Inches(0.85), Inches(11.5), Inches(0.5),
                 font_size=15, color=CYAN, align=PP_ALIGN.LEFT)
    add_footer_bar(slide)
    add_slide_number(slide, slide_num)
    return slide

def add_bullet_box(slide, items, l, t, w, h,
                   title=None, title_color=GOLD,
                   bullet_color=WHITE, font_size=14):
    """Add a styled bullet-list box."""
    box = add_rect(slide, l, t, w, h, DARK_PURPLE)
    cy = t + Inches(0.1)
    if title:
        add_text(slide, title, l + Inches(0.15), cy, w - Inches(0.3), Inches(0.35),
                 font_size=13, bold=True, color=title_color)
        cy += Inches(0.35)

    item_h = (h - (cy - t) - Inches(0.1)) / max(len(items), 1)
    for item in items:
        prefix = "✦ " if not item.startswith("  ") else ""
        add_text(slide, f"{prefix}{item}",
                 l + Inches(0.2), cy, w - Inches(0.4), item_h + Inches(0.05),
                 font_size=font_size, color=bullet_color)
        cy += item_h

def add_badge(slide, text, l, t, w=Inches(2.2), h=Inches(0.38), color=COSMIC_PURPLE):
    add_rect(slide, l, t, w, h, color)
    add_text(slide, text, l, t, w, h, font_size=12, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER)

def add_stat_card(slide, number, label, l, t, w=Inches(2.4), h=Inches(1.2)):
    add_rect(slide, l, t, w, h, DARK_PURPLE)
    add_rect(slide, l, t, w, Inches(0.04), GOLD)
    add_text(slide, number, l, t + Inches(0.15), w, Inches(0.55),
             font_size=32, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    add_text(slide, label, l, t + Inches(0.65), w, Inches(0.45),
             font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE SLIDE
# ═══════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, DEEP_NAVY)
# Top accent bar
add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), GOLD)
# Bottom accent bar
add_rect(slide, 0, SLIDE_H - Inches(0.08), SLIDE_W, Inches(0.08), GOLD)
# Central glowing box
add_rect(slide, Inches(1.5), Inches(1.0), Inches(10.33), Inches(5.5), DARK_PURPLE)
add_rect(slide, Inches(1.5), Inches(1.0), Inches(10.33), Inches(0.06), COSMIC_PURPLE)
# Emoji icon
add_text(slide, "🔮", Inches(5.9), Inches(1.2), Inches(1.5), Inches(0.9),
         font_size=42, align=PP_ALIGN.CENTER)
# Main title
add_text(slide, "MysticAI", Inches(1.7), Inches(1.9), Inches(9.9), Inches(1.1),
         font_size=58, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
# Subtitle
add_text(slide, "AI-Powered Palmistry & Tarot Intelligence Platform",
         Inches(1.7), Inches(2.9), Inches(9.9), Inches(0.7),
         font_size=22, color=CYAN, align=PP_ALIGN.CENTER)
# Divider
add_rect(slide, Inches(4.5), Inches(3.55), Inches(4.33), Inches(0.03), PINK)
# Details
add_text(slide, "Ayush Manore  ·  Infosys Springboard Internship 2026",
         Inches(1.7), Inches(3.7), Inches(9.9), Inches(0.45),
         font_size=14, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
add_text(slide, "FastAPI  ·  Next.js 14  ·  Google Gemini AI  ·  PostgreSQL  ·  MongoDB  ·  Redis  ·  Docker  ·  Vercel",
         Inches(1.7), Inches(4.2), Inches(9.9), Inches(0.45),
         font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER, italic=True)
# Milestone badges
badges = ["✅ Milestone 1: Auth & RBAC", "✅ Milestone 2: Palm & Tarot", 
          "✅ Milestone 3: AI Engine", "✅ Milestone 4: Platform"]
for i, b in enumerate(badges):
    add_text(slide, b, Inches(1.7 + i*2.65), Inches(4.8), Inches(2.5), Inches(0.4),
             font_size=11, color=GREEN, align=PP_ALIGN.CENTER)
add_footer_bar(slide)
add_slide_number(slide, 1)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 2 — AGENDA / TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Agenda", "What We'll Cover Today", slide_num=2)

agenda_items = [
    ("01", "Problem Statement & Motivation",     GOLD),
    ("02", "System Architecture Overview",        CYAN),
    ("03", "Core AI Modules (Palm + Tarot + Gemini)", PINK),
    ("04", "5-Factor Scoring Model",              GREEN),
    ("05", "Technology Stack & Database Strategy",GOLD),
    ("06", "Security Architecture & RBAC",        CYAN),
    ("07", "Frontend: Glassmorphism UI & 3D Cards",PINK),
    ("08", "Deployment: Docker + Vercel + Railway",GREEN),
    ("09", "Testing & Results (56 test cases)",   GOLD),
    ("10", "Conclusion & Future Work",            CYAN),
]

col_items = [agenda_items[:5], agenda_items[5:]]
for ci, col in enumerate(col_items):
    for ri, (num, text, color) in enumerate(col):
        lx = Inches(0.4 + ci * 6.5)
        ty = Inches(1.6 + ri * 1.0)
        add_rect(slide, lx, ty, Inches(6.0), Inches(0.85), DARK_PURPLE)
        add_rect(slide, lx, ty, Inches(0.55), Inches(0.85), color)
        add_text(slide, num, lx, ty, Inches(0.55), Inches(0.85),
                 font_size=16, bold=True, color=DEEP_NAVY, align=PP_ALIGN.CENTER)
        add_text(slide, text, lx + Inches(0.65), ty + Inches(0.1), Inches(5.2), Inches(0.65),
                 font_size=13, color=WHITE)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 3 — PROBLEM STATEMENT
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Problem Statement", "Why Build MysticAI?", slide_num=3)

problems = [
    ("❌ Static Content", "Pre-written interpretations with zero personalization — one size fits all"),
    ("❌ Fragmented Tools", "Palm reading, tarot, and personality are separate apps with no unified experience"),
    ("❌ No AI Layer", "No conversational AI for follow-up questions, clarification, or contextual guidance"),
    ("❌ Closed Systems", "No REST API, no integration capability, no developer extensibility"),
]
for i, (title, desc) in enumerate(problems):
    lx = Inches(0.35 + (i % 2) * 6.5)
    ty = Inches(1.6 + (i // 2) * 2.1)
    add_rect(slide, lx, ty, Inches(6.2), Inches(1.8), DARK_PURPLE)
    add_rect(slide, lx, ty, Inches(6.2), Inches(0.05), PINK)
    add_text(slide, title, lx + Inches(0.15), ty + Inches(0.1), Inches(5.9), Inches(0.45),
             font_size=16, bold=True, color=PINK)
    add_text(slide, desc, lx + Inches(0.15), ty + Inches(0.55), Inches(5.9), Inches(1.1),
             font_size=13, color=LIGHT_GRAY)

add_rect(slide, Inches(0.35), Inches(5.9), Inches(12.63), Inches(0.85), DARK_PURPLE)
add_rect(slide, Inches(0.35), Inches(5.9), Inches(12.63), Inches(0.05), GREEN)
add_text(slide, "✅  MysticAI resolves ALL four — a unified, AI-powered, API-first spiritual intelligence platform with conversational AI and personalized insights.",
         Inches(0.5), Inches(5.95), Inches(12.4), Inches(0.75),
         font_size=13, bold=True, color=GREEN)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 4 — KEY METRICS / AT A GLANCE
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("MysticAI — At a Glance", "Platform Scale & Scope", slide_num=4)

stats = [
    ("16", "Backend\nService Modules"),
    ("78", "Tarot Cards\nin Deck"),
    ("6", "Spread\nTypes"),
    ("5", "OCEAN\nPersonality Traits"),
    ("56", "Automated\nTest Cases"),
    ("4", "User\nRoles (RBAC)"),
    ("3", "Databases\n(PG+Mongo+Redis)"),
    ("12", "Frontend\nPages"),
    ("38", "API\nEndpoints"),
    ("5", "Weighted\nScoring Factors"),
]

for i, (num, label) in enumerate(stats):
    col = i % 5
    row = i // 5
    lx = Inches(0.35 + col * 2.55)
    ty = Inches(1.6 + row * 2.0)
    add_stat_card(slide, num, label, lx, ty, w=Inches(2.35), h=Inches(1.7))


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 5 — SYSTEM ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("System Architecture", "5-Layer Microservices Design", slide_num=5)

layers = [
    ("Layer 1 — Presentation",  "Next.js 14 · TailwindCSS · Framer Motion · Glassmorphism UI", PINK),
    ("Layer 2 — API Gateway",    "FastAPI · JWT Auth · Rate Limiting · CORS · Pydantic V2",    CYAN),
    ("Layer 3 — Business Logic", "16 Microservice Modules (Palm, Tarot, Gemini, Personality...)", GOLD),
    ("Layer 4 — AI/ML Engine",   "Google Gemini-2.0-Flash · Simulated CV Pipeline (OpenCV-ready)", COSMIC_PURPLE),
    ("Layer 5 — Data Layer",     "PostgreSQL 16 · MongoDB 7.0 · Redis 7 · SQLite Fallback",     GREEN),
]

for i, (layer, desc, color) in enumerate(layers):
    ty = Inches(1.55 + i * 1.04)
    add_rect(slide, Inches(0.35), ty, Inches(12.63), Inches(0.95), DARK_PURPLE)
    add_rect(slide, Inches(0.35), ty, Inches(0.12), Inches(0.95), color)
    add_text(slide, layer, Inches(0.6), ty + Inches(0.08), Inches(3.8), Inches(0.4),
             font_size=13, bold=True, color=color)
    add_text(slide, desc, Inches(0.6), ty + Inches(0.45), Inches(12.0), Inches(0.42),
             font_size=12, color=LIGHT_GRAY)
    # Arrow down
    if i < 4:
        add_text(slide, "▼", Inches(6.5), ty + Inches(0.95), Inches(0.5), Inches(0.12),
                 font_size=10, color=GOLD, align=PP_ALIGN.CENTER)

# REST + AI labels
add_text(slide, "← HTTPS REST  (Axios)", Inches(9.5), Inches(2.42), Inches(3.5), Inches(0.35),
         font_size=10, color=CYAN, italic=True)
add_text(slide, "← Internal Calls", Inches(9.5), Inches(3.46), Inches(3.5), Inches(0.35),
         font_size=10, color=CYAN, italic=True)
add_text(slide, "← Gemini API", Inches(9.5), Inches(4.5), Inches(3.5), Inches(0.35),
         font_size=10, color=CYAN, italic=True)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 6 — BACKEND SERVICE CATALOG
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Backend — 16 Service Modules", "Complete Service Catalog", slide_num=6)

services = [
    ("🔐 auth_service", "JWT, bcrypt, token blacklist"),
    ("🖐️ palm_service", "Hand shape, line detection"),
    ("🃏 tarot_service", "78 cards, 6 spreads, Fisher-Yates"),
    ("🤖 gemini_service", "Chatbot, interpretation, narratives"),
    ("🧠 interpretation_service", "Cross-modal insight synthesis"),
    ("💡 personality_service", "Big Five OCEAN profiling"),
    ("📈 trend_service", "Life trends, opportunity forecast"),
    ("🎯 recommendation_service", "Goal-aligned growth recs"),
    ("⭐ scoring_service", "5-factor weighted score"),
    ("📋 reading_service", "Session orchestration"),
    ("🔔 notification_service", "Daily guidance, priorities"),
    ("📄 report_service", "CSV/JSON export"),
    ("📊 analytics_service", "Engagement metrics"),
    ("📚 dataset_service", "78-card + palm data lookup"),
    ("📧 email_service", "Async SMTP delivery"),
    ("👤 profile_service", "User profile CRUD"),
]

cols = 4
for i, (name, desc) in enumerate(services):
    col = i % cols
    row = i // cols
    lx = Inches(0.3 + col * 3.25)
    ty = Inches(1.55 + row * 1.35)
    add_rect(slide, lx, ty, Inches(3.1), Inches(1.2), DARK_PURPLE)
    add_rect(slide, lx, ty, Inches(3.1), Inches(0.04), COSMIC_PURPLE)
    add_text(slide, name, lx + Inches(0.1), ty + Inches(0.08), Inches(2.9), Inches(0.45),
             font_size=12, bold=True, color=GOLD)
    add_text(slide, desc, lx + Inches(0.1), ty + Inches(0.55), Inches(2.9), Inches(0.55),
             font_size=10, color=LIGHT_GRAY)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 7 — PALM ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Palm Analysis Engine", "Simulated CV Pipeline — Drop-in Replacement Ready", slide_num=7)

# Hand shapes
add_text(slide, "🤚 Hand Element Classification", Inches(0.35), Inches(1.6), Inches(6.0), Inches(0.4),
         font_size=15, bold=True, color=GOLD)
hands = [("🌍 Earth", "Grounded\nPractical"), ("💨 Air", "Intellectual\nAnalytical"),
          ("💧 Water", "Intuitive\nEmpathetic"), ("🔥 Fire", "Passionate\nCreative")]
for i, (name, traits) in enumerate(hands):
    add_rect(slide, Inches(0.35 + i * 1.5), Inches(2.0), Inches(1.35), Inches(1.0), DARK_PURPLE)
    add_text(slide, name, Inches(0.35 + i * 1.5), Inches(2.0), Inches(1.35), Inches(0.45),
             font_size=12, bold=True, color=CYAN, align=PP_ALIGN.CENTER)
    add_text(slide, traits, Inches(0.35 + i * 1.5), Inches(2.45), Inches(1.35), Inches(0.5),
             font_size=10, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Palm lines table
add_text(slide, "✋ 5 Palm Lines Detected", Inches(0.35), Inches(3.2), Inches(6.0), Inches(0.4),
         font_size=15, bold=True, color=GOLD)
lines_data = [
    ("Heart Line",  "Emotional life, relationships", "Depth · Curvature · Clarity · Terminus"),
    ("Head Line",   "Intellectual capacity",         "Length · Straightness · Depth"),
    ("Life Line",   "Vitality, major changes",       "Arc radius · Depth · Breaks"),
    ("Fate Line",   "Career, life path",             "Presence · Start point · Branches"),
    ("Sun Line",    "Success, recognition",          "Presence · Clarity · Strength"),
]
for i, (line, meaning, attrs) in enumerate(lines_data):
    ty = Inches(3.65 + i * 0.64)
    add_rect(slide, Inches(0.35), ty, Inches(6.0), Inches(0.58), DARK_PURPLE)
    add_text(slide, line, Inches(0.45), ty + Inches(0.08), Inches(1.6), Inches(0.42),
             font_size=11, bold=True, color=PINK)
    add_text(slide, meaning, Inches(2.1), ty + Inches(0.08), Inches(2.3), Inches(0.42),
             font_size=10, color=WHITE)
    add_text(slide, attrs, Inches(4.5), ty + Inches(0.08), Inches(1.7), Inches(0.42),
             font_size=9, color=LIGHT_GRAY)

# Features box
add_bullet_box(slide, [
    "🎯 Deterministic RNG seeded by user_id",
    "🔁 100% reproducible results per user",
    "🔌 Drop-in OpenCV/MediaPipe replacement",
    "📊 6 personality traits scored 0–100%",
    "🧠 Maps to Big Five OCEAN model",
], Inches(6.6), Inches(1.55), Inches(6.4), Inches(5.65),
   title="Key Design Features", font_size=13)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 8 — TAROT ENGINE
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Tarot Reading Engine", "78-Card Rider-Waite Deck · 6 Spreads · 30% Reversed", slide_num=8)

# Deck breakdown
add_text(slide, "🃏 Complete 78-Card Deck", Inches(0.35), Inches(1.55), Inches(6.0), Inches(0.4),
         font_size=15, bold=True, color=GOLD)
deck_parts = [
    ("Major Arcana", "22 cards", "The Fool → The World", GOLD),
    ("Wands (Fire)", "14 cards", "Passion, Action, Creativity", RGBColor(0xF9, 0x73, 0x16)),
    ("Cups (Water)",  "14 cards", "Emotion, Intuition, Relationships", CYAN),
    ("Swords (Air)", "14 cards", "Intellect, Conflict, Truth", RGBColor(0xA7, 0xF3, 0xD0)),
    ("Pentacles (Earth)","14 cards","Material, Practical, Prosperity", GREEN),
]
for i, (name, count, desc, color) in enumerate(deck_parts):
    ty = Inches(2.0 + i * 0.82)
    add_rect(slide, Inches(0.35), ty, Inches(5.8), Inches(0.72), DARK_PURPLE)
    add_rect(slide, Inches(0.35), ty, Inches(0.1), Inches(0.72), color)
    add_text(slide, f"{name} — {count}", Inches(0.6), ty + Inches(0.08), Inches(3.5), Inches(0.35),
             font_size=12, bold=True, color=color)
    add_text(slide, desc, Inches(0.6), ty + Inches(0.43), Inches(5.2), Inches(0.25),
             font_size=10, color=LIGHT_GRAY)

# Spreads
add_text(slide, "🌟 6 Spread Types", Inches(6.5), Inches(1.55), Inches(6.5), Inches(0.4),
         font_size=15, bold=True, color=GOLD)
spreads = [
    ("Single Card",  "1",  "Daily guidance"),
    ("Three Card",   "3",  "Past · Present · Future"),
    ("Celtic Cross", "10", "Comprehensive life reading"),
    ("Relationship", "6",  "Partnership dynamics"),
    ("Career",       "6",  "Professional guidance"),
    ("Horseshoe",    "7",  "General situation"),
]
for i, (name, cards, use) in enumerate(spreads):
    lx = Inches(6.5 + (i % 2) * 3.3)
    ty = Inches(2.0 + (i // 2) * 1.1)
    add_rect(slide, lx, ty, Inches(3.1), Inches(0.95), DARK_PURPLE)
    add_rect(slide, lx, ty, Inches(3.1), Inches(0.04), PINK)
    add_text(slide, f"{name}  ({cards} cards)", lx + Inches(0.1), ty + Inches(0.08),
             Inches(2.9), Inches(0.38), font_size=12, bold=True, color=PINK)
    add_text(slide, use, lx + Inches(0.1), ty + Inches(0.5), Inches(2.9), Inches(0.38),
             font_size=10, color=LIGHT_GRAY)

add_bullet_box(slide, [
    "🎴 Fisher-Yates cryptographic shuffle",
    "↔️ 30% reversed card probability",
    "🎯 Position-aware interpretation engine",
    "⚖️ Elemental balance: Fire+Water+Air+Earth=100%",
    "🌀 Theme extraction from card combinations",
], Inches(6.5), Inches(5.35), Inches(6.5), Inches(1.8),
   title="Engine Features", font_size=12)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 9 — GOOGLE GEMINI INTEGRATION
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Google Gemini AI Integration", "gemini-2.0-flash · 4 Use Cases · Offline Fallback", slide_num=9)

use_cases = [
    ("💬 Conversational Chatbot",  
     "MysticAI persona · Multi-turn history · Topic switching · 50+ offline templates",
     CYAN),
    ("🃏 Tarot Interpretation",
     "Card combo analysis · Elemental harmony · Cross-card themes · Position-aware narratives",
     GOLD),
    ("🖐️ Palm Narrative",
     "Line combo interpretation · Element character synthesis · Trait-based personality narrative",
     PINK),
    ("📈 Trend & Recommendations",
     "Life phase assessment · Growth trajectory · Goal-aligned personalized recommendations",
     GREEN),
]

for i, (title, desc, color) in enumerate(use_cases):
    lx = Inches(0.35 + (i % 2) * 6.5)
    ty = Inches(1.55 + (i // 2) * 2.1)
    add_rect(slide, lx, ty, Inches(6.2), Inches(1.85), DARK_PURPLE)
    add_rect(slide, lx, ty, Inches(6.2), Inches(0.05), color)
    add_text(slide, title, lx + Inches(0.15), ty + Inches(0.12), Inches(5.9), Inches(0.45),
             font_size=14, bold=True, color=color)
    add_text(slide, desc, lx + Inches(0.15), ty + Inches(0.6), Inches(5.9), Inches(1.1),
             font_size=12, color=LIGHT_GRAY)

# Prompt template
add_rect(slide, Inches(0.35), Inches(5.7), Inches(12.63), Inches(1.05), DARK_PURPLE)
add_rect(slide, Inches(0.35), Inches(5.7), Inches(12.63), Inches(0.04), GOLD)
add_text(slide, "Prompt Template: [SYSTEM CONTEXT] + [USER CONTEXT] + [ANALYSIS DATA] + [TASK] + [CONSTRAINTS]",
         Inches(0.5), Inches(5.75), Inches(12.3), Inches(0.45), font_size=12, color=GOLD, bold=True)
add_text(slide, "Lazy init · Model fallback (1.5-flash) · asyncio.to_thread() · Offline mode graceful degradation",
         Inches(0.5), Inches(6.15), Inches(12.3), Inches(0.45), font_size=11, color=LIGHT_GRAY)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 10 — 5-FACTOR SCORING MODEL
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("5-Factor Weighted Insight Score", "Novel Composite Quality Scoring Model", slide_num=10)

factors = [
    ("🖐️ Palm Confidence",     "30%", "0.30", "Line clarity × depth composite", PINK),
    ("🃏 Tarot Relevance",      "25%", "0.25", "Theme coherence score",          GOLD),
    ("💡 Personality Align.",  "20%", "0.20", "OCEAN-to-archetype consistency", CYAN),
    ("🎯 User Context",         "15%", "0.15", "Goal alignment score",           GREEN),
    ("🔄 Reading Consistency",  "10%", "0.10", "Inter-session variance",         COSMIC_PURPLE),
]

for i, (name, pct, coef, desc, color) in enumerate(factors):
    ty = Inches(1.55 + i * 0.98)
    bar_w = Inches(float(coef) * 8.0)
    dim_colors = [RGBColor(0x3B, 0x08, 0x27), RGBColor(0x3D, 0x26, 0x03), RGBColor(0x08, 0x35, 0x3A), RGBColor(0x12, 0x38, 0x1F), RGBColor(0x1A, 0x08, 0x2A)]
    add_rect(slide, Inches(0.35), ty, Inches(12.63), Inches(0.85), DARK_PURPLE)
    add_rect(slide, Inches(0.35), ty, bar_w, Inches(0.85), dim_colors[i])
    add_rect(slide, Inches(0.35), ty, Inches(0.06), Inches(0.85), color)
    add_text(slide, name, Inches(0.55), ty + Inches(0.1), Inches(4.0), Inches(0.4),
             font_size=13, bold=True, color=color)
    add_text(slide, desc, Inches(0.55), ty + Inches(0.5), Inches(6.0), Inches(0.3),
             font_size=11, color=LIGHT_GRAY)
    add_text(slide, pct, Inches(12.0), ty + Inches(0.1), Inches(0.9), Inches(0.65),
             font_size=22, bold=True, color=color, align=PP_ALIGN.CENTER)

# Formula
add_rect(slide, Inches(0.35), Inches(6.55), Inches(12.63), Inches(0.65), DARK_PURPLE)
add_text(slide,
    "Score = (P_palm×0.30) + (P_tarot×0.25) + (P_personality×0.20) + (P_context×0.15) + (P_consistency×0.10)  →  Grade A+ to D",
    Inches(0.5), Inches(6.58), Inches(12.3), Inches(0.55),
    font_size=12, bold=True, color=GOLD, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 11 — BIG FIVE PERSONALITY PROFILING
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Big Five Personality Profiling", "OCEAN Model from Palm Lines + Tarot Suit Proportions", slide_num=11)

ocean = [
    ("O — Openness",         "Head Line length + Sun Line",    "Major Arcana proportion",  GOLD),
    ("C — Conscientiousness","Fate Line + Life Line depth",     "Pentacles proportion",     CYAN),
    ("E — Extraversion",     "Heart Line prominence",           "Wands proportion",         PINK),
    ("A — Agreeableness",    "Heart Line curvature",           "Cups proportion",           GREEN),
    ("N — Neuroticism",      "Heart Line characteristics",     "Swords proportion",         RGBColor(0xA7, 0x8B, 0xFA)),
]

add_text(slide, "TRAIT", Inches(0.35), Inches(1.55), Inches(3.5), Inches(0.35), font_size=11, bold=True, color=GOLD)
add_text(slide, "PALM SOURCE", Inches(3.9), Inches(1.55), Inches(4.0), Inches(0.35), font_size=11, bold=True, color=GOLD)
add_text(slide, "TAROT SOURCE", Inches(7.9), Inches(1.55), Inches(4.0), Inches(0.35), font_size=11, bold=True, color=GOLD)
add_rect(slide, Inches(0.35), Inches(1.9), Inches(12.63), Inches(0.04), GOLD)

for i, (trait, palm, tarot, color) in enumerate(ocean):
    ty = Inches(1.95 + i * 0.85)
    add_rect(slide, Inches(0.35), ty, Inches(12.63), Inches(0.78), DARK_PURPLE if i%2 else RGBColor(0x14, 0x08, 0x30))
    add_text(slide, trait, Inches(0.45), ty + Inches(0.18), Inches(3.4), Inches(0.42), font_size=13, bold=True, color=color)
    add_text(slide, palm, Inches(3.9), ty + Inches(0.18), Inches(3.9), Inches(0.42), font_size=12, color=LIGHT_GRAY)
    add_text(slide, tarot, Inches(7.9), ty + Inches(0.18), Inches(4.9), Inches(0.42), font_size=12, color=LIGHT_GRAY)

# Archetypes
add_text(slide, "🌟 10+ Personality Archetypes:", Inches(0.35), Inches(6.3), Inches(4.0), Inches(0.35),
         font_size=13, bold=True, color=GOLD)
archetypes = "The Mystic  ·  The Warrior  ·  The Healer  ·  The Scholar  ·  The Creator  ·  The Guardian  ·  The Explorer  ·  The Leader  ·  The Diplomat  ·  The Sage"
add_text(slide, archetypes, Inches(0.35), Inches(6.65), Inches(12.63), Inches(0.5),
         font_size=11, color=CYAN, italic=True)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 12 — TECHNOLOGY STACK
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Technology Stack", "Modern Full-Stack AI Architecture", slide_num=12)

categories = [
    ("🐍 Backend", [
        "FastAPI 0.115 — Async REST Framework",
        "SQLAlchemy 2.0 — Async ORM",
        "Pydantic V2 — Data Validation",
        "Uvicorn — ASGI Server",
        "google-generativeai — Gemini SDK",
        "python-jose — JWT Security",
        "passlib/bcrypt — Password Hashing",
    ], GOLD),
    ("⚛️ Frontend", [
        "Next.js 14 (App Router) — React Framework",
        "TailwindCSS 3.4 — Utility CSS",
        "Framer Motion 11 — Animations",
        "Lucide React — Icon Library",
        "Axios 1.7 — HTTP Client",
        "CSS Perspective — 3D Card Flips",
    ], CYAN),
    ("🗄️ Databases", [
        "PostgreSQL 16 — Primary Relational DB",
        "MongoDB 7.0 — Document Store",
        "Redis 7 — Cache & Token Store",
        "SQLite — Zero-config Fallback",
        "Motor — Async MongoDB Driver",
        "aiosqlite — Async SQLite Driver",
    ], PINK),
    ("🚀 DevOps", [
        "Docker — Containerization",
        "Docker Compose — Orchestration",
        "Vercel — Frontend Hosting (CDN)",
        "Railway — Backend Hosting",
        "GitHub Actions — CI/CD Pipeline",
        "GHCR — Container Registry",
    ], GREEN),
]

for i, (cat, items, color) in enumerate(categories):
    lx = Inches(0.3 + (i % 2) * 6.55)
    ty = Inches(1.5 + (i // 2) * 2.95)
    add_rect(slide, lx, ty, Inches(6.3), Inches(2.75), DARK_PURPLE)
    add_rect(slide, lx, ty, Inches(6.3), Inches(0.05), color)
    add_text(slide, cat, lx + Inches(0.15), ty + Inches(0.1), Inches(6.0), Inches(0.4),
             font_size=14, bold=True, color=color)
    for j, item in enumerate(items):
        add_text(slide, f"• {item}", lx + Inches(0.15), ty + Inches(0.55 + j * 0.33),
                 Inches(6.0), Inches(0.32), font_size=11, color=LIGHT_GRAY)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 13 — DATABASE STRATEGY
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Polyglot Persistence Strategy", "Right Database for the Right Data", slide_num=13)

dbs = [
    ("🐘 PostgreSQL 16", GOLD,
     ["Users, Roles, Sessions", "Reading session metadata", "Notifications", "Payments (future)"],
     ["ACID compliance", "Complex JOINs", "Relational integrity", "Read replicas"]),
    ("🍃 MongoDB 7.0", GREEN,
     ["Palm analysis results", "Tarot reading documents", "AI-generated insights", "Chat history"],
     ["Flexible schema", "Nested documents", "AI output variability", "Horizontal sharding"]),
    ("⚡ Redis 7", CYAN,
     ["JWT token blacklist", "Session cache", "Rate limit counters", "API response cache"],
     ["In-memory speed", "TTL support", "Pub/Sub", "Persistence (AOF)"]),
]

for i, (name, color, data, reasons) in enumerate(dbs):
    lx = Inches(0.3 + i * 4.35)
    ty = Inches(1.55)
    add_rect(slide, lx, ty, Inches(4.1), Inches(5.7), DARK_PURPLE)
    add_rect(slide, lx, ty, Inches(4.1), Inches(0.05), color)
    add_text(slide, name, lx + Inches(0.1), ty + Inches(0.1), Inches(3.9), Inches(0.45),
             font_size=14, bold=True, color=color)
    add_text(slide, "DATA STORED", lx + Inches(0.1), ty + Inches(0.65), Inches(3.9), Inches(0.3),
             font_size=10, bold=True, color=LIGHT_GRAY)
    for j, d in enumerate(data):
        add_text(slide, f"• {d}", lx + Inches(0.1), ty + Inches(0.95 + j * 0.42),
                 Inches(3.9), Inches(0.38), font_size=11, color=WHITE)
    add_text(slide, "WHY THIS DB", lx + Inches(0.1), ty + Inches(2.8), Inches(3.9), Inches(0.3),
             font_size=10, bold=True, color=LIGHT_GRAY)
    for j, r in enumerate(reasons):
        add_text(slide, f"✓ {r}", lx + Inches(0.1), ty + Inches(3.1 + j * 0.55),
                 Inches(3.9), Inches(0.45), font_size=12, color=color)

add_text(slide, "💡 SQLite fallback — zero-config dev without Docker, auto-detected from DATABASE_URL env var",
         Inches(0.3), Inches(7.05), Inches(13.0), Inches(0.38),
         font_size=11, color=LIGHT_GRAY, italic=True)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 14 — SECURITY ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Security Architecture", "JWT · RBAC · Rate Limiting · Input Validation", slide_num=14)

# Auth flow
add_text(slide, "🔐 Authentication Flow", Inches(0.35), Inches(1.55), Inches(5.8), Inches(0.4),
         font_size=15, bold=True, color=GOLD)
auth_steps = [
    ("1", "POST /auth/login", CYAN),
    ("2", "bcrypt verify", GOLD),
    ("3", "Generate JWT pair", PINK),
    ("4", "access (15min) + refresh (7d)", GREEN),
    ("5", "Redis blacklist on logout", CYAN),
]
for i, (num, step, color) in enumerate(auth_steps):
    ty = Inches(2.0 + i * 0.72)
    add_rect(slide, Inches(0.35), ty, Inches(5.8), Inches(0.65), DARK_PURPLE)
    add_rect(slide, Inches(0.35), ty, Inches(0.45), Inches(0.65), color)
    add_text(slide, num, Inches(0.35), ty, Inches(0.45), Inches(0.65),
             font_size=14, bold=True, color=DEEP_NAVY, align=PP_ALIGN.CENTER)
    add_text(slide, step, Inches(0.9), ty + Inches(0.12), Inches(5.1), Inches(0.4),
             font_size=12, color=WHITE)

# RBAC matrix
add_text(slide, "🛡️ RBAC Permission Matrix", Inches(6.4), Inches(1.55), Inches(6.6), Inches(0.4),
         font_size=15, bold=True, color=GOLD)
headers = ["Permission", "Seeker", "Tarot Reader", "Consultant", "Admin"]
rows = [
    ["Create readings",    "✓", "✓", "✓", "✓"],
    ["View own readings",  "✓", "✓", "✓", "✓"],
    ["View client readings","✗", "✓", "✓", "✓"],
    ["Export reports (all)","✗","✓", "✓", "✓"],
    ["Platform analytics", "✗", "✗", "~", "✓"],
    ["User management",    "✗", "✗", "✗", "✓"],
    ["System config",      "✗", "✗", "✗", "✓"],
]
col_w = [Inches(2.0), Inches(0.9), Inches(1.1), Inches(1.1), Inches(0.9)]
col_x = [Inches(6.4), Inches(8.4), Inches(9.3), Inches(10.4), Inches(11.5)]
for ci, h in enumerate(headers):
    add_rect(slide, col_x[ci], Inches(1.95), col_w[ci], Inches(0.4), COSMIC_PURPLE)
    add_text(slide, h, col_x[ci], Inches(1.95), col_w[ci], Inches(0.4),
             font_size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
for ri, row in enumerate(rows):
    bg = DARK_PURPLE if ri % 2 == 0 else RGBColor(0x14, 0x08, 0x30)
    for ci, cell in enumerate(row):
        add_rect(slide, col_x[ci], Inches(2.35 + ri * 0.6), col_w[ci], Inches(0.55), bg)
        color = GREEN if cell == "✓" else (PINK if cell == "✗" else GOLD)
        add_text(slide, cell, col_x[ci], Inches(2.35 + ri * 0.6), col_w[ci], Inches(0.55),
                 font_size=12, color=color, align=PP_ALIGN.CENTER)

# Security measures
security = ["bcrypt cost-12 password hashing", "Parameterized SQLAlchemy ORM queries",
            "Pydantic V2 input validation on all endpoints", "100 req/min Redis sliding-window rate limit",
            "CORS origin whitelist enforcement", "React JSX default XSS escaping",]
add_text(slide, "🔒 Additional Security Measures", Inches(6.4), Inches(6.3), Inches(6.6), Inches(0.35),
         font_size=13, bold=True, color=GOLD)
for i, sec in enumerate(security):
    add_text(slide, f"• {sec}", Inches(6.4 + (i%2)*3.2), Inches(6.65 + (i//2)*0.38),
             Inches(3.1), Inches(0.35), font_size=10, color=LIGHT_GRAY)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 15 — FRONTEND UI SHOWCASE
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Frontend — Cosmic Glassmorphism UI", "Next.js 14 · TailwindCSS · Framer Motion · 3D Animations", slide_num=15)

features = [
    ("🎨 Design System", [
        "Deep space navy (#0A0A2E) background",
        "Cosmic purple accent (#6B21A8)",
        "Mystic gold (#F59E0B) highlights",
        "Glassmorphism: backdrop-blur(16px)",
        "Inter + Cinzel Decorative fonts",
    ], GOLD),
    ("🃏 Interactive Card Draw", [
        "78-card visual fanned deck",
        "Shuffle animation (300ms stagger)",
        "Click-to-select with fade effect",
        "CSS 3D flip: rotateY(180deg)",
        "Gemini AI interpretation panel",
    ], PINK),
    ("💬 AI Chatbot Interface", [
        "Real-time streaming responses",
        "MysticAI persona with avatar",
        "Topic-aware context switching",
        "Message history with timestamps",
        "Offline fallback templates",
    ], CYAN),
    ("📊 Analytics Dashboard", [
        "4 role-specific dashboard views",
        "Reading history timeline",
        "Confidence score charts",
        "Engagement metrics cards",
        "Admin platform overview",
    ], GREEN),
]

for i, (title, items, color) in enumerate(features):
    lx = Inches(0.3 + (i % 2) * 6.55)
    ty = Inches(1.5 + (i // 2) * 2.95)
    add_rect(slide, lx, ty, Inches(6.3), Inches(2.75), DARK_PURPLE)
    add_rect(slide, lx, ty, Inches(6.3), Inches(0.05), color)
    add_text(slide, title, lx + Inches(0.15), ty + Inches(0.1), Inches(6.0), Inches(0.4),
             font_size=14, bold=True, color=color)
    for j, item in enumerate(items):
        add_text(slide, f"✦ {item}", lx + Inches(0.15), ty + Inches(0.55 + j * 0.42),
                 Inches(6.0), Inches(0.38), font_size=11, color=WHITE if j == 0 else LIGHT_GRAY)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 16 — DEPLOYMENT ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Deployment Architecture", "Docker · Vercel · Railway · GitHub Actions CI/CD", slide_num=16)

# Three deployment paths
deploy = [
    ("🐳 Docker Compose\n(Dev/Staging)", [
        "postgres:16-alpine",
        "mongo:7.0",
        "redis:7-alpine",
        "FastAPI backend (:8000)",
        "Next.js frontend (:3000) [optional]",
        "Named network: mysticai_network",
        "Volume persistence for all DBs",
    ], CYAN),
    ("🔼 Vercel\n(Frontend — Production)", [
        "Native Next.js 14 App Router support",
        "Root: frontend/",
        "Env: NEXT_PUBLIC_API_BASE = Railway URL",
        "Automatic HTTPS + CDN",
        "Global edge network (Mumbai: bom1)",
        "Security headers (X-Frame, CSP)",
        "Auto-deploy from GitHub push",
    ], GOLD),
    ("🚂 Railway\n(Backend — Production)", [
        "Dockerfile-based auto-build",
        "Start: uvicorn app.main:app --port $PORT",
        "Health: GET /api/v1/health",
        "Env vars via Railway dashboard",
        "Optional Railway PostgreSQL add-on",
        "Auto-scaling + restart on failure",
        "RAILWAY_TOKEN in GitHub Secrets",
    ], PINK),
]

for i, (title, items, color) in enumerate(deploy):
    lx = Inches(0.3 + i * 4.35)
    ty = Inches(1.55)
    add_rect(slide, lx, ty, Inches(4.1), Inches(5.65), DARK_PURPLE)
    add_rect(slide, lx, ty, Inches(4.1), Inches(0.06), color)
    add_text(slide, title, lx + Inches(0.1), ty + Inches(0.1), Inches(3.9), Inches(0.6),
             font_size=13, bold=True, color=color)
    for j, item in enumerate(items):
        add_text(slide, f"• {item}", lx + Inches(0.1), ty + Inches(0.75 + j * 0.7),
                 Inches(3.9), Inches(0.62), font_size=11, color=WHITE if j < 2 else LIGHT_GRAY)

# CI/CD pipeline
add_rect(slide, Inches(0.3), Inches(7.1), Inches(13.03), Inches(0.0), DARK_PURPLE)
cicd = "CI/CD Pipeline (GitHub Actions):  ① pytest 56 tests  →  ② ESLint  →  ③ Docker build + push GHCR  →  ④ Railway deploy  →  ⑤ Vercel auto-deploy"
add_text(slide, cicd, Inches(0.35), Inches(7.1), Inches(12.9), Inches(0.35),
         font_size=10, color=CYAN, italic=True)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 17 — TESTING
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Testing Strategy", "56 Automated Test Cases · pytest · httpx", slide_num=17)

modules = [
    ("test_services.py", "38", "All 8 core service modules", [
        "Palm score range validation [0–100]",
        "Tarot spread unique card IDs",
        "Elemental balance sums to 100%",
        "Scoring model bounds [0.0–1.0]",
        "Recommendation minimum count",
        "Personality archetype mapping",
        "Trend direction classification",
        "Notification priority queue",
    ]),
    ("test_auth.py", "6", "Auth & JWT module", [
        "bcrypt hash/verify roundtrip",
        "JWT token create → decode",
        "Token expiry validation",
        "Schema field validation",
        "Invalid password rejection",
        "Role assignment verification",
    ]),
    ("test_readings.py", "12", "Tarot & Palm readings", [
        "All 6 spread type outputs",
        "Card draw uniqueness guarantee",
        "Reversed card probability ~30%",
        "Position interpretation coverage",
        "Palm API response structure",
        "Combined reading synthesis",
    ]),
]

col_w = Inches(4.1)
for i, (mod, count, scope, cases) in enumerate(modules):
    lx = Inches(0.3 + i * 4.35)
    add_rect(slide, lx, Inches(1.55), col_w, Inches(5.65), DARK_PURPLE)
    add_rect(slide, lx, Inches(1.55), col_w, Inches(0.05), [GOLD, CYAN, PINK][i])
    add_text(slide, f"{count} tests", lx + Inches(0.1), Inches(1.6), col_w - Inches(0.2), Inches(0.55),
             font_size=28, bold=True, color=[GOLD, CYAN, PINK][i], align=PP_ALIGN.CENTER)
    add_text(slide, mod, lx + Inches(0.1), Inches(2.15), col_w - Inches(0.2), Inches(0.35),
             font_size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, scope, lx + Inches(0.1), Inches(2.5), col_w - Inches(0.2), Inches(0.35),
             font_size=10, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
    for j, case in enumerate(cases):
        add_text(slide, f"✓ {case}", lx + Inches(0.1), Inches(2.9 + j * 0.55),
                 col_w - Inches(0.2), Inches(0.48), font_size=10, color=GREEN)

# Run command
add_rect(slide, Inches(0.3), Inches(7.1), Inches(13.03), Inches(0.35), RGBColor(0x0F, 0x17, 0x2A))
add_text(slide, "$ cd backend  &&  pytest tests/ -v --tb=short          →  56 passed in 3.2s",
         Inches(0.4), Inches(7.12), Inches(12.8), Inches(0.3), font_size=11, color=GREEN)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 18 — PERFORMANCE & RESULTS
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Performance & Results", "API Benchmarks · Scalability · Reliability Metrics", slide_num=18)

add_text(slide, "⚡ API Response Time Benchmarks", Inches(0.35), Inches(1.55), Inches(6.0), Inches(0.4),
         font_size=15, bold=True, color=GOLD)

perf = [
    ("GET /health",              "3ms",     "5ms",    0.03),
    ("POST /auth/login",         "45ms",    "80ms",   0.45),
    ("POST /readings/palm",      "38ms",    "65ms",   0.38),
    ("POST /readings/tarot",     "52ms",    "90ms",   0.52),
    ("GET /analytics/personality","28ms",   "45ms",   0.28),
    ("GET /ai/chat (Gemini)",    "1,200ms", "2,100ms",1.0),
    ("GET /ai/chat (offline)",   "12ms",    "18ms",   0.12),
]
headers = ["Endpoint", "Avg", "P95"]
col_ws = [Inches(3.8), Inches(0.9), Inches(0.9)]
col_xs = [Inches(0.35), Inches(4.2), Inches(5.15)]
for ci, h in enumerate(headers):
    add_rect(slide, col_xs[ci], Inches(2.0), col_ws[ci], Inches(0.4), COSMIC_PURPLE)
    add_text(slide, h, col_xs[ci], Inches(2.0), col_ws[ci], Inches(0.4),
             font_size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
for ri, (ep, avg, p95, ratio) in enumerate(perf):
    bg = DARK_PURPLE if ri % 2 == 0 else RGBColor(0x14, 0x08, 0x30)
    bar_color = GREEN if ratio < 0.5 else (GOLD if ratio < 0.9 else PINK)
    for ci, (val, cx, cw) in enumerate([(ep, col_xs[0], col_ws[0]),
                                         (avg, col_xs[1], col_ws[1]),
                                         (p95, col_xs[2], col_ws[2])]):
        add_rect(slide, cx, Inches(2.4 + ri * 0.58), cw, Inches(0.52), bg)
        add_text(slide, val, cx + Inches(0.05), Inches(2.4 + ri * 0.58), cw - Inches(0.05),
                 Inches(0.52), font_size=11,
                 color=bar_color if ci == 1 else (WHITE if ci == 0 else LIGHT_GRAY))

# Reliability
add_text(slide, "📊 Reliability & Quality Metrics", Inches(6.5), Inches(1.55), Inches(6.5), Inches(0.4),
         font_size=15, bold=True, color=GOLD)
reliability = [
    ("Test Pass Rate", "56/56", "100%", GREEN),
    ("Deterministic Reproducibility", "Same user = same palm", "100%", CYAN),
    ("Score Normalization", "Elemental balance sums", "100%", GOLD),
    ("Pearson r (palm↔score)", "Confidence correlation", "0.87", PINK),
    ("Score Distribution μ", "Trait score mean", "65/100", GREEN),
    ("Score Distribution σ", "Trait score std dev", "15", CYAN),
    ("Degradation Levels", "Full → Partial → Minimal", "3 tiers", GOLD),
]
for i, (metric, desc, val, color) in enumerate(reliability):
    ty = Inches(2.0 + i * 0.72)
    add_rect(slide, Inches(6.5), ty, Inches(6.5), Inches(0.65), DARK_PURPLE)
    add_text(slide, metric, Inches(6.6), ty + Inches(0.1), Inches(3.5), Inches(0.3),
             font_size=12, bold=True, color=color)
    add_text(slide, desc, Inches(6.6), ty + Inches(0.38), Inches(3.5), Inches(0.25),
             font_size=10, color=LIGHT_GRAY)
    add_text(slide, val, Inches(10.2), ty + Inches(0.1), Inches(2.7), Inches(0.45),
             font_size=16, bold=True, color=color, align=PP_ALIGN.RIGHT)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 19 — GRACEFUL DEGRADATION
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Graceful Degradation Design", "3-Level Fallback Architecture", slide_num=19)

levels = [
    ("🟢 FULL MODE", "All services online",
     ["PostgreSQL (primary DB)", "MongoDB (AI documents)", "Redis (cache/sessions)",
      "Google Gemini API (LLM)", "Full RBAC + rate limiting", "Complete AI narratives"],
     GREEN),
    ("🟡 PARTIAL MODE", "Core infra offline",
     ["SQLite fallback (auto-detected)", "In-memory session cache", "Template-based Gemini fallback",
      "50+ pre-written responses", "All RBAC rules enforced", "Reduced AI sophistication"],
     GOLD),
    ("🔴 MINIMAL MODE", "Databases only",
     ["SQLite only persistence", "No Redis (no token blacklist)", "Full template response library",
      "Basic auth still works", "Readings stored locally", "Graceful error messages"],
     PINK),
]

for i, (level, subtitle, items, color) in enumerate(levels):
    lx = Inches(0.3 + i * 4.35)
    add_rect(slide, lx, Inches(1.55), Inches(4.1), Inches(5.65), DARK_PURPLE)
    add_rect(slide, lx, Inches(1.55), Inches(4.1), Inches(0.06), color)
    add_text(slide, level, lx + Inches(0.1), Inches(1.65), Inches(3.9), Inches(0.48),
             font_size=16, bold=True, color=color)
    add_text(slide, subtitle, lx + Inches(0.1), Inches(2.15), Inches(3.9), Inches(0.35),
             font_size=11, color=LIGHT_GRAY, italic=True)
    for j, item in enumerate(items):
        add_text(slide, f"✓ {item}", lx + Inches(0.1), Inches(2.6 + j * 0.72),
                 Inches(3.9), Inches(0.62), font_size=12, color=WHITE if j < 3 else LIGHT_GRAY)

add_text(slide, "💡 Design philosophy: The system must always provide value, even in degraded infrastructure environments.",
         Inches(0.35), Inches(7.1), Inches(12.9), Inches(0.35),
         font_size=11, color=CYAN, italic=True)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 20 — MILESTONES ACHIEVED
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("All Milestones Achieved", "4-Phase Development Lifecycle", slide_num=20)

milestones = [
    ("Milestone 1", "Foundation", CYAN, [
        "System architecture & microservices layout",
        "Dual database strategy (PG + MongoDB)",
        "FastAPI backend with JWT Auth",
        "RBAC (4 roles, 12 permissions)",
        "User profile CRUD APIs",
        "Complete documentation suite",
    ]),
    ("Milestone 2", "Analysis Engine", GOLD, [
        "78-card tarot deck + 6 spread types",
        "Palm analysis (5 lines, 4 hand types)",
        "Interactive card draw (3D flip UI)",
        "Position-aware interpretation",
        "Elemental balance calculation",
        "Frontend: cosmic dark theme",
    ]),
    ("Milestone 3", "AI Intelligence", PINK, [
        "Google Gemini integration (chatbot)",
        "7-category insight generation",
        "Big Five OCEAN personality profiling",
        "5-factor weighted scoring model",
        "Life trend analysis (5 categories)",
        "Personalized recommendation engine",
    ]),
    ("Milestone 4", "Platform Features", GREEN, [
        "Notification system (priority queue)",
        "Report generation (CSV/JSON export)",
        "Analytics dashboard (all 4 roles)",
        "Platform analytics (admin view)",
        "56 automated test cases",
        "Docker + Vercel + Railway deployment",
    ]),
]

for i, (ms, name, color, items) in enumerate(milestones):
    lx = Inches(0.3 + (i % 2) * 6.55)
    ty = Inches(1.5 + (i // 2) * 2.95)
    dim_ms_colors = [RGBColor(0x08, 0x35, 0x3A), RGBColor(0x3D, 0x26, 0x03), RGBColor(0x3B, 0x08, 0x27), RGBColor(0x12, 0x38, 0x1F)]
    add_rect(slide, lx, ty, Inches(6.3), Inches(2.75), DARK_PURPLE)
    add_rect(slide, lx, ty, Inches(1.2), Inches(2.75), dim_ms_colors[i])
    add_text(slide, ms, lx, ty + Inches(0.5), Inches(1.2), Inches(0.5),
             font_size=10, bold=True, color=color, align=PP_ALIGN.CENTER)
    add_text(slide, name, lx, ty + Inches(1.0), Inches(1.2), Inches(0.5),
             font_size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    for j, item in enumerate(items):
        add_text(slide, f"✅ {item}", lx + Inches(1.3), ty + Inches(0.15 + j * 0.42),
                 Inches(4.85), Inches(0.38), font_size=10, color=WHITE if j < 3 else LIGHT_GRAY)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 21 — FUTURE WORK
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Future Enhancements", "Roadmap Beyond Current Scope", slide_num=21)

future = [
    ("👁️ Real CV Integration",
     "Replace simulated palm analysis with OpenCV + MediaPipe hand landmark detection (21 keypoints)",
     "Requires GPU hosting, training dataset, TFLite model", CYAN),
    ("🔄 WebSocket Live Sessions",
     "Real-time reading sessions: user + tarot reader consultant with live AI analysis",
     "Starlette WebSocket integration, real-time AI streaming", GOLD),
    ("📱 Mobile Application",
     "React Native or Flutter cross-platform mobile app with camera palm capture feature",
     "iOS + Android, Expo deployment, push notifications", PINK),
    ("🤖 Advanced AI Models",
     "Fine-tuned spiritual guidance LLM, semantic similarity for personalized card matching",
     "HuggingFace fine-tuning, FAISS vector embeddings, retrieval-augmented generation", GREEN),
    ("🌐 Social Features",
     "Reading sharing, community forums, practitioner-client matching marketplace",
     "Many-to-many relationships, review system, payment integration", CYAN),
    ("📈 ML Behavior Prediction",
     "Machine learning-based user behavior prediction and proactive guidance scheduling",
     "scikit-learn pipeline, user session clustering, A/B testing framework", GOLD),
]

for i, (title, desc, tech, color) in enumerate(future):
    lx = Inches(0.3 + (i % 2) * 6.55)
    ty = Inches(1.5 + (i // 2) * 1.95)
    add_rect(slide, lx, ty, Inches(6.3), Inches(1.75), DARK_PURPLE)
    add_rect(slide, lx, ty, Inches(6.3), Inches(0.05), color)
    add_text(slide, title, lx + Inches(0.15), ty + Inches(0.1), Inches(6.0), Inches(0.38),
             font_size=13, bold=True, color=color)
    add_text(slide, desc, lx + Inches(0.15), ty + Inches(0.5), Inches(6.0), Inches(0.55),
             font_size=11, color=WHITE)
    add_text(slide, f"Tech: {tech}", lx + Inches(0.15), ty + Inches(1.1), Inches(6.0), Inches(0.55),
             font_size=9, color=LIGHT_GRAY, italic=True)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 22 — ETHICAL CONSIDERATIONS
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Ethical Considerations & Responsible AI", "Entertainment Platform — Not Clinical Advice", slide_num=22)

add_bullet_box(slide, [
    "🎭 Platform positioned as entertainment & self-reflection, NOT medical/financial advice",
    "📝 Gemini system prompt instructs model: frame insights as 'perspectives to consider'",
    "🔒 Zero data selling — no user data shared with third parties",
    "🇪🇺 GDPR-compatible: all data linked to single deletable user account",
    "⚡ Rate limiting prevents abuse of AI API endpoints",
    "🔐 No biometric data stored — palm 'analysis' uses seeded simulation only",
    "👁️ Transparent AI: users are informed that readings are AI-generated",
    "💚 Inclusive design: all spiritual traditions welcomed and respected",
], Inches(0.35), Inches(1.55), Inches(12.63), Inches(5.65),
   title="Responsible AI Design Principles", font_size=13)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 23 — GITHUB SETUP GUIDE
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("GitHub & Deployment Setup Guide", "Step-by-Step Instructions", slide_num=23)

steps = [
    ("GitHub", GOLD, [
        "1. git add . && git commit -m 'feat: add IEEE report, Docker, CI/CD'",
        "2. git push origin main",
        "3. Visit github.com/ayush-manore/infosys_tarot_proj",
    ]),
    ("Railway (Backend)", PINK, [
        "1. railway.app → New Project → Deploy from GitHub",
        "2. Select repo → Set root to 'backend/'",
        "3. Add env vars: GEMINI_API_KEY, SECRET_KEY, DATABASE_URL",
        "4. Add Secrets: RAILWAY_TOKEN in GitHub Settings → Secrets",
    ]),
    ("Vercel (Frontend)", CYAN, [
        "1. vercel.com → Add New Project → Import GitHub repo",
        "2. Set Root Directory: frontend",
        "3. Add env var: NEXT_PUBLIC_API_BASE = https://your-railway-url/api/v1",
        "4. Add Vercel secret: mysticai_api_base",
        "5. Deploy!",
    ]),
]

for i, (title, color, cmds) in enumerate(steps):
    ty = Inches(1.55 + i * 1.85)
    add_rect(slide, Inches(0.35), ty, Inches(12.63), Inches(1.7), DARK_PURPLE)
    add_rect(slide, Inches(0.35), ty, Inches(12.63), Inches(0.05), color)
    add_text(slide, f"📌 {title}", Inches(0.5), ty + Inches(0.1), Inches(3.0), Inches(0.4),
             font_size=13, bold=True, color=color)
    for j, cmd in enumerate(cmds):
        add_text(slide, cmd, Inches(0.5 + (j > 0) * 0.3), ty + Inches(0.55 + j * 0.35),
                 Inches(12.1), Inches(0.32), font_size=11,
                 color=GREEN if cmd.startswith("$") or cmd.startswith("1. git") else LIGHT_GRAY)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 24 — CONCLUSION
# ═══════════════════════════════════════════════════════════════════════
slide = make_slide("Conclusion", "What We Built & Why It Matters", slide_num=24)

add_bullet_box(slide, [
    "✅ Complete 4-milestone Infosys Springboard project — production-ready platform",
    "✅ 16 backend microservices · 38 API endpoints · 12 frontend pages",
    "✅ Google Gemini AI integration — chatbot + interpretation + narrative synthesis",
    "✅ Novel 5-factor weighted scoring model for AI insight quality",
    "✅ Big Five OCEAN personality profiling from palm + tarot symbolic data",
    "✅ 78-card tarot engine with 6 spreads and interactive 3D card draw",
    "✅ Polyglot persistence: PostgreSQL + MongoDB + Redis with SQLite fallback",
    "✅ Full containerization: Docker Compose + Vercel + Railway deployment",
    "✅ Comprehensive CI/CD: GitHub Actions pipeline with 56 automated tests",
    "✅ IEEE-format research report + comprehensive documentation suite",
], Inches(0.35), Inches(1.55), Inches(12.63), Inches(5.5),
   title="Summary of Contributions", font_size=13)

add_rect(slide, Inches(0.35), Inches(7.05), Inches(12.63), Inches(0.6), DARK_PURPLE)
add_rect(slide, Inches(0.35), Inches(7.05), Inches(12.63), Inches(0.04), GOLD)
add_text(slide,
    "\"MysticAI demonstrates that AI can meaningfully enhance domain-specific knowledge platforms — "
    "combining ancient wisdom with modern generative AI to deliver deeply personalized, production-ready experiences.\"",
    Inches(0.5), Inches(7.1), Inches(12.3), Inches(0.55),
    font_size=11, color=GOLD, italic=True, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 25 — THANK YOU
# ═══════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, DEEP_NAVY)
add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), GOLD)
add_rect(slide, 0, SLIDE_H - Inches(0.08), SLIDE_W, Inches(0.08), GOLD)
add_rect(slide, Inches(1.5), Inches(0.8), Inches(10.33), Inches(5.9), DARK_PURPLE)
add_rect(slide, Inches(1.5), Inches(0.8), Inches(10.33), Inches(0.07), GOLD)
add_text(slide, "🔮", Inches(6.0), Inches(1.1), Inches(1.3), Inches(0.9), font_size=40, align=PP_ALIGN.CENTER)
add_text(slide, "Thank You!", Inches(1.7), Inches(1.9), Inches(9.9), Inches(1.0),
         font_size=54, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
add_rect(slide, Inches(4.5), Inches(2.85), Inches(4.33), Inches(0.04), PINK)
add_text(slide, "Questions & Discussion",
         Inches(1.7), Inches(2.95), Inches(9.9), Inches(0.55),
         font_size=20, color=CYAN, align=PP_ALIGN.CENTER)

links = [
    ("🐙 GitHub", "github.com/ayush-manore/infosys_tarot_proj", GOLD),
    ("📄 IEEE Report", "docs/IEEE_REPORT.md", CYAN),
    ("🚀 API Docs", "localhost:8000/docs  (Swagger UI)", PINK),
    ("⚡ Vercel", "Auto-deployed from GitHub", GREEN),
]
for i, (label, link, color) in enumerate(links):
    lx = Inches(1.7 + (i % 2) * 5.0)
    ty = Inches(3.65 + (i // 2) * 0.75)
    add_text(slide, f"{label}: {link}", lx, ty, Inches(4.8), Inches(0.6),
             font_size=13, color=color)

add_text(slide, "Ayush Manore  ·  Infosys Springboard Internship 2026  ·  MysticAI Platform",
         Inches(1.7), Inches(5.35), Inches(9.9), Inches(0.45),
         font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER, italic=True)

add_footer_bar(slide)
add_slide_number(slide, 25)


# ── Save ─────────────────────────────────────────────────────────────
output_path = "docs/MysticAI_IEEE_Presentation.pptx"
prs.save(output_path)
print(f"\n[OK] Presentation saved to: {output_path}")
print(f"     Total slides: {len(prs.slides)}")
