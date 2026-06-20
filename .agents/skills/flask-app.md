# Flask application skill

Use this file for changes to routes, templates, static files, configuration,
file serving, Markdown rendering, or view statistics.

## Architecture

- Create the application through the factory in `app/__init__.py`.
- Keep HTTP concerns in `app/routes` and reusable logic in `app/services`.
- Register routes as Blueprints.
- Use Blueprint-qualified Jinja endpoints, for example
  `url_for("files.view_file", filename=filename)`.
- Resolve files through `APP_PATHS`; behavior must not depend on the process
  working directory.

## File handling and security

- Keep filename extension allowlisting and safe-name validation.
- Reject path separators, hidden names, traversal attempts, unsupported
  extensions, missing files, and oversized files with appropriate status codes.
- Use safe path joining and verify that the final target is a regular file.
- Sanitize Markdown HTML through the existing service. Never apply Jinja
  `safe` to content that has not passed through the sanitizer.
- Keep user-controlled values escaped in templates and encoded in URLs.

## State and concurrency

- Tests must redirect `APP_PATHS.views_json` to `tmp_path`.
- Preserve atomic writes and inter-process locking for view counters because
  Gunicorn uses multiple workers and threads.
- Do not increment views for requests that fail validation or file reading.

## UI behavior

- Preserve dark/light theme behavior and responsive layouts.
- Keep search and filters server-rendered and usable without JavaScript.
- Ensure interactive controls are keyboard accessible and have labels.
- Verify generated links by requesting the affected pages through Flask's test
  client; template compilation alone is insufficient.
