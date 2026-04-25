"""
Main FastAPI application entry point.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core import get_settings, setup_logging
from app.db import init_db
from app.api import logs_router, incidents_router

# Setup logging
settings = get_settings()
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger("incident_manager.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI startup/shutdown."""
    # Startup
    logger.info(
        "Starting application",
        extra={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "debug": settings.DEBUG,
        }
    )
    init_db()
    logger.info("Database initialized")

    yield

    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-grade AI-powered Incident Management System",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(logs_router)
app.include_router(incidents_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method,
        }
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
