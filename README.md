# AI Engineering Platform Prototype

This repository is a credible executable prototype foundation for an AI Engineering Platform.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## Docker deployment

```bash
cp .env.example .env
docker compose up --build
```

Then open:

- http://localhost:8000/
- http://localhost:8000/api/health
- http://localhost:8000/api/dashboard/overview
- http://localhost:8000/api/analytics/release-readiness

## Included platform primitives

- repository workflows
- issue lifecycle
- pull request lifecycle
- task tracking
- AI planning engine
- dashboard metrics
- release readiness analytics
- project and governance scaffolding
- demo auth flow

## Current position

This is a real prototype foundation that is deployable locally in a container and is materially beyond a static report. It is not a production-grade enterprise platform, but it is now a much more serious implementation.
