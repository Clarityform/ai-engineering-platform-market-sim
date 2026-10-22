from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.store import store

app = FastAPI(title="AI Engineering Platform", version="0.2.0")


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse(
        """
        <html>
          <head><title>AI Engineering Platform</title></head>
          <body>
            <h1>AI Engineering Platform</h1>
            <ul>
              <li><a href="/health">/health</a></li>
              <li><a href="/metrics">/metrics</a></li>
              <li><a href="/repos">/repos</a></li>
              <li><a href="/issues">/issues</a></li>
              <li><a href="/pulls">/pulls</a></li>
              <li><a href="/tasks">/tasks</a></li>
            </ul>
          </body>
        </html>
        """
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "ai-engineering-platform"}


@app.get("/ready")
def ready() -> dict:
    return {"status": "ready", "service": "ai-engineering-platform"}


@app.get("/metrics")
def metrics() -> dict:
    return store.health_metrics()


@app.get("/repos")
def list_repos() -> list:
    return store.list_repos()


@app.post("/repos")
def create_repo(owner: str, name: str, visibility: str = "private", description: str | None = None) -> dict:
    return store.create_repo(owner=owner, name=name, visibility=visibility, description=description)


@app.get("/repos/{repo_id}")
def get_repo(repo_id: str) -> dict:
    repo = store.get_repo(repo_id)
    if repo is None:
        raise ValueError("repo not found")
    return repo


@app.get("/issues")
def list_issues() -> list:
    return store.list_issues()


@app.post("/issues")
def create_issue(repo_id: str, title: str, body: str | None = None) -> dict:
    return store.create_issue(repo_id=repo_id, title=title, body=body)


@app.get("/pulls")
def list_pull_requests() -> list:
    return store.list_pull_requests()


@app.post("/pulls")
def create_pull_request(repo_id: str, title: str, source_branch: str, target_branch: str, body: str | None = None) -> dict:
    return store.create_pull_request(
        repo_id=repo_id,
        title=title,
        source_branch=source_branch,
        target_branch=target_branch,
        body=body,
    )


@app.get("/tasks")
def list_tasks() -> list:
    return store.list_tasks()


@app.post("/tasks")
def create_task(repo_id: str, title: str, description: str) -> dict:
    return store.create_task(repo_id=repo_id, title=title, description=description)


@app.get("/ai/plans")
def list_ai_plans() -> list:
    return store.list_ai_plans()


@app.post("/ai/plan")
def create_ai_plan(repo_id: str, task_title: str, description: str) -> dict:
    return store.create_ai_plan(repo_id=repo_id, task_title=task_title, description=description)


@app.post("/ai/summarize")
def summarize(repo_id: str, title: str) -> dict:
    return store.summarize(repo_id=repo_id, title=title)
