import os

from flask import Blueprint

from app.config import APP_PATHS

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return {"status": "ok"}


@health_bp.get("/ready")
def ready():
    views_directory = APP_PATHS.views_json.parent
    checks = {
        "files": APP_PATHS.codes_dir.is_dir()
        and os.access(APP_PATHS.codes_dir, os.R_OK),
        "views": views_directory.is_dir() and os.access(views_directory, os.W_OK),
    }
    status = 200 if all(checks.values()) else 503
    return {"status": "ok" if status == 200 else "not_ready", "checks": checks}, status
