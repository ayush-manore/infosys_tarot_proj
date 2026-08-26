# 🔌 API Reference — Palmistry & Tarot Intelligence Platform

## Table of Contents
1. [API Overview](#1-api-overview)
2. [Authentication Endpoints](#2-authentication-endpoints)
3. [User Management Endpoints](#3-user-management-endpoints)
4. [Profile Management Endpoints](#4-profile-management-endpoints)
5. [Health & System Endpoints](#5-health--system-endpoints)
6. [Error Handling](#6-error-handling)
7. [Rate Limiting](#7-rate-limiting)
8. [Authentication Guide](#8-authentication-guide)

---

## 1. API Overview

### Base URL

```
Development: http://localhost:8000/api/v1
Production:  https://api.palmistry-tarot.com/api/v1
```

### Common Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Content-Type` | Yes | `application/json` |
| `Authorization` | Conditional | `Bearer <access_token>` (for protected routes) |
| `X-Request-ID` | No | Client-generated UUID for request tracing |

### Response Format

All responses follow this structure:

```json
{
    "status": "success",
    "message": "Operation completed successfully",
    "data": { ... },
    "meta": {
        "timestamp": "2025-01-15T10:30:00Z",
        "request_id": "uuid-string"
    }
}
```

### Error Response Format

```json
{
    "status": "error",
    "message": "Human-readable error message",
    "error": {
        "code": "VALIDATION_ERROR",
        "details": [
            {
                "field": "email",
                "message": "Invalid email format"
            }
        ]
    },
    "meta": {
        "timestamp": "2025-01-15T10:30:00Z",
        "request_id": "uuid-string"
    }
}
```

---

## 2. Authentication Endpoints

### 2.1 Register User

Creates a new user account with email and password.

```
POST /api/v1/auth/register
```

**Request Body:**

```json
{
    "email": "user@example.com",
    "password": "SecureP@ss123",
    "confirm_password": "SecureP@ss123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Validation Rules:**
- `email`: Valid email format, unique
- `password`: Min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char
- `confirm_password`: Must match `password`
- `first_name`: 2-100 chars, alphabetic
- `last_name`: 2-100 chars, alphabetic

**Response (201 Created):**

```json
{
    "status": "success",
    "message": "User registered successfully",
    "data": {
        "user": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            "role": "user",
            "is_verified": false,
            "created_at": "2025-01-15T10:30:00Z"
        },
        "tokens": {
            "access_token": "eyJhbGciOiJSUzI1NiIs...",
            "refresh_token": "eyJhbGciOiJSUzI1NiIs...",
            "token_type": "Bearer",
            "expires_in": 900
        }
    }
}
```

**Error Responses:**

| Code | Error | Description |
|------|-------|-------------|
| 400 | `VALIDATION_ERROR` | Invalid input fields |
| 409 | `EMAIL_EXISTS` | Email already registered |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many registration attempts |

---

### 2.2 Login

Authenticates a user and returns JWT tokens.

```
POST /api/v1/auth/login
```

**Request Body:**

```json
{
    "email": "user@example.com",
    "password": "SecureP@ss123"
}
```

**Response (200 OK):**

```json
{
    "status": "success",
    "message": "Login successful",
    "data": {
        "user": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            "role": "user",
            "last_login_at": "2025-01-15T10:30:00Z"
        },
        "tokens": {
            "access_token": "eyJhbGciOiJSUzI1NiIs...",
            "refresh_token": "eyJhbGciOiJSUzI1NiIs...",
            "token_type": "Bearer",
            "expires_in": 900
        }
    }
}
```

**Error Responses:**

| Code | Error | Description |
|------|-------|-------------|
| 401 | `INVALID_CREDENTIALS` | Wrong email or password |
| 403 | `ACCOUNT_DISABLED` | Account has been deactivated |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many login attempts |

---

### 2.3 Refresh Token

Gets a new access token using a valid refresh token.

```
POST /api/v1/auth/refresh
```

**Request Body:**

```json
{
    "refresh_token": "eyJhbGciOiJSUzI1NiIs..."
}
```

**Response (200 OK):**

```json
{
    "status": "success",
    "message": "Token refreshed successfully",
    "data": {
        "access_token": "eyJhbGciOiJSUzI1NiIs...",
        "token_type": "Bearer",
        "expires_in": 900
    }
}
```

---

### 2.4 Logout

Invalidates the current tokens.

```
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
    "refresh_token": "eyJhbGciOiJSUzI1NiIs..."
}
```

**Response (200 OK):**

```json
{
    "status": "success",
    "message": "Logged out successfully"
}
```

---

### 2.5 Google OAuth2 Login

Initiates Google OAuth2 flow.

```
GET /api/v1/auth/google
```

**Response (302 Redirect):**
Redirects to Google's OAuth consent screen.

---

### 2.6 Google OAuth2 Callback

Handles the callback from Google OAuth.

```
GET /api/v1/auth/google/callback?code=<auth_code>&state=<state>
```

**Response (200 OK):**

```json
{
    "status": "success",
    "message": "Google login successful",
    "data": {
        "user": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@gmail.com",
            "role": "user",
            "oauth_provider": "google"
        },
        "tokens": {
            "access_token": "eyJhbGciOiJSUzI1NiIs...",
            "refresh_token": "eyJhbGciOiJSUzI1NiIs...",
            "token_type": "Bearer",
            "expires_in": 900
        },
        "is_new_user": true
    }
}
```

---

### 2.7 Change Password

```
PUT /api/v1/auth/password
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
    "current_password": "OldP@ss123",
    "new_password": "NewP@ss456",
    "confirm_password": "NewP@ss456"
}
```

**Response (200 OK):**

```json
{
    "status": "success",
    "message": "Password changed successfully"
}
```

---

## 3. User Management Endpoints

### 3.1 Get Current User

```
GET /api/v1/users/me
Authorization: Bearer <access_token>
```

**Response (200 OK):**

```json
{
    "status": "success",
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "role": {
            "name": "user",
            "permissions": {
                "can_read": true,
                "can_create_reading": true
            }
        },
        "is_verified": true,
        "login_count": 15,
        "last_login_at": "2025-01-15T10:30:00Z",
        "created_at": "2025-01-01T00:00:00Z"
    }
}
```

---

### 3.2 List Users (Admin Only)

```
GET /api/v1/users?page=1&per_page=20&role=user&search=john
Authorization: Bearer <access_token>
```

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `per_page` | int | 20 | Items per page (max 100) |
| `role` | string | all | Filter by role |
| `search` | string | - | Search by name/email |
| `is_active` | bool | true | Filter by active status |
| `sort_by` | string | created_at | Sort field |
| `sort_order` | string | desc | 'asc' or 'desc' |

**Response (200 OK):**

```json
{
    "status": "success",
    "data": {
        "users": [
            {
                "id": "uuid",
                "email": "user@example.com",
                "role": "user",
                "is_active": true,
                "created_at": "2025-01-01T00:00:00Z"
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 20,
            "total": 156,
            "total_pages": 8,
            "has_next": true,
            "has_prev": false
        }
    }
}
```

---

### 3.3 Update User Role (Admin Only)

```
PUT /api/v1/users/{user_id}/role
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
    "role": "tarot_reader"
}
```

---

### 3.4 Deactivate User (Admin Only)

```
DELETE /api/v1/users/{user_id}
Authorization: Bearer <access_token>
```

**Response (200 OK):**

```json
{
    "status": "success",
    "message": "User deactivated successfully"
}
```

---

## 4. Profile Management Endpoints

### 4.1 Get My Profile

```
GET /api/v1/profiles/me
Authorization: Bearer <access_token>
```

**Response (200 OK):**

```json
{
    "status": "success",
    "data": {
        "id": "uuid",
        "user_id": "uuid",
        "first_name": "John",
        "last_name": "Doe",
        "display_name": "JohnD",
        "avatar_url": "https://s3.../avatars/uuid.jpg",
        "date_of_birth": "1995-06-15",
        "age_group": "26-35",
        "gender": "male",
        "country": "India",
        "timezone": "Asia/Kolkata",
        "spiritual_interests": ["palmistry", "tarot", "astrology"],
        "spiritual_goals": ["self_discovery", "career_guidance"],
        "experience_level": "beginner",
        "preferred_spread": "three_card",
        "preferred_reading_time": "evening",
        "notification_enabled": true,
        "current_goals": [
            {
                "title": "Understand my life path",
                "category": "personal_growth",
                "status": "active"
            }
        ],
        "bio": "Exploring spirituality and personal growth through palmistry and tarot.",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-15T10:30:00Z"
    }
}
```

---

### 4.2 Create/Update Profile

```
PUT /api/v1/profiles/me
Authorization: Bearer <access_token>
```

**Request Body (all fields optional):**

```json
{
    "first_name": "John",
    "last_name": "Doe",
    "display_name": "JohnD",
    "date_of_birth": "1995-06-15",
    "age_group": "26-35",
    "gender": "male",
    "country": "India",
    "timezone": "Asia/Kolkata",
    "spiritual_interests": ["palmistry", "tarot"],
    "spiritual_goals": ["self_discovery", "career_guidance"],
    "experience_level": "beginner",
    "preferred_spread": "three_card",
    "preferred_reading_time": "evening",
    "notification_enabled": true,
    "bio": "Exploring spirituality through palmistry and tarot."
}
```

**Response (200 OK):**

```json
{
    "status": "success",
    "message": "Profile updated successfully",
    "data": { ... }
}
```

---

### 4.3 Upload Avatar

```
POST /api/v1/profiles/me/avatar
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Form Data:**
- `avatar`: Image file (jpg, png, webp; max 5MB)

**Response (200 OK):**

```json
{
    "status": "success",
    "message": "Avatar uploaded successfully",
    "data": {
        "avatar_url": "https://s3.../avatars/uuid.jpg"
    }
}
```

---

### 4.4 Manage Goals

```
POST /api/v1/profiles/me/goals
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
    "title": "Develop my intuition",
    "category": "spiritual_growth",
    "description": "I want to improve my intuitive abilities through regular practice",
    "target_date": "2025-06-01"
}
```

**Response (201 Created):**

```json
{
    "status": "success",
    "message": "Goal added successfully",
    "data": {
        "goals": [
            {
                "id": "uuid",
                "title": "Develop my intuition",
                "category": "spiritual_growth",
                "status": "active",
                "created_at": "2025-01-15T10:30:00Z"
            }
        ]
    }
}
```

---

### 4.5 Update Goal Status

```
PUT /api/v1/profiles/me/goals/{goal_id}
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
    "status": "completed"
}
```

---

## 5. Health & System Endpoints

### 5.1 Health Check

```
GET /api/v1/health
```

**Response (200 OK):**

```json
{
    "status": "healthy",
    "version": "1.0.0",
    "services": {
        "postgresql": "connected",
        "mongodb": "connected",
        "redis": "connected"
    },
    "uptime_seconds": 86400,
    "timestamp": "2025-01-15T10:30:00Z"
}
```

### 5.2 API Documentation

```
GET /docs          → Swagger UI (interactive)
GET /redoc         → ReDoc (read-only)
GET /openapi.json  → Raw OpenAPI schema
```

---

## 6. Error Handling

### Error Codes

| HTTP Code | Error Code | Description |
|-----------|-----------|-------------|
| 400 | `VALIDATION_ERROR` | Request body validation failed |
| 400 | `BAD_REQUEST` | Malformed request |
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 401 | `INVALID_CREDENTIALS` | Wrong email/password |
| 401 | `TOKEN_EXPIRED` | Access token has expired |
| 403 | `FORBIDDEN` | Insufficient permissions |
| 403 | `ACCOUNT_DISABLED` | Account is deactivated |
| 404 | `NOT_FOUND` | Resource not found |
| 409 | `CONFLICT` | Resource already exists (e.g., duplicate email) |
| 422 | `UNPROCESSABLE_ENTITY` | Semantically invalid request |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server-side error |

### Error Response Example

```json
{
    "status": "error",
    "message": "Validation failed",
    "error": {
        "code": "VALIDATION_ERROR",
        "details": [
            {
                "field": "password",
                "message": "Password must be at least 8 characters",
                "type": "min_length"
            },
            {
                "field": "email",
                "message": "Invalid email format",
                "type": "invalid_format"
            }
        ]
    },
    "meta": {
        "timestamp": "2025-01-15T10:30:00Z",
        "request_id": "req_abc123"
    }
}
```

---

## 7. Rate Limiting

### Default Limits

| Endpoint Category | Limit | Window |
|-------------------|-------|--------|
| Auth (login/register) | 10 requests | 1 minute |
| General API | 100 requests | 1 minute |
| File uploads | 10 requests | 5 minutes |
| Admin endpoints | 200 requests | 1 minute |

### Rate Limit Headers

Every response includes these headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705312200
```

---

## 8. Authentication Guide

### Token Lifecycle

```
1. User registers/logs in → receives access_token (15min) + refresh_token (7 days)
2. Client stores refresh_token securely (httpOnly cookie or secure storage)
3. Client sends access_token in Authorization header for API calls
4. When access_token expires (401), client uses refresh_token to get new access_token
5. When refresh_token expires, user must log in again
6. On logout, both tokens are invalidated
```

### JWT Payload Structure

```json
{
    "sub": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "role": "user",
    "type": "access",
    "iat": 1705312200,
    "exp": 1705313100,
    "jti": "unique-token-id"
}
```

### Using the API with cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test@123","confirm_password":"Test@123","first_name":"Test","last_name":"User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test@123"}'

# Access protected endpoint
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..."

# Refresh token
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"eyJhbGciOiJSUzI1NiIs..."}'
```

---

## Endpoint Summary Table

| Method | Endpoint | Auth | Roles | Description |
|--------|----------|------|-------|-------------|
| POST | `/auth/register` | ❌ | - | Register new user |
| POST | `/auth/login` | ❌ | - | Login |
| POST | `/auth/refresh` | ❌ | - | Refresh token |
| POST | `/auth/logout` | ✅ | All | Logout |
| GET | `/auth/google` | ❌ | - | Google OAuth redirect |
| GET | `/auth/google/callback` | ❌ | - | Google OAuth callback |
| PUT | `/auth/password` | ✅ | All | Change password |
| GET | `/users/me` | ✅ | All | Get current user |
| GET | `/users` | ✅ | Admin | List all users |
| PUT | `/users/{id}/role` | ✅ | Admin | Update user role |
| DELETE | `/users/{id}` | ✅ | Admin | Deactivate user |
| GET | `/profiles/me` | ✅ | All | Get my profile |
| PUT | `/profiles/me` | ✅ | All | Update my profile |
| POST | `/profiles/me/avatar` | ✅ | All | Upload avatar |
| POST | `/profiles/me/goals` | ✅ | All | Add goal |
| PUT | `/profiles/me/goals/{id}` | ✅ | All | Update goal |
| GET | `/health` | ❌ | - | Health check |
