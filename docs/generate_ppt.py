import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_visual_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    img_landing = os.path.join(assets_dir, "website_hero_landing.jpg")
    img_datasets = os.path.join(assets_dir, "website_datasets_explorer.jpg")
    img_dashboard = os.path.join(assets_dir, "website_dashboard_profile.jpg")
    img_swagger = os.path.join(assets_dir, "website_swagger_docs.jpg")

    # Theme Colors
    BG_COLOR = RGBColor(15, 23, 42)         # #0F172A - Deep Navy/Slate
    CARD_BG = RGBColor(30, 41, 59)          # #1E293B - Slate Card
    CARD_BORDER = RGBColor(51, 65, 85)      # #334155 - Card Border
    
    PRIMARY_CYAN = RGBColor(56, 189, 248)   # #38BDF8 - Sky Blue / Cyan
    ACCENT_PURPLE = RGBColor(168, 85, 247)  # #A855F7 - Modern Purple
    ACCENT_GOLD = RGBColor(245, 158, 11)    # #F59E0B - Amber/Gold
    ACCENT_GREEN = RGBColor(16, 185, 129)   # #10B981 - Emerald Green
    
    TEXT_MAIN = RGBColor(248, 250, 252)     # #F8FAFC - Bright White
    TEXT_MUTED = RGBColor(203, 213, 225)    # #CBD5E1 - Slate Light Gray (higher contrast)
    TEXT_DIM = RGBColor(148, 163, 184)      # #94A3B8

    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="MILESTONE 1 REVIEW", tag_color=PRIMARY_CYAN):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.3))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_right = tf_tag.margin_top = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = tag_color

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN

        # Decorative bar
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.fill.background()

    def add_image_card(slide, img_path, left, top, width, height, label="LIVE PLATFORM INTERFACE"):
        # Image background container
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left - 0.08), Inches(top - 0.08), Inches(width + 0.16), Inches(height + 0.5)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        # Label above image
        tb = slide.shapes.add_textbox(Inches(left), Inches(top + height + 0.05), Inches(width), Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"📷 {label}"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_CYAN

        # Insert picture
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, Inches(left), Inches(top), Inches(width), Inches(height))

    # =========================================================================
    # SLIDE 1: Title Slide with Hero UI Preview
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide1)

    # Left content column
    tag_box = slide1.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(6.0), Inches(0.35))
    tf = tag_box.text_frame
    p = tf.paragraphs[0]
    p.text = "CAPSTONE PROJECT • MILESTONE 1 REVIEW"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_CYAN

    # Main Title
    t_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.8), Inches(1.8))
    tf = t_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Palmistry & Tarot\nIntelligence Platform"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN

    p_sub = tf.add_paragraph()
    p_sub.text = "A Multimodal AI Platform for Computer Vision & Knowledge Graph-Driven Analysis"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = TEXT_MUTED

    # Bullet pills on left
    bullets_s1 = [
        ("⚡ High-Performance Async Backend", "FastAPI (Python 3.11) with Pydantic schemas"),
        ("🌐 Modern Glassmorphic Frontend", "Next.js 14 App Router + TailwindCSS"),
        ("🛡️ Enterprise Auth & 4-Tier RBAC", "Bcrypt password hashing & JWT token lifecycle"),
        ("📚 Digitized Core Knowledge Bases", "Complete 78-Card Tarot + 7-Line Palmistry Datasets")
    ]
    top_curr = 3.3
    for title, desc in bullets_s1:
        card_b = slide1.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_curr), Inches(5.8), Inches(0.8)
        )
        card_b.fill.solid()
        card_b.fill.fore_color.rgb = CARD_BG
        card_b.line.color.rgb = CARD_BORDER
        card_b.line.width = Pt(1)

        tb_b = slide1.shapes.add_textbox(Inches(0.95), Inches(top_curr + 0.1), Inches(5.5), Inches(0.6))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        p1 = tf_b.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY_CYAN
        p2 = tf_b.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        top_curr += 0.9

    # Right Image: Hero Landing Page UI
    add_image_card(slide1, img_landing, 7.0, 1.2, 5.5, 5.5, "Live Website Landing Page (Next.js 14)")

    slide1.notes_slide.notes_text_frame.text = (
        "Good morning/afternoon professors. For Milestone 1 of our project, we have established the full-stack architecture, "
        "polyglot database, secure authentication, and interactive knowledge bases for our Palmistry & Tarot Intelligence Platform."
    )

    # =========================================================================
    # SLIDE 2: Problem Statement & Domain in Computer Science
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide2)
    add_header(slide2, "Problem Statement & Computational Domain Modeling", "DOMAIN FORMALIZATION")

    # 3 High-level visual cards
    c_w = 3.7
    gap = 0.31
    l1 = 0.8
    l2 = l1 + c_w + gap
    l3 = l2 + c_w + gap

    # Card 1: The Problem
    card1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l1), Inches(1.6), Inches(c_w), Inches(5.3))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = PRIMARY_CYAN
    card1.line.width = Pt(1.5)

    tb = slide2.shapes.add_textbox(Inches(l1 + 0.2), Inches(1.8), Inches(c_w - 0.4), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📌 Problem & Motivation"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_CYAN
    
    p_sub = tf.add_paragraph()
    p_sub.text = "Transforming subjective symbols into structured computation."
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = TEXT_DIM
    p_sub.space_after = Pt(12)

    points_c1 = [
        "Unstandardized Data: Traditional practices lack structured schemas and algorithmic consistency.",
        "Multimodal AI Solution: Formalizes visual morphology and symbolic knowledge graphs into unified reflection metrics.",
        "Milestone 1 Scope: Establishing clean API contracts, secure identity, and core reference knowledge bases."
    ]
    for pt in points_c1:
        p = tf.add_paragraph()
        p.space_after = Pt(8)
        p.text = f"• {pt}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MUTED

    # Card 2: Tarot as Knowledge Graph
    card2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l2), Inches(1.6), Inches(c_w), Inches(5.3))
    card2.fill.solid()
    card2.fill.fore_color.rgb = CARD_BG
    card2.line.color.rgb = ACCENT_PURPLE
    card2.line.width = Pt(1.5)

    tb = slide2.shapes.add_textbox(Inches(l2 + 0.2), Inches(1.8), Inches(c_w - 0.4), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🃏 Tarot: Knowledge Graph"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    
    p_sub = tf.add_paragraph()
    p_sub.text = "78 Discrete Semantic Nodes & Spreads"
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = TEXT_DIM
    p_sub.space_after = Pt(12)

    points_c2 = [
        "78 Discrete Nodes: 22 Major Arcana (life archetypes) + 56 Minor Arcana (4 elemental domains).",
        "Binary Orientation State: Upright (direct expression) vs. Reversed (internalized block).",
        "Positional Spreads: Multi-node directed graph (e.g. Node 1=Past, Node 2=Present, Node 3=Future)."
    ]
    for pt in points_c2:
        p = tf.add_paragraph()
        p.space_after = Pt(8)
        p.text = f"• {pt}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MUTED

    # Card 3: Palmistry as Computer Vision
    card3 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l3), Inches(1.6), Inches(c_w), Inches(5.3))
    card3.fill.solid()
    card3.fill.fore_color.rgb = CARD_BG
    card3.line.color.rgb = ACCENT_GOLD
    card3.line.width = Pt(1.5)

    tb = slide2.shapes.add_textbox(Inches(l3 + 0.2), Inches(1.8), Inches(c_w - 0.4), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "✋ Palmistry: Computer Vision"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD
    
    p_sub = tf.add_paragraph()
    p_sub.text = "Geometric Landmarks & Ridge Features"
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = TEXT_DIM
    p_sub.space_after = Pt(12)

    points_c3 = [
        "21 Hand Landmarks: 3D coordinates extracted using Google MediaPipe framework.",
        "ROI Segmentation: Isolates palm plane for perspective-corrected analysis.",
        "Ridge Feature Vectors: Measures length, curvature, and continuity of major crease lines (Heart, Head, Life, Fate)."
    ]
    for pt in points_c3:
        p = tf.add_paragraph()
        p.space_after = Pt(8)
        p.text = f"• {pt}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MUTED

    slide2.notes_slide.notes_text_frame.text = (
        "We explain the domain in strict computer science terms: Tarot as a finite semantic knowledge graph with 78 nodes, "
        "and Palmistry as an anatomical computer vision problem with 21 landmark coordinates and crease ridge extraction."
    )

    # =========================================================================
    # SLIDE 3: System Architecture & Modern Tech Stack
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide3)
    add_header(slide3, "System Architecture & Polyglot Data Strategy", "FULL-STACK ARCHITECTURE")

    # 3 Column architecture summary
    arch_cols = [
        ("🌐 Frontend Client", "Next.js 14 • React • Tailwind", PRIMARY_CYAN, [
            "Next.js 14 App Router for rapid SSR & client interactivity.",
            "Cosmic dark glassmorphism theme with responsive UI.",
            "Client-side JWT session handling & state synchronization."
        ]),
        ("⚡ Async Backend", "FastAPI • Python 3.11 • Pydantic", ACCENT_PURPLE, [
            "Asynchronous ASGI non-blocking event loop.",
            "Strict Pydantic request/response schema validation.",
            "Auto-generated OpenAPI / Swagger live testing interface."
        ]),
        ("🗄️ Polyglot Database", "PostgreSQL / SQLite • MongoDB • Redis", ACCENT_GOLD, [
            "Relational SQL: ACID compliance for User Auth & RBAC.",
            "MongoDB: Schema-less store for 21-point hand coordinates & AI logs.",
            "Redis: Sub-millisecond JWT blacklist token checking & caching."
        ])
    ]

    for i, (col_title, col_sub, col_color, col_bullets) in enumerate(arch_cols):
        c_left = 0.8 + i * (c_w + gap)
        c_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(c_w), Inches(4.3))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = CARD_BG
        c_box.line.color.rgb = col_color
        c_box.line.width = Pt(1.5)

        tb = slide3.shapes.add_textbox(Inches(c_left + 0.2), Inches(1.8), Inches(c_w - 0.4), Inches(3.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = col_title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col_color

        p2 = tf.add_paragraph()
        p2.text = col_sub
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_DIM
        p2.space_after = Pt(12)

        for b in col_bullets:
            p_b = tf.add_paragraph()
            p_b.space_after = Pt(6)
            p_b.text = f"✔ {b}"
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = TEXT_MUTED

    # Bottom summary ribbon
    ribbon = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.85))
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = CARD_BG
    ribbon.line.color.rgb = CARD_BORDER
    tb_r = slide3.shapes.add_textbox(Inches(1.0), Inches(6.18), Inches(11.3), Inches(0.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "💡 Polyglot Strategy: Relational SQL guarantees ACID transactions for users/roles, while MongoDB stores high-dimensional AI & CV telemetry without rigid schema migration overhead."
    p.font.size = Pt(10)
    p.font.color.rgb = PRIMARY_CYAN

    slide3.notes_slide.notes_text_frame.text = (
        "Our architecture uses an async microservices pattern with FastAPI, Next.js 14, and a polyglot database strategy "
        "separating relational auth data from flexible document payloads."
    )

    # =========================================================================
    # SLIDE 4: Interactive Datasets & Card Draw Simulator (WITH IMAGE)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide4)
    add_header(slide4, "Digitized Knowledge Bases & Draw Simulator", "CORE DATASETS & SIMULATOR")

    # Left Column: Concise Takeaways
    tb_left = slide4.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(4.6), Inches(5.3))
    tf = tb_left.text_frame
    tf.word_wrap = True

    pts_s4 = [
        ("📚 78-Card Tarot Dataset", "Complete 22 Major Arcana + 56 Minor Arcana (Wands, Cups, Swords, Pentacles) with keywords and upright/reversed definitions."),
        ("✋ 7-Line Palmistry Reference", "Heart, Head, Life, Fate, Sun, Mercury, and Girdle lines mapped with morphological variation rules."),
        ("🎲 Interactive Draw Simulator", "Real-time pseudo-random sampling of 1-card, 3-card (Past/Present/Future), and 5-card spreads with dynamic orientation."),
        ("🔍 Live Search & Filter APIs", "Instant in-memory filtering by suit, arcana type, element, and keyword via `/api/v1/datasets/tarot/cards`.")
    ]
    for b_title, b_desc in pts_s4:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = b_title + "\n"
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = PRIMARY_CYAN

        p2 = tf.add_paragraph()
        p2.space_after = Pt(10)
        r2 = p2.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MUTED

    # Right Image: Datasets Explorer Screenshot
    add_image_card(slide4, img_datasets, 5.6, 1.6, 6.9, 5.1, "Interactive Tarot & Palmistry Explorer (/datasets)")

    slide4.notes_slide.notes_text_frame.text = (
        "Here is the interactive dataset explorer interface. We digitized all 78 Tarot cards and 7 palm lines. "
        "Users can filter cards in real-time and simulate live 3-card spread draws."
    )

    # =========================================================================
    # SLIDE 5: Authentication, RBAC & Dashboard (WITH IMAGE)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide5)
    add_header(slide5, "User Authentication, 4-Tier RBAC & Dashboard", "SECURITY & USER INTERFACE")

    # Left Column: Concise Takeaways
    tb_left = slide5.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(4.6), Inches(5.3))
    tf = tb_left.text_frame
    tf.word_wrap = True

    pts_s5 = [
        ("🔐 Salted Bcrypt Password Hashing", "Zero plaintext passwords. Evaluated with one-way cost factor 12 hashing."),
        ("🎫 Dual JWT Stateless Authentication", "15-minute Access Tokens + 7-day Refresh Tokens with instant Redis token blacklisting on logout."),
        ("🛡️ 4-Tier Granular RBAC Roles", "Enforces access across `guest`, `user`, `tarot_reader`, and `admin` via FastAPI dependency injection."),
        ("👤 Seeker Dashboard & Profiles", "Personalized user preferences, date of birth, spiritual goals, and preferred card spreads.")
    ]
    for b_title, b_desc in pts_s5:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = b_title + "\n"
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = ACCENT_PURPLE

        p2 = tf.add_paragraph()
        p2.space_after = Pt(10)
        r2 = p2.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MUTED

    # Right Image: Dashboard & Profile Screenshot
    add_image_card(slide5, img_dashboard, 5.6, 1.6, 6.9, 5.1, "Authenticated Seeker Dashboard & Profile Preferences (/dashboard)")

    slide5.notes_slide.notes_text_frame.text = (
        "This slide showcases the user authentication, RBAC permission system, and seeker dashboard. "
        "Passwords are encrypted with bcrypt, sessions are managed with JWT, and users can customize their spiritual goals."
    )

    # =========================================================================
    # SLIDE 6: FastAPI Endpoints & Swagger Documentation (WITH IMAGE)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide6)
    add_header(slide6, "Verified REST API & Interactive Swagger Specs", "API ECOSYSTEM & VALIDATION")

    # Left Column: Concise Takeaways
    tb_left = slide6.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(4.6), Inches(5.3))
    tf = tb_left.text_frame
    tf.word_wrap = True

    pts_s6 = [
        ("🔌 100% Typed REST Endpoints", "Built using FastAPI routers: `/auth`, `/users`, `/profiles`, and `/datasets`."),
        ("🛡️ Automatic Pydantic Validation", "Incoming request bodies and outgoing responses are strictly validated against schema models."),
        ("📖 Interactive Swagger UI (/docs)", "Built-in OpenAPI interface allowing examiners to authenticate with JWT and test live queries directly in the browser."),
        ("✅ Zero-Config Fallback Mode", "Runs out-of-the-box with SQLite and in-memory caches, plus Docker Compose support for production.")
    ]
    for b_title, b_desc in pts_s6:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = b_title + "\n"
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = ACCENT_GREEN

        p2 = tf.add_paragraph()
        p2.space_after = Pt(10)
        r2 = p2.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MUTED

    # Right Image: Swagger Docs Screenshot
    add_image_card(slide6, img_swagger, 5.6, 1.6, 6.9, 5.1, "FastAPI Interactive Swagger Workbench (/docs)")

    slide6.notes_slide.notes_text_frame.text = (
        "All backend endpoints are strongly typed, validated with Pydantic, and self-documented via Swagger UI at /docs, "
        "enabling direct in-browser testing during viva defense."
    )

    # =========================================================================
    # SLIDE 7: Milestone 1 Summary & Phase 2 Roadmap
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide7)
    add_header(slide7, "Milestone 1 Summary & Phase 2 Roadmap", "PROJECT STATUS & FUTURE SCOPE")

    # Left: Completed Milestone 1
    c1 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.65), Inches(5.3))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = ACCENT_GREEN
    c1.line.width = Pt(1.5)

    tb = slide7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.25), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "✅ Milestone 1: Delivered Foundations"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(10)

    m1_items = [
        "Async Microservices Architecture (FastAPI + Next.js 14)",
        "Polyglot Persistence (SQL + MongoDB Document + Redis)",
        "Bcrypt Password Hashing & Stateless JWT Auth",
        "4-Tier RBAC Permission Hierarchy",
        "Complete 78-Card Tarot & 7-Line Palmistry Datasets",
        "Interactive Card Draw Simulator & Search Filters",
        "Seeker Dashboard & Profile Customization",
        "Live OpenAPI / Swagger API Workbench"
    ]
    for item in m1_items:
        p = tf.add_paragraph()
        p.space_after = Pt(4)
        p.text = f"✔ {item}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MUTED

    # Right: Future Roadmap
    c2 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(1.6), Inches(5.65), Inches(5.3))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = PRIMARY_CYAN
    c2.line.width = Pt(1.5)

    tb = slide7.shapes.add_textbox(Inches(7.05), Inches(1.8), Inches(5.25), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚀 Phase 2: Future Development Roadmap"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_CYAN
    p.space_after = Pt(10)

    m2_items = [
        ("MediaPipe 21-Point Palm Detection", "Live 3D hand landmark coordinate mapping."),
        ("OpenCV Line Crease Segmentation", "Adaptive CLAHE & Canny edge ridge extraction."),
        ("Generative AI / LLM Narrative Synthesis", "Dynamic multi-turn prompt pipeline for custom readings."),
        ("Celery Background Task Queue", "Asynchronous image processing and report rendering."),
        ("PDF Report Generator", "Downloadable reflection summaries stored in MongoDB."),
        ("Live Reader WebSocket Chat", "Real-time consultation with certified readers.")
    ]
    for title, desc in m2_items:
        p = tf.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = f"➔ {title}: "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = PRIMARY_CYAN
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MUTED

    slide7.notes_slide.notes_text_frame.text = (
        "To conclude: In Milestone 1, we established all architectural, security, database, and knowledge foundations. "
        "In Milestone 2, we will integrate Google MediaPipe and OpenCV for computer vision, and connect generative AI for narrative report generation. "
        "Thank you! We are now open for questions."
    )

    # Save output
    output_path = os.path.join(os.path.dirname(__file__), "Milestone_1_Presentation.pptx")
    prs.save(output_path)
    print(f"Visual Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_visual_presentation()
