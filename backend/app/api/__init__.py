"""API module with routes."""

from .logs import router as logs_router
from .incidents import router as incidents_router

__all__ = ["logs_router", "incidents_router"]
