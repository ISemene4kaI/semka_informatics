import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from .config import AppConfig, AppPaths, AppVariables

import bleach
import markdown
from flask import Flask, abort, render_template, send_from_directory, jsonify
from werkzeug.utils import safe_join

app = Flask(__name__)


APP_CONFIG = AppConfig(
    dns=os.getenv("APP_DNS", "localhost"),
    host=os.getenv("APP_HOST", "0.0.0.0"),
    port=int(os.getenv("APP_PORT", "8000"))
)
#APP_PATHS.views_json
APP_PATHS = AppPaths(
    codes_dir=Path(os.getenv("FILES_DIR", "./app/code_storage")),
    static_dir=Path(os.getenv("STATIC_DIR", "./app/static")),
    templates_dir=Path(os.getenv("TEMPLATES_DIR", "./app/templates")),
    views_json=Path(os.getenv("VIEWS_FILE", "./app.views.json"))
)

APP_VARIABLES = AppVariables()

# ========== Checkers ================

def is_allowed(filename):
    global APP_VARIABLES
    return "." in filename and filename.rsplit(".", 1)[1].lower() in APP_VARIABLES.allowed_extensions

def is_safe_filename(filename):
    return bool(filename) and "/" not in filename and "\\" not in filename and not filename.startswith(".")

def list_allowed_filenames():
    global APP_PATHS
    return [filename for filename in os.listdir(APP_PATHS.codes_dir) if is_allowed(filename)]

# ========== Additional func ================

def get_safe_file_path(filename):
    global APP_PATHS

    if not is_safe_filename(filename):
        abort(403)

    if not is_allowed(filename):
        abort(403)

    path = safe_join(APP_PATHS.codes_dir, filename)

    if path is None:
        abort(403)

    if not os.path.isfile(path):
        abort(404)

    return path



def read_text_file_limited(path):
    global APP_VARIABLES
    size = os.path.getsize(path)

    if size > APP_VARIABLES.max_file_bytes:
        abort(413)

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def parse_filename(filename):
    global APP_VARIABLES
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


def build_file_entry(filename):
    global APP_PATHS, APP_VARIABLES
    path = os.path.join(APP_PATHS.codes_dir, filename)
    ext = filename.rsplit(".", 1)[1].lower()
    _, _, title = parse_filename(filename)
    mtime = os.path.getmtime(path)

    return {
        "filename": filename,
        "title": title,
        "icon": APP_VARIABLES.lang_icons.get(ext, "📄"),
        "ext": ext,
        "mtime": datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M"),
        "mtime_raw": mtime,
    }


def get_latest_files(limit=10):
    files = [build_file_entry(filename) for filename in list_allowed_filenames()]
    files.sort(key=lambda item: item["mtime_raw"], reverse=True)
    return files[:limit]


def load_views():
    global APP_PATHS
    if not os.path.exists(APP_PATHS.views_json):
        return {}

    try:
        with open(APP_PATHS.views_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError, json.JSONDecodeError):
        return {}


def save_views(data):
    global APP_PATHS
    os.makedirs(os.path.dirname(APP_PATHS.views_json), exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(APP_PATHS.views_json),
        prefix="views_",
        suffix=".tmp",
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        os.replace(tmp_path, APP_PATHS.views_json)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def increase_view(filename):
    views = load_views()
    views[filename] = int(views.get(filename, 0)) + 1
    save_views(views)
    return views[filename]


@app.route("/")
def index():
    works = {}
    total = 0

    for filename in list_allowed_filenames():
        work, _, _ = parse_filename(filename)
        entry = build_file_entry(filename)
        entry.pop("mtime_raw", None)

        works.setdefault(work, []).append(entry)
        total += 1

    latest = get_latest_files(limit=5)

    return render_template(
        "index.html",
        works=works,
        latest=latest,
        total=total,
    )


@app.route("/view/<filename>")
def view_file(filename):
    path = get_safe_file_path(filename)
    views = increase_view(filename)
    content = read_text_file_limited(path)
    ext = filename.rsplit(".", 1)[1].lower()
    _, _, title = parse_filename(filename)

    if ext == "md":
        raw_html = markdown.markdown(
            content,
            extensions=["fenced_code", "tables"],
        )

        allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
            "p",
            "pre",
            "code",
            "hr",
            "br",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "table",
            "thead",
            "tbody",
            "tr",
            "th",
            "td",
            "blockquote",
            "span",
        })

        allowed_attrs = {
            **bleach.sanitizer.ALLOWED_ATTRIBUTES,
            "a": ["href", "title", "target", "rel"],
            "code": ["class"],
            "span": ["class"],
        }

        clean_html = bleach.clean(
            raw_html,
            tags=allowed_tags,
            attributes=allowed_attrs,
            protocols=["http", "https", "mailto"],
            strip=True,
        )

        return render_template(
            "view.html",
            filename=filename,
            title=title,
            markdown=clean_html,
            is_markdown=True,
            language=ext,
            views=views,
        )

    lines = content.splitlines()

    return render_template(
        "view.html",
        filename=filename,
        title=title,
        lines=lines,
        is_markdown=False,
        language=ext,
        views=views,
    )


@app.route("/download/<filename>")
def download(filename):
    path = get_safe_file_path(filename)

    return send_from_directory(
        APP_PATHS.codes_dir,
        os.path.basename(path),
        as_attachment=True,
    )


@app.route("/updates")
def updates():
    return render_template(
        "updates.html",
        latest=get_latest_files(),
    )

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host=APP_CONFIG.host, port=APP_CONFIG.port)