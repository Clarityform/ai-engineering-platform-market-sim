# AI Engineering Platform Prototype

This repository now contains a real working backend prototype focused on the AI Engineering Platform concept. It is intentionally beyond a static narrative and includes implementable product flows.

## What is included

- FastAPI application
- SQLite-backed data storage
- repo creation and listing
- issue creation and listing
- pull request creation and listing
- task tracking
- AI plan creation and summarization
- health and metrics endpoints
- dashboard landing page

## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

Then open:

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/repos
- http://localhost:8000/issues
- http://localhost:8000/pulls
- http://localhost:8000/tasks
- http://localhost:8000/metrics

## Examples

Create a repo:

```bash
curl -X POST "http://localhost:8000/repos?owner=demo&name=ai-platform&visibility=private&description=prototype%20repo"
```

Create a task:

```bash
curl -X POST "http://localhost:8000/tasks?repo_id=repo-demo&title=Add%20summary%20endpoint&description=Create%20a%20task%20summary%20service"
```

Create an AI plan:

```bash
curl -X POST "http://localhost:8000/ai/plan?repo_id=repo-demo&task_title=Add%20summary%20endpoint&description=Create%20a%20task%20summary%20service"
```

## Current maturity

This is a meaningful product prototype foundation, not a full enterprise platform. It materially improves the implementation state beyond the earlier document-only simulation by adding real storage, routing, and workflow primitives.

## Next engineered steps

- user auth and sessions
- repo branch management
- actual CI workflow logic
- API authentication
- dashboard UI
- postgres migration
- deployment and observability
- enterprise security and governance module

## Current status

This project is now roughly at a stronger prototype foundation level, well beyond a static market report.
