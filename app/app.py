import os
import re
import json
import tempfile
import markdown
import bleach

from datetime import datetime
from flask import Flask, render_template, abort, send_from_directory
from werkzeug.utils import safe_join

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(BASE_DIR, "code_storage")
VIEWS_FILE = os.path.join(BASE_DIR, "views.json")

MAX_FILE_BYTES = 1_000_000

ALLOWED_EXTENSIONS = {
    "py","js","html","css",
    "cpp","c","java","txt",
    "md","json"
}

LANG_ICONS = {
    "py":"🐍",
    "cpp":"⚙️",
    "c":"⚙️",
    "js":"📜",
    "json":"🧾",
    "md":"📄",
    "txt":"📄"
}


def is_allowed(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS


def is_safe_filename(filename):

    if not filename:
        return False

    if "/" in filename or "\\" in filename:
        return False

    if filename.startswith("."):
        return False

    return True


def get_safe_file_path(filename):

    if not is_safe_filename(filename):
        abort(403)

    if not is_allowed(filename):
        abort(403)

    path = safe_join(CODE_DIR, filename)

    if path is None:
        abort(403)

    if not os.path.isfile(path):
        abort(404)

    return path


def read_text_file_limited(path):

    size = os.path.getsize(path)

    if size > MAX_FILE_BYTES:
        abort(413)

    with open(path,"r",encoding="utf-8",errors="replace") as f:
        return f.read()

def get_latest_files():

    files = []

    for f in os.listdir(CODE_DIR):

        if not is_allowed(f):
            continue

        path = os.path.join(CODE_DIR,f)

        ext = f.split(".")[-1]

        mtime = os.path.getmtime(path)

        work,part,title = parse_filename(f)

        files.append({
            "filename":f,
            "title":title,
            "icon":LANG_ICONS.get(ext,"📄"),
            "ext":ext,
            "mtime":datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M"),
            "mtime_raw":mtime
        })

    files.sort(key=lambda x: x["mtime_raw"], reverse=True)

    return files[:10]

def load_views():

    if not os.path.exists(VIEWS_FILE):
        return {}

    try:
        with open(VIEWS_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_views(data):

    os.makedirs(os.path.dirname(VIEWS_FILE), exist_ok=True)

    fd,tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(VIEWS_FILE),
        prefix="views_",
        suffix=".tmp"
    )

    try:

        with os.fdopen(fd,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False)

        os.replace(tmp_path,VIEWS_FILE)

    finally:

        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def increase_view(filename):

    views = load_views()

    views[filename] = int(views.get(filename,0)) + 1

    save_views(views)

    return views[filename]


def parse_filename(filename):

    name = filename.rsplit(".",1)[0]

    m = re.match(r"(\d+)(?:part(\d+))?",name)

    if not m:
        return None,None,name

    work = int(m.group(1))
    part = m.group(2)

    if part:
        title = f"Практическая работа {work} часть {part}"
    else:
        title = f"Практическая работа {work}"

    return work,part,title


@app.route("/")
def index():

    works = {}
    total = 0

    for f in os.listdir(CODE_DIR):

        if not is_allowed(f):
            continue

        path = os.path.join(CODE_DIR, f)

        work, part, title = parse_filename(f)

        ext = f.split(".")[-1]

        mtime = os.path.getmtime(path)

        entry = {
            "filename": f,
            "title": title,
            "icon": LANG_ICONS.get(ext, "📄"),
            "ext": ext,
            "mtime": datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M"),
        }

        if work not in works:
            works[work] = []

        works[work].append(entry)

        total += 1

    latest = get_latest_files()[:5]

    return render_template(
        "index.html",
        works=works,
        latest=latest,
        total=total
    )


@app.route("/view/<filename>")
def view_file(filename):

    path = get_safe_file_path(filename)

    views = increase_view(filename)

    content = read_text_file_limited(path)

    ext = filename.rsplit(".",1)[1].lower()

    if ext == "md":

        raw_html = markdown.markdown(
            content,
            extensions=["fenced_code","tables"]
        )

        allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
            "p","pre","code","hr","br","h1","h2","h3","h4","h5","h6",
            "table","thead","tbody","tr","th","td","blockquote","span"
        })

        allowed_attrs = {
            **bleach.sanitizer.ALLOWED_ATTRIBUTES,
            "a":["href","title","target","rel"],
            "code":["class"],
            "span":["class"]
        }

        clean_html = bleach.clean(
            raw_html,
            tags=allowed_tags,
            attributes=allowed_attrs,
            protocols=["http","https","mailto"],
            strip=True
        )

        return render_template(
            "view.html",
            filename=filename,
            markdown=clean_html,
            is_markdown=True,
            views=views
        )

    lines = content.splitlines()

    return render_template(
        "view.html",
        filename=filename,
        lines=lines,
        is_markdown=False,
        language=ext,
        views=views
    )


@app.route("/download/<filename>")
def download(filename):

    path = get_safe_file_path(filename)

    return send_from_directory(
        CODE_DIR,
        os.path.basename(path),
        as_attachment=True
    )
    
@app.route("/updates")
def updates():

    latest_files = get_latest_files()

    return render_template(
        "updates.html",
        latest=latest_files
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)