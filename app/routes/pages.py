from flask import Blueprint, Response, render_template, request

from app.services.file_service import (
    build_file_entry,
    get_latest_files,
    list_allowed_filenames,
    parse_filename,
)
from app.services.views_service import load_views

pages_bp = Blueprint("pages", __name__)


@pages_bp.get("/")
def index():
    query = request.args.get("q", "").strip().casefold()
    selected_language = request.args.get("lang", "").strip().lower()
    entries = [build_file_entry(name) for name in list_allowed_filenames()]
    languages = sorted({entry["ext"] for entry in entries})

    if query:
        entries = [
            entry
            for entry in entries
            if query in entry["filename"].casefold()
            or query in entry["title"].casefold()
        ]
    if selected_language:
        entries = [entry for entry in entries if entry["ext"] == selected_language]

    works = {}
    for entry in entries:
        work, _, _ = parse_filename(entry["filename"])
        works.setdefault(work, []).append(entry)

    return render_template(
        "index.html",
        works=works,
        languages=languages,
        query=request.args.get("q", "").strip(),
        selected_language=selected_language,
        total=len(entries),
    )


@pages_bp.get("/updates")
def updates():
    return render_template("updates.html", latest=get_latest_files())


@pages_bp.get("/stats")
def stats():
    views = load_views()
    entries = [build_file_entry(name) for name in list_allowed_filenames()]
    for entry in entries:
        entry["views"] = int(views.get(entry["filename"], 0))
    entries.sort(key=lambda entry: entry["views"], reverse=True)
    return render_template(
        "stats.html",
        entries=entries,
        total_views=sum(entry["views"] for entry in entries),
    )


@pages_bp.get("/feed.xml")
def feed():
    xml = render_template("feed.xml", files=get_latest_files(limit=20))
    return Response(xml, mimetype="application/rss+xml")
