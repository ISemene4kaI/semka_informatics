# Testing skill

Use this file whenever behavior changes or a defect is fixed.

## Environment

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/pip install -r requirements-solutions.txt
```

## Required final checks

```bash
MPLCONFIGDIR=/tmp/matplotlib .venv/bin/pytest -q
.venv/bin/ruff check .
.venv/bin/python -m py_compile app/code_storage/*.py
git diff --check
```

## Test organization

- Route and health behavior belongs in `tests/test_health.py` or a focused route
  test module.
- Service behavior belongs in `tests/test_services.py`.
- Numerical solutions belong in `tests/test_solutions.py`.
- Use fixtures and `monkeypatch` instead of changing global project files.
- Use `tmp_path` for view databases, generated images, plots, and temporary
  source files.

## Coverage expectations

- Test successful routes and expected `403`, `404`, and `413` responses.
- Test search and filtering with both matches and empty results.
- Test unsafe Markdown and path traversal attempts.
- Test numerical functions against an independent expected result.
- Test failure behavior for malformed inputs, singular matrices, missing files,
  and non-convergence when those paths are introduced or changed.
