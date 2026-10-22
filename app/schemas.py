from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Role = Literal["ADMIN", "DEVELOPER", "VIEWER"]
TaskStatus = Literal["BACKLOG", "READY", "IN_PROGRESS", "BLOCKED", "DONE"]
Priority = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    role: Role = "DEVELOPER"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: str
    created_at: datetime


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RepositoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    provider: str = "LOCAL"
    external_url: str | None = None
    default_branch: str = "main"
    description: str = ""


class RepositoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    provider: str
    external_url: str | None
    default_branch: str
    description: str


class BranchCreate(BaseModel):
    repository_id: int
    name: str
    protected: bool = False
    head_sha: str | None = None


class BranchOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    repository_id: int
    name: str
    protected: bool
    head_sha: str | None


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    description: str = ""
    status: TaskStatus = "BACKLOG"
    priority: Priority = "MEDIUM"
    repository_id: int | None = None
    owner_email: EmailStr | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: Priority | None = None
    owner_email: EmailStr | None = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: str
    priority: str
    repository_id: int | None
    owner_email: str | None
    created_at: datetime


class PullRequestCreate(BaseModel):
    repository_id: int
    number: int = Field(ge=1)
    title: str
    source_branch: str
    target_branch: str = "main"
    checks_passed: bool = False
    review_approved: bool = False


class PullRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    repository_id: int
    number: int
    title: str
    state: str
    source_branch: str
    target_branch: str
    checks_passed: bool
    review_approved: bool


class EnvironmentCreate(BaseModel):
    name: str
    kind: str = "LOCAL"
    protected: bool = True
    requires_approval: bool = True


class EnvironmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    kind: str
    protected: bool
    requires_approval: bool


class DeploymentCreate(BaseModel):
    environment_id: int
    repository_id: int
    version: str
    coverage: float = Field(ge=0, le=1)
    risk: float = Field(ge=0, le=1)
    compliance: float = Field(ge=0, le=1)
    health: float = Field(ge=0, le=1)


class DeploymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    environment_id: int
    repository_id: int
    version: str
    status: str
    coverage: float
    risk: float
    compliance: float
    health: float
    readiness_score: float


class AIAnalyzeIn(BaseModel):
    title: str = "Engineering plan"
    text: str = Field(min_length=5, max_length=12000)


class AIPlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    summary: str
    risks_json: str
    recommendations_json: str
    provider: str
    created_at: datetime
