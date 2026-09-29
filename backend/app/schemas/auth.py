"""
User & Auth Pydantic Schemas
===========================
Data validation and serialization shapes for Users and Authentication.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ==========================================
# Auth Request & Response Schemas
# ==========================================

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    confirm_password: str
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[str] = Field("user", description="User role: user, tarot_reader, spiritual_consultant, admin")

    @field_validator('role')
    def validate_role(cls, v):
        allowed = ['user', 'tarot_reader', 'spiritual_consultant', 'admin']
        if v and v not in allowed:
            raise ValueError(f'Role must be one of: {", ".join(allowed)}')
        return v or 'user'

    @field_validator('confirm_password')
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str

    @field_validator('confirm_password')
    def passwords_match(cls, v, info):
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('New passwords do not match')
        return v


# ==========================================
# Token Output Schemas
# ==========================================

class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 900  # 15 minutes in seconds


class TokenPayload(BaseModel):
    sub: str
    email: str
    role: str
    type: str
    exp: int
    iat: int
    jti: str


# ==========================================
# User Response Schemas
# ==========================================

class RoleResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    permissions: dict = {}

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: UUID
    email: str
    role: RoleResponse
    oauth_provider: Optional[str] = None
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime] = None
    login_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    status: str = "success"
    message: str
    data: dict
