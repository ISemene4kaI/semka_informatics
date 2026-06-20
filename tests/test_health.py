from app.app import app
from app.config import APP_PATHS


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_pages_and_download(tmp_path, monkeypatch):
    monkeypatch.setattr(APP_PATHS, "views_json", tmp_path / "views.json")
    client = app.test_client()

    assert client.get("/").status_code == 200
    assert client.get("/updates").status_code == 200
    assert client.get("/view/1part1.py").status_code == 200

    response = client.get("/download/1part1.py")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment;")
