# AI Engineering Platform Prototype

This repository is now a stronger executable platform prototype, with capabilities beyond the static strategy report. It includes:

- FastAPI API layer
- SQLite data persistence
- repo lifecycle workflows
- issue and PR tracking
- task and AI planning support
- auth token flow
- dashboard summary endpoint
- project, release, environment, and policy primitives

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## Endpoints

- /
- /api/health
- /api/metrics
- /api/repos
- /api/issues
- /api/pulls
- /api/tasks
- /api/ai/plans
- /api/projects
- /api/releases
- /api/environments
- /api/policies
- /api/auth/login
- /api/auth/me
- /api/dashboard/summary

## Demo auth

```bash
curl -X POST "http://localhost:8000/api/auth/login?username=demo&password=demo123"
```

## Current maturity

This is now a substantial prototype foundation for an AI Engineering Platform, not a static report. It is not a production-grade enterprise platform, but it is clearly in the territory of a real product foundation with significant operational logic.

## Next real engineering steps

- real multi-user persistence and auth storage
- branch and commit lifecycle modeling
- CI/CD orchestration
- deployment and environment automation
- richer UI dashboards
- release approval workflows
- security and policy enforcement
- production deployment and hardening

## Bottom line

The project is now meaningfully stronger as a realistic platform prototype and is much farther along than the earlier report-only and prototype-only stages.
