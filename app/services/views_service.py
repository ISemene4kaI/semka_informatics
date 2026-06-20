import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

import fcntl

from app.config import APP_PATHS


def load_views() -> dict:
    if not os.path.exists(APP_PATHS.views_json):
        return {}

    try:
        with open(APP_PATHS.views_json, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, ValueError, json.JSONDecodeError):
        return {}


def save_views(data: dict) -> None:
    directory = APP_PATHS.views_json.parent
    directory.mkdir(parents=True, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(
        dir=directory,
        prefix="views_",
        suffix=".tmp",
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        os.replace(tmp_path, APP_PATHS.views_json)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@contextmanager
def views_lock():
    lock_path = Path(f"{APP_PATHS.views_json}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with open(lock_path, "a", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)


def increase_view(filename: str) -> int:
    with views_lock():
        views = load_views()
        views[filename] = int(views.get(filename, 0)) + 1
        save_views(views)
        return views[filename]
