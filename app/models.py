from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RepoCreate(BaseModel):
    owner: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    visibility: str = Field(default="private")
    description: Optional[str] = None


class Repo(BaseModel):
    id: str
    owner: str
    name: str
    visibility: str
    default_branch: str = "main"
    description: Optional[str] = None


class IssueCreate(BaseModel):
    repo_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    body: Optional[str] = None


class Issue(BaseModel):
    id: str
    repo_id: str
    title: str
    body: str = ""
    state: str = "open"


class PullRequestCreate(BaseModel):
    repo_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    source_branch: str = Field(..., min_length=1)
    target_branch: str = Field(..., min_length=1)
    body: Optional[str] = None


class PullRequest(BaseModel):
    id: str
    repo_id: str
    title: str
    source_branch: str
    target_branch: str
    body: str = ""
    state: str = "open"


class TaskCreate(BaseModel):
    repo_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class Task(BaseModel):
    id: str
    repo_id: str
    title: str
    description: str
    status: str = "queued"


class AIPlanCreate(BaseModel):
    repo_id: str = Field(..., min_length=1)
    task_title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class AIPlan(BaseModel):
    id: str
    repo_id: str
    task_title: str
    description: str
    steps: List[str]
    risk_score: float
    confidence: float


class SummaryRequest(BaseModel):
    repo_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)


class SummaryResult(BaseModel):
    repo_id: str
    repo_name: str
    title: str
    summary: str
    risk_level: str
    delivery_score: int
