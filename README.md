# AI Engineering Platform Prototype

This repository now contains a stronger real prototype foundation with a more product-like structure. It includes:

- FastAPI app layering
- SQLite-backed persistence
- repo, issue, pull request, and task workflows
- AI planning endpoint
- auth flow with demo token login
- dashboard summary endpoint
- a lightweight web dashboard entry point for prototype visibility

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

Then open:

- http://localhost:8000/
- http://localhost:8000/api/health
- http://localhost:8000/api/repos
- http://localhost:8000/api/issues
- http://localhost:8000/api/pulls
- http://localhost:8000/api/tasks
- http://localhost:8000/api/ai/plans
- http://localhost:8000/api/dashboard/summary

## Demo auth

```bash
curl -X POST "http://localhost:8000/api/auth/login?username=demo&password=demo123"
```

Then use the token in the Authorization header:

```bash
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/api/auth/me
```

## Current maturity

This is a real prototype foundation, not a production-grade platform. It is materially stronger than a static market simulation and is now in a credible executable prototype stage.

## Next real stages

- multi-user sessions and real auth persistence
- branch, commit, and merge models
- release and environment tracking
- CI/CD integration
- richer dashboard UI
- policy and governance controls
- full backend persistence and migrations
- deployment orchestration

## Bottom line

This repository is now substantially beyond a static strategy document and is closer to a real product foundation for an AI Engineering Platform.
