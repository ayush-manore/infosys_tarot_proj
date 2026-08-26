"""
Database Connection Manager
===========================
Sets up connections to all three data stores:
1. PostgreSQL (via SQLAlchemy async) — structured data
2. MongoDB (via Motor async) — document data  
3. Redis (via redis-py async) — cache & sessions

Each connection is managed as a singleton and provides
async context managers for clean resource management.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from app.config import settings


# =============================================================================
# SQLAlchemy Base Model
# =============================================================================

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    
    All models inherit from this class:
        class User(Base):
            __tablename__ = "users"
            ...
    
    This is the "declarative base" pattern — it automatically tracks
    all model classes and their table definitions.
    """
    pass


# =============================================================================
# PostgreSQL Connection (SQLAlchemy Async)
# =============================================================================

# Create the async engine — this manages the connection pool
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_size=20,         # Max connections in the pool
    max_overflow=10,      # Extra connections allowed above pool_size
    pool_timeout=30,      # Seconds to wait for a connection from pool
    pool_recycle=1800,    # Recycle connections after 30 minutes
)

# Create a session factory — sessions are individual database conversations
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit (useful for returning data)
)


async def get_db():
    """
    FastAPI dependency that provides a database session.
    
    Usage in routes:
        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    
    The session is automatically committed on success and
    rolled back on error (via the try/except).
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_postgres():
    """Create all tables defined in models. Run once at startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_postgres():
    """Close the connection pool. Run once at shutdown."""
    await engine.dispose()


# =============================================================================
# MongoDB Connection (Motor Async)
# =============================================================================

class MongoDB:
    """
    MongoDB connection manager using Motor (async driver).
    
    Motor wraps PyMongo and makes it non-blocking, which is
    essential for use with FastAPI's async handlers.
    
    Usage:
        db = mongodb.get_db()
        result = await db.palm_analyses.find_one({"user_id": "..."})
    """
    client: AsyncIOMotorClient = None
    
    def connect(self):
        """Initialize the MongoDB client."""
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    def get_db(self):
        """Get the database instance."""
        return self.client[settings.MONGODB_DB]
    
    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()


# Singleton instance
mongodb = MongoDB()


async def get_mongodb():
    """FastAPI dependency for MongoDB database access."""
    return mongodb.get_db()


# =============================================================================
# Redis Connection (Async)
# =============================================================================

class RedisManager:
    """
    Redis connection manager for caching and session management.
    
    Redis stores:
    - JWT token blacklist (for logout)
    - Rate limiting counters
    - Session cache
    - Temporary data
    """
    client: Redis = None
    
    async def connect(self):
        """Initialize the Redis client."""
        self.client = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,  # Auto-decode bytes to strings
        )
    
    async def close(self):
        """Close the Redis connection."""
        if self.client:
            await self.client.close()


# Singleton instance
redis_manager = RedisManager()


async def get_redis() -> Redis:
    """FastAPI dependency for Redis access."""
    return redis_manager.client
