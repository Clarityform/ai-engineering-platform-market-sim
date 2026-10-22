from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routers import auth, core

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Local-first engineering workflow prototype. External integrations are interfaces only.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(core.router)


@app.get("/health", tags=["operations"])
async def health():
    return {"status": "ok", "environment": settings.environment, "maturity": "LOCAL_PROTOTYPE"}


@app.get("/metrics", tags=["operations"])
async def metrics():
    from sqlalchemy import text

    from app.database import SessionLocal

    async with SessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        db_ok = result.scalar() == 1
    return {"forgeops_up": 1, "database_probe_ok": int(db_ok), "metrics_kind": "DEMO_NOT_PROMETHEUS"}
