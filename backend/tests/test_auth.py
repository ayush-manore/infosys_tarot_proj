"""
Authentication Endpoint Tests
==============================
Tests for registration, login, and token management.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4


class TestAuthEndpoints:
    """Tests for auth API endpoints."""

    def test_password_hashing(self):
        """Test bcrypt password hashing and verification."""
        from app.utils.security import hash_password, verify_password

        password = "test_password_123"
        hashed = hash_password(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False

    def test_jwt_token_creation(self):
        """Test JWT token creation and decoding."""
        from app.utils.security import create_access_token, decode_token

        payload = {"sub": str(uuid4()), "role": "user"}
        token = create_access_token(payload)

        assert token is not None
        assert isinstance(token, str)

        decoded = decode_token(token)
        assert decoded is not None
        assert decoded["sub"] == payload["sub"]
        assert decoded["role"] == payload["role"]

    def test_jwt_token_expiry(self):
        """Test that JWT tokens contain expiry field."""
        from app.utils.security import create_access_token, decode_token

        payload = {"sub": str(uuid4())}
        token = create_access_token(payload)
        decoded = decode_token(token)

        assert "exp" in decoded

    def test_invalid_token_decoding(self):
        """Test that invalid tokens are rejected."""
        from app.utils.security import decode_token

        result = decode_token("invalid.token.string")
        assert result is None

    def test_registration_payload_validation(self):
        """Test that registration schema validates required fields."""
        from app.schemas.auth import UserRegister

        # Valid payload
        valid = UserRegister(
            email="test@example.com",
            password="securepassword123",
            confirm_password="securepassword123",
        )
        assert valid.email == "test@example.com"

    def test_login_payload_validation(self):
        """Test that login schema validates required fields."""
        from app.schemas.auth import UserLogin

        valid = UserLogin(
            email="test@example.com",
            password="password123",
        )
        assert valid.email == "test@example.com"
