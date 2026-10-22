# AI Engineering Platform Prototype

This repository now includes a real executable prototype with a functional API layer and persistent SQLite-backed data storage. It steps beyond a static narrative and provides runnable product primitives for repos, issues, pull requests, tasks, and AI planning.

## What is included

- FastAPI backend
- SQLite data layer
- repo CRUD workflow
- issue management
- pull request flow
- task management
- AI plan generation
- health and metrics endpoints
- mounted API architecture for a more realistic app layout

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
- http://localhost:8000/api/metrics

## Example API calls

```bash
curl -X POST "http://localhost:8000/api/repos?owner=demo&name=ai-platform&visibility=private&description=prototype%20repo"
curl -X POST "http://localhost:8000/api/tasks?repo_id=repo-1&title=Add%20summary%20endpoint&description=Create%20summary%20task"
curl -X POST "http://localhost:8000/api/ai/plan?repo_id=repo-1&task_title=Add%20summary%20endpoint&description=Create%20summary%20task"
```

## Current maturity

This is a real prototype foundation, not a finished production platform. It is a meaningful next step beyond a static market document and is now clearly in executable product territory.

## Next real engineering stages

- user authentication
- branch and merge logic
- CI/CD workflow adapter
- dashboard UI
- stronger deployment model
- release and environment management
- policy and governance layer
- secure enterprise configuration

## Bottom line

This project is now significantly stronger as a working prototype and is approaching the level of a credible platform foundation.
