from __future__ import annotations

from typing import Any, Dict, List, Optional


class InMemoryStore:
    def __init__(self) -> None:
        self.repos: Dict[str, Dict[str, Any]] = {}
        self.issues: Dict[str, Dict[str, Any]] = {}
        self.pull_requests: Dict[str, Dict[str, Any]] = {}
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.ai_plans: Dict[str, Dict[str, Any]] = {}

    def seed_default_repo(self) -> None:
        if not self.repos:
            repo_id = "repo-demo"
            self.repos[repo_id] = {
                "id": repo_id,
                "name": "platform-demo",
                "owner": "demo",
                "visibility": "private",
                "default_branch": "main",
                "description": "AI Engineering Platform prototype",
            }

    def create_repo(self, owner: str, name: str, visibility: str, description: Optional[str]) -> Dict[str, Any]:
        repo_id = f"repo-{len(self.repos) + 1}"
        repo = {
            "id": repo_id,
            "name": name,
            "owner": owner,
            "visibility": visibility,
            "default_branch": "main",
            "description": description or "",
        }
        self.repos[repo_id] = repo
        return repo

    def list_repos(self) -> List[Dict[str, Any]]:
        return list(self.repos.values())

    def get_repo(self, repo_id: str) -> Optional[Dict[str, Any]]:
        return self.repos.get(repo_id)

    def create_issue(self, repo_id: str, title: str, body: Optional[str]) -> Dict[str, Any]:
        issue_id = f"issue-{len(self.issues) + 1}"
        issue = {
            "id": issue_id,
            "repo_id": repo_id,
            "title": title,
            "body": body or "",
            "state": "open",
        }
        self.issues[issue_id] = issue
        return issue

    def list_issues(self) -> List[Dict[str, Any]]:
        return list(self.issues.values())

    def create_pull_request(self, repo_id: str, title: str, source_branch: str, target_branch: str, body: Optional[str]) -> Dict[str, Any]:
        pr_id = f"pr-{len(self.pull_requests) + 1}"
        pr = {
            "id": pr_id,
            "repo_id": repo_id,
            "title": title,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "body": body or "",
            "state": "open",
        }
        self.pull_requests[pr_id] = pr
        return pr

    def list_pull_requests(self) -> List[Dict[str, Any]]:
        return list(self.pull_requests.values())

    def create_task(self, repo_id: str, title: str, description: str) -> Dict[str, Any]:
        task_id = f"task-{len(self.tasks) + 1}"
        task = {
            "id": task_id,
            "repo_id": repo_id,
            "title": title,
            "description": description,
            "status": "queued",
        }
        self.tasks[task_id] = task
        return task

    def list_tasks(self) -> List[Dict[str, Any]]:
        return list(self.tasks.values())

    def create_ai_plan(self, repo_id: str, task_title: str, description: str) -> Dict[str, Any]:
        plan_id = f"plan-{len(self.ai_plans) + 1}"
        steps = [
            "Understand repo context",
            "Review issue and constraints",
            "Implement the requested change",
            "Add or update tests",
            "Validate build and quality checks",
            "Summarize the rollout plan",
        ]
        plan = {
            "id": plan_id,
            "repo_id": repo_id,
            "task_title": task_title,
            "description": description,
            "steps": steps,
            "risk_score": 0.24,
            "confidence": 0.9,
        }
        self.ai_plans[plan_id] = plan
        return plan

    def summarize(self, repo_id: str, title: str) -> Dict[str, Any]:
        repo = self.get_repo(repo_id)
        return {
            "repo_id": repo_id,
            "repo_name": repo["name"] if repo else "unknown",
            "title": title,
            "summary": "The task is scoped to the repository health, user workflow, and engineering delivery layer. The recommended approach is to implement the change in a small, testable iteration with explicit validation gates.",
            "risk_level": "medium",
            "delivery_score": 86,
        }

    def health_metrics(self) -> Dict[str, Any]:
        return {
            "repos": len(self.repos),
            "issues": len(self.issues),
            "prs": len(self.pull_requests),
            "tasks": len(self.tasks),
            "plans": len(self.ai_plans),
            "platform_status": "ready",
        }


store = InMemoryStore()
store.seed_default_repo()
