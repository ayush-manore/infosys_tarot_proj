# 🔮 Palmistry & Tarot Intelligence Platform (MysticAI)

> **Milestone 1 — Week 1 Completed**: Project Initialization, System Architecture, Database Schema, Core Auth, User Profile Management, UI Wireframes, and Comprehensive Learning Documentation.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.11+**
- **Node.js 18+** & npm
- **Docker & Docker Compose** (Optional, for database containers)

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

# Copy environment settings
cp .env.example .env

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

## 📂 Project Structure

```
palmistry-tarot-platform/
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
│   │   ├── routers/              # API Route Handlers (auth, users, profiles)
│   │   ├── services/             # Business Logic Layer
│   │   └── utils/                # JWT Security & Dependencies
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/                     # Next.js Frontend
│   ├── src/
│   │   ├── app/                  # App Router Pages (Landing, Auth, Dashboard, Profile)
│   │   └── globals.css           # Tailwind & Glassmorphism styles
│   ├── tailwind.config.js
│   └── package.json
├── docker-compose.yml            # Containerization configuration
└── README.md
```

---

## 🎯 Week 1 Accomplishments

- [x] Defined system architecture and microservices layout
- [x] Designed dual database strategy (PostgreSQL for relational, MongoDB for unstructured AI outputs)
- [x] Created full documentation suite (Architecture, Schemas, API Reference, Workflows)
- [x] Wrote internship **Learning Guide** explaining FastAPI, JWT, RBAC, ORM, React & Docker
- [x] Built FastAPI backend with JWT Auth, Role-Based Access Control (4 roles), and User Profile CRUD
- [x] Built Next.js frontend with cosmic dark theme, glassmorphism UI, and auth screens
- [x] Generated high-fidelity UI wireframes for 5 core screens
- [x] Configured Docker Compose environment
