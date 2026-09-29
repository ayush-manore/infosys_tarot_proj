"""
FastAPI Main Application Entry Point
====================================
Configures middleware, routes, lifespan handlers (DB initialization),
and error handlers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

from app.config import settings
from app.database import init_postgres, close_postgres, mongodb, redis_manager
from app.routers import auth, users, profiles, datasets, readings, analytics, reports, notifications, ai


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initializes database tables and connection pools on startup,
    and cleanly closes connections on shutdown.
    """
    # Startup actions
    print(f"[START] Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    try:
        await init_postgres()
        print("[OK] PostgreSQL connected and tables initialized.")
    except Exception as e:
        print(f"[WARN] PostgreSQL warning: {e}")

    try:
        mongodb.connect()
        print("[OK] MongoDB connected.")
    except Exception as e:
        print(f"[WARN] MongoDB warning: {e}")

    try:
        await redis_manager.connect()
        print("[OK] Redis connected.")
    except Exception as e:
        print(f"[WARN] Redis warning: {e}")

    yield

    # Shutdown actions
    print("[STOP] Shutting down services...")
    await close_postgres()
    mongodb.close()
    await redis_manager.close()
    print("[DONE] Shutdown complete.")


# Create FastAPI instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Palmistry & Tarot Intelligence Platform API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API Routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(profiles.router, prefix=settings.API_V1_PREFIX)
app.include_router(datasets.router, prefix=settings.API_V1_PREFIX)
app.include_router(readings.router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX)
app.include_router(reports.router, prefix=settings.API_V1_PREFIX)
app.include_router(notifications.router, prefix=settings.API_V1_PREFIX)
app.include_router(ai.router, prefix=settings.API_V1_PREFIX)


# System Health Check Endpoint
@app.get("/api/v1/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "timestamp": time.time()
    }


@app.get("/", tags=["System"])
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "docs": "/docs",
        "health": "/api/v1/health"
    }
