import os
from flask import Flask, render_template, abort

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


@app.route("/")
def index():
    files = [
        f for f in os.listdir(CODE_DIR)
        if os.path.isfile(os.path.join(CODE_DIR, f))
        and is_allowed(f)
        and not f.startswith(".")
    ]
    return render_template("index.html", files=files)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)