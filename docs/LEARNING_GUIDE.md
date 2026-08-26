# 📚 Learning Guide — Palmistry & Tarot Intelligence Platform

> **For Interns**: This guide explains every technology, pattern, and concept used in this project. Read each section to understand *why* we chose each tool and *how* it works under the hood.

## Table of Contents
1. [Project Overview & Why This Stack](#1-project-overview--why-this-stack)
2. [Python & FastAPI (Backend)](#2-python--fastapi-backend)
3. [JWT Authentication Deep-Dive](#3-jwt-authentication-deep-dive)
4. [OAuth2 — Login with Google](#4-oauth2--login-with-google)
5. [Role-Based Access Control (RBAC)](#5-role-based-access-control-rbac)
6. [SQLAlchemy ORM & Database Patterns](#6-sqlalchemy-orm--database-patterns)
7. [MongoDB & NoSQL Concepts](#7-mongodb--nosql-concepts)
8. [Redis — Caching & Sessions](#8-redis--caching--sessions)
9. [React & Next.js (Frontend)](#9-react--nextjs-frontend)
10. [TailwindCSS — Utility-First CSS](#10-tailwindcss--utility-first-css)
11. [Docker & Containerization](#11-docker--containerization)
12. [REST API Design Principles](#12-rest-api-design-principles)
13. [Git Workflow](#13-git-workflow)
14. [Computer Vision Concepts (Preview)](#14-computer-vision-concepts-preview)
15. [AI/LLM Integration Concepts (Preview)](#15-aillm-integration-concepts-preview)
16. [Recommended Learning Resources](#16-recommended-learning-resources)

---

## 1. Project Overview & Why This Stack

### What Are We Building?

An AI-powered platform that:
1. **Analyzes palm images** using computer vision to detect lines and patterns
2. **Interprets tarot cards** using AI to generate personalized spiritual insights
3. **Creates personality profiles** based on palm and tarot analysis
4. **Provides guidance** for career, relationships, personal growth

### Why This Tech Stack?

| Technology | Why We Chose It |
|-----------|----------------|
| **Python + FastAPI** | Python is the #1 language for AI/ML. FastAPI is the fastest Python web framework with automatic API docs. |
| **Next.js + React** | Industry-standard frontend framework. Server-side rendering (SSR) for SEO. File-based routing. |
| **PostgreSQL** | Most advanced open-source relational database. ACID compliant. Great for structured data. |
| **MongoDB** | Flexible schema for AI outputs. Perfect for storing varying analysis results. |
| **Redis** | Blazing fast in-memory store. Perfect for caching, sessions, and rate limiting. |
| **Docker** | Containerization ensures "it works on my machine" becomes "it works everywhere." |
| **TailwindCSS** | Utility-first CSS framework. Rapid development. Consistent design system. |

### How Does the Architecture Work?

Think of the platform as a **restaurant**:

```
Customer (User) → Waiter (Frontend) → Kitchen Manager (API Gateway)
→ Chefs (Services) → Pantry (Database)
```

- **Customer (User)**: Interacts with the website
- **Waiter (Frontend/Next.js)**: Takes requests, presents results beautifully
- **Kitchen Manager (FastAPI Gateway)**: Routes requests, checks credentials, manages queue
- **Chefs (Microservices)**: Each chef specializes (auth, palm analysis, tarot, etc.)
- **Pantry (Database)**: Stores all ingredients (data)

---

## 2. Python & FastAPI (Backend)

### What is FastAPI?

FastAPI is a modern Python web framework for building APIs. It's built on top of:
- **Starlette** (for web handling)
- **Pydantic** (for data validation)
- **Uvicorn** (for async server)

### Key FastAPI Concepts

#### 2.1 Async/Await

Python's `async/await` allows handling multiple requests concurrently without threads:

```python
# ❌ Synchronous - blocks while waiting for database
def get_user(user_id: str):
    user = db.query(User).filter(User.id == user_id).first()  # Waits here
    return user

# ✅ Asynchronous - doesn't block, can handle other requests
async def get_user(user_id: str):
    user = await db.execute(select(User).filter(User.id == user_id))  # Non-blocking
    return user.scalar_one_or_none()
```

**Why it matters**: When the database query takes 50ms, a sync server sits idle. An async server processes other requests during that 50ms.

#### 2.2 Dependency Injection

FastAPI's dependency injection system lets you declare what a function needs, and FastAPI provides it:

```python
# Define a dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """This function extracts and validates the JWT token"""
    user = decode_token(token)
    return user

# Use it in a route - FastAPI automatically calls get_current_user first
@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user
```

**Analogy**: It's like a restaurant where the waiter (dependency) automatically brings water (user info) before you even order food (make a request).

#### 2.3 Pydantic Models (Schemas)

Pydantic validates and serializes data automatically:

```python
from pydantic import BaseModel, EmailStr, validator

class UserRegister(BaseModel):
    email: EmailStr                          # Auto-validates email format
    password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

# FastAPI automatically validates incoming JSON against this schema
@router.post("/register")
async def register(data: UserRegister):     # If validation fails, returns 422 automatically
    ...
```

#### 2.4 Middleware

Middleware processes requests BEFORE they reach your route handler:

```python
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Adds a unique request ID to every request for tracing"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

**Think of it like**: Security at a building entrance. Everyone passes through security (middleware) before reaching their floor (route handler).

#### 2.5 Project Structure Pattern

```
app/
├── main.py          # App factory - creates and configures the FastAPI app
├── config.py        # Settings loaded from environment variables
├── database.py      # Database connection setup
├── models/          # SQLAlchemy models (database table definitions)
├── schemas/         # Pydantic models (API request/response shapes)
├── routers/         # Route handlers (thin - just receives and responds)
├── services/        # Business logic (thick - actual processing)
├── middleware/       # Request/response interceptors
└── utils/           # Shared utilities
```

**The Service Layer Pattern**:
```
Router (thin) → Service (thick) → Model (database)
```
- **Router**: "Hey, someone wants to register"
- **Service**: "Let me check if email exists, hash the password, create the user, generate tokens"
- **Model**: "I'll insert this row into the database"

---

## 3. JWT Authentication Deep-Dive

### What is JWT?

**JWT (JSON Web Token)** is a compact, URL-safe way to represent claims between two parties.

A JWT looks like:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

It has 3 parts separated by dots:

```
HEADER.PAYLOAD.SIGNATURE
```

#### Part 1: Header

```json
{
    "alg": "HS256",    // Algorithm used for signing
    "typ": "JWT"       // Type of token
}
```

#### Part 2: Payload (Claims)

```json
{
    "sub": "user-uuid-123",     // Subject (who this token is for)
    "email": "user@test.com",   // Custom claim
    "role": "user",             // Custom claim
    "iat": 1705312200,          // Issued at (Unix timestamp)
    "exp": 1705313100,          // Expires at (15 min later)
    "jti": "unique-id"          // JWT ID (for blacklisting)
}
```

#### Part 3: Signature

```
HMACSHA256(
    base64UrlEncode(header) + "." + base64UrlEncode(payload),
    secret_key
)
```

### Why JWT for This Project?

```
Session-Based Auth (Traditional):
Client → Server: "I'm user 123"
Server → Database: "Check session store for user 123"
Database → Server: "Here's the session data"
Server → Client: "OK, you're authenticated"
→ Requires database lookup EVERY request

JWT Auth (Our Approach):
Client → Server: "Here's my JWT token"
Server → Server: "Let me verify the signature... looks valid!"
Server → Client: "OK, you're authenticated"
→ No database lookup needed! The token itself contains all the info.
```

### Access Token vs Refresh Token

| | Access Token | Refresh Token |
|---|-------------|---------------|
| **Lifetime** | 15 minutes | 7 days |
| **Stored** | Memory / localStorage | httpOnly cookie |
| **Purpose** | Authenticate API requests | Get new access tokens |
| **On Expiry** | Get new one via refresh | Must log in again |

```
Timeline:
[Login] → Access Token (15min) + Refresh Token (7 days)
           ↓
[15min later] → Access Token expires
           ↓
[Refresh] → New Access Token (15min)  ← using Refresh Token
           ↓
[7 days later] → Refresh Token expires
           ↓
[Must Login Again]
```

### Token Blacklisting

When a user logs out, we can't "destroy" a JWT (it's self-contained). Instead, we add its `jti` (JWT ID) to a Redis blacklist:

```python
# On logout
redis.setex(f"blacklist:{token_jti}", ttl_remaining, "1")

# On every request (middleware)
if redis.get(f"blacklist:{token_jti}"):
    raise HTTPException(401, "Token has been revoked")
```

---

## 4. OAuth2 — Login with Google

### What is OAuth2?

OAuth2 lets users log in with their existing Google/GitHub/Facebook account instead of creating a new password.

### The OAuth2 Flow (Authorization Code Grant)

```
Step 1: User clicks "Login with Google"
Step 2: We redirect user to Google's consent page
Step 3: User grants permission
Step 4: Google redirects back to our app with an "authorization code"
Step 5: Our backend exchanges this code for Google's access token
Step 6: We use Google's token to fetch the user's profile (email, name, picture)
Step 7: We create/find the user in our database
Step 8: We issue our own JWT tokens
```

```mermaid
sequenceDiagram
    participant User
    participant Our App
    participant Google

    User->>Our App: Click "Login with Google"
    Our App->>Google: Redirect to consent page
    Google->>User: Show consent form
    User->>Google: Grant permission
    Google->>Our App: Authorization code
    Our App->>Google: Exchange code for token
    Google->>Our App: Access token + user info
    Our App->>Our App: Create/find user in DB
    Our App->>User: Our JWT tokens
```

### Why OAuth2?

1. **User convenience**: No new password to remember
2. **Security**: We never handle the user's Google password
3. **Trust**: Users trust Google's auth more than a new platform
4. **Less friction**: Faster sign-up → more users

---

## 5. Role-Based Access Control (RBAC)

### What is RBAC?

RBAC restricts system access based on the roles assigned to users. Each role has a set of permissions.

### Our 4 Roles

```
Admin (God mode)
  ├── Can do everything
  ├── User management
  ├── System configuration
  └── Platform analytics

Spiritual Consultant
  ├── View all users' data
  ├── Access analytics
  ├── Create consultations
  └── Own readings

Tarot Reader
  ├── View client data
  ├── Manage sessions
  ├── Create readings
  └── Own readings

User (Default)
  ├── Own profile (CRUD)
  ├── Create readings
  └── View own history
```

### How We Implement It

```python
# 1. Define role check as a dependency
def require_role(allowed_roles: list[str]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.name not in allowed_roles:
            raise HTTPException(403, "Insufficient permissions")
        return current_user
    return role_checker

# 2. Use it on routes
@router.get("/users")
async def list_users(
    user: User = Depends(require_role(["admin"]))  # Only admins
):
    return await user_service.list_all_users()

@router.get("/analytics")
async def get_analytics(
    user: User = Depends(require_role(["admin", "spiritual_consultant"]))  # Admin + Consultant
):
    return await analytics_service.get_dashboard()
```

---

## 6. SQLAlchemy ORM & Database Patterns

### What is an ORM?

**ORM (Object-Relational Mapping)** lets you interact with databases using Python objects instead of raw SQL:

```python
# ❌ Raw SQL - error-prone, no type safety
cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, pw))

# ✅ SQLAlchemy ORM - type-safe, readable, secure
user = User(email=email, password_hash=hashed_pw)
db.add(user)
await db.commit()
```

### SQLAlchemy Key Concepts

#### Models (Table Definitions)

```python
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255))
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))

    # Relationships - lets you access related data as Python attributes
    role = relationship("Role", back_populates="users")
    profile = relationship("UserProfile", back_populates="user", uselist=False)
```

#### Async Session Pattern

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Create async engine
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

# Use in routes via dependency injection
async def get_db():
    async with AsyncSession(engine) as session:
        try:
            yield session           # Give session to route
            await session.commit()  # Auto-commit if no errors
        except Exception:
            await session.rollback()  # Rollback on error
            raise
```

#### Common Query Patterns

```python
# Find one by ID
user = await db.get(User, user_id)

# Find one by email
result = await db.execute(select(User).where(User.email == email))
user = result.scalar_one_or_none()

# Find all with filters
result = await db.execute(
    select(User)
    .where(User.is_active == True)
    .order_by(User.created_at.desc())
    .limit(20)
    .offset(0)
)
users = result.scalars().all()

# Join queries
result = await db.execute(
    select(User)
    .join(Role)
    .where(Role.name == "admin")
)
```

### Database Migrations with Alembic

Alembic tracks changes to your database schema over time:

```bash
# "I added a new column to the users table"
alembic revision --autogenerate -m "add_phone_to_users"

# "Apply all pending migrations"
alembic upgrade head

# "Oops, rollback the last migration"
alembic downgrade -1
```

---

## 7. MongoDB & NoSQL Concepts

### SQL vs NoSQL

```
SQL (PostgreSQL):                    NoSQL (MongoDB):
┌──────────────────────┐            ┌─────────────────────────┐
│ Fixed schema          │            │ Flexible schema          │
│ Tables with rows      │            │ Collections with docs    │
│ Joins for relations   │            │ Nested documents         │
│ ACID transactions     │            │ Document-level atomicity │
│ Good for: users,      │            │ Good for: AI outputs,    │
│   payments, sessions  │            │   analysis results       │
└──────────────────────┘            └─────────────────────────┘
```

### Why We Use Both

- **PostgreSQL**: User accounts, roles, relationships (structured, relational)
- **MongoDB**: Palm analysis results, tarot readings, AI insights (varied structure, nested data)

### Motor — Async MongoDB Driver

```python
from motor.motor_asyncio import AsyncIOMotorClient

# Connect
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.palmistry_tarot

# Insert a document
palm_analysis = {
    "user_id": "uuid-string",
    "palm_lines": {
        "life_line": { "detected": True, "confidence": 0.89 },
        "head_line": { "detected": True, "confidence": 0.87 }
    }
}
result = await db.palm_analyses.insert_one(palm_analysis)

# Find documents
analysis = await db.palm_analyses.find_one({"user_id": "uuid-string"})

# Update
await db.palm_analyses.update_one(
    {"_id": result.inserted_id},
    {"$set": {"palm_lines.life_line.confidence": 0.92}}
)
```

---

## 8. Redis — Caching & Sessions

### What is Redis?

Redis is an **in-memory data store**. It's like a super-fast dictionary that lives in RAM:

```
Dictionary (Python):       Redis:
my_dict = {}               SET key value
my_dict["key"] = "value"   GET key
del my_dict["key"]         DEL key
                           SETEX key 300 value  ← Auto-deletes after 300 seconds!
```

### Why Redis?

| Use Case | Why Not Database? |
|----------|------------------|
| **Token Blacklist** | Need sub-millisecond lookups for every API request |
| **Session Cache** | Avoid hitting PostgreSQL for every request |
| **Rate Limiting** | Need atomic counters with TTL |
| **Temp Data** | Short-lived data that doesn't need persistence |

### Redis in Our Project

```python
import aioredis

redis = aioredis.from_url("redis://localhost:6379")

# Token blacklisting
async def blacklist_token(token_jti: str, ttl: int):
    await redis.setex(f"blacklist:{token_jti}", ttl, "1")

async def is_token_blacklisted(token_jti: str) -> bool:
    return await redis.get(f"blacklist:{token_jti}") is not None

# Rate limiting
async def check_rate_limit(ip: str, limit: int = 100, window: int = 60):
    key = f"ratelimit:{ip}"
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, window)
    return current <= limit
```

---

## 9. React & Next.js (Frontend)

### What is React?

React is a JavaScript library for building user interfaces using **components**:

```jsx
// A component is just a function that returns UI (JSX)
function WelcomeCard({ name }) {
    return (
        <div className="card">
            <h2>Welcome, {name}!</h2>
            <p>Ready for your reading?</p>
        </div>
    );
}
```

### What is Next.js?

Next.js is a **React framework** that adds:
- **File-based routing**: Create `app/about/page.js` → get `/about` route
- **Server-Side Rendering (SSR)**: HTML generated on server → better SEO
- **API Routes**: Build backend endpoints within Next.js
- **Image Optimization**: Automatic image resizing and lazy loading
- **Built-in CSS support**: CSS Modules, Tailwind, etc.

### App Router (Next.js 14+)

```
src/app/
├── layout.js          → Root layout (wraps all pages)
├── page.js            → Home page (/)
├── auth/
│   ├── login/
│   │   └── page.js    → Login page (/auth/login)
│   └── register/
│       └── page.js    → Register page (/auth/register)
├── dashboard/
│   └── page.js        → Dashboard (/dashboard)
└── profile/
    └── page.js        → Profile (/profile)
```

### Key React Concepts Used

#### State Management (useState)

```jsx
function LoginForm() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        const response = await api.login(email, password);
        setLoading(false);
    };
}
```

#### Context API (Global State)

```jsx
// AuthContext provides user data to ALL components
const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);

    return (
        <AuthContext.Provider value={{ user, setUser }}>
            {children}
        </AuthContext.Provider>
    );
}

// Any component can access user data:
function Dashboard() {
    const { user } = useContext(AuthContext);
    return <h1>Welcome, {user.name}!</h1>;
}
```

#### Custom Hooks

```jsx
// Reusable authentication logic
function useAuth() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check if user is logged in on mount
        const token = localStorage.getItem('access_token');
        if (token) {
            fetchUser(token).then(setUser);
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => { ... };
    const logout = async () => { ... };

    return { user, loading, login, logout };
}
```

---

## 10. TailwindCSS — Utility-First CSS

### What is Utility-First CSS?

Instead of writing custom CSS classes, you compose styles using utility classes:

```html
<!-- ❌ Traditional CSS -->
<div class="card">
    <h2 class="card-title">Hello</h2>
</div>
<style>
    .card { background: white; border-radius: 8px; padding: 16px; box-shadow: ... }
    .card-title { font-size: 20px; font-weight: bold; color: #333; }
</style>

<!-- ✅ TailwindCSS -->
<div class="bg-white rounded-lg p-4 shadow-lg">
    <h2 class="text-xl font-bold text-gray-800">Hello</h2>
</div>
```

### Common Tailwind Patterns in Our Project

```html
<!-- Glassmorphism Card -->
<div class="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-6 shadow-xl">

<!-- Gradient Button -->
<button class="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 shadow-lg hover:shadow-purple-500/25">

<!-- Cosmic Background -->
<div class="bg-gradient-to-br from-gray-900 via-indigo-950 to-purple-950 min-h-screen">
```

### Customizing Tailwind (tailwind.config.js)

```javascript
module.exports = {
    theme: {
        extend: {
            colors: {
                cosmic: {
                    900: '#0a0a1a',
                    800: '#12122a',
                    700: '#1a1a3e',
                },
                mystic: {
                    gold: '#f0c27f',
                    purple: '#a855f7',
                },
            },
            fontFamily: {
                heading: ['Outfit', 'sans-serif'],
                body: ['Inter', 'sans-serif'],
            },
        },
    },
};
```

---

## 11. Docker & Containerization

### What is Docker?

Docker packages your application and ALL its dependencies into a **container** — a lightweight, portable, self-sufficient unit.

**Analogy**: Shipping containers revolutionized trade because any container fits on any ship. Docker does the same for software — any container runs on any Docker host.

### Key Docker Concepts

```
Image       → Blueprint (like a class in OOP)
Container   → Running instance (like an object)
Dockerfile  → Recipe to build an image
docker-compose.yml → Recipe to run multiple containers together
```

### Our Docker Setup

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16        # Official PostgreSQL image
    environment:
      POSTGRES_DB: palmistry
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    ports:
      - "5432:5432"           # Host:Container port mapping

  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"

  redis:
    image: redis:7-alpine     # Alpine = smaller image
    ports:
      - "6379:6379"

  backend:
    build: ./backend          # Build from Dockerfile in ./backend
    ports:
      - "8000:8000"
    depends_on:               # Start databases first
      - postgres
      - mongodb
      - redis
```

### Docker Commands

```bash
# Start all services
docker-compose up -d        # -d = detached (background)

# View running containers
docker-compose ps

# View logs
docker-compose logs backend

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up --build
```

---

## 12. REST API Design Principles

### RESTful URL Design

```
Nouns, not verbs:
✅ GET /api/v1/users         → List users
✅ GET /api/v1/users/123     → Get user 123
✅ POST /api/v1/users        → Create user
✅ PUT /api/v1/users/123     → Update user 123
✅ DELETE /api/v1/users/123  → Delete user 123

❌ GET /api/v1/getUsers
❌ POST /api/v1/createUser
❌ POST /api/v1/deleteUser/123
```

### HTTP Methods

| Method | Purpose | Idempotent? | Has Body? |
|--------|---------|-------------|-----------|
| GET | Read resource | ✅ | ❌ |
| POST | Create resource | ❌ | ✅ |
| PUT | Replace resource | ✅ | ✅ |
| PATCH | Partial update | ❌ | ✅ |
| DELETE | Remove resource | ✅ | ❌ |

### HTTP Status Codes We Use

| Code | Meaning | When We Return It |
|------|---------|------------------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST |
| 204 | No Content | Successful delete with no body |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Valid token but insufficient role |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource (email exists) |
| 422 | Unprocessable | Valid JSON but semantically wrong |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Error | Bug in our code |

---

## 13. Git Workflow

### Branch Strategy

```
main (production)
  └── develop (integration)
       ├── feature/auth-system
       ├── feature/palm-analysis
       ├── feature/tarot-engine
       └── fix/login-bug
```

### Git Commands for Daily Work

```bash
# Start a new feature
git checkout develop
git pull origin develop
git checkout -b feature/auth-system

# Work on your feature
git add .
git commit -m "feat: implement JWT authentication"

# Push and create PR
git push origin feature/auth-system
# → Create Pull Request on GitHub

# Commit message convention
feat: add user registration endpoint
fix: resolve password validation bug
docs: update API reference
refactor: extract auth logic into service
test: add unit tests for login endpoint
chore: update dependencies
```

---

## 14. Computer Vision Concepts (Preview)

> **Coming in Weeks 3-4**: This section previews the CV concepts you'll implement.

### MediaPipe Hands

MediaPipe detects 21 hand landmarks in real-time:

```
Landmark 0: Wrist
Landmarks 1-4: Thumb
Landmarks 5-8: Index finger
Landmarks 9-12: Middle finger
Landmarks 13-16: Ring finger
Landmarks 17-20: Pinky
```

### Palm Line Detection Pipeline

```
1. Input Image → Resize to 640x640
2. MediaPipe → Detect hand, extract palm region
3. OpenCV → Grayscale, Gaussian blur, histogram equalization
4. Canny Edge Detection → Find edges (palm lines)
5. Hough Transform → Convert edges to line segments
6. Custom CNN → Classify lines (life, head, heart, fate, sun)
7. Feature Extraction → Length, depth, curvature, branches
```

---

## 15. AI/LLM Integration Concepts (Preview)

> **Coming in Weeks 5-6**: This section previews the AI integration approach.

### LangChain

LangChain is a framework for building LLM-powered applications:

```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert palmist and tarot reader."),
    ("user", """
    Analyze the following palm reading data and provide insights:
    Palm Lines: {palm_data}
    User Context: {user_context}
    
    Provide insights for: personality, career, relationships.
    """)
])

# Create the chain
chain = prompt | ChatOpenAI(model="gpt-4") | output_parser

# Run it
result = await chain.ainvoke({
    "palm_data": palm_analysis_json,
    "user_context": user_profile_json
})
```

### Prompt Engineering

The quality of AI outputs depends heavily on how you structure prompts:

```
Good Prompt Structure:
1. System Role: "You are an expert palmist with 20 years of experience"
2. Context: User profile, reading preferences, previous readings
3. Input Data: Palm line measurements, tarot card selections
4. Output Format: Structured JSON with categories and confidence scores
5. Constraints: "Be supportive", "Avoid negative predictions", "Focus on growth"
```

---

## 16. Recommended Learning Resources

### Python & FastAPI
- [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Real Python — Async IO](https://realpython.com/async-io-python/)
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)

### React & Next.js
- [Next.js Learn Course](https://nextjs.org/learn) (official interactive tutorial)
- [React Docs](https://react.dev/learn)
- [TailwindCSS Docs](https://tailwindcss.com/docs)

### Databases
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [MongoDB University](https://university.mongodb.com/) (free courses)
- [Redis University](https://university.redis.com/) (free courses)

### Docker
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [Docker Compose Tutorial](https://docs.docker.com/compose/gettingstarted/)

### Authentication
- [JWT.io — Introduction](https://jwt.io/introduction)
- [OAuth 2.0 Simplified](https://aaronparecki.com/oauth-2-simplified/)

### AI/ML (Preview)
- [MediaPipe Hands Guide](https://mediapipe.readthedocs.io/)
- [LangChain Docs](https://python.langchain.com/docs/)
- [OpenAI API Reference](https://platform.openai.com/docs)

### General
- [Git Branching Tutorial](https://learngitbranching.js.org/)
- [REST API Design Guide](https://restfulapi.net/)
