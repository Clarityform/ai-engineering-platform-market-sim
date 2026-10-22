# ForgeOps AI Engineering Platform

**Maturity: local prototype, not production infrastructure.** This is a runnable API foundation with a small workflow model, JWT authentication, role checks, heuristic planning, readiness scoring, and integration contracts. It does not connect to GitHub, deploy to a cloud, call an external AI provider, or export real Prometheus telemetry.

## Quick start (Python 3.12 recommended)

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
# Replace JWT_SECRET with a long random value before exposing the service.
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`. First registration receives ADMIN role for bootstrapping; subsequent registrations cannot self-assign ADMIN. This bootstrap behavior is for a single-user local demo. For a shared environment, use an explicit administrative provisioning process and disable public registration.

## Docker

```bash
docker compose up --build
```

SQLite data is persisted in the `forgeops_data` named volume. For PostgreSQL, set `DATABASE_URL` to a PostgreSQL async URL such as `postgresql+asyncpg://user:password@host:5432/forgeops` and provide a reachable database. A real PostgreSQL deployment needs migrations, backups, connection-pool tuning and operational ownership; `create_all` is only used for prototype startup.

## Main API

- `GET /health`, `GET /metrics`
- `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`
- `GET/POST /api/repositories`
- `GET/POST /api/branches`
- `GET/POST/PATCH /api/tasks`
- `GET/POST /api/pull-requests`
- `GET/POST /api/environments`
- `GET/POST /api/deployments`
- `POST /api/ai/analyze`, `GET /api/ai/plans`
- `GET /api/dashboard`

All workflow endpoints except health/metrics and registration/login require a bearer token. Use `/docs` to authenticate and exercise the API. Passwords are hashed with bcrypt. JWTs are signed using an environment secret.

## Readiness model

Score = 100 × (0.30 × coverage + 0.25 × (1 − risk) + 0.25 × compliance + 0.20 × health). Inputs are in [0, 1]. Below 75 is blocked. A passing score in a protected or approval-gated environment becomes `AWAITING_APPROVAL`, never an automatic cloud deployment. This is a transparent demo heuristic, not a validated compliance or safety certification.

The AI planner is a deterministic keyword-based local heuristic. Its result is advisory and explicitly does not prove the code is safe. Provider interfaces in `app/adapters.py` are contracts only.

## Architecture

```text
HTTP / OpenAPI
    └── FastAPI routers + Pydantic schemas
         ├── Auth boundary (JWT + bcrypt + role checks)
         ├── Workflow services (readiness / decisions)
         ├── Local heuristic AI planner
         ├── SQLAlchemy async data models
         └── Adapter contracts (VCS / deploy / telemetry / AI)
```

## Environment and maturity boundaries

**Implemented locally:** SQLite persistence, API routes, typed request/response schemas, bcrypt password hashing, JWT login, basic RBAC, task lifecycle fields, repository/branch/PR/environment/deployment models, heuristic AI plans, dashboard counts, demo metrics, Docker packaging, starter tests.

**Staging work still required:** Alembic migrations, robust account recovery and rate limits, audit events, refresh-token/revocation strategy, secure secret management, PostgreSQL integration tests, API pagination, request IDs, structured logs, real telemetry, dependency scanning, CI policy, backup/restore drills, threat modeling, and security review.

**Production requires actual infrastructure:** managed database, secrets manager, TLS/reverse proxy, SSO/MFA, least-privilege IAM, CI/CD and artifact provenance, deployment runners, real GitHub/GitLab and cloud adapters, OpenTelemetry/Prometheus, alerting/on-call, data retention policy, disaster recovery, load and penetration tests, and an operator-approved release process.

## Security notes

- Change the local JWT secret before any shared use.
- Do not commit `.env`, API tokens, credentials, account IDs, or private operational evidence.
- Do not expose SQLite or `/docs` to the public internet.
- The first-user ADMIN bootstrap is convenient for local setup only.
- Adapter interfaces deliberately fail closed until a real implementation and credentials are configured.
- No live external services are called by this prototype.

## Tests

```bash
pytest -q
```

Tests cover health, scoring, release decisions, and heuristic risk detection. They are starter tests, not a full integration or security test suite.
