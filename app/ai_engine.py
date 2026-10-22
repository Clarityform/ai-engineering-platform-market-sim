import re

RISK_RULES = {
    "security": (
        r"\b(auth|token|secret|credential|permission|encrypt|security)\b",
        "Security-sensitive change: review threat model, secret handling and access scope.",
    ),
    "data": (
        r"\b(database|migration|schema|delete|data loss|backup)\b",
        "Data integrity risk: test migration and restore path against a disposable copy.",
    ),
    "availability": (
        r"\b(deploy|release|production|rollout|downtime|availability)\b",
        "Availability risk: define health checks, staged rollout and rollback trigger.",
    ),
    "breaking": (
        r"\b(api|breaking change|compatibility|contract)\b",
        "Compatibility risk: verify API contracts and backward compatibility.",
    ),
    "money": (
        r"\b(payment|billing|price|trade|order|financial)\b",
        "Financial-impacting path: require deterministic tests and human approval.",
    ),
}


def analyze(text: str) -> dict:
    found = [
        message
        for _, (pattern, message) in RISK_RULES.items()
        if re.search(pattern, text, flags=re.IGNORECASE)
    ]
    if not found:
        found = ["No keyword-triggered risk detected; this is not proof of safety."]

    recommendations = [
        "Convert each acceptance criterion into an automated test.",
        "Assign an accountable owner and explicit rollback condition.",
        "Review the diff and evidence before approving a release.",
    ]

    summary = (
        "Local heuristic analysis only. "
        + f"Detected {len(found)} risk category/categories. "
        + "This engine does not call an external AI model or verify source code."
    )

    return {
        "summary": summary,
        "risks": found,
        "recommendations": recommendations,
    }
