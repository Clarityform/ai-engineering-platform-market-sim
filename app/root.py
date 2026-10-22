from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router

app = FastAPI(title="AI Engineering Platform", version="0.5.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/")
def index() -> dict:
    return {
        "name": "AI Engineering Platform",
        "status": "prototype",
        "version": "0.5.0",
        "routes": [
            "/api/health",
            "/api/metrics",
            "/api/dashboard/overview",
            "/api/analytics/release-readiness",
            "/api/repos",
            "/api/issues",
            "/api/pulls",
            "/api/tasks",
            "/api/ai/plans",
            "/api/projects",
            "/api/releases",
            "/api/environments",
            "/api/policies",
        ],
    }
