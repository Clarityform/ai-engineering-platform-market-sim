from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Request

from app.auth import authenticate, verify_token
from app.store import store

router = APIRouter(prefix="/api")


@router.post("/auth/login")
def login(username: str, password: str) -> dict:
    user = authenticate(username, password)
    if user is None:
        raise HTTPException(status_code=401, detail="invalid username or password")
    return {"token": __import__("app.auth", fromlist=["create_token"]).create_token(username), "user": user}


@router.get("/auth/me")
def me(request: Request) -> dict:
    auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")

    token = auth_header.split(" ", 1)[1]
    try:
        payload = verify_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="invalid token payload")

    return {"user": {"username": username, "role": payload.get("role", "member")}}


@router.get("/dashboard/summary")
def dashboard_summary() -> dict:
    metrics = store.health_metrics()
    repos = store.list_repos()
    tasks = store.list_tasks()
    plans = store.list_ai_plans()
    return {
        "metrics": metrics,
        "repo_count": len(repos),
        "task_count": len(tasks),
        "plan_count": len(plans),
        "status": "operational",
        "feature_flags": {
            "repos": True,
            "issues": True,
            "pull_requests": True,
            "ai_planning": True,
            "security": False,
            "enterprise": False,
        },
    }
