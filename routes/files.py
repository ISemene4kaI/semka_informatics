import os

from flask import Blueprint, render_template, send_from_directory

from app.config import APP_PATHS
from app.services.file_service import (
    get_safe_file_path,
    parse_filename,
    read_text_file_limited,
)
from app.services.markdown_service import render_markdown_safe
from app.services.views_service import increase_view

files_bp = Blueprint("files", __name__)


@files_bp.route("/view/<filename>")
def view_file(filename):
    path = get_safe_file_path(filename)
    views = increase_view(filename)
    content = read_text_file_limited(path)
    ext = filename.rsplit(".", 1)[1].lower()
    _, _, title = parse_filename(filename)

    if ext == "md":
        clean_html = render_markdown_safe(content)

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


@files_bp.route("/download/<filename>")
def download(filename):
    path = get_safe_file_path(filename)

    return send_from_directory(
        APP_PATHS.codes_dir,
        os.path.basename(path),
        as_attachment=True,
    )