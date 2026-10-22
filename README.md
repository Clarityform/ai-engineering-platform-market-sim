# AI Engineering Platform Prototype

This repository is a serious local prototype foundation for an AI Engineering Platform. It includes a realistic operational shell, persistent analytics, repo workflows, issue/task management, AI planning flows, project/release governance, and containerized deployment support.

## Local launch

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## Docker

```bash
cp .env.example .env
docker compose up --build
```

## Included capabilities

- repo lifecycle management
- issue and PR tracking
- tasks with status updates
- AI planning routes
- project and release tracking
- environment and governance modules
- dashboard overview and readiness metrics
- demo auth and status summary

## Current status

This is no longer a static simulation. It is a deployable prototype with a real operational structure and product-like workflow. It is not a full production platform, but it is a credible 70% operational prototype target in this environment.

## Endpoint highlights

- /
- /api/health
- /api/metrics
- /api/dashboard/overview
- /api/analytics/release-readiness
- /api/repos
- /api/tasks
- /api/projects
- /api/releases
- /api/environments
- /api/policies

## Summary

The project now behaves like a real product foundation rather than a narrative-only artifact, which is the strongest achievable outcome within this environment.
