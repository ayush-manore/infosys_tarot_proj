# AI-Powered Palmistry & Tarot Intelligence Platform — Final Project Report

---

## 1. Executive Summary

The **Palmistry & Tarot Intelligence Platform** is a full-stack AI-powered spiritual intelligence application that analyzes palm images and tarot card selections to generate personalized spiritual insights. The platform combines computer vision simulation, AI interpretation models, symbolic analysis, tarot reading workflows, and interactive guidance systems to create engaging and customized spiritual experiences.

**Key Achievements:**
- ✅ Secure authentication with JWT and role-based access control (4 roles)
- ✅ Palm image analysis with simulated CV pipeline (5 palm lines, hand shape classification)
- ✅ Tarot reading engine with 78-card deck, 6 spread types, and position interpretations
- ✅ AI interpretation engine with 7-category insight generation
- ✅ Big Five personality profiling from palm + tarot data
- ✅ Life trend analysis with opportunity/challenge forecasting
- ✅ 5-factor weighted scoring model for insight confidence
- ✅ Personalized recommendation engine (growth, career, relationships, spiritual)
- ✅ Notification & engagement system
- ✅ Report generation & export (CSV/JSON)
- ✅ Platform analytics with engagement metrics
- ✅ Comprehensive test suite (50+ test cases)

---

## 2. Project Objectives

| Objective | Status |
|---|---|
| Build AI-powered spiritual intelligence platform | ✅ Complete |
| Implement secure authentication and RBAC | ✅ Complete |
| Build palm image analysis and feature detection | ✅ Complete (Simulated CV) |
| Develop tarot reading and card interpretation systems | ✅ Complete |
| Implement AI interpretation engine | ✅ Complete |
| Build personality profiling system | ✅ Complete |
| Implement life trend analysis | ✅ Complete |
| Build recommendation engine | ✅ Complete |
| Implement scoring and confidence model | ✅ Complete |
| Build notification system | ✅ Complete |
| Implement reports and export | ✅ Complete |
| Build analytics dashboard | ✅ Complete |
| Comprehensive testing | ✅ Complete |
| Documentation | ✅ Complete |

---

## 3. Technology Stack

### Backend
| Technology | Purpose | Version |
|---|---|---|
| **FastAPI** | REST API Framework | 0.104+ |
| **SQLAlchemy** (Async) | ORM for PostgreSQL/SQLite | 2.0+ |
| **Motor** | Async MongoDB Driver | 3.3+ |
| **Redis** (aioredis) | Caching, Rate Limiting, Token Blacklist | 4.0+ |
| **Pydantic** | Data Validation & Schemas | 2.0+ |
| **bcrypt** | Password Hashing | 4.0+ |
| **PyJWT** | JSON Web Token Auth | 2.8+ |
| **Uvicorn** | ASGI Server | 0.24+ |

### Frontend
| Technology | Purpose | Version |
|---|---|---|
| **Next.js** | React Framework (App Router) | 14+ |
| **TailwindCSS** | Utility-first CSS | 3.0+ |
| **Lucide React** | Icon Library | Latest |

### Infrastructure
| Technology | Purpose |
|---|---|
| **PostgreSQL 16** | Primary Relational Database |
| **MongoDB 7.0** | Document Store for AI Readings |
| **Redis 7** | Session Store & Cache |
| **Docker Compose** | Container Orchestration |

---

## 4. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js 14)                     │
│  ┌──────────┬──────────┬──────────┬──────────┬────────────────┐  │
│  │ Landing  │ Auth     │Dashboard │Readings  │ Reports/Notif  │  │
│  │ Page     │ Pages    │(4 Roles) │Palm/Tarot│ Analytics      │  │
│  └──────────┴──────────┴──────────┴──────────┴────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST API
┌────────────────────────────▼────────────────────────────────────┐
│                    FASTAPI BACKEND                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    API Routers                            │   │
│  │  Auth │ Users │ Profiles │ Readings │ Datasets            │   │
│  │  Analytics │ Reports │ Notifications                      │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│  ┌──────────────────────▼───────────────────────────────────┐   │
│  │                  Service Layer                            │   │
│  │  PalmService          │ InterpretationService             │   │
│  │  TarotService         │ PersonalityService                │   │
│  │  ReadingService       │ TrendService                      │   │
│  │  ScoringService       │ RecommendationService             │   │
│  │  NotificationService  │ ReportService                     │   │
│  │  AnalyticsService     │                                   │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│  ┌──────────────────────▼───────────────────────────────────┐   │
│  │                   Data Layer                              │   │
│  │  SQLAlchemy (Users, Roles, Readings, Notifications)       │   │
│  │  Motor (MongoDB: AI Reading Documents)                    │   │
│  │  Redis (Cache, Token Blacklist, Rate Limiting)            │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
    ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
    │PostgreSQL│         │ MongoDB │         │  Redis  │
    │   16     │         │   7.0   │         │    7    │
    └─────────┘         └─────────┘         └─────────┘
```

---

## 5. Module Descriptions

### 5.1 Authentication & Authorization (Milestone 1)
- **JWT-based authentication** with access/refresh tokens
- **4 roles**: User (Seeker), Tarot Reader, Spiritual Consultant, Admin
- **Role-based access control** with granular permissions (12 permission types)
- **Password security**: bcrypt hashing with salt
- **Token blacklisting** via Redis for secure logout
- **Rate limiting** middleware support

### 5.2 Palm Analysis Engine (Milestone 2)
- **Simulated CV pipeline** that models real computer vision workflows
- **Hand shape classification**: Earth, Air, Water, Fire — mapped to personality elements
- **5 palm lines detected**: Heart, Head, Life, Fate, Sun
- **Line measurements**: depth, clarity, length, curvature, characteristics
- **Personality trait extraction**: 6 traits scored 0-100%
- **Deterministic seeding** for reproducible results per user
- **Drop-in replacement ready** for OpenCV/MediaPipe integration

### 5.3 Tarot Reading Engine (Milestone 2)
- **78-card deck** loaded from comprehensive JSON dataset
- **6 spread types**: Single Card, Three Card, Celtic Cross, Relationship, Career, Horseshoe
- **Card orientation**: 30% reversed polarity simulation
- **Position-aware interpretation**: contextual meaning based on spread position
- **Elemental balance calculation**: Fire, Water, Air, Earth percentages
- **Theme extraction**: automated theme identification from card combinations
- **Narrative synthesis**: AI-generated reading narratives

### 5.4 AI Interpretation Engine (Milestone 3)
- **7-category insight generation**: Personality, Relationships, Career, Finance, Health & Wellness, Personal Growth, Life Opportunities
- **Palm interpretation synthesis**: combining line data + hand shape into themed narratives
- **Tarot interpretation synthesis**: cross-card pattern detection, elemental harmony
- **Combined reading synthesis**: weighted scoring from both sources
- **5-factor weighted scoring model**:
  - Palm Analysis Confidence: 30%
  - Tarot Interpretation Relevance: 25%
  - Personality Alignment: 20%
  - User Context Relevance: 15%
  - Reading Consistency: 10%

### 5.5 Personality Intelligence Module (Milestone 3)
- **Big Five personality mapping**: Openness, Conscientiousness, Extraversion, Agreeableness, Emotional Sensitivity
- **Element-aware scoring**: personality scores modified by hand element affinity
- **Personality archetype determination**: 10+ unique archetypes
- **Strength/weakness identification** with actionable advice
- **Behavioral pattern analysis**: Decision Making, Stress Response, Communication Style, Learning Style
- **Development recommendations**: personalized growth plans

### 5.6 Life Trend Analysis Engine (Milestone 3)
- **5 trend categories**: Emotional, Professional, Spiritual, Vitality, Creativity
- **Trend direction detection**: ascending, stable, transitioning, resting
- **Opportunity identification**: Career Pivot, Relationship Deepening, Creative Breakthrough, Self-Discovery, Leadership
- **Challenge forecasting**: Emotional Turbulence, Career Uncertainty, Energy Depletion, Creative Block
- **Growth potential assessment**: Expansion, Cultivation, Preparation, Gestation phases
- **Historical trend comparison** from reading history

### 5.7 Recommendation Engine (Milestone 3)
- **Personal growth recommendations** based on trait scores
- **Relationship guidance** from emotional intelligence data
- **Career suggestions** from career drive + analytical thinking scores
- **Goal-aligned recommendations** matched to user profile goals
- **Spiritual development insights** with practice suggestions
- **Daily recommendation** generation with date-based rotation

### 5.8 Scoring Engine (Milestone 3)
- **5-factor weighted insight score** with letter grade output (A+ through D)
- **Self-development score**: trait balance, strength leverage, growth awareness, action readiness, engagement
- **Guidance relevance scoring**: goal alignment, priority distribution, coverage
- **Quality tier classification**: Exceptional, Strong, Good, Moderate, Developing

### 5.9 Notification System (Milestone 4)
- **Daily spiritual guidance** with rotating messages
- **Reading reminders** for engagement
- **Growth alerts** for progress tracking
- **Platform announcements** for admin communications
- **Read/unread tracking** with dismiss functionality
- **Priority system**: Low, Normal, High, Urgent

### 5.10 Reports & Export (Milestone 4)
- **4 report types**: Palmistry, Tarot, Personality, Spiritual Guidance (combined)
- **Section-based reports** with narratives and structured data
- **CSV export** for data analysis
- **JSON export** for programmatic consumption
- **Report summaries** for quick overview

### 5.11 Analytics Dashboard (Milestone 4)
- **User analytics**: reading counts, type distribution, confidence metrics, activity timeline
- **Platform analytics** (admin): total users, retention rate, daily readings, system health
- **Engagement metrics**: reading streak, feedback score, notification engagement, engagement level
- **Charts-ready data**: confidence timeline, weekly trends, rating distribution

---

## 6. Database Schema

### Relational (PostgreSQL/SQLite)

| Table | Key Fields | Purpose |
|---|---|---|
| `roles` | id, name, permissions (JSON) | RBAC role definitions |
| `users` | id, email, hashed_password, role_id, is_active | User accounts |
| `user_profiles` | id, user_id, full_name, spiritual_goals, interests | User preferences |
| `reading_sessions` | id, user_id, reading_type, spread_type, status, confidence_score | Reading records |
| `notifications` | id, user_id, type, title, message, priority, is_read | User notifications |

### Document Store (MongoDB)
- `palm_analyses`: Raw palm analysis results with line measurements
- `tarot_readings`: Card spreads, interpretations, and narratives
- `combined_readings`: Synthesized insights from both sources

---

## 7. API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | User registration |
| POST | `/api/v1/auth/login` | User login |
| POST | `/api/v1/auth/logout` | Token blacklist |
| POST | `/api/v1/auth/refresh` | Refresh access token |

### Readings
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/readings/palm` | Create palm reading |
| POST | `/api/v1/readings/tarot` | Create tarot reading |
| POST | `/api/v1/readings/combined` | Create combined reading |
| GET | `/api/v1/readings/history` | Get reading history |
| GET | `/api/v1/readings/tarot/daily` | Get daily guidance card |

### Analytics & AI
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/analytics/user` | User reading analytics |
| GET | `/api/v1/analytics/personality` | AI personality profile |
| GET | `/api/v1/analytics/interpretation` | Combined interpretation |
| GET | `/api/v1/analytics/trends` | Life trend analysis |
| GET | `/api/v1/analytics/recommendations` | Personalized recommendations |
| GET | `/api/v1/analytics/insight-score` | 5-factor insight score |
| GET | `/api/v1/analytics/engagement` | Engagement metrics |
| GET | `/api/v1/analytics/platform` | Platform analytics (admin) |

### Reports
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/reports/palm` | Generate palm report |
| GET | `/api/v1/reports/tarot` | Generate tarot report |
| GET | `/api/v1/reports/personality` | Generate personality report |
| GET | `/api/v1/reports/spiritual-guidance` | Full spiritual guidance report |
| GET | `/api/v1/reports/export/csv` | Export report as CSV |
| GET | `/api/v1/reports/export/json` | Export report as JSON |

### Notifications
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/notifications` | List notifications |
| POST | `/api/v1/notifications/daily-guidance` | Generate daily guidance |
| PUT | `/api/v1/notifications/{id}/read` | Mark as read |
| PUT | `/api/v1/notifications/mark-all-read` | Mark all read |
| DELETE | `/api/v1/notifications/{id}` | Dismiss notification |

---

## 8. Frontend Pages

| Page | Route | Description |
|---|---|---|
| Landing Page | `/` | Marketing page with feature showcase |
| Login | `/auth/login` | JWT login with role-aware redirect |
| Register | `/auth/register` | User registration |
| Dashboard | `/dashboard` | Role-based dashboard (4 views) |
| Palm Reading | `/palm-reading` | Palm image upload & analysis |
| Tarot Reading | `/tarot-reading` | Spread selection & card reveal |
| Profile | `/profile` | User profile & spiritual goals |
| Datasets | `/datasets` | Knowledge base (78 cards, 7 lines) |
| Reports | `/reports` | Report generation & export |
| Notifications | `/notifications` | Notification center |

---

## 9. Testing Summary

| Test File | Tests | Coverage Area |
|---|---|---|
| `test_services.py` | 38 | All 8 service modules |
| `test_auth.py` | 6 | Password hashing, JWT, schema validation |
| `test_readings.py` | 12 | All spread types, card uniqueness, elemental balance |
| **Total** | **56** | **Full service layer + auth + readings** |

**Running tests:**
```bash
cd backend
pip install pytest
pytest tests/ -v
```

---

## 10. How to Run

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional, for databases)

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### With Docker (full stack databases)
```bash
docker-compose up -d   # Starts PostgreSQL, MongoDB, Redis
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev
```

The backend automatically falls back to **SQLite** if PostgreSQL is unavailable, and provides **simulated** MongoDB/Redis if those services are not running.

---

## 11. Project Structure

```
infosys_tarot_proj/
├── backend/
│   ├── app/
│   │   ├── config.py              # Environment configuration
│   │   ├── database.py            # Database connections (Postgres/SQLite, MongoDB, Redis)
│   │   ├── main.py                # FastAPI application entry point
│   │   ├── data/                  # Reference datasets
│   │   │   ├── tarot_cards.json        # 78 tarot card definitions
│   │   │   ├── palmistry_lines.json    # Palm line reference data
│   │   │   └── dataset_catalog.json    # Dataset catalog metadata
│   │   ├── models/                # SQLAlchemy ORM models
│   │   │   ├── user.py, role.py, profile.py, reading.py, notification.py
│   │   ├── schemas/               # Pydantic validation schemas
│   │   │   ├── auth.py, user.py, reading.py, notification.py
│   │   ├── routers/               # API endpoint routers
│   │   │   ├── auth.py, users.py, profiles.py, datasets.py
│   │   │   ├── readings.py, analytics.py, reports.py, notifications.py
│   │   ├── services/              # Business logic services
│   │   │   ├── palm_service.py         # Palm analysis (Simulated CV)
│   │   │   ├── tarot_service.py        # Tarot reading engine
│   │   │   ├── reading_service.py      # Reading session orchestrator
│   │   │   ├── interpretation_service.py  # AI interpretation engine
│   │   │   ├── personality_service.py  # Big Five personality profiling
│   │   │   ├── trend_service.py        # Life trend analysis
│   │   │   ├── recommendation_service.py # Growth recommendations
│   │   │   ├── scoring_service.py      # 5-factor scoring model
│   │   │   ├── notification_service.py # Notification management
│   │   │   ├── report_service.py       # Report generation & export
│   │   │   └── analytics_service.py    # Analytics & metrics
│   │   └── utils/                 # Utilities
│   │       ├── security.py             # Password hashing, JWT
│   │       └── dependencies.py         # Auth dependencies
│   ├── tests/                     # Test suite
│   │   ├── conftest.py, test_services.py, test_auth.py, test_readings.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/app/                   # Next.js App Router pages
│   │   ├── page.js                     # Landing page
│   │   ├── auth/login/page.js          # Login page
│   │   ├── auth/register/page.js       # Registration page
│   │   ├── dashboard/page.js           # Role-based dashboard
│   │   ├── palm-reading/page.js        # Palm reading interface
│   │   ├── tarot-reading/page.js       # Tarot reading interface
│   │   ├── profile/page.js             # User profile
│   │   ├── datasets/page.js            # Knowledge base
│   │   ├── reports/page.js             # Reports & export
│   │   └── notifications/page.js       # Notification center
│   ├── tailwind.config.js
│   └── package.json
├── docker-compose.yml             # PostgreSQL, MongoDB, Redis
├── docs/                          # Project documentation
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── DATABASE_SCHEMA.md
│   ├── WORKFLOW_DIAGRAMS.md
│   └── PROJECT_REPORT.md          # This document
└── README.md
```

---

## 12. Key Design Decisions

1. **Simulated CV Pipeline**: Palm analysis uses deterministic simulation with seeded RNG rather than real OpenCV/MediaPipe, enabling full functionality without GPU dependencies. Architecture supports drop-in replacement.

2. **Hybrid Database Strategy**: PostgreSQL for relational data (users, sessions), MongoDB for flexible AI reading documents, Redis for caching and token management. SQLite fallback ensures the app runs without Docker.

3. **5-Factor Weighted Scoring**: Insight quality is objectively measured using a composite model combining palm confidence, tarot relevance, personality alignment, user context, and reading consistency.

4. **Role-Based Dashboard Architecture**: Single dashboard page with 4 role-specific views (User, Tarot Reader, Consultant, Admin) with real-time persona switching via backend authentication.

5. **Service-Oriented Architecture**: All business logic is encapsulated in 11 independent service modules, enabling easy testing, replacement, and scaling.

---

## 13. Future Enhancements

- **Real CV Integration**: Replace simulated palm analysis with OpenCV + MediaPipe hand landmark detection
- **LLM Integration**: Connect interpretation engine to OpenAI/Gemini for dynamic narrative generation
- **Mobile App**: React Native or Flutter client
- **Real-time Features**: WebSocket-based live reading sessions
- **Social Features**: Reading sharing, community forums
- **Advanced Analytics**: Machine learning-based user behavior prediction

---

## 14. Conclusion

The Palmistry & Tarot Intelligence Platform successfully delivers a comprehensive, production-ready spiritual intelligence system. All 4 milestones have been completed with 11 backend services, 8 API routers, 10 frontend pages, and 56 automated tests. The architecture is designed for extensibility, with clear separation between simulated and production AI components.

---

*Report generated for Infosys Springboard Project Submission*
*Platform: AI-Powered Palmistry & Tarot Intelligence Platform*
*Author: Ayush Manore*
