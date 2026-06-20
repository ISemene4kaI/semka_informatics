from app.app import app
from app.config import APP_PATHS, APP_VARIABLES


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}

    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_pages_and_download(tmp_path, monkeypatch):
    monkeypatch.setattr(APP_PATHS, "views_json", tmp_path / "views.json")
    client = app.test_client()

    assert client.get("/").status_code == 200
    assert client.get("/updates").status_code == 200
    assert client.get("/stats").status_code == 200
    assert client.get("/feed.xml").status_code == 200
    assert client.get("/view/1part1.py").status_code == 200

    response = client.get("/download/1part1.py")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment;")


def test_search_and_language_filter():
    client = app.test_client()

    response = client.get("/?q=10&lang=md")

    assert response.status_code == 200
    assert b"10part1.md" in response.data
    assert b"10part2.py" not in response.data


def test_file_errors(monkeypatch):
    client = app.test_client()

    assert client.get("/view/.secret.py").status_code == 403
    assert client.get("/view/missing.py").status_code == 404

    monkeypatch.setattr(APP_VARIABLES, "max_file_bytes", 1)
    assert client.get("/view/1part1.py").status_code == 413
