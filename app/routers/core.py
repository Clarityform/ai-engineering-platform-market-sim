import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Repository, Branch, Task, PullRequest, Environment, Deployment, AIPlan, User
from app.schemas import (
    RepositoryCreate,
    RepositoryOut,
    BranchCreate,
    BranchOut,
    TaskCreate,
    TaskUpdate,
    TaskOut,
    PullRequestCreate,
    PullRequestOut,
    EnvironmentCreate,
    EnvironmentOut,
    DeploymentCreate,
    DeploymentOut,
    AIAnalyzeIn,
    AIPlanOut,
)
from app.auth import current_user, require_roles
from app.ai_engine import analyze
from app.services import readiness_score, deployment_decision

router = APIRouter(prefix="/api", tags=["engineering"])


@router.get("/repositories", response_model=list[RepositoryOut])
async def list_repositories(db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    return list((await db.scalars(select(Repository).order_by(Repository.id.desc()))).all())


@router.post("/repositories", response_model=RepositoryOut, status_code=201)
async def create_repository(
    payload: RepositoryCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("ADMIN", "DEVELOPER")),
):
    obj = Repository(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.post("/branches", response_model=BranchOut, status_code=201)
async def create_branch(payload: BranchCreate, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    if not await db.get(Repository, payload.repository_id):
        raise HTTPException(404, "Repository not found")
    obj = Branch(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/branches", response_model=list[BranchOut])
async def list_branches(
    repository_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
):
    q = select(Branch)
    if repository_id is not None:
        q = q.where(Branch.repository_id == repository_id)
    return list((await db.scalars(q.order_by(Branch.id.desc()))).all())


@router.get("/tasks", response_model=list[TaskOut])
async def list_tasks(db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    return list((await db.scalars(select(Task).order_by(Task.id.desc()))).all())


@router.post("/tasks", response_model=TaskOut, status_code=201)
async def create_task(
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("ADMIN", "DEVELOPER")),
):
    if payload.repository_id and not await db.get(Repository, payload.repository_id):
        raise HTTPException(404, "Repository not found")
    obj = Task(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch("/tasks/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("ADMIN", "DEVELOPER")),
):
    obj = await db.get(Task, task_id)
    if not obj:
        raise HTTPException(404, "Task not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.post("/pull-requests", response_model=PullRequestOut, status_code=201)
async def create_pr(payload: PullRequestCreate, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    if not await db.get(Repository, payload.repository_id):
        raise HTTPException(404, "Repository not found")
    if await db.scalar(
        select(PullRequest.id).where(
            PullRequest.repository_id == payload.repository_id,
            PullRequest.number == payload.number,
        )
    ):
        raise HTTPException(409, "PR number already exists for repository")
    obj = PullRequest(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/pull-requests", response_model=list[PullRequestOut])
async def list_prs(db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    return list((await db.scalars(select(PullRequest).order_by(PullRequest.id.desc()))).all())


@router.post("/environments", response_model=EnvironmentOut, status_code=201)
async def create_environment(
    payload: EnvironmentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("ADMIN", "DEVELOPER")),
):
    obj = Environment(**payload.model_dump())
    db.add(obj)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(409, "Environment name already exists")
    await db.refresh(obj)
    return obj


@router.get("/environments", response_model=list[EnvironmentOut])
async def list_environments(db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    return list((await db.scalars(select(Environment).order_by(Environment.id))).all())


@router.post("/deployments", response_model=DeploymentOut, status_code=201)
async def create_deployment(
    payload: DeploymentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("ADMIN", "DEVELOPER")),
):
    env = await db.get(Environment, payload.environment_id)
    repo = await db.get(Repository, payload.repository_id)
    if not env or not repo:
        raise HTTPException(404, "Environment or repository not found")
    score = readiness_score(payload.coverage, payload.risk, payload.compliance, payload.health)
    obj = Deployment(
        **payload.model_dump(),
        readiness_score=score,
        status=deployment_decision(score, env.protected, env.requires_approval),
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/deployments", response_model=list[DeploymentOut])
async def list_deployments(db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    return list((await db.scalars(select(Deployment).order_by(Deployment.id.desc()))).all())


@router.post("/ai/analyze", response_model=AIPlanOut, status_code=201)
async def ai_analyze(payload: AIAnalyzeIn, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    result = analyze(payload.text)
    obj = AIPlan(
        title=payload.title,
        input_text=payload.text,
        summary=result["summary"],
        risks_json=json.dumps(result["risks"]),
        recommendations_json=json.dumps(result["recommendations"]),
        provider="HEURISTIC_LOCAL",
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/ai/plans", response_model=list[AIPlanOut])
async def list_ai_plans(db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    return list((await db.scalars(select(AIPlan).order_by(AIPlan.id.desc()))).all())


@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    async def count(model):
        return await db.scalar(select(func.count()).select_from(model)) or 0

    return {
        "repositories": await count(Repository),
        "branches": await count(Branch),
        "tasks": await count(Task),
        "pull_requests": await count(PullRequest),
        "environments": await count(Environment),
        "deployments": await count(Deployment),
        "ai_plans": await count(AIPlan),
        "mode": "LOCAL_PROTOTYPE",
    }
