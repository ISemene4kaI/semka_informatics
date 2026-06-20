from concurrent.futures import ThreadPoolExecutor

from app.config import APP_PATHS
from app.services.file_service import list_allowed_filenames
from app.services.markdown_service import render_markdown_safe
from app.services.views_service import increase_view, load_views


def test_filenames_are_sorted_naturally():
    filenames = list_allowed_filenames()

    assert filenames.index("2part1.py") < filenames.index("10part1.md")
    assert filenames.index("10part1.md") < filenames.index("10part2.py")


def test_markdown_removes_unsafe_html():
    rendered = render_markdown_safe(
        '[safe](https://example.com) <script>alert("xss")</script>'
    )

    assert "<script" not in rendered
    assert 'href="https://example.com"' in rendered


def test_view_counter_is_safe_for_concurrent_updates(tmp_path, monkeypatch):
    monkeypatch.setattr(APP_PATHS, "views_json", tmp_path / "views.json")

    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(increase_view, ["1part1.py"] * 25))

    assert load_views()["1part1.py"] == 25
