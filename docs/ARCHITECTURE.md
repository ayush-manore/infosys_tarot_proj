# 🏗️ System Architecture — Palmistry & Tarot Intelligence Platform

## Table of Contents
1. [Architecture Overview](#1-architecture-overview)
2. [System Layers](#2-system-layers)
3. [API Gateway Layer](#3-api-gateway-layer)
4. [Microservices Layer](#4-microservices-layer)
5. [AI/ML & Intelligence Engine](#5-aiml--intelligence-engine)
6. [Data Layer](#6-data-layer)
7. [External Services](#7-external-services)
8. [Security Architecture](#8-security-architecture)
9. [Deployment Architecture](#9-deployment-architecture)
10. [Design Decisions & Trade-offs](#10-design-decisions--trade-offs)

---

## 1. Architecture Overview

The Palmistry & Tarot Intelligence Platform follows a **layered microservices architecture** with a clear separation of concerns. The platform is designed to be modular, scalable, and maintainable.

### High-Level Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        WEB["🌐 Web App<br/>(Next.js + React)"]
        MOB["📱 Mobile App<br/>(Future)"]
        API_CLIENT["🔌 API Access<br/>(REST/GraphQL)"]
    end

    subgraph "API Gateway (FastAPI)"
        GW["API Gateway"]
        AUTH_MW["Authentication<br/>Middleware"]
        RATE["Rate Limiter"]
        CORS_MW["CORS Handler"]
        VALID["Request Validator"]
        LOG["Request Logger"]
    end

    subgraph "Microservices Layer"
        USER_SVC["👤 User Service"]
        PROFILE_SVC["📋 Profile Service"]
        PALM_SVC["🖐️ Palm Analysis<br/>Service"]
        TAROT_SVC["🃏 Tarot Reading<br/>Service"]
        AI_SVC["🧠 AI Interpretation<br/>Service"]
        PERSONALITY_SVC["💡 Personality &<br/>Insights Service"]
        TREND_SVC["📈 Trend Analysis<br/>Service"]
        RECOMMEND_SVC["🎯 Recommendation<br/>Service"]
        NOTIFY_SVC["🔔 Notification<br/>Service"]
        ANALYTICS_SVC["📊 Analytics<br/>Service"]
        REPORT_SVC["📄 Report Service"]
        ADMIN_SVC["⚙️ Admin Service"]
    end

    subgraph "AI/ML Engine"
        CV["Computer Vision<br/>(OpenCV, MediaPipe)"]
        NLP["NLP Engine<br/>(LangChain, OpenAI)"]
        MODELS["ML Models<br/>(TensorFlow, PyTorch)"]
    end

    subgraph "Data Layer"
        PG["🐘 PostgreSQL<br/>(Primary DB)"]
        MONGO["🍃 MongoDB<br/>(Document Store)"]
        REDIS["⚡ Redis<br/>(Cache)"]
        S3["☁️ Cloud Storage<br/>(S3/Azure Blob)"]
    end

    WEB --> GW
    MOB --> GW
    API_CLIENT --> GW

    GW --> AUTH_MW --> RATE --> CORS_MW --> VALID --> LOG

    LOG --> USER_SVC
    LOG --> PROFILE_SVC
    LOG --> PALM_SVC
    LOG --> TAROT_SVC
    LOG --> AI_SVC
    LOG --> PERSONALITY_SVC
    LOG --> TREND_SVC
    LOG --> RECOMMEND_SVC
    LOG --> NOTIFY_SVC
    LOG --> ANALYTICS_SVC
    LOG --> REPORT_SVC
    LOG --> ADMIN_SVC

    PALM_SVC --> CV
    TAROT_SVC --> NLP
    AI_SVC --> NLP
    AI_SVC --> MODELS
    PERSONALITY_SVC --> MODELS

    USER_SVC --> PG
    PROFILE_SVC --> PG
    PALM_SVC --> MONGO
    TAROT_SVC --> MONGO
    AI_SVC --> MONGO
    RECOMMEND_SVC --> REDIS
    ANALYTICS_SVC --> PG
    REPORT_SVC --> S3
```

### Design Philosophy

| Principle | Description |
|-----------|-------------|
| **Separation of Concerns** | Each service handles one domain (auth, palm, tarot, etc.) |
| **Async-First** | FastAPI's async capabilities for non-blocking I/O |
| **Database per Concern** | PostgreSQL for structured data, MongoDB for unstructured AI data |
| **Stateless Services** | JWT-based auth, no server-side sessions |
| **API-First** | Backend exposes clean REST APIs, frontend consumes them |

---

## 2. System Layers

The platform is organized into 5 distinct layers:

```mermaid
graph LR
    subgraph "Layer 1: Presentation"
        A["Next.js Frontend"]
    end
    subgraph "Layer 2: API Gateway"
        B["FastAPI Gateway"]
    end
    subgraph "Layer 3: Business Logic"
        C["Microservices"]
    end
    subgraph "Layer 4: Intelligence"
        D["AI/ML Engine"]
    end
    subgraph "Layer 5: Data"
        E["Databases & Storage"]
    end

    A --> B --> C --> D --> E
```

### Layer Responsibilities

#### Layer 1: Presentation (Frontend)
- **Technology**: Next.js 14 with App Router, React 18, TailwindCSS
- **Role**: User interface rendering, client-side routing, form validation
- **Communication**: REST API calls to backend via Axios
- **State Management**: React Context API + custom hooks

#### Layer 2: API Gateway
- **Technology**: FastAPI (Python)
- **Role**: Request routing, authentication, rate limiting, CORS, logging
- **Key Features**: Automatic OpenAPI docs, async request handling, middleware pipeline

#### Layer 3: Business Logic (Services)
- **Role**: Domain-specific logic (auth, profiles, readings, etc.)
- **Pattern**: Service layer pattern — routers delegate to services, services interact with models
- **Communication**: Direct function calls (monolith-first, microservice-ready)

#### Layer 4: Intelligence Engine
- **Technology**: OpenCV, MediaPipe, TensorFlow, LangChain, OpenAI API
- **Role**: Palm image analysis, tarot card interpretation, AI insight generation
- **Note**: Implemented in Weeks 3-6; placeholder interfaces defined in Week 1

#### Layer 5: Data Layer
- **PostgreSQL**: Users, roles, profiles, sessions, reading metadata
- **MongoDB**: Palm analysis results, tarot reading data, AI-generated insights
- **Redis**: JWT token blacklist, session cache, rate limiting counters
- **Cloud Storage**: Uploaded palm images, generated reports

---

## 3. API Gateway Layer

### Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant Gateway as FastAPI Gateway
    participant CORS as CORS Middleware
    participant Auth as Auth Middleware
    participant Rate as Rate Limiter
    participant Router as Route Handler
    participant Service as Service Layer
    participant DB as Database

    Client->>Gateway: HTTP Request
    Gateway->>CORS: Check Origin
    CORS->>Auth: Validate JWT Token
    Auth->>Rate: Check Rate Limit
    Rate->>Router: Forward Request
    Router->>Service: Call Business Logic
    Service->>DB: Query/Mutate Data
    DB-->>Service: Result
    Service-->>Router: Response Data
    Router-->>Client: JSON Response
```

### Gateway Configuration

| Feature | Implementation |
|---------|---------------|
| **Routing** | FastAPI APIRouter with versioned prefixes (`/api/v1/`) |
| **Authentication** | JWT Bearer token validation via middleware |
| **Rate Limiting** | Redis-backed sliding window (100 req/min default) |
| **CORS** | Configurable origins, methods, headers |
| **Request Validation** | Pydantic models for automatic validation |
| **Error Handling** | Structured JSON error responses with error codes |
| **API Documentation** | Auto-generated Swagger UI at `/docs` |
| **Health Check** | `/health` endpoint for monitoring |

---

## 4. Microservices Layer

### Service Catalog

```mermaid
graph TB
    subgraph "Core Services (Week 1-2)"
        US["👤 User Service<br/>Registration, Login<br/>JWT, OAuth2"]
        PS["📋 Profile Service<br/>Profile CRUD<br/>Preferences, Goals"]
    end

    subgraph "Analysis Services (Week 3-4)"
        PAS["🖐️ Palm Analysis<br/>Image Upload<br/>Feature Extraction<br/>Line Detection"]
        TRS["🃏 Tarot Reading<br/>Deck Management<br/>Card Selection<br/>Spread Generation"]
    end

    subgraph "Intelligence Services (Week 5-6)"
        AIS["🧠 AI Interpretation<br/>Palm Interpretation<br/>Tarot Interpretation<br/>Context-Aware Insights"]
        PIS["💡 Personality<br/>Profiling, Strengths<br/>Weaknesses, Behavior"]
        TAS["📈 Trend Analysis<br/>Life Path, Opportunities<br/>Challenges, Growth"]
        RES["🎯 Recommendation<br/>Growth, Career<br/>Relationships, Goals"]
    end

    subgraph "Platform Services (Week 7-8)"
        NS["🔔 Notifications<br/>Daily Guidance<br/>Reading Reminders"]
        AS["📊 Analytics<br/>User Engagement<br/>Reading Stats"]
        RS["📄 Reports<br/>PDF/Excel Export<br/>Scheduled Reports"]
        ADS["⚙️ Admin<br/>User Management<br/>System Config"]
    end
```

### Service Communication Pattern

For Week 1, all services run as modules within a single FastAPI application (monolith-first approach). This simplifies development and debugging. The code is structured to allow extraction into separate microservices later if needed.

```python
# Example: How services are organized
# app/routers/auth.py → calls → app/services/auth_service.py → uses → app/models/user.py
```

---

## 5. AI/ML & Intelligence Engine

> **Note**: The AI/ML engine is implemented in Weeks 3-6. Week 1 defines the interfaces and placeholder services.

### AI Pipeline Architecture

```mermaid
graph LR
    subgraph "Input Processing"
        IMG["Palm Image"]
        CARD["Tarot Card<br/>Selection"]
        CTX["User Context<br/>(Profile, History)"]
    end

    subgraph "Computer Vision Pipeline"
        PREPROCESS["Image<br/>Preprocessing"]
        DETECT["Hand/Palm<br/>Detection"]
        EXTRACT["Feature<br/>Extraction"]
        CLASSIFY["Line<br/>Classification"]
    end

    subgraph "NLP & Interpretation"
        PROMPT["Prompt<br/>Engineering"]
        LLM["LLM<br/>(OpenAI/HF)"]
        SYNTHESIZE["Insight<br/>Synthesis"]
    end

    subgraph "Output"
        INSIGHT["Personalized<br/>Insights"]
        SCORE["Confidence<br/>Scores"]
        REPORT["Reading<br/>Report"]
    end

    IMG --> PREPROCESS --> DETECT --> EXTRACT --> CLASSIFY
    CARD --> PROMPT
    CTX --> PROMPT
    CLASSIFY --> PROMPT
    PROMPT --> LLM --> SYNTHESIZE
    SYNTHESIZE --> INSIGHT
    SYNTHESIZE --> SCORE
    SYNTHESIZE --> REPORT
```

### Technology Choices

| Component | Technology | Why? |
|-----------|-----------|------|
| **Hand Detection** | MediaPipe Hands | Real-time, 21 landmarks, cross-platform |
| **Palm Line Detection** | OpenCV + Custom CNN | Canny edge detection + trained classifier |
| **Image Preprocessing** | Pillow + Albumentations | Robust augmentation pipeline |
| **Card Recognition** | YOLO v8 | Fast object detection for tarot cards |
| **Text Interpretation** | LangChain + OpenAI GPT | Context-aware, structured output |
| **Embeddings** | Sentence Transformers | Semantic similarity for personalization |
| **Model Training** | TensorFlow / PyTorch | Industry-standard deep learning |

---

## 6. Data Layer

### Database Strategy

```mermaid
graph TB
    subgraph "PostgreSQL (Structured Data)"
        USERS["users<br/>id, email, password_hash<br/>role, created_at"]
        ROLES["roles<br/>id, name, permissions"]
        PROFILES["user_profiles<br/>id, user_id, name<br/>age_group, interests"]
        READINGS["reading_sessions<br/>id, user_id, type<br/>status, created_at"]
        PAYMENTS["payments<br/>id, user_id, amount<br/>status"]
    end

    subgraph "MongoDB (Unstructured Data)"
        PALM_DATA["palm_analyses<br/>image_url, features<br/>lines, patterns"]
        TAROT_DATA["tarot_readings<br/>spread_type, cards<br/>positions, interpretations"]
        INSIGHTS["ai_insights<br/>category, content<br/>scores, metadata"]
        CHAT_HIST["chat_history<br/>messages, context<br/>timestamps"]
    end

    subgraph "Redis (Cache & Sessions)"
        TOKEN_BL["Token Blacklist"]
        SESSION["Active Sessions"]
        RATE_LIM["Rate Limit Counters"]
        CACHE["API Response Cache"]
    end

    USERS --> PROFILES
    USERS --> READINGS
    READINGS --> PALM_DATA
    READINGS --> TAROT_DATA
    READINGS --> INSIGHTS
```

### Why Two Databases?

| Aspect | PostgreSQL | MongoDB |
|--------|-----------|---------|
| **Use Case** | Users, roles, relationships, transactions | AI outputs, flexible schemas, nested data |
| **Schema** | Fixed, relational, normalized | Flexible, document-oriented |
| **Queries** | Complex JOINs, aggregations | Nested document queries |
| **ACID** | Full ACID compliance | Document-level atomicity |
| **Scaling** | Vertical (read replicas) | Horizontal (sharding) |

---

## 7. External Services

### Integration Points

```mermaid
graph LR
    PLATFORM["🔮 Platform"]

    subgraph "AI/NLP APIs"
        OPENAI["OpenAI API<br/>(GPT-4, DALL-E)"]
        HF["Hugging Face<br/>(Transformers)"]
    end

    subgraph "Cloud Infrastructure"
        AWS_S3["AWS S3<br/>(Image Storage)"]
        CLOUD["AWS/Azure<br/>(Compute)"]
    end

    subgraph "Auth Providers"
        GOOGLE["Google OAuth2"]
    end

    subgraph "Communication"
        EMAIL["SendGrid<br/>(Email)"]
        SMS["Twilio<br/>(SMS)"]
    end

    subgraph "Monitoring"
        GA["Google Analytics"]
        SENTRY["Sentry<br/>(Error Tracking)"]
    end

    PLATFORM --> OPENAI
    PLATFORM --> HF
    PLATFORM --> AWS_S3
    PLATFORM --> CLOUD
    PLATFORM --> GOOGLE
    PLATFORM --> EMAIL
    PLATFORM --> SMS
    PLATFORM --> GA
    PLATFORM --> SENTRY
```

---

## 8. Security Architecture

### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Google as Google OAuth
    participant DB as Database

    Note over User,DB: Standard Login Flow
    User->>Frontend: Enter credentials
    Frontend->>Backend: POST /api/v1/auth/login
    Backend->>DB: Verify credentials
    DB-->>Backend: User data
    Backend->>Backend: Generate JWT (access + refresh)
    Backend-->>Frontend: {access_token, refresh_token}
    Frontend->>Frontend: Store tokens

    Note over User,DB: OAuth2 Flow
    User->>Frontend: Click "Login with Google"
    Frontend->>Google: Redirect to Google OAuth
    Google-->>Frontend: Authorization code
    Frontend->>Backend: POST /api/v1/auth/google/callback
    Backend->>Google: Exchange code for tokens
    Google-->>Backend: Google user info
    Backend->>DB: Find/Create user
    Backend->>Backend: Generate JWT
    Backend-->>Frontend: {access_token, refresh_token}
```

### Security Measures

| Measure | Implementation |
|---------|---------------|
| **Password Hashing** | bcrypt with auto-generated salt |
| **JWT Tokens** | RS256 signing, 15min access, 7d refresh |
| **Token Refresh** | Silent refresh via httpOnly cookie |
| **Token Blacklist** | Redis-backed blacklist for revoked tokens |
| **RBAC** | Decorator-based role checking on routes |
| **Input Validation** | Pydantic models on all endpoints |
| **SQL Injection** | SQLAlchemy ORM (parameterized queries) |
| **XSS Protection** | React's default escaping + CSP headers |
| **CORS** | Whitelist-based origin checking |
| **Rate Limiting** | Redis sliding window per IP/user |

### Role-Based Access Control Matrix

| Resource | User | Tarot Reader | Spiritual Consultant | Admin |
|----------|------|-------------|---------------------|-------|
| Own Profile | ✅ CRUD | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| Own Readings | ✅ Read | ✅ Read | ✅ Read | ✅ Read |
| Create Reading | ✅ | ✅ | ✅ | ✅ |
| View Other Users | ❌ | ✅ (clients) | ✅ (clients) | ✅ (all) |
| Reading Analytics | ❌ | ✅ (own) | ✅ (all) | ✅ (all) |
| User Management | ❌ | ❌ | ❌ | ✅ |
| System Config | ❌ | ❌ | ❌ | ✅ |
| Reports Export | ✅ (own) | ✅ (clients) | ✅ (all) | ✅ (all) |

---

## 9. Deployment Architecture

### Development Environment (Docker Compose)

```mermaid
graph TB
    subgraph "Docker Compose Network"
        FE["📦 Frontend<br/>Next.js<br/>Port 3000"]
        BE["📦 Backend<br/>FastAPI<br/>Port 8000"]
        PG["📦 PostgreSQL<br/>Port 5432"]
        MG["📦 MongoDB<br/>Port 27017"]
        RD["📦 Redis<br/>Port 6379"]
    end

    FE -->|API calls| BE
    BE -->|SQL queries| PG
    BE -->|Document queries| MG
    BE -->|Cache/Sessions| RD
```

### Production Environment (Week 7-8)

```mermaid
graph TB
    subgraph "CDN / Edge"
        CF["CloudFront / Vercel"]
    end

    subgraph "Application Layer"
        ALB["Load Balancer"]
        BE1["FastAPI Instance 1"]
        BE2["FastAPI Instance 2"]
    end

    subgraph "Data Layer"
        RDS["AWS RDS<br/>(PostgreSQL)"]
        ATLAS["MongoDB Atlas"]
        EC["ElastiCache<br/>(Redis)"]
        S3["S3 Bucket"]
    end

    CF --> ALB
    ALB --> BE1
    ALB --> BE2
    BE1 --> RDS
    BE1 --> ATLAS
    BE1 --> EC
    BE1 --> S3
    BE2 --> RDS
    BE2 --> ATLAS
    BE2 --> EC
    BE2 --> S3
```

---

## 10. Design Decisions & Trade-offs

### Decision Log

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| **Backend Framework** | FastAPI | Django, Flask, Express | Async support, auto docs, type hints, performance |
| **Frontend Framework** | Next.js | Create React App, Vite | SSR/SSG, file-based routing, API routes, SEO |
| **Primary DB** | PostgreSQL | MySQL, SQLite | ACID compliance, JSON support, extensions |
| **Document Store** | MongoDB | DynamoDB, Firestore | Flexible schema, rich queries, aggregation pipeline |
| **Cache** | Redis | Memcached | Data structures, pub/sub, persistence options |
| **Auth Strategy** | JWT | Session-based | Stateless, scalable, mobile-friendly |
| **CSS Framework** | TailwindCSS | Styled Components, CSS Modules | Rapid development, consistent design, utility-first |
| **Containerization** | Docker | Vagrant, bare metal | Reproducible environments, easy deployment |
| **Monolith-First** | Single FastAPI app | Separate microservices | Simpler development, easier debugging, extract later |
| **ORM** | SQLAlchemy | Tortoise ORM, Prisma | Mature ecosystem, migration support, community |

### Scalability Considerations

1. **Horizontal Scaling**: Stateless backend allows multiple instances behind a load balancer
2. **Database Read Replicas**: PostgreSQL replicas for read-heavy analytics queries
3. **Caching Strategy**: Redis caching for frequently accessed data (user profiles, reading results)
4. **Async Processing**: Background tasks for AI model inference (Celery + Redis as broker)
5. **CDN**: Static assets and generated reports served via CDN
6. **Image Optimization**: Uploaded palm images resized and compressed before storage

---

## Appendix: File Organization Convention

```
backend/
├── app/
│   ├── main.py          # App factory, middleware registration
│   ├── config.py        # Pydantic Settings (env-based config)
│   ├── database.py      # DB connection factories
│   ├── models/          # SQLAlchemy ORM models (DB tables)
│   ├── schemas/         # Pydantic schemas (API contracts)
│   ├── routers/         # FastAPI route handlers (thin layer)
│   ├── services/        # Business logic (thick layer)
│   ├── middleware/       # Custom middleware (auth, logging)
│   └── utils/           # Shared utilities (security, helpers)
```

**Naming Convention**:
- Models: `PascalCase` (e.g., `User`, `UserProfile`)
- Tables: `snake_case` (e.g., `users`, `user_profiles`)
- Endpoints: `kebab-case` (e.g., `/api/v1/auth/login`)
- Files: `snake_case` (e.g., `auth_service.py`)
