from flask import Blueprint, render_template

from app.services.file_service import (
    build_file_entry,
    get_latest_files,
    list_allowed_filenames,
    parse_filename,
)

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
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


@pages_bp.route("/updates")
def updates():
    return render_template(
        "updates.html",
        latest=get_latest_files(),
    )