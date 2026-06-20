import os
from datetime import datetime

from flask import abort
from werkzeug.utils import safe_join

from app.config import APP_PATHS, APP_VARIABLES


def is_allowed(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in APP_VARIABLES.allowed_extensions
    )


def is_safe_filename(filename: str) -> bool:
    return (
        bool(filename)
        and "/" not in filename
        and "\\" not in filename
        and not filename.startswith(".")
    )


def list_allowed_filenames() -> list[str]:
    filenames = [
        filename
        for filename in os.listdir(APP_PATHS.codes_dir)
        if is_allowed(filename)
        and os.path.isfile(os.path.join(APP_PATHS.codes_dir, filename))
    ]
    return sorted(filenames, key=filename_sort_key)


def filename_sort_key(filename: str) -> tuple:
    work, part, _ = parse_filename(filename)
    return (
        work is None,
        work or 0,
        int(part or 0),
        filename.casefold(),
    )


def get_safe_file_path(filename: str) -> str:
    if not is_safe_filename(filename) or not is_allowed(filename):
        abort(403)

    path = safe_join(APP_PATHS.codes_dir, filename)

    if path is None:
        abort(403)

    if not os.path.isfile(path):
        abort(404)

    return path


def read_text_file_limited(path: str) -> str:
    size = os.path.getsize(path)

    if size > APP_VARIABLES.max_file_bytes:
        abort(413)

    with open(path, "r", encoding="utf-8", errors="replace") as file:
        return file.read()


def parse_filename(filename: str):
    name = filename.rsplit(".", 1)[0]
    match = APP_VARIABLES.filename_pattern.match(name)

    if not match:
        return None, None, name

    work = int(match.group(1))
    part = match.group(2)

    if part:
        title = f"Практическая работа {work} часть {part}"
    else:
        title = f"Практическая работа {work}"

    return work, part, title


def build_file_entry(filename: str) -> dict:
    path = os.path.join(APP_PATHS.codes_dir, filename)
    ext = filename.rsplit(".", 1)[1].lower()
    _, _, title = parse_filename(filename)
    mtime = os.path.getmtime(path)

    return {
        "filename": filename,
        "title": title,
        "icon": APP_VARIABLES.lang_icons.get(ext, ""),
        "ext": ext,
        "mtime": datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M"),
        "mtime_raw": mtime,
        "size": os.path.getsize(path),
        "size_human": format_file_size(os.path.getsize(path)),
    }


def format_file_size(size: int) -> str:
    if size < 1024:
        return f"{size} Б"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} КБ"
    return f"{size / (1024 * 1024):.1f} МБ"


def get_latest_files(limit: int = 10) -> list[dict]:
    files = [build_file_entry(filename) for filename in list_allowed_filenames()]
    files.sort(key=lambda item: item["mtime_raw"], reverse=True)
    return files[:limit]


def get_file_neighbors(filename: str) -> tuple[str | None, str | None]:
    filenames = list_allowed_filenames()
    try:
        index = filenames.index(filename)
    except ValueError:
        return None, None

    previous_filename = filenames[index - 1] if index > 0 else None
    next_filename = filenames[index + 1] if index < len(filenames) - 1 else None
    return previous_filename, next_filename
