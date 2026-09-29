"""
Authentication Service
======================
Handles business logic for user registration, authentication, token refreshing,
password management, and OAuth2 Google integration.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.user import User
from app.models.role import Role
from app.models.profile import UserProfile
from app.schemas.auth import UserRegister, UserLogin
from app.utils.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)


class AuthService:
    @staticmethod
    async def register_user(db: AsyncSession, data: UserRegister) -> dict:
        """Register a new user account with default 'user' role and profile."""
        # 1. Check if email already exists
        existing_user = await db.execute(select(User).where(User.email == data.email))
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email address is already registered"
            )

        # 2. Get or create the selected role
        selected_role_name = data.role or "user"
        role_result = await db.execute(select(Role).where(Role.name == selected_role_name))
        user_role = role_result.scalar_one_or_none()

        if not user_role:
            # Fallback: create the role if it doesn't exist
            user_role = Role(
                name=selected_role_name,
                description=f"{selected_role_name.replace('_', ' ').title()} role",
                permissions={"can_read": True, "can_create_reading": True, "role": selected_role_name}
            )
            db.add(user_role)
            await db.flush()

        # 3. Create user record
        new_user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            role_id=user_role.id,
            is_active=True,
            is_verified=False
        )
        db.add(new_user)
        await db.flush()

        # 4. Create associated user profile
        new_profile = UserProfile(
            user_id=new_user.id,
            first_name=data.first_name,
            last_name=data.last_name,
            display_name=f"{data.first_name} {data.last_name}".strip() if data.first_name else data.email.split('@')[0],
            spiritual_interests=["palmistry", "tarot"],
            spiritual_goals=["self_discovery"]
        )
        db.add(new_profile)
        await db.commit()

        # Re-query user with role
        res = await db.execute(
            select(User).options(joinedload(User.role)).where(User.id == new_user.id)
        )
        user_loaded = res.scalar_one()

        # 5. Generate tokens
        token_data = {"sub": str(user_loaded.id), "email": user_loaded.email, "role": user_loaded.role.name}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return {
            "user": user_loaded,
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": 900
            }
        }

    @staticmethod
    async def login_user(db: AsyncSession, data: UserLogin) -> dict:
        """Authenticate user credentials and return JWT token pair."""
        res = await db.execute(
            select(User).options(joinedload(User.role)).where(User.email == data.email)
        )
        user = res.scalar_one_or_none()

        if not user or not user.password_hash or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account has been deactivated"
            )

        # Update login metadata
        user.last_login_at = datetime.now(timezone.utc)
        user.login_count += 1
        await db.commit()

        token_payload = {"sub": str(user.id), "email": user.email, "role": user.role.name}
        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)

        return {
            "user": user,
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": 900
            }
        }

    @staticmethod
    async def refresh_tokens(db: AsyncSession, refresh_token: str) -> dict:
        """Issue new access token from valid refresh token."""
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        user_id = payload.get("sub")
        res = await db.execute(
            select(User).options(joinedload(User.role)).where(User.id == user_id)
        )
        user = res.scalar_one_or_none()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        token_payload = {"sub": str(user.id), "email": user.email, "role": user.role.name}
        new_access_token = create_access_token(token_payload)

        return {
            "access_token": new_access_token,
            "token_type": "Bearer",
            "expires_in": 900
        }
