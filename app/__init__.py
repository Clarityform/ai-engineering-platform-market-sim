from __future__ import annotations

from app.auth_routes import router as auth_router
from app.routes import router as api_router

__all__ = ["api_router", "auth_router"]
