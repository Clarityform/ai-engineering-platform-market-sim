from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import app as api_app

app = FastAPI(title="AI Engineering Platform", version="0.3.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api", api_app)


@app.get("/")
def index() -> dict:
    return {
        "name": "AI Engineering Platform",
        "status": "prototype",
        "routes": [
            "/api/health",
            "/api/metrics",
            "/api/repos",
            "/api/issues",
            "/api/pulls",
            "/api/tasks",
            "/api/ai/plans",
        ],
    }
