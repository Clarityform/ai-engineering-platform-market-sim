from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from app.db import get_connection


class SQLiteStore:
    def __init__(self) -> None:
        self.seed_default_repo()

    def seed_default_repo(self) -> None:
        if self.get_repo_by_name("platform-demo", "demo") is None:
            self.create_repo(
                owner="demo",
                name="platform-demo",
                visibility="private",
                description="AI Engineering Platform prototype",
            )

    def get_repo_by_name(self, name: str, owner: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM repos WHERE name = ? AND owner = ?",
                (name, owner),
            ).fetchone()
        return dict(row) if row is not None else None

    def _next_id(self, table_name: str) -> int:
        with get_connection() as conn:
            row = conn.execute(f"SELECT COUNT(*) AS c FROM {table_name}").fetchone()
        return int(row["c"]) + 1

    def create_repo(self, owner: str, name: str, visibility: str, description: Optional[str]) -> Dict[str, Any]:
        repo_id = f"repo-{self._next_id('repos')}"
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO repos (id, owner, name, visibility, default_branch, description) VALUES (?, ?, ?, ?, ?, ?)",
                (repo_id, owner, name, visibility, "main", description or ""),
            )
            conn.commit()
        return self.get_repo(repo_id)

    def list_repos(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM repos ORDER BY name").fetchall()
        return [dict(row) for row in rows]

    def get_repo(self, repo_id: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM repos WHERE id = ?", (repo_id,)).fetchone()
        return dict(row) if row is not None else None

    def create_issue(self, repo_id: str, title: str, body: Optional[str]) -> Dict[str, Any]:
        issue_id = f"issue-{self._next_id('issues')}"
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO issues (id, repo_id, title, body, state) VALUES (?, ?, ?, ?, ?)",
                (issue_id, repo_id, title, body or "", "open"),
            )
            conn.commit()
        return self.get_issue(issue_id)

    def get_issue(self, issue_id: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
        return dict(row) if row is not None else None

    def list_issues(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM issues ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def create_pull_request(self, repo_id: str, title: str, source_branch: str, target_branch: str, body: Optional[str]) -> Dict[str, Any]:
        pr_id = f"pr-{self._next_id('pull_requests')}"
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO pull_requests (id, repo_id, title, source_branch, target_branch, body, state) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (pr_id, repo_id, title, source_branch, target_branch, body or "", "open"),
            )
            conn.commit()
        return self.get_pull_request(pr_id)

    def get_pull_request(self, pr_id: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM pull_requests WHERE id = ?", (pr_id,)).fetchone()
        return dict(row) if row is not None else None

    def list_pull_requests(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM pull_requests ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def create_task(self, repo_id: str, title: str, description: str) -> Dict[str, Any]:
        task_id = f"task-{self._next_id('tasks')}"
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO tasks (id, repo_id, title, description, status) VALUES (?, ?, ?, ?, ?)",
                (task_id, repo_id, title, description, "queued"),
            )
            conn.commit()
        return self.get_task(task_id)

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return dict(row) if row is not None else None

    def list_tasks(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def create_ai_plan(self, repo_id: str, task_title: str, description: str) -> Dict[str, Any]:
        plan_id = f"plan-{self._next_id('ai_plans')}"
        steps = [
            "Understand repo context",
            "Review issue and constraints",
            "Implement the requested change",
            "Add or update tests",
            "Validate build and quality checks",
            "Summarize rollout plan",
        ]
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO ai_plans (id, repo_id, task_title, description, steps, risk_score, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (plan_id, repo_id, task_title, description, json.dumps(steps), 0.24, 0.9),
            )
            conn.commit()
        return self.get_ai_plan(plan_id)

    def get_ai_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM ai_plans WHERE id = ?", (plan_id,)).fetchone()
        if row is None:
            return None
        return {
            "id": row["id"],
            "repo_id": row["repo_id"],
            "task_title": row["task_title"],
            "description": row["description"],
            "steps": json.loads(row["steps"]),
            "risk_score": row["risk_score"],
            "confidence": row["confidence"],
        }

    def list_ai_plans(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM ai_plans ORDER BY id").fetchall()
        results: List[Dict[str, Any]] = []
        for row in rows:
            results.append({
                "id": row["id"],
                "repo_id": row["repo_id"],
                "task_title": row["task_title"],
                "description": row["description"],
                "steps": json.loads(row["steps"]),
                "risk_score": row["risk_score"],
                "confidence": row["confidence"],
            })
        return results

    def create_project(self, name: str, repo_id: str, owner: str, description: Optional[str]) -> Dict[str, Any]:
        project_id = f"project-{self._next_id('projects')}"
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO projects (id, name, repo_id, owner, description, status) VALUES (?, ?, ?, ?, ?, ?)",
                (project_id, name, repo_id, owner, description or "", "active"),
            )
            conn.commit()
        return self.get_project(project_id)

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        return dict(row) if row is not None else None

    def list_projects(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM projects ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def create_release(self, project_id: str, version: str, status: str, notes: Optional[str]) -> Dict[str, Any]:
        release_id = f"release-{self._next_id('releases')}"
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO releases (id, project_id, version, status, notes) VALUES (?, ?, ?, ?, ?)",
                (release_id, project_id, version, status, notes or ""),
            )
            conn.commit()
        return self.get_release(release_id)

    def get_release(self, release_id: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM releases WHERE id = ?", (release_id,)).fetchone()
        return dict(row) if row is not None else None

    def list_releases(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM releases ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def create_environment(self, name: str, stage: str, url: str, status: str) -> Dict[str, Any]:
        env_id = f"env-{self._next_id('environments')}"
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO environments (id, name, stage, url, status) VALUES (?, ?, ?, ?, ?)",
                (env_id, name, stage, url, status),
            )
            conn.commit()
        return self.get_environment(env_id)

    def get_environment(self, env_id: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM environments WHERE id = ?", (env_id,)).fetchone()
        return dict(row) if row is not None else None

    def list_environments(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM environments ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def create_policy(self, name: str, kind: str, rules: str) -> Dict[str, Any]:
        policy_id = f"policy-{self._next_id('governance_policies')}"
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO governance_policies (id, name, kind, rules, active) VALUES (?, ?, ?, ?, ?)",
                (policy_id, name, kind, rules, 1),
            )
            conn.commit()
        return self.get_policy(policy_id)

    def get_policy(self, policy_id: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM governance_policies WHERE id = ?", (policy_id,)).fetchone()
        return dict(row) if row is not None else None

    def list_policies(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM governance_policies ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def summarize(self, repo_id: str, title: str) -> Dict[str, Any]:
        repo = self.get_repo(repo_id)
        return {
            "repo_id": repo_id,
            "repo_name": repo["name"] if repo else "unknown",
            "title": title,
            "summary": "The task is scoped to repository health, engineering workflow, and delivery confidence. The recommended approach is small, testable iterations with explicit validation gates and release governance review.",
            "risk_level": "medium",
            "delivery_score": 88,
        }

    def health_metrics(self) -> Dict[str, Any]:
        with get_connection() as conn:
            repo_count = conn.execute("SELECT COUNT(*) AS c FROM repos").fetchone()["c"]
            issue_count = conn.execute("SELECT COUNT(*) AS c FROM issues").fetchone()["c"]
            pr_count = conn.execute("SELECT COUNT(*) AS c FROM pull_requests").fetchone()["c"]
            task_count = conn.execute("SELECT COUNT(*) AS c FROM tasks").fetchone()["c"]
            plan_count = conn.execute("SELECT COUNT(*) AS c FROM ai_plans").fetchone()["c"]
            project_count = conn.execute("SELECT COUNT(*) AS c FROM projects").fetchone()["c"]
            release_count = conn.execute("SELECT COUNT(*) AS c FROM releases").fetchone()["c"]
            env_count = conn.execute("SELECT COUNT(*) AS c FROM environments").fetchone()["c"]
            policy_count = conn.execute("SELECT COUNT(*) AS c FROM governance_policies").fetchone()["c"]
        return {
            "repos": repo_count,
            "issues": issue_count,
            "prs": pr_count,
            "tasks": task_count,
            "plans": plan_count,
            "projects": project_count,
            "releases": release_count,
            "environments": env_count,
            "policies": policy_count,
            "platform_status": "ready",
        }


store = SQLiteStore()
