# Project reference

## Purpose

`semka_informatics` is a Flask website that publishes programming and numerical
methods assignments. It displays source files from `app/code_storage`, safely
renders Markdown, offers downloads, and tracks file views.

## Repository layout

- `app/app.py` — application entry point.
- `app/__init__.py` — Flask factory, middleware, and error handlers.
- `app/config.py` — environment configuration and absolute project paths.
- `app/routes/` — page, file, and health Blueprints.
- `app/services/` — file handling, Markdown rendering, and view persistence.
- `app/templates/` — Jinja templates.
- `app/static/` — browser CSS and JavaScript.
- `app/code_storage/` — files published as assignment solutions.
- `tests/` — route, service, security, and numerical tests.
- `requirements.txt` — production website dependencies.
- `requirements-dev.txt` — test and lint dependencies.
- `requirements-solutions.txt` — NumPy and Matplotlib for assignment scripts.
- `.github/workflows/ci.yml` — CI and GHCR image publication.

## Runtime and deployment

- Python 3.12, Flask, and Gunicorn.
- Production listens on port `8000`.
- k3s runs the application behind Traefik.
- Argo CD reads manifests from `ISemene4kaI/sites_kubernetes`.
- `/health` is the liveness endpoint.
- `/ready` is the readiness endpoint.
- View counts are persisted at `/data/views.json` on a PVC.
- The container runs as a non-root user.
- Argo CD Image Updater tracks the digest of the GHCR `latest` tag.

## Variant data

Current numerical-method assignments use:

- `S = 9` — student number.
- `G = 32` — group number.
- `K = 1`.

Keep these values consistent between manual Markdown calculations, executable
solutions, and tests unless the user explicitly changes the variant.
