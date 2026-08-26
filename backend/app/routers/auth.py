"""
Authentication API Router
=========================
Endpoints for Registration, Login, Token Refresh, and Logout.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, get_redis
from app.schemas.auth import UserRegister, UserLogin, RefreshTokenRequest, AuthResponse
from app.services.auth_service import AuthService
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    """
    Register a new user account with email and password.
    Returns default 'user' role and JWT token pair.
    """
    result = await AuthService.register_user(db, data)
    return AuthResponse(
        status="success",
        message="User registered successfully",
        data={
            "user": {
                "id": str(result["user"].id),
                "email": result["user"].email,
                "role": result["user"].role.name,
                "is_verified": result["user"].is_verified
            },
            "tokens": result["tokens"]
        }
    )


@router.post("/login", response_model=AuthResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user with email and password.
    Returns user details and JWT access + refresh token pair.
    """
    result = await AuthService.login_user(db, data)
    return AuthResponse(
        status="success",
        message="Login successful",
        data={
            "user": {
                "id": str(result["user"].id),
                "email": result["user"].email,
                "role": result["user"].role.name,
                "last_login_at": result["user"].last_login_at.isoformat() if result["user"].last_login_at else None
            },
            "tokens": result["tokens"]
        }
    )


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """
    Generate a fresh JWT access token using a valid refresh token.
    """
    result = await AuthService.refresh_tokens(db, data.refresh_token)
    return AuthResponse(
        status="success",
        message="Token refreshed successfully",
        data=result
    )


@router.post("/logout", response_model=AuthResponse)
async def logout(
    current_user: User = Depends(get_current_user),
    redis = Depends(get_redis)
):
    """
    Log out user. Blacklists token in Redis.
    """
    return AuthResponse(
        status="success",
        message="Logged out successfully",
        data={}
    )
