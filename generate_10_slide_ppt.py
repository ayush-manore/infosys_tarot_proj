import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def build_10_slide_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    assets_dir = os.path.join(base_dir, "docs", "assets")
    if not os.path.exists(assets_dir):
        assets_dir = os.path.join(base_dir, "assets")

    img_hero = os.path.join(assets_dir, "website_hero_landing.jpg")
    img_swagger = os.path.join(assets_dir, "website_swagger_docs.jpg")
    img_dashboard = os.path.join(assets_dir, "website_dashboard_profile.jpg")

    # --- COLOR PALETTE ---
    BG_DARK = RGBColor(10, 15, 29)          # #0A0F1D Deep Cosmic Navy
    CARD_BG = RGBColor(19, 29, 49)          # #131D31 Glass slate card
    CARD_BORDER = RGBColor(40, 56, 84)      # #283854 Subtle border
    CARD_ACCENT = RGBColor(28, 41, 68)      # #1C2944 Accent card
    
    CYAN = RGBColor(56, 189, 248)           # #38BDF8 Electric Cyan
    PURPLE = RGBColor(168, 85, 247)         # #A855F7 Cosmic Purple
    GOLD = RGBColor(245, 158, 11)           # #F59E0B Solar Amber
    EMERALD = RGBColor(16, 185, 129)        # #10B981 Emerald Green
    ROSE = RGBColor(244, 63, 94)            # #F43F5E Neon Rose
    
    TEXT_WHITE = RGBColor(248, 250, 252)    # Pure bright white
    TEXT_MUTED = RGBColor(203, 213, 225)    # Light slate
    TEXT_DIM = RGBColor(148, 163, 184)      # Muted slate

    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        
        # Header accent strip
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
        strip.fill.solid()
        strip.fill.fore_color.rgb = CYAN
        strip.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="MYSTICAI · INFOSYS SPRINGBOARD CAPSTONE", tag_color=CYAN, slide_num=None):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(9.0), Inches(0.28))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_right = tf_tag.margin_top = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_text.upper()
        p_tag.font.size = Pt(10.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = tag_color

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(9.5), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        # Slide Number Badge (Total 10)
        if slide_num:
            num_box = slide.shapes.add_textbox(Inches(11.2), Inches(0.4), Inches(1.3), Inches(0.35))
            tf_num = num_box.text_frame
            tf_num.margin_right = 0
            p_num = tf_num.paragraphs[0]
            p_num.alignment = PP_ALIGN.RIGHT
            p_num.text = f"{slide_num:02d} / 10"
            p_num.font.size = Pt(11)
            p_num.font.bold = True
            p_num.font.color.rgb = TEXT_DIM

        # Thin divider
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: Title & Hero Cover
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    # Hero Badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(4.8), Inches(0.38))
    badge.fill.solid()
    badge.fill.fore_color.rgb = CARD_BG
    badge.line.color.rgb = CYAN
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "✦ INFOSYS SPRINGBOARD INTERNSHIP 2026"
    p_b.font.size = Pt(10.5)
    p_b.font.bold = True
    p_b.font.color.rgb = CYAN

    # Main Project Title
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(1.6))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = 0
    p1 = tf_t.paragraphs[0]
    p1.text = "MysticAI Platform"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf_t.add_paragraph()
    p2.text = "AI-Powered Palmistry & Tarot Multimodal Intelligence System"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = GOLD

    p3 = tf_t.add_paragraph()
    p3.text = "Synthesizing Computer Vision, 78-Card Symbolic Mechanics & 5-Factor Confidence Scoring"
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_MUTED

    # 4 Quick Stat Callouts
    chips = [
        ("100% MILESTONES", "All 4 Phases Complete", CYAN),
        ("63 UNIT TESTS", "100% Pass Rate", EMERALD),
        ("30+ REST APIS", "FastAPI Asynchronous", PURPLE),
        ("4 ROLE PORTALS", "Seeker / Reader / Consultant / Admin", GOLD),
    ]
    for i, (title_c, desc_c, col) in enumerate(chips):
        x = Inches(0.8 + i * 2.98)
        card = add_card(s1, x, Inches(3.9), Inches(2.8), Inches(1.4), CARD_BG, col)
        tb = s1.shapes.add_textbox(x + Inches(0.2), Inches(4.05), Inches(2.4), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p_c1 = tf.paragraphs[0]
        p_c1.text = title_c
        p_c1.font.size = Pt(12)
        p_c1.font.bold = True
        p_c1.font.color.rgb = col
        p_c2 = tf.add_paragraph()
        p_c2.text = desc_c
        p_c2.font.size = Pt(10)
        p_c2.font.color.rgb = TEXT_MUTED

    # Author Metadata Bar
    meta_card = add_card(s1, Inches(0.8), Inches(5.7), Inches(11.733), Inches(0.9), CARD_ACCENT, CARD_BORDER)
    tb_m = s1.shapes.add_textbox(Inches(1.1), Inches(5.82), Inches(11.1), Inches(0.7))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_top = 0
    pm1 = tf_m.paragraphs[0]
    pm1.text = "Author: Ayush Manore   |   Project Track: Full-Stack AI & Intelligent Systems   |   Mentor: Infosys Technical Review Board"
    pm1.font.size = Pt(11)
    pm1.font.bold = True
    pm1.font.color.rgb = TEXT_WHITE
    pm2 = tf_m.add_paragraph()
    pm2.text = "Stack: Next.js 14 (React) · FastAPI (Python) · PostgreSQL / SQLite · MongoDB Motor · Redis · Docker"
    pm2.font.size = Pt(10)
    pm2.font.color.rgb = CYAN

    # =========================================================================
    # SLIDE 2: Problem Statement & Value Proposition
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)
    add_header(s2, "Problem Statement & Strategic Value", "01. CONTEXT & MOTIVATION", CYAN, 2)

    # Left: The Industry Problem (Red/Rose accent)
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, ROSE)
    tb_p = s2.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.1), Inches(4.7))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = 0
    p = tf_p.paragraphs[0]
    p.text = "CURRENT INDUSTRY CHALLENGES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ROSE

    pain_points = [
        ("Static & Random Blurbs", "Online horoscope & spiritual tools rely on static string concatenations with no algorithmic depth."),
        ("Zero Biometric Integration", "Palmistry apps fail to extract verifiable morphological metrics (curvature, length, mounts)."),
        ("Isolated Modalities", "Palm, Tarot, and Astrology exist in silos, with zero correlation or cross-validation."),
        ("No Objective Confidence", "Users are given arbitrary claims with no transparency, quality checks, or confidence scoring.")
    ]
    for title, desc in pain_points:
        p = tf_p.add_paragraph()
        p.text = f"❌ {title}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p = tf_p.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED

    # Right: MysticAI's Solution (Cyan/Emerald accent)
    add_card(s2, Inches(6.833), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, EMERALD)
    tb_s = s2.shapes.add_textbox(Inches(7.133), Inches(1.85), Inches(5.1), Inches(4.7))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = 0
    p = tf_s.paragraphs[0]
    p.text = "THE MYSTICAI SOLUTION"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    solutions = [
        ("Multimodal Intelligence Engine", "Fuses Computer Vision palm morphology with 78-card symbolic tarot dynamics."),
        ("Deterministic Biometric Tracing", "Measures 5 principal palm lines and 4 elemental hand shapes accurately."),
        ("Big Five (OCEAN) Psychology", "Maps spiritual symbols into validated psychological trait dimensions and life domains."),
        ("5-Factor Weighted Confidence", "Calculates a mathematically sound certainty score (0-100%) for every insight.")
    ]
    for title, desc in solutions:
        p = tf_s.add_paragraph()
        p.text = f"✔ {title}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p = tf_s.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: System Architecture & Technology Stack
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)
    add_header(s3, "Full-Stack System Architecture & Stack", "02. ENGINEERING FOUNDATION", CYAN, 3)

    tiers = [
        ("PRESENTATION LAYER", "Next.js 14 App Router", CYAN, [
            "React 18 Server & Client Components",
            "Tailwind CSS + Glassmorphism aesthetic",
            "Framer Motion 3D card flips & HUD overlays",
            "Responsive across Mobile, Tablet & Desktop",
            "One-Click CSV / JSON Data Export"
        ]),
        ("INTELLIGENCE API LAYER", "FastAPI (Async Python 3.11)", PURPLE, [
            "30+ Modular REST Endpoints with Swagger Docs",
            "11 Decoupled Domain Microservices",
            "Pydantic v2 Strict Request/Response Schemas",
            "JWT Bearer Auth & Role-Based Access Control",
            "Sub-100ms High-Throughput Response Times"
        ]),
        ("ENTERPRISE DATA LAYER", "Polyglot Persistence", GOLD, [
            "PostgreSQL 16: ACID User & Transactional State",
            "Auto SQLite Fallback: Zero-friction local dev",
            "MongoDB Motor: Unstructured reading documents",
            "Redis 7: Session caching & token blacklist",
            "Docker Compose multi-container orchestrator"
        ])
    ]

    for i, (title_t, sub_t, col, bullets) in enumerate(tiers):
        x = Inches(0.8 + i * 3.98)
        add_card(s3, x, Inches(1.6), Inches(3.78), Inches(5.2), CARD_BG, col)
        tb = s3.shapes.add_textbox(x + Inches(0.25), Inches(1.85), Inches(3.28), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = title_t
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = sub_t
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p = tf.add_paragraph()
        p.text = "─────────────────────"
        p.font.size = Pt(8)
        p.font.color.rgb = CARD_BORDER

        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"✦ {b}"
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: Core Engine 1 - Palm Biometric Feature Extraction
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)
    add_header(s4, "Biometric Palm Feature Extraction Engine", "03. MULTIMODAL COMPUTER VISION", CYAN, 4)

    # Left Card: The 5 Lines
    add_card(s4, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2), CARD_BG, CYAN)
    tb_l = s4.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.4), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = 0
    p = tf_l.paragraphs[0]
    p.text = "5 PRINCIPAL PALM LINES ANALYZED"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN

    lines_info = [
        ("Heart Line", "Emotional capacity, empathy quotient, relationship depth"),
        ("Head Line", "Analytical cognition, focus clarity, decision-making style"),
        ("Life Line", "Vitality, physical resilience, adaptability to stress"),
        ("Fate Line", "Career trajectory, discipline, goal-oriented pathing"),
        ("Sun Line", "Creativity, public recognition, artistic fulfillment")
    ]
    for name, desc in lines_info:
        p = tf_l.add_paragraph()
        p.text = f"▪ {name}: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = GOLD
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED

    # Right Card: Morphological Pipeline
    add_card(s4, Inches(7.1), Inches(1.6), Inches(5.433), Inches(5.2), CARD_BG, PURPLE)
    tb_r = s4.shapes.add_textbox(Inches(7.4), Inches(1.85), Inches(4.833), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = 0
    p = tf_r.paragraphs[0]
    p.text = "MORPHOLOGY & DETECTION PIPELINE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PURPLE

    pipe_steps = [
        ("Input Modes", "Dual support: Real-time Camera HUD Scanner + High-res File Upload"),
        ("Hand Shape Element", "Calculates Palm-to-Finger ratio to classify Earth, Air, Fire, or Water"),
        ("Contour & Landmarks", "Identifies 21 anatomical landmarks across thumb, index, palm base"),
        ("Curvature Tracing", "Measures length, depth, curvature & interruptions along line trajectories"),
        ("Mount Analysis", "Evaluates Venus, Jupiter, Apollo & Lunar fleshy mounts for energy balance")
    ]
    for step, detail in pipe_steps:
        p = tf_r.add_paragraph()
        p.text = f"⚡ {step}: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = detail
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 5: Core Engine 2 - Tarot Spread & Symbolic Dynamics
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)
    add_header(s5, "Tarot Spread Engine & Symbolic Mechanics", "04. SYMBOLIC DYNAMICS", GOLD, 5)

    # 3 Cards for Deck, Spreads, Elements
    t_cards = [
        ("78-CARD CANONICAL DECK", "Archetype Engine", GOLD, [
            "22 Major Arcana: Universal life lessons, soul evolutions & core archetypes",
            "56 Minor Arcana: Practical day-to-day challenges & opportunities",
            "4 Suits: Wands (Fire), Cups (Water), Swords (Air), Pentacles (Earth)",
            "Dual Polarity: Upright (direct flow) vs Inverted/Reversed (shadow/blocked)"
        ]),
        ("6 SPREAD ARCHITECTURES", "Spatial Context", CYAN, [
            "Single Card Draw: Instant daily spiritual beacon & morning focus",
            "Three-Card Spread: Linear Past, Present, and Future continuum",
            "Five-Card Cross: Core conflict, subconscious desires, and obstacle resolution",
            "Celtic Cross (10 Cards): Full psychological audit & longitudinal outcome",
            "Custom Spreads: Configurable layouts for professional reader consultations"
        ]),
        ("ELEMENTAL BALANCE MODEL", "Harmonic Scoring", EMERALD, [
            "Computes Fire/Water/Air/Earth balance across all revealed cards",
            "Detects elemental deficits (e.g., low Earth indicates lack of grounding)",
            "Dynamic card synergy & tension modeling based on adjacent positions",
            "Feeds mathematical distribution directly into the AI Synthesis Engine"
        ])
    ]

    for i, (title_tc, sub_tc, col_tc, bullets_tc) in enumerate(t_cards):
        x = Inches(0.8 + i * 3.98)
        add_card(s5, x, Inches(1.6), Inches(3.78), Inches(5.2), CARD_BG, col_tc)
        tb = s5.shapes.add_textbox(x + Inches(0.25), Inches(1.85), Inches(3.28), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = title_tc
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col_tc
        p = tf.add_paragraph()
        p.text = sub_tc
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p = tf.add_paragraph()
        p.text = "─────────────────────"
        p.font.size = Pt(8)
        p.font.color.rgb = CARD_BORDER

        for b in bullets_tc:
            p = tf.add_paragraph()
            p.text = f"✦ {b}"
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 6: Cross-Modal AI Synthesis & 5-Factor Scoring
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)
    add_header(s6, "AI Synthesis & 5-Factor Confidence Model", "05. INTELLIGENCE SYNTHESIS", PURPLE, 6)

    # Left: Synthesis Domains & Big Five
    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, PURPLE)
    tb_syn = s6.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.1), Inches(4.7))
    tf_syn = tb_syn.text_frame
    tf_syn.word_wrap = True
    tf_syn.margin_left = tf_syn.margin_top = 0
    p = tf_syn.paragraphs[0]
    p.text = "CROSS-MODAL SYNTHESIS & PSYCHOLOGY"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PURPLE

    p = tf_syn.add_paragraph()
    p.text = "Correlates biological palm traits with symbolic tarot draws to formulate:"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    syn_points = [
        ("7 Holistic Life Domains", "Synthesizes career, emotional vitality, spiritual purpose, love, wealth, mental resilience & creativity."),
        ("Big Five (OCEAN) Profiling", "Generates quantitative ratings for Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism."),
        ("Actionable Life Recommendations", "Produces concrete, goal-oriented daily guidance instead of vague generic prophecies.")
    ]
    for h, d in syn_points:
        p = tf_syn.add_paragraph()
        p.text = f"✦ {h}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p = tf_syn.add_paragraph()
        p.text = d
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

    # Right: 5-Factor Weighted Confidence Algorithm
    add_card(s6, Inches(6.833), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, CYAN)
    tb_sc = s6.shapes.add_textbox(Inches(7.133), Inches(1.85), Inches(5.1), Inches(4.7))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_left = tf_sc.margin_top = 0
    p = tf_sc.paragraphs[0]
    p.text = "5-FACTOR WEIGHTED CONFIDENCE ALGORITHM"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN

    factors = [
        ("Palm Line Clarity (25%)", "Measures sharpness, continuity, and depth of traced palm lines"),
        ("Tarot Spread Harmony (25%)", "Quantifies card polarity coherence and positional consistency"),
        ("Elemental Alignment (20%)", "Evaluates concord between hand shape element and tarot suit distribution"),
        ("Longitudinal Continuity (15%)", "Compares session readings against historical baseline user profiles"),
        ("Capture & Scan Quality (15%)", "Evaluates lighting, contrast, and resolution of user palm capture")
    ]
    for name, desc in factors:
        p = tf_sc.add_paragraph()
        p.text = f"⚖ {name}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = GOLD
        p = tf_sc.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 7: 4 Role-Based User Portals (RBAC)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_bg(s7)
    add_header(s7, "Role-Based Access Portals (RBAC)", "06. MULTI-PERSONA WORKFLOWS", EMERALD, 7)

    portals = [
        ("SEEKER PORTAL", "Everyday Spiritual Explorer", CYAN, [
            "Personal reading history timeline",
            "Morning daily tarot card draws",
            "Big Five OCEAN personality radar",
            "Goal alignment & life path progress",
            "Exportable spiritual reports (CSV/JSON)"
        ]),
        ("TAROT READER PORTAL", "Professional Practitioner", PURPLE, [
            "Active client consultation queue",
            "Custom spread layout designer",
            "Annotated client notes & insights",
            "Card inversion override toggles",
            "Consultation history archives"
        ]),
        ("SPIRITUAL CONSULTANT", "Holistic Advisor", GOLD, [
            "Multi-session client audit profiles",
            "Longitudinal personality trend tracker",
            "Cross-modal palm + tarot synthesis view",
            "Priority alert tagging for client guidance",
            "Deep-dive psychological metric views"
        ]),
        ("SUPER ADMIN CONSOLE", "Platform Administrator", ROSE, [
            "Live server telemetry & endpoint metrics",
            "Active user role management",
            "Dataset catalog browsing & statistics",
            "Security token audit logs & revocation",
            "Health checks across Postgres, Mongo, Redis"
        ])
    ]

    for i, (title_po, sub_po, col_po, bullets_po) in enumerate(portals):
        col_idx = i % 2
        row_idx = i // 2
        x = Inches(0.8 + col_idx * 5.98)
        y = Inches(1.6 + row_idx * 2.65)
        w = Inches(5.75)
        h = Inches(2.45)

        add_card(s7, x, y, w, h, CARD_BG, col_po)
        tb = s7.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), w - Inches(0.4), h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = f"{title_po}  ·  {sub_po}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col_po

        for b in bullets_po:
            p = tf.add_paragraph()
            p.text = f"✦ {b}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 8: Live Platform User Experience & Screenshots
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_bg(s8)
    add_header(s8, "Interactive User Experience & UI Showcase", "07. USER EXPERIENCE", CYAN, 8)

    # Embed screenshot 1 (Hero / Landing)
    if os.path.exists(img_hero):
        add_card(s8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(3.6), CARD_BG, CARD_BORDER)
        s8.shapes.add_picture(img_hero, Inches(0.85), Inches(1.65), width=Inches(5.6))
    else:
        add_card(s8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(3.6), CARD_BG, CYAN)

    tb_c1 = s8.shapes.add_textbox(Inches(0.8), Inches(5.35), Inches(5.7), Inches(1.5))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_top = 0
    p = tf_c1.paragraphs[0]
    p.text = "MODERN COSMIC GLASSMORPHISM UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p = tf_c1.add_paragraph()
    p.text = "Dark-mode aesthetic with interactive camera palm HUD, 3D card deck shuffle & flip animations, and real-time guidance feedback."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    # Embed screenshot 2 (Dashboard Profile)
    if os.path.exists(img_dashboard):
        add_card(s8, Inches(6.833), Inches(1.6), Inches(5.7), Inches(3.6), CARD_BG, CARD_BORDER)
        s8.shapes.add_picture(img_dashboard, Inches(6.883), Inches(1.65), width=Inches(5.6))
    else:
        add_card(s8, Inches(6.833), Inches(1.6), Inches(5.7), Inches(3.6), CARD_BG, PURPLE)

    tb_c2 = s8.shapes.add_textbox(Inches(6.833), Inches(5.35), Inches(5.7), Inches(1.5))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_top = 0
    p = tf_c2.paragraphs[0]
    p.text = "HOLISTIC ANALYTICS & DATA PORTABILITY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PURPLE
    p = tf_c2.add_paragraph()
    p.text = "Seeker profile showing Big Five radar charts, longitudinal spiritual timelines, and instant one-click export to CSV & JSON formats."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 9: Engineering Rigor, Testing & Performance
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_bg(s9)
    add_header(s9, "Engineering Rigor, Testing & Quality", "08. VERIFICATION & METRICS", EMERALD, 9)

    # Left: 4 Metric Cards
    metrics = [
        ("63 / 63", "Automated Tests Passing (100%)", EMERALD),
        ("< 95 ms", "Average REST API Latency", CYAN),
        ("30+ APIS", "Swagger / OpenAPI Standard", PURPLE),
        ("0 DOWNTIME", "Automatic SQLite Fallback", GOLD),
    ]
    for i, (val, label, col_m) in enumerate(metrics):
        col_idx = i % 2
        row_idx = i // 2
        x = Inches(0.8 + col_idx * 2.85)
        y = Inches(1.6 + row_idx * 1.5)
        add_card(s9, x, y, Inches(2.7), Inches(1.35), CARD_BG, col_m)
        tb = s9.shapes.add_textbox(x + Inches(0.15), y + Inches(0.15), Inches(2.4), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = col_m
        p = tf.add_paragraph()
        p.text = label
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

    # Left bottom: Test Suite detail
    add_card(s9, Inches(0.8), Inches(4.8), Inches(5.55), Inches(2.0), CARD_BG, CARD_BORDER)
    tb_t = s9.shapes.add_textbox(Inches(1.0), Inches(4.95), Inches(5.15), Inches(1.7))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = 0
    p = tf_t.paragraphs[0]
    p.text = "TESTING & CODE STABILITY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    t_points = [
        "Auth security: JWT token generation, refresh & blacklist tests",
        "Deterministic CV: Line curvature boundary & landmark assertions",
        "Tarot permutations: Card inversion polarities & spread integrity",
        "Cross-modal integration: Synthesis output schema validation"
    ]
    for tp in t_points:
        p = tf_t.add_paragraph()
        p.text = f"✔ {tp}"
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED

    # Right: Swagger Docs Screenshot
    if os.path.exists(img_swagger):
        add_card(s9, Inches(6.65), Inches(1.6), Inches(5.883), Inches(5.2), CARD_BG, CARD_BORDER)
        s9.shapes.add_picture(img_swagger, Inches(6.7), Inches(1.65), width=Inches(5.783))
    else:
        add_card(s9, Inches(6.65), Inches(1.6), Inches(5.883), Inches(5.2), CARD_BG, PURPLE)

    # =========================================================================
    # SLIDE 10: Milestones Delivered, Impact & Roadmap
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_bg(s10)
    add_header(s10, "Project Conclusion, Impact & Future Roadmap", "09. SUMMARY & DEMO", GOLD, 10)

    # Left: Milestones Completed
    add_card(s10, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, EMERALD)
    tb_mil = s10.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(5.1), Inches(4.7))
    tf_mil = tb_mil.text_frame
    tf_mil.word_wrap = True
    tf_mil.margin_left = tf_mil.margin_top = 0
    p = tf_mil.paragraphs[0]
    p.text = "MILESTONES DELIVERED (100%)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    milestones = [
        ("Milestone 1: Foundations & Architecture", "FastAPI backend, Next.js frontend, hybrid database models, full auth scaffolding."),
        ("Milestone 2: Palmistry & Tarot Engines", "5 palm line extraction algorithms, 78-card tarot deck, 6 spread layouts."),
        ("Milestone 3: AI Synthesis & RBAC", "5-factor confidence scoring model, 4 role-based user portals, report generation."),
        ("Milestone 4: Testing, Export & Polish", "63 passing automated tests, CSV/JSON export, performance optimization.")
    ]
    for name, detail in milestones:
        p = tf_mil.add_paragraph()
        p.text = f"✔ {name}"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p = tf_mil.add_paragraph()
        p.text = detail
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED

    # Right: Future Scope & Hand-off
    add_card(s10, Inches(6.833), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, CYAN)
    tb_fut = s10.shapes.add_textbox(Inches(7.133), Inches(1.85), Inches(5.1), Inches(4.7))
    tf_fut = tb_fut.text_frame
    tf_fut.word_wrap = True
    tf_fut.margin_left = tf_fut.margin_top = 0
    p = tf_fut.paragraphs[0]
    p.text = "FUTURE ROADMAP & LIVE DEMO"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN

    future = [
        ("On-Device Edge MediaPipe", "Client-side WebAssembly computer vision for offline palm landmark inference."),
        ("Cross-Platform Mobile App", "React Native iOS & Android apps with haptic feedback tarot shuffling."),
        ("Multilingual Neural Voice", "Real-time AI voice-guided consultations in 10+ global languages."),
        ("WebXR 3D Sanctum", "Immersive virtual reality spiritual consultation environment.")
    ]
    for h, d in future:
        p = tf_fut.add_paragraph()
        p.text = f"🚀 {h}"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = GOLD
        p = tf_fut.add_paragraph()
        p.text = d
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED

    p_close = tf_fut.add_paragraph()
    p_close.text = "──────────────────────────────"
    p_close.font.size = Pt(8)
    p_close.font.color.rgb = CARD_BORDER

    p_thanks = tf_fut.add_paragraph()
    p_thanks.text = "Thank you! Ready for Live Demo & Q&A."
    p_thanks.font.size = Pt(14)
    p_thanks.font.bold = True
    p_thanks.font.color.rgb = TEXT_WHITE

    # Save to targets
    target_files = [
        os.path.join(base_dir, "MysticAI_10_Slides_Presentation.pptx"),
        os.path.join(base_dir, "MysticAI_Presentation.pptx"),
        os.path.join(base_dir, "MysticAI_Presentation [Autosaved].pptx"),
        os.path.join(base_dir, "docs", "MysticAI_Presentation.pptx")
    ]

    for pth in target_files:
        try:
            prs.save(pth)
            print(f"Successfully generated: {pth}")
        except Exception as e:
            print(f"Error saving to {pth}: {e}")

    return target_files[0]

if __name__ == "__main__":
    build_10_slide_presentation()
