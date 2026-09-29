"""
Database Connection Manager
===========================
Sets up connections to all data stores:
1. Primary Relational DB: PostgreSQL (or automatic local SQLite fallback with aiosqlite)
2. Document Store: MongoDB (via Motor async)
3. Cache & Sessions: Redis (with in-memory fallback)

Each connection is resilient to offline services for seamless local development.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.future import select
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
import os
import asyncio
from typing import Optional

from app.config import settings


# =============================================================================
# SQLAlchemy Base Model
# =============================================================================

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    Automatically tracks model classes and table definitions.
    """
    pass


# =============================================================================
# Relational Database Connection (PostgreSQL with SQLite Fallback)
# =============================================================================

def _build_engine(url: str):
    is_sqlite = url.startswith("sqlite")
    if is_sqlite:
        return create_async_engine(
            url,
            echo=settings.DEBUG,
            connect_args={"check_same_thread": False},
        )
    return create_async_engine(
        url,
        echo=settings.DEBUG,
        pool_size=20,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
    )


# Active engine and session factory
engine = _build_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    """
    FastAPI dependency providing an active database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_postgres():
    """
    Create tables and seed default roles.
    Falls back to SQLite if PostgreSQL connection fails.
    """
    global engine, AsyncSessionLocal

    # Test primary engine connection
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("[OK] Database connected and tables created successfully.")
    except Exception as e:
        print(f"[WARN] Primary database connection failed ({e}). Falling back to local SQLite...")
        sqlite_url = "sqlite+aiosqlite:///./palmistry_tarot.db"
        engine = _build_engine(sqlite_url)
        AsyncSessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print(f"[OK] Fallback SQLite database initialized at ./palmistry_tarot.db")

    # Seed default roles if needed
    try:
        from app.models.role import Role
        async with AsyncSessionLocal() as session:
            role_definitions = [
                ("user", "Regular platform user — Seeker", {
                    "can_read": True,
                    "can_create_reading": True,
                    "can_view_own_history": True,
                    "can_upload_palm_image": True,
                    "can_submit_feedback": True,
                    "role": "user",
                }),
                ("tarot_reader", "Tarot reading specialist", {
                    "can_read": True,
                    "can_create_reading": True,
                    "can_view_own_history": True,
                    "can_upload_palm_image": True,
                    "can_submit_feedback": True,
                    "can_interpret_readings": True,
                    "can_view_client_history": True,
                    "can_manage_spreads": True,
                    "role": "tarot_reader",
                }),
                ("spiritual_consultant", "Professional palmist and spiritual guide", {
                    "can_read": True,
                    "can_create_reading": True,
                    "can_view_own_history": True,
                    "can_upload_palm_image": True,
                    "can_submit_feedback": True,
                    "can_interpret_readings": True,
                    "can_view_client_history": True,
                    "can_manage_spreads": True,
                    "can_perform_palm_analysis": True,
                    "can_generate_reports": True,
                    "can_consult_clients": True,
                    "role": "spiritual_consultant",
                }),
                ("admin", "Platform administrator with full access", {
                    "can_read": True,
                    "can_create_reading": True,
                    "can_view_own_history": True,
                    "can_upload_palm_image": True,
                    "can_submit_feedback": True,
                    "can_interpret_readings": True,
                    "can_view_client_history": True,
                    "can_manage_spreads": True,
                    "can_perform_palm_analysis": True,
                    "can_generate_reports": True,
                    "can_consult_clients": True,
                    "can_manage_users": True,
                    "can_view_analytics": True,
                    "can_manage_roles": True,
                    "can_manage_datasets": True,
                    "role": "admin",
                }),
            ]
            for role_name, desc, perms in role_definitions:
                res = await session.execute(select(Role).where(Role.name == role_name))
                existing = res.scalar_one_or_none()
                if not existing:
                    session.add(Role(
                        name=role_name,
                        description=desc,
                        permissions=perms,
                    ))
                else:
                    # Update existing role permissions and description
                    existing.description = desc
                    existing.permissions = perms
            await session.commit()
            print("[OK] Default system roles verified/seeded with granular permissions.")
    except Exception as e:
        print(f"[WARN] Role seeding note: {e}")


async def close_postgres():
    """Close the database connection pool."""
    if engine:
        await engine.dispose()


# =============================================================================
# MongoDB Connection (Motor Async)
# =============================================================================

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None

    def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=2000)
        except Exception as e:
            print(f"[WARN] MongoDB init warning: {e}")
            self.client = None

    def get_db(self):
        if self.client:
            return self.client[settings.MONGODB_DB]
        return None

    def close(self):
        if self.client:
            self.client.close()


mongodb = MongoDB()


async def get_mongodb():
    """FastAPI dependency for MongoDB database access."""
    return mongodb.get_db()


# =============================================================================
# Redis Connection with In-Memory Fallback
# =============================================================================

class InMemoryCache:
    """Lightweight in-memory cache fallback when Redis is offline."""
    def __init__(self):
        self._store = {}

    async def get(self, key: str):
        return self._store.get(key)

    async def setex(self, key: str, time: int, value: str):
        self._store[key] = value

    async def delete(self, key: str):
        self._store.pop(key, None)

    async def close(self):
        self._store.clear()


class RedisManager:
    client = None

    async def connect(self):
        try:
            r = Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=2,
            )
            # Test ping
            await r.ping()
            self.client = r
            print("[OK] Redis connected successfully.")
        except Exception:
            print("[INFO] Redis server not detected. Using fast in-memory cache fallback.")
            self.client = InMemoryCache()

    async def close(self):
        if self.client:
            await self.client.close()


redis_manager = RedisManager()


async def get_redis():
    """FastAPI dependency for Redis access."""
    return redis_manager.client
