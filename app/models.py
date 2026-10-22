from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey, Float, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def now_utc():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(24), default="DEVELOPER")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    provider: Mapped[str] = mapped_column(String(24), default="LOCAL")
    external_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    default_branch: Mapped[str] = mapped_column(String(120), default="main")
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    protected: Mapped[bool] = mapped_column(Boolean, default=False)
    head_sha: Mapped[str | None] = mapped_column(String(80), nullable=True)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(240))
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(24), default="BACKLOG")
    priority: Mapped[str] = mapped_column(String(16), default="MEDIUM")
    repository_id: Mapped[int | None] = mapped_column(ForeignKey("repositories.id"), nullable=True)
    owner_email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class PullRequest(Base):
    __tablename__ = "pull_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"), index=True)
    number: Mapped[int]
    title: Mapped[str] = mapped_column(String(240))
    state: Mapped[str] = mapped_column(String(24), default="OPEN")
    source_branch: Mapped[str] = mapped_column(String(120))
    target_branch: Mapped[str] = mapped_column(String(120), default="main")
    checks_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    review_approved: Mapped[bool] = mapped_column(Boolean, default=False)


class Environment(Base):
    __tablename__ = "environments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    kind: Mapped[str] = mapped_column(String(24), default="LOCAL")
    protected: Mapped[bool] = mapped_column(Boolean, default=True)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True)


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[int] = mapped_column(primary_key=True)
    environment_id: Mapped[int] = mapped_column(ForeignKey("environments.id"), index=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"), index=True)
    version: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(24), default="PLANNED")
    coverage: Mapped[float] = mapped_column(Float, default=0.0)
    risk: Mapped[float] = mapped_column(Float, default=0.5)
    compliance: Mapped[float] = mapped_column(Float, default=0.5)
    health: Mapped[float] = mapped_column(Float, default=0.5)
    readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class AIPlan(Base):
    __tablename__ = "ai_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(240))
    input_text: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text)
    risks_json: Mapped[str] = mapped_column(Text, default="[]")
    recommendations_json: Mapped[str] = mapped_column(Text, default="[]")
    provider: Mapped[str] = mapped_column(String(40), default="HEURISTIC_LOCAL")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
