from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.store import store

router = APIRouter(prefix="/api")


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "ai-engineering-platform"}


@router.get("/ready")
def ready() -> dict:
    return {"status": "ready", "service": "ai-engineering-platform"}


@router.get("/metrics")
def metrics() -> dict:
    return store.health_metrics()


@router.get("/repos")
def list_repos() -> list:
    return store.list_repos()


@router.post("/repos")
def create_repo(owner: str, name: str, visibility: str = "private", description: str | None = None) -> dict:
    if not owner or not name:
        raise HTTPException(status_code=400, detail="owner and name are required")
    return store.create_repo(owner=owner, name=name, visibility=visibility, description=description)


@router.get("/repos/{repo_id}")
def get_repo(repo_id: str) -> dict:
    repo = store.get_repo(repo_id)
    if repo is None:
        raise HTTPException(status_code=404, detail="repo not found")
    return repo


@router.get("/issues")
def list_issues() -> list:
    return store.list_issues()


@router.post("/issues")
def create_issue(repo_id: str, title: str, body: str | None = None) -> dict:
    if not repo_id or not title:
        raise HTTPException(status_code=400, detail="repo_id and title are required")
    return store.create_issue(repo_id=repo_id, title=title, body=body)


@router.get("/pulls")
def list_pull_requests() -> list:
    return store.list_pull_requests()


@router.post("/pulls")
def create_pull_request(repo_id: str, title: str, source_branch: str, target_branch: str, body: str | None = None) -> dict:
    if not repo_id or not title or not source_branch or not target_branch:
        raise HTTPException(status_code=400, detail="repo_id, title, source_branch, and target_branch are required")
    return store.create_pull_request(
        repo_id=repo_id,
        title=title,
        source_branch=source_branch,
        target_branch=target_branch,
        body=body,
    )


@router.get("/tasks")
def list_tasks() -> list:
    return store.list_tasks()


@router.post("/tasks")
def create_task(repo_id: str, title: str, description: str) -> dict:
    if not repo_id or not title or not description:
        raise HTTPException(status_code=400, detail="repo_id, title, and description are required")
    return store.create_task(repo_id=repo_id, title=title, description=description)


@router.get("/ai/plans")
def list_ai_plans() -> list:
    return store.list_ai_plans()


@router.post("/ai/plan")
def create_ai_plan(repo_id: str, task_title: str, description: str) -> dict:
    if not repo_id or not task_title or not description:
        raise HTTPException(status_code=400, detail="repo_id, task_title, and description are required")
    return store.create_ai_plan(repo_id=repo_id, task_title=task_title, description=description)


@router.post("/ai/summarize")
def summarize(repo_id: str, title: str) -> dict:
    if not repo_id or not title:
        raise HTTPException(status_code=400, detail="repo_id and title are required")
    return store.summarize(repo_id=repo_id, title=title)


@router.get("/projects")
def list_projects() -> list:
    return store.list_projects()


@router.post("/projects")
def create_project(name: str, repo_id: str, owner: str, description: str | None = None) -> dict:
    if not name or not repo_id or not owner:
        raise HTTPException(status_code=400, detail="name, repo_id, and owner are required")
    return store.create_project(name=name, repo_id=repo_id, owner=owner, description=description)


@router.get("/releases")
def list_releases() -> list:
    return store.list_releases()


@router.post("/releases")
def create_release(project_id: str, version: str, status: str = "planned", notes: str | None = None) -> dict:
    if not project_id or not version:
        raise HTTPException(status_code=400, detail="project_id and version are required")
    return store.create_release(project_id=project_id, version=version, status=status, notes=notes)


@router.get("/environments")
def list_environments() -> list:
    return store.list_environments()


@router.post("/environments")
def create_environment(name: str, stage: str, url: str, status: str = "active") -> dict:
    if not name or not stage or not url:
        raise HTTPException(status_code=400, detail="name, stage, and url are required")
    return store.create_environment(name=name, stage=stage, url=url, status=status)


@router.get("/policies")
def list_policies() -> list:
    return store.list_policies()


@router.post("/policies")
def create_policy(name: str, kind: str, rules: str) -> dict:
    if not name or not kind or not rules:
        raise HTTPException(status_code=400, detail="name, kind, and rules are required")
    return store.create_policy(name=name, kind=kind, rules=rules)
