from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

SECRET_KEY = os.environ.get("APP_SECRET_KEY", "ai-platform-demo-secret")

USERS: Dict[str, Dict[str, str]] = {
    "demo": {"id": "user-demo", "username": "demo", "role": "admin", "password": "demo123"},
}


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("utf-8"))


def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "role": USERS[username]["role"],
        "exp": int((datetime.now(timezone.utc) + timedelta(hours=12)).timestamp()),
    }
    encoded = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signature = hmac.new(SECRET_KEY.encode("utf-8"), encoded.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{encoded}.{signature}"


def verify_token(token: str) -> Dict[str, Any]:
    if not token or "." not in token:
        raise ValueError("invalid token")
    encoded, signature = token.split(".", 1)
    expected = hmac.new(SECRET_KEY.encode("utf-8"), encoded.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise ValueError("invalid signature")

    payload = json.loads(_b64url_decode(encoded).decode("utf-8"))
    if int(payload["exp"]) < int(datetime.now(timezone.utc).timestamp()):
        raise ValueError("token expired")
    return payload


def authenticate(username: str, password: str) -> Optional[Dict[str, str]]:
    user = USERS.get(username)
    if user is None:
        return None
    if user["password"] != password:
        return None
    return {"id": user["id"], "username": user["username"], "role": user["role"]}
