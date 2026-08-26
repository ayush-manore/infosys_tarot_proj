# 🔄 Workflow Diagrams — Palmistry & Tarot Intelligence Platform

## Table of Contents
1. [User Registration & Login Flow](#1-user-registration--login-flow)
2. [Palm Reading Workflow](#2-palm-reading-workflow)
3. [Tarot Reading Workflow](#3-tarot-reading-workflow)
4. [AI Insight Generation Pipeline](#4-ai-insight-generation-pipeline)
5. [Role-Based Access Flow](#5-role-based-access-flow)
6. [Token Refresh Flow](#6-token-refresh-flow)
7. [Profile Management Flow](#7-profile-management-flow)
8. [End-to-End User Journey](#8-end-to-end-user-journey)

---

## 1. User Registration & Login Flow

### Registration Flow

```mermaid
flowchart TD
    A["🌐 User visits website"] --> B{"Has account?"}
    
    B -->|No| C["📝 Register page"]
    C --> D["Enter email, password, name"]
    D --> E{"Validate input"}
    E -->|Invalid| F["❌ Show validation errors"]
    F --> D
    E -->|Valid| G["Check if email exists"]
    G -->|Exists| H["❌ Email already registered"]
    H --> D
    G -->|New| I["Hash password (bcrypt)"]
    I --> J["Create user in PostgreSQL"]
    J --> K["Create default profile"]
    K --> L["Assign 'user' role"]
    L --> M["Generate JWT tokens"]
    M --> N["✅ Redirect to Dashboard"]
    
    B -->|Yes| O["🔐 Login page"]
    O --> P["Enter email, password"]
    P --> Q{"Validate credentials"}
    Q -->|Invalid| R["❌ Invalid email or password"]
    R --> P
    Q -->|Valid| S["Update last_login_at"]
    S --> M
    
    B -->|OAuth| T["🔗 Click 'Login with Google'"]
    T --> U["Redirect to Google OAuth"]
    U --> V["User grants permission"]
    V --> W["Google sends auth code"]
    W --> X["Exchange code for Google token"]
    X --> Y["Fetch Google user info"]
    Y --> Z{"User exists?"}
    Z -->|Yes| AA["Link to existing account"]
    Z -->|No| AB["Create new user with Google data"]
    AA --> M
    AB --> M
```

### Login Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant PG as PostgreSQL
    participant R as Redis

    U->>F: Enter email + password
    F->>F: Client-side validation
    F->>B: POST /api/v1/auth/login
    B->>PG: Find user by email
    PG-->>B: User record
    B->>B: Verify password (bcrypt)
    B->>B: Generate access_token (15min)
    B->>B: Generate refresh_token (7days)
    B->>PG: Update last_login_at
    B->>R: Store session info
    B-->>F: { tokens, user_data }
    F->>F: Store access_token in memory
    F->>F: Store refresh_token in cookie
    F-->>U: Redirect to Dashboard
```

---

## 2. Palm Reading Workflow

> Implemented in Weeks 3-4. Interfaces defined in Week 1.

### Upload & Analysis Flow

```mermaid
flowchart TD
    A["🖐️ User opens Palm Reading"] --> B["📸 Camera / Upload"]
    
    B -->|Camera| C["Real-time hand detection overlay"]
    C --> D["Guide: 'Position hand in center'"]
    D --> E["Guide: 'Hold steady...'"]
    E --> F["Capture image"]
    
    B -->|Upload| G["Select image from device"]
    G --> F
    
    F --> H["📤 Upload to server"]
    H --> I["Create reading_session (PostgreSQL)"]
    I --> J["Store original image (S3)"]
    J --> K["🔍 Image Preprocessing"]
    
    K --> K1["Resize to 640x640"]
    K --> K2["Color correction"]
    K --> K3["Noise reduction"]
    
    K1 & K2 & K3 --> L["✋ Hand Detection (MediaPipe)"]
    L --> L1{"Hand detected?"}
    L1 -->|No| L2["❌ 'No hand detected. Please try again.'"]
    L2 --> B
    
    L1 -->|Yes| M["Extract palm region"]
    M --> N["🔬 Feature Extraction"]
    
    N --> N1["Life Line detection"]
    N --> N2["Head Line detection"]
    N --> N3["Heart Line detection"]
    N --> N4["Fate Line detection"]
    N --> N5["Sun Line detection"]
    N --> N6["Palm shape classification"]
    N --> N7["Finger structure analysis"]
    
    N1 & N2 & N3 & N4 & N5 & N6 & N7 --> O["📊 Store analysis (MongoDB)"]
    O --> P["🧠 AI Interpretation Engine"]
    P --> Q["Generate personalized insights"]
    Q --> R["Calculate confidence scores"]
    R --> S["📋 Display results to user"]
    S --> T["Save to reading history"]
```

### Palm Feature Extraction Detail

```mermaid
flowchart LR
    subgraph "Input"
        IMG["Palm Image"]
    end
    
    subgraph "Preprocessing"
        GRAY["Grayscale"]
        BLUR["Gaussian Blur"]
        EQ["Histogram\nEqualization"]
        THRESH["Adaptive\nThreshold"]
    end
    
    subgraph "Detection"
        CANNY["Canny Edge\nDetection"]
        HOUGH["Hough Line\nTransform"]
        CNN["Custom CNN\nClassifier"]
    end
    
    subgraph "Analysis"
        LENGTH["Line Length"]
        DEPTH["Line Depth"]
        CURVE["Curvature"]
        BREAKS["Breaks/Forks"]
    end
    
    subgraph "Output"
        RESULT["Feature\nVector"]
    end
    
    IMG --> GRAY --> BLUR --> EQ --> THRESH
    THRESH --> CANNY --> HOUGH --> CNN
    CNN --> LENGTH & DEPTH & CURVE & BREAKS
    LENGTH & DEPTH & CURVE & BREAKS --> RESULT
```

---

## 3. Tarot Reading Workflow

> Implemented in Weeks 3-4. Interfaces defined in Week 1.

### Card Selection Flow

```mermaid
flowchart TD
    A["🃏 User opens Tarot Reading"] --> B["Select reading type"]
    
    B --> B1["Single Card\n(Quick insight)"]
    B --> B2["Three Card\n(Past/Present/Future)"]
    B --> B3["Celtic Cross\n(Deep analysis)"]
    B --> B4["Relationship\nSpread"]
    B --> B5["Career\nSpread"]
    B --> B6["Life Path\nSpread"]
    
    B1 & B2 & B3 & B4 & B5 & B6 --> C["Optional: Enter a question"]
    C --> D["🔄 Card Shuffling Animation"]
    D --> E["Spread layout displayed"]
    E --> F["User taps to reveal card"]
    
    F --> G{"All cards revealed?"}
    G -->|No| F
    G -->|Yes| H["📤 Send to server"]
    
    H --> I["Create reading_session"]
    I --> J["Store card selections (MongoDB)"]
    J --> K["🧠 AI Interpretation"]
    
    K --> K1["Individual card meanings"]
    K --> K2["Position-specific interpretation"]
    K --> K3["Card combination analysis"]
    K --> K4["Context from user profile"]
    
    K1 & K2 & K3 & K4 --> L["📝 Generate narrative"]
    L --> M["Create action items"]
    M --> N["Calculate confidence score"]
    N --> O["📋 Display full reading"]
    O --> P["Save to history"]
    P --> Q["Offer: Save as PDF / Share"]
```

### Tarot Spread Layouts

```mermaid
graph TD
    subgraph "Single Card"
        S1["🃏"]
    end
    
    subgraph "Three Card Spread"
        T1["🃏 Past"] --- T2["🃏 Present"] --- T3["🃏 Future"]
    end
    
    subgraph "Celtic Cross (10 cards)"
        CC1["🃏 1\nPresent"]
        CC2["🃏 2\nChallenge"]
        CC3["🃏 3\nPast"]
        CC4["🃏 4\nFuture"]
        CC5["🃏 5\nAbove"]
        CC6["🃏 6\nBelow"]
        CC7["🃏 7\nAdvice"]
        CC8["🃏 8\nExternal"]
        CC9["🃏 9\nHopes"]
        CC10["🃏 10\nOutcome"]
    end
```

---

## 4. AI Insight Generation Pipeline

```mermaid
flowchart TD
    subgraph "Data Collection"
        A1["Palm Analysis Data"]
        A2["Tarot Reading Data"]
        A3["User Profile"]
        A4["Reading History"]
    end
    
    subgraph "Context Assembly"
        B["Merge all data into context"]
        B --> C["Build prompt template"]
        C --> D["Add system instructions"]
        D --> E["Add output format spec"]
    end
    
    subgraph "AI Processing (LangChain + OpenAI)"
        F["Send to GPT-4"]
        F --> G["Parse structured output"]
        G --> H["Validate against schema"]
        H --> I{"Valid?"}
        I -->|No| J["Retry with corrections"]
        J --> F
        I -->|Yes| K["Extract insights"]
    end
    
    subgraph "Insight Categories"
        K --> L1["💫 Personality Traits"]
        K --> L2["❤️ Relationships"]
        K --> L3["💼 Career"]
        K --> L4["💰 Finance"]
        K --> L5["🏥 Health & Wellness"]
        K --> L6["🌱 Personal Growth"]
        K --> L7["🎯 Life Opportunities"]
    end
    
    subgraph "Scoring"
        L1 & L2 & L3 & L4 & L5 & L6 & L7 --> M["Calculate Insight Score"]
        M --> M1["Palm Confidence: 30%"]
        M --> M2["Tarot Relevance: 25%"]
        M --> M3["Personality Alignment: 20%"]
        M --> M4["Context Relevance: 15%"]
        M --> M5["Reading Consistency: 10%"]
        M1 & M2 & M3 & M4 & M5 --> N["Overall Insight Score"]
    end
    
    subgraph "Output"
        N --> O["Store in MongoDB"]
        O --> P["Return to user"]
    end
    
    A1 & A2 & A3 & A4 --> B
    E --> F
```

---

## 5. Role-Based Access Flow

```mermaid
flowchart TD
    A["📨 API Request"] --> B["Extract JWT token"]
    B --> C{"Token valid?"}
    
    C -->|No token| D["❌ 401 Unauthorized"]
    C -->|Expired| E["❌ 401 Token Expired"]
    C -->|Blacklisted| F["❌ 401 Token Revoked"]
    
    C -->|Valid| G["Extract user role from token"]
    G --> H{"Check route permissions"}
    
    H --> I{"Is Admin route?"}
    I -->|Yes| J{"Role == admin?"}
    J -->|No| K["❌ 403 Forbidden"]
    J -->|Yes| L["✅ Allow access"]
    
    H --> M{"Is Consultant route?"}
    M -->|Yes| N{"Role == admin OR consultant?"}
    N -->|No| K
    N -->|Yes| L
    
    H --> O{"Is Reader route?"}
    O -->|Yes| P{"Role == admin OR consultant OR reader?"}
    P -->|No| K
    P -->|Yes| L
    
    H --> Q{"Is User route?"}
    Q -->|Yes| R{"Any authenticated role?"}
    R -->|Yes| L
    
    L --> S["Execute route handler"]
    S --> T["Return response"]
```

---

## 6. Token Refresh Flow

```mermaid
sequenceDiagram
    participant F as Frontend
    participant B as Backend
    participant R as Redis

    Note over F: Access token expired (401)
    
    F->>F: Intercept 401 response
    F->>B: POST /api/v1/auth/refresh<br/>{refresh_token}
    
    B->>B: Decode refresh token
    B->>R: Check if blacklisted
    
    alt Token blacklisted
        R-->>B: Token found in blacklist
        B-->>F: 401 Refresh token revoked
        F-->>F: Redirect to login
    else Token valid
        R-->>B: Not blacklisted
        B->>B: Generate new access_token
        B->>R: Blacklist old refresh_token
        B->>B: Generate new refresh_token
        B-->>F: { new_access_token, new_refresh_token }
        F->>F: Retry original request
    end
```

---

## 7. Profile Management Flow

```mermaid
flowchart TD
    A["👤 User opens Profile"] --> B["Fetch current profile"]
    B --> C["Display profile form"]
    
    C --> D{"What to update?"}
    
    D -->|Personal Info| E["Edit name, DOB, gender"]
    D -->|Spiritual Interests| F["Select: Palmistry, Tarot,\nAstrology, Numerology"]
    D -->|Goals| G["Add/Edit spiritual goals"]
    D -->|Preferences| H["Set reading preferences\n(spread type, time)"]
    D -->|Avatar| I["Upload profile picture"]
    
    E & F & G & H --> J["Save changes"]
    I --> K["Upload to S3"]
    K --> L["Update avatar_url"]
    L --> J
    
    J --> M["PUT /api/v1/profiles/me"]
    M --> N{"Validation"}
    N -->|Invalid| O["Show errors"]
    O --> C
    N -->|Valid| P["Update PostgreSQL"]
    P --> Q["✅ Success notification"]
```

---

## 8. End-to-End User Journey

```mermaid
journey
    title User Journey: First-Time Palm Reading
    section Discovery
        Visit Landing Page: 5: User
        Browse features: 4: User
        Decide to try: 5: User
    section Onboarding
        Register / Google Login: 5: User
        Complete profile: 4: User
        Set spiritual interests: 4: User
        Set goals: 3: User
    section First Reading
        Choose Palm Reading: 5: User
        Upload palm image: 4: User
        Wait for analysis: 3: User
        View results: 5: User
        Read personality insights: 5: User
        Read career guidance: 4: User
    section Engagement
        Save reading to history: 4: User
        Export as PDF: 3: User
        Try Tarot Reading: 5: User
        Share with friend: 4: User
    section Retention
        Return next day: 4: User
        View daily guidance: 5: User
        Track progress: 4: User
        Complete another reading: 5: User
```

---

## Data Flow Overview

```mermaid
flowchart LR
    subgraph "Frontend (Next.js)"
        UI["User Interface"]
        STORE["Local State"]
    end
    
    subgraph "API Gateway (FastAPI)"
        AUTH["Auth Middleware"]
        ROUTER["Router"]
    end
    
    subgraph "Services"
        AUTH_SVC["Auth Service"]
        PROFILE_SVC["Profile Service"]
        PALM_SVC["Palm Service"]
        TAROT_SVC["Tarot Service"]
        AI_SVC["AI Service"]
    end
    
    subgraph "Data Stores"
        PG["PostgreSQL"]
        MONGO["MongoDB"]
        REDIS["Redis"]
        S3["S3 Storage"]
    end
    
    UI <-->|REST API| AUTH
    AUTH --> ROUTER
    ROUTER --> AUTH_SVC & PROFILE_SVC & PALM_SVC & TAROT_SVC & AI_SVC
    
    AUTH_SVC --> PG & REDIS
    PROFILE_SVC --> PG & S3
    PALM_SVC --> MONGO & S3
    TAROT_SVC --> MONGO
    AI_SVC --> MONGO
    
    UI --> STORE
```
