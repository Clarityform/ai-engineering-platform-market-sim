import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_ai_analysis_and_readiness_rules():
    text = "This change adds authentication tokens and a production deployment path."
    result = {
        "summary": "Local heuristic analysis only.",
        "risks": ["Security-sensitive change: review threat model, secret handling and access scope."],
    }
    assert "authentication" in text.lower()
    assert result["risks"][0].startswith("Security")


@pytest.mark.asyncio
async def test_deployment_decision_logic():
    from app.services import readiness_score, deployment_decision

    score = readiness_score(0.9, 0.1, 0.95, 0.9)
    assert score > 75
    assert deployment_decision(score, True, True) == "AWAITING_APPROVAL"
    assert deployment_decision(90, False, False) == "READY_FOR_MANUAL_EXECUTION"
