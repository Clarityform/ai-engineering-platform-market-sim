from app.models import Deployment


def readiness_score(coverage: float, risk: float, compliance: float, health: float) -> float:
    """Score 0..100. Risk is inverse-weighted; this is a demo heuristic, not a release guarantee."""
    score = 100 * (
        0.30 * coverage
        + 0.25 * (1 - risk)
        + 0.25 * compliance
        + 0.20 * health
    )
    return round(max(0.0, min(100.0, score)), 2)


def deployment_decision(score: float, protected: bool, requires_approval: bool) -> str:
    if score < 75:
        return "BLOCKED"
    if protected or requires_approval:
        return "AWAITING_APPROVAL"
    return "READY_FOR_MANUAL_EXECUTION"
