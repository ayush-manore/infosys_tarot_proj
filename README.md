# 🔮 MysticAI — Palmistry & Tarot Intelligence Platform

> **Full-stack AI-powered spiritual intelligence platform** with palm analysis, tarot reading, **interactive card draw**, **Gemini AI chatbot**, personality profiling, life trend analysis, recommendation engine, notifications, reports, analytics, and comprehensive testing.
>
> **Tech Stack:** FastAPI · Next.js 14 · SQLite/PostgreSQL · MongoDB · Redis · TailwindCSS · Google Gemini AI · Docker

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🃏 **Interactive Card Draw** | Shuffle a visual deck and pick cards one-by-one with 3D flip animations — just like real life |
| 🤖 **MysticAI Chatbot** | Gemini-powered conversational AI for tarot guidance, palm insights, and spiritual advice |
| 🔮 **Tarot Engine** | 6 spread types, 78-card deck, position-specific interpretations, elemental balance |
| 🤚 **Palm Analysis** | CV-based palm line detection with personality trait mapping |
| 🧠 **AI Interpretation** | Deep narrative synthesis across personality, career, health, and relationships |
| 📊 **Analytics Dashboard** | Reading history, life trends, confidence scoring, and exportable reports |
| 🔐 **RBAC System** | 4 roles (Seeker, Tarot Reader, Consultant, Admin) with granular permissions |
| 📈 **Life Trend Analysis** | Pattern detection across reading history with opportunity forecasting |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.11+**
- **Node.js 18+** & npm
- **Docker & Docker Compose** (Optional, for database containers)
- **Google Gemini API Key** — [Get one free here](https://aistudio.google.com/apikey)

---

### 2. Backend Setup (FastAPI + Python)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment settings and add your Gemini API key
cp .env.example .env
# Edit .env and set: GEMINI_API_KEY=your-actual-key

# Run FastAPI dev server
uvicorn app.main:app --reload --port 8000
```

The API will be live at:
- **API Base**: `http://localhost:8000/api/v1`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc API Reference**: `http://localhost:8000/redoc`

---

### 3. Frontend Setup (Next.js + React + TailwindCSS)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run Next.js development server
npm run dev
```

The Web Application will be live at `http://localhost:3000`.

---

### 4. Docker Environment (PostgreSQL + MongoDB + Redis)

Spin up all databases and services in one command:

```bash
docker-compose up -d
```

Services exposed:
- **PostgreSQL**: `localhost:5432`
- **MongoDB**: `localhost:27017`
- **Redis**: `localhost:6379`
- **FastAPI**: `localhost:8000`

---

## 🤖 Gemini AI Chatbot Setup

1. Visit [Google AI Studio](https://aistudio.google.com/apikey) and create a free API key
2. Add it to `backend/.env`:
   ```
   GEMINI_API_KEY=your-actual-gemini-api-key
   GEMINI_MODEL=gemini-2.0-flash
   ```
3. Restart the backend server
4. Navigate to `/chat` in the frontend to start chatting with MysticAI

> **Note:** The chatbot works in offline/fallback mode even without an API key — it provides template-based spiritual guidance responses.

---

## 📂 Project Structure

```
mysticai-platform/
├── docs/                          # Complete Documentation Suite
│   ├── ARCHITECTURE.md            # System Architecture & Microservices
│   ├── DATABASE_SCHEMA.md         # PostgreSQL ERD & MongoDB Schemas
│   ├── API_REFERENCE.md           # API Endpoints & Request/Response shapes
│   ├── LEARNING_GUIDE.md          # Comprehensive Internship Learning Manual
│   └── WORKFLOW_DIAGRAMS.md       # Mermaid Diagrams for User Flows
├── backend/                       # FastAPI Backend
│   ├── app/
│   │   ├── main.py               # FastAPI App entrypoint & CORS
│   │   ├── config.py             # Pydantic Settings
│   │   ├── database.py           # PostgreSQL, MongoDB & Redis connections
│   │   ├── models/               # SQLAlchemy Models (User, Role, Profile, Reading)
│   │   ├── schemas/              # Pydantic Request/Response Schemas
│   │   ├── routers/              # API Route Handlers (auth, users, profiles, ai)
│   │   ├── services/             # Business Logic (tarot, palm, gemini, analytics)
│   │   │   ├── gemini_service.py # Gemini AI integration (chatbot, interpretation)
│   │   │   ├── tarot_service.py  # 78-card deck, shuffling, spreads
│   │   │   └── ...               # 15+ service modules
│   │   └── utils/                # JWT Security & Dependencies
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/                     # Next.js Frontend
│   ├── src/app/
│   │   ├── page.js              # Landing page
│   │   ├── draw-cards/page.js   # ⭐ Interactive card draw (NEW)
│   │   ├── chat/page.js         # ⭐ AI Chatbot page (NEW)
│   │   ├── tarot-reading/       # Standard tarot reading
│   │   ├── palm-reading/        # Palm analysis
│   │   ├── dashboard/           # Role-based dashboards (4 roles)
│   │   ├── auth/                # Login & Register
│   │   ├── profile/             # User profile management
│   │   ├── reports/             # Reading reports
│   │   ├── notifications/       # Notification center
│   │   └── datasets/            # Mystic knowledge base
│   ├── tailwind.config.js
│   ├── next.config.js
│   └── package.json
├── docker-compose.yml            # Containerization configuration
└── README.md
```

---

## 🎯 All Milestones Completed

- [x] System architecture and microservices layout
- [x] Dual database strategy (PostgreSQL + MongoDB)
- [x] Complete documentation suite (Architecture, Schemas, API Reference, Workflows)
- [x] FastAPI backend with JWT Auth, RBAC (4 roles), User Profile CRUD
- [x] Next.js frontend with cosmic dark theme, glassmorphism UI
- [x] 78-card tarot deck with 6 spread types and position-specific interpretations
- [x] Palm analysis engine with 5 palm lines and personality trait mapping
- [x] AI interpretation engine with Gemini integration
- [x] **Interactive card draw** — shuffle, fan, pick, and flip cards with 3D animations
- [x] **AI Chatbot** — Gemini-powered conversational spiritual guide
- [x] Personality profiling (Big Five mapping, spiritual archetypes)
- [x] Life trend analysis and opportunity forecasting
- [x] Recommendation engine with personalized growth practices
- [x] Notification system and reading history
- [x] Analytics dashboard with exportable reports
- [x] Docker Compose environment
- [x] Comprehensive test suite

---

## 🌐 Deployment

### Frontend (Vercel)
1. Push the repo to GitHub
2. Go to [vercel.com](https://vercel.com) → Import your GitHub repo
3. Set Root Directory to `frontend`
4. Add environment variable: `NEXT_PUBLIC_API_BASE=https://your-backend-url/api/v1`
5. Deploy!

### Backend (Railway / Render / Fly.io)
1. Push the repo to GitHub
2. Connect to [Railway](https://railway.app) or [Render](https://render.com)
3. Set Root Directory to `backend`
4. Add environment variables from `.env.example`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 📜 License

This project was built as part of the Infosys Springboard Internship Program.

---

<p align="center">
  Built with ❤️ using FastAPI, Next.js, TailwindCSS & Google Gemini AI
</p>
