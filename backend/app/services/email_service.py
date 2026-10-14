"""
Email Service
=============
Handles all email notifications for MysticAI platform using Gmail SMTP.

Features:
- Scheduled reading reminders
- Daily spiritual guidance emails
- Monthly spiritual report emails
- Welcome emails on registration
"""

import smtplib
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone
from typing import Optional
import logging

from app.config import settings

logger = logging.getLogger(__name__)


# ============================================================================
# Email Templates
# ============================================================================

def _build_html(title: str, body_html: str, user_name: str = "Seeker") -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
<style>
  body {{ margin:0; padding:0; background:#070714; font-family:'Segoe UI',Arial,sans-serif; }}
  .wrapper {{ max-width:600px; margin:0 auto; padding:32px 16px; }}
  .card {{ background:linear-gradient(135deg,#1e1b4b,#0f0c29); border-radius:20px; border:1px solid rgba(168,85,247,0.3); overflow:hidden; }}
  .header {{ background:linear-gradient(90deg,#7c3aed,#4f46e5); padding:32px 40px; text-align:center; }}
  .header h1 {{ margin:0; color:#fde68a; font-size:24px; letter-spacing:1px; }}
  .header p {{ margin:8px 0 0; color:rgba(255,255,255,0.7); font-size:14px; }}
  .sparkle {{ font-size:28px; margin-bottom:8px; display:block; }}
  .body {{ padding:36px 40px; color:#e5e7eb; }}
  .body h2 {{ color:#c4b5fd; margin:0 0 12px; font-size:20px; }}
  .body p {{ line-height:1.7; margin:0 0 16px; color:#d1d5db; }}
  .highlight {{ background:rgba(139,92,246,0.15); border-left:3px solid #a855f7; border-radius:0 8px 8px 0; padding:14px 18px; margin:20px 0; }}
  .highlight p {{ margin:0; color:#c4b5fd; font-style:italic; }}
  .stat-row {{ display:flex; gap:12px; margin:20px 0; flex-wrap:wrap; }}
  .stat {{ flex:1; min-width:120px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:16px; text-align:center; }}
  .stat .val {{ font-size:26px; font-weight:800; color:#a78bfa; }}
  .stat .lbl {{ font-size:11px; color:#9ca3af; text-transform:uppercase; letter-spacing:1px; margin-top:4px; }}
  .btn {{ display:inline-block; background:linear-gradient(90deg,#7c3aed,#4f46e5); color:white!important; text-decoration:none; padding:14px 32px; border-radius:12px; font-weight:700; font-size:14px; margin:8px 0; }}
  .footer {{ text-align:center; padding:24px 40px; border-top:1px solid rgba(255,255,255,0.05); }}
  .footer p {{ margin:0; color:#6b7280; font-size:12px; }}
  .section {{ margin:24px 0; }}
  .section-title {{ font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#8b5cf6; margin-bottom:12px; }}
  .rec-item {{ background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px 16px; margin:8px 0; }}
  .rec-item strong {{ color:#e9d5ff; }}
  .rec-item p {{ margin:4px 0 0; font-size:13px; color:#9ca3af; }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="card">
    <div class="header">
      <span class="sparkle">✨</span>
      <h1>MysticAI</h1>
      <p>Palmistry & Tarot Intelligence Platform</p>
    </div>
    <div class="body">
      <h2>Dear {user_name},</h2>
      {body_html}
    </div>
    <div class="footer">
      <p>© {datetime.now().year} MysticAI · Palmistry & Tarot Intelligence Platform</p>
      <p style="margin-top:6px;">You received this because you are a registered member. <a href="#" style="color:#8b5cf6;">Manage preferences</a></p>
    </div>
  </div>
</div>
</body>
</html>
"""


def _reminder_body(reading_type: str = "tarot", custom_message: str = "") -> str:
    msgs = {
        "tarot": "The cards are waiting to share their ancient wisdom with you. Your tarot reading today could unlock insights about relationships, career, and your soul's journey.",
        "palm": "Your palm holds the map of your destiny. A palm reading analysis today can reveal hidden talents, life patterns, and growth opportunities.",
        "combined": "A combined palm & tarot session offers the deepest insights. The stars align for your reading today.",
    }
    msg = custom_message or msgs.get(reading_type, msgs["tarot"])
    return f"""
<p>The cosmos has a message for you today. Your spiritual practice awaits! 🌙</p>
<div class="highlight"><p>{msg}</p></div>
<p>Regular readings help you stay aligned with your highest self and navigate life's transitions with clarity and confidence.</p>
<div style="text-align:center;margin:28px 0;">
  <a href="http://localhost:3000/tarot-reading" class="btn">🔮 Start Your Reading</a>
  &nbsp;
  <a href="http://localhost:3000/palm-reading" class="btn" style="background:linear-gradient(90deg,#059669,#0d9488);">🤚 Palm Analysis</a>
</div>
<p style="font-size:13px;color:#9ca3af;">Tip: The best readings happen when you are calm and focused. Take 3 deep breaths before you begin.</p>
"""


def _daily_guidance_body(affirmation: str = "", crystal: str = "") -> str:
    aff = affirmation or "I am aligned with the universe. My path is guided by wisdom and love."
    cry = crystal or "Amethyst — for spiritual clarity and intuition"
    return f"""
<p>Every day is a new chapter in your spiritual journey. Here is your personalized guidance for today:</p>
<div class="highlight"><p>✨ Today's Affirmation: <strong>"{aff}"</strong></p></div>
<div class="section">
  <div class="section-title">🔮 Today's Crystal Ally</div>
  <div class="rec-item"><strong>{cry}</strong><p>Keep it close or meditate with it for best results today.</p></div>
</div>
<div class="section">
  <div class="section-title">🌙 Daily Practice</div>
  <div class="rec-item"><strong>3-Minute Morning Intention</strong><p>Sit quietly, hold your crystal if available, and state your affirmation 3 times with intention.</p></div>
  <div class="rec-item"><strong>Evening Reflection</strong><p>Before sleep, journal 3 things you are grateful for and one insight from today.</p></div>
</div>
<div style="text-align:center;margin:28px 0;">
  <a href="http://localhost:3000/ai-insights" class="btn">🧠 View AI Insights</a>
</div>
"""


def _monthly_report_body(stats: dict) -> str:
    readings = stats.get("total_readings", 0)
    streak = stats.get("streak_days", 0)
    top_insight = stats.get("top_insight", "Your spiritual journey is progressing beautifully")
    month = stats.get("month", datetime.now().strftime("%B %Y"))
    growth = stats.get("growth_score", 78)
    dominant = stats.get("dominant_element", "Fire")

    return f"""
<p>Your <strong>{month}</strong> spiritual journey report is ready! Here's a reflection of your growth, insights, and cosmic alignment this month.</p>

<div class="stat-row">
  <div class="stat"><div class="val">{readings}</div><div class="lbl">Total Readings</div></div>
  <div class="stat"><div class="val">{streak}</div><div class="lbl">Day Streak</div></div>
  <div class="stat"><div class="val">{growth}%</div><div class="lbl">Growth Score</div></div>
  <div class="stat"><div class="val">{dominant}</div><div class="lbl">Dominant Element</div></div>
</div>

<div class="highlight"><p>✨ Top Insight: {top_insight}</p></div>

<div class="section">
  <div class="section-title">📊 Monthly Summary</div>
  <div class="rec-item"><strong>Spiritual Growth</strong><p>You've shown consistent dedication to your practice this month. Your energy patterns suggest you are entering a phase of expansion.</p></div>
  <div class="rec-item"><strong>Key Theme</strong><p>The {dominant} element dominated your readings, pointing towards themes of {'transformation and courage' if dominant == 'Fire' else 'emotional depth and intuition' if dominant == 'Water' else 'intellectual growth and communication' if dominant == 'Air' else 'stability and manifestation'}.</p></div>
  <div class="rec-item"><strong>Next Month Focus</strong><p>The cosmic calendar suggests focusing on self-compassion and grounding practices as you integrate this month's lessons.</p></div>
</div>

<div style="text-align:center;margin:28px 0;">
  <a href="http://localhost:3000/reports" class="btn">📋 View Full Report</a>
  &nbsp;
  <a href="http://localhost:3000/ai-insights" class="btn" style="background:linear-gradient(90deg,#059669,#0d9488);">🧠 AI Insights</a>
</div>
<p style="font-size:13px;color:#9ca3af;">This report was automatically generated based on your activity and AI analysis on the MysticAI platform.</p>
"""


# ============================================================================
# Core Email Sender
# ============================================================================

def _send_smtp(to_email: str, subject: str, html_body: str, plain_body: str = "") -> bool:
    """Send email via Gmail SMTP. Returns True on success."""
    gmail_user = getattr(settings, "GMAIL_USER", "") or ""
    gmail_pass = getattr(settings, "GMAIL_APP_PASSWORD", "") or ""

    if not gmail_user or not gmail_pass:
        logger.warning(f"Email skipped (GMAIL_USER/GMAIL_APP_PASSWORD not configured). Would send: {subject} → {to_email}")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"MysticAI ✨ <{gmail_user}>"
        msg["To"] = to_email

        if plain_body:
            msg.attach(MIMEText(plain_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, to_email, msg.as_string())

        logger.info(f"Email sent: {subject} → {to_email}")
        return True
    except Exception as e:
        logger.error(f"Email send failed for {to_email}: {e}")
        return False


async def send_email_async(to_email: str, subject: str, html_body: str, plain_body: str = "") -> bool:
    """Async wrapper around SMTP sender."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _send_smtp, to_email, subject, html_body, plain_body)


# ============================================================================
# Public Email API
# ============================================================================

async def send_welcome_email(to_email: str, user_name: str = "Seeker") -> bool:
    body_html = f"""
<p>Welcome to <strong>MysticAI</strong> — your personal AI-powered spiritual intelligence platform! 🌙</p>
<div class="highlight"><p>"The stars don't control your destiny — they illuminate the path. You choose the journey."</p></div>
<div class="section">
  <div class="section-title">🚀 Get Started</div>
  <div class="rec-item"><strong>🤚 Palm Reading</strong><p>Upload a clear photo of your palm for AI-powered feature detection and personality analysis.</p></div>
  <div class="rec-item"><strong>🔮 Tarot Reading</strong><p>Draw cards and receive AI interpretations combining traditional symbolism with your unique energy profile.</p></div>
  <div class="rec-item"><strong>🧠 AI Insights</strong><p>Explore your personality intelligence report, life trend analysis, and personalized recommendations.</p></div>
</div>
<div style="text-align:center;margin:28px 0;">
  <a href="http://localhost:3000/dashboard" class="btn">🌟 Go to Your Dashboard</a>
</div>
"""
    html = _build_html("Welcome to MysticAI", body_html, user_name)
    return await send_email_async(to_email, "✨ Welcome to MysticAI — Your Spiritual Journey Begins", html)


async def send_reading_reminder(to_email: str, user_name: str = "Seeker",
                                 reading_type: str = "tarot", custom_message: str = "") -> bool:
    body_html = _reminder_body(reading_type, custom_message)
    html = _build_html("Reading Reminder", body_html, user_name)
    icons = {"tarot": "🔮", "palm": "🤚", "combined": "✨"}
    icon = icons.get(reading_type, "✨")
    subj = f"{icon} Your {reading_type.title()} Reading Awaits — MysticAI"
    return await send_email_async(to_email, subj, html)


async def send_daily_guidance(to_email: str, user_name: str = "Seeker",
                               affirmation: str = "", crystal: str = "") -> bool:
    body_html = _daily_guidance_body(affirmation, crystal)
    html = _build_html("Daily Spiritual Guidance", body_html, user_name)
    today = datetime.now().strftime("%A, %B %d")
    return await send_email_async(to_email, f"🌙 Your Daily Spiritual Guidance — {today}", html)


async def send_monthly_report(to_email: str, user_name: str = "Seeker", stats: Optional[dict] = None) -> bool:
    body_html = _monthly_report_body(stats or {})
    month = datetime.now().strftime("%B %Y")
    html = _build_html(f"Monthly Spiritual Report — {month}", body_html, user_name)
    return await send_email_async(to_email, f"📊 Your {month} Spiritual Journey Report — MysticAI", html)
