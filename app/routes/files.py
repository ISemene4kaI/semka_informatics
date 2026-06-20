import os

from flask import Blueprint, render_template, send_from_directory

from app.config import APP_PATHS
from app.services.file_service import (
    build_file_entry,
    get_file_neighbors,
    get_safe_file_path,
    parse_filename,
    read_text_file_limited,
)
from app.services.markdown_service import render_markdown_safe
from app.services.views_service import increase_view

files_bp = Blueprint("files", __name__)


@files_bp.get("/view/<filename>")
def view_file(filename):
    path = get_safe_file_path(filename)
    content = read_text_file_limited(path)
    views = increase_view(filename)
    entry = build_file_entry(filename)
    ext = entry["ext"]
    _, _, title = parse_filename(filename)
    previous_filename, next_filename = get_file_neighbors(filename)

    context = {
        "filename": filename,
        "title": title,
        "language": ext,
        "views": views,
        "size": entry["size_human"],
        "modified": entry["mtime"],
        "previous_filename": previous_filename,
        "next_filename": next_filename,
    }

    if ext == "md":
        return render_template(
            "view.html",
            markdown=render_markdown_safe(content),
            is_markdown=True,
            **context,
        )

    return render_template(
        "view.html",
        content=content,
        is_markdown=False,
        **context,
    )


@files_bp.get("/download/<filename>")
def download(filename):
    path = get_safe_file_path(filename)
    return send_from_directory(
        APP_PATHS.codes_dir,
        os.path.basename(path),
        as_attachment=True,
    )
