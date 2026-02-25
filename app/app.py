import os
import re
from datetime import datetime
from flask import Flask, render_template, abort, send_from_directory

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(BASE_DIR, "code_storage")

ALLOWED_EXTENSIONS = {
    "py", "js", "html", "css",
    "cpp", "c", "java", "txt",
    "md", "json"
}


def is_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def make_display_title(filename: str) -> str:
    name = filename.rsplit(".", 1)[0]  # без расширения

    # 1part2 / 12part3 / 7part10
    m = re.match(r"^(?P<work>\d+)(?:part(?P<part>\d+))?$", name, flags=re.IGNORECASE)
    if m:
        work = int(m.group("work"))
        part = m.group("part")
        if part is not None:
            return f"Практическая работа {work} часть {int(part)}"
        return f"Практическая работа {work}"

    # fallback
    return name


@app.route("/")
def index():
    entries = []
    for f in os.listdir(CODE_DIR):
        full = os.path.join(CODE_DIR, f)
        if (
            os.path.isfile(full)
            and is_allowed(f)
            and not f.startswith(".")
        ):
            mtime = os.path.getmtime(full)
            entries.append({
                "filename": f,
                "ext": f.rsplit(".", 1)[1].lower(),
                "title": make_display_title(f),
                "mtime": datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M"),
                "mtime_ts": mtime,
            })

    # чтобы было красиво: сначала по номеру/части (примерно), затем по дате
    entries.sort(key=lambda x: (x["title"], -x["mtime_ts"]))

    return render_template("index.html", entries=entries)


@app.route("/view/<filename>")
def view_file(filename):
    if not is_allowed(filename):
        abort(403)

    file_path = os.path.join(CODE_DIR, filename)

    if not os.path.abspath(file_path).startswith(os.path.abspath(CODE_DIR)):
        abort(403)

    if not os.path.exists(file_path):
        abort(404)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    extension = filename.rsplit(".", 1)[1].lower()

    return render_template(
        "view.html",
        filename=filename,
        content=content,
        language=extension
    )
    
@app.route("/download/<filename>")
def download_file(filename):
    if not is_allowed(filename):
        abort(403)

    file_path = os.path.join(CODE_DIR, filename)

    # защита от выхода из директории
    if not os.path.abspath(file_path).startswith(os.path.abspath(CODE_DIR)):
        abort(403)

    if not os.path.exists(file_path):
        abort(404)

    return send_from_directory(CODE_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)