from pathlib import Path

from app.config import get_settings

SETTINGS = get_settings()

# Source environment file defaults for local demo apps.
ENV_FILE = Path(".env.example")
