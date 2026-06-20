# Instructions for AI agents

## Core principles

- Understand the requested outcome and inspect the relevant code before editing.
- Prefer the smallest complete change that solves the underlying problem.
- Follow established project conventions instead of introducing parallel
  patterns without a strong reason.
- Use clear names, simple control flow, explicit interfaces, and standard
  library or framework features where possible.
- Avoid speculative abstractions, premature optimization, duplicated logic,
  hidden side effects, and unnecessary dependencies.
- Preserve backward compatibility unless the task explicitly requires a
  breaking change.
- Never silently overwrite unrelated user changes in a dirty worktree.

## Correctness

- Treat input validation, boundary conditions, error handling, concurrency,
  filesystem behavior, and deployment constraints as part of correctness.
- Trace data through the complete execution path before changing behavior.
- Confirm assumptions against code, configuration, tests, or authoritative
  documentation; do not invent missing APIs or infrastructure capabilities.
- Keep business logic separate from transport, templates, and persistence.
- Make failure modes explicit and return appropriate status codes or errors.
- For numerical code, verify results independently, account for floating-point
  tolerance, and report convergence or residuals where relevant.

## Security

- Assume all request parameters, filenames, file contents, environment values,
  and external data are untrusted.
- Validate inputs with allowlists where practical and preserve path traversal,
  size-limit, and content-sanitization protections.
- Do not expose secrets, internal paths, stack traces, credentials, tokens, or
  sensitive configuration in logs or responses.
- Do not weaken authentication, authorization, TLS, container security,
  sandboxing, or Kubernetes security contexts to make a change easier.
- Avoid command injection, unsafe deserialization, arbitrary file access, XSS,
  race conditions, and insecure temporary-file handling.
- Add dependencies only when justified and keep production dependencies minimal.

## Testing and verification

- Every bug fix must include a regression test when the behavior is testable.
- Every new behavior must include success, failure, and important edge-case
  coverage proportional to its risk.
- Run the narrowest relevant tests while iterating, then run the complete
  project checks before finishing.
- Verify more than syntax: exercise runtime behavior, rendered routes,
  numerical outputs, filesystem effects, and configuration rendering as needed.
- Do not mutate persistent project data during tests. Redirect state to isolated
  temporary paths.
- Never claim a check passed unless it was actually executed. Report any check
  that could not run and the exact reason.

## Change quality

- Keep commits and diffs focused. Do not reformat or rename unrelated files.
- Update documentation and configuration when behavior or operational steps
  change.
- Keep code readable without relying on comments to explain confusing design.
- Comments should explain intent, constraints, or non-obvious decisions rather
  than restating code.
- Remove temporary debugging code, generated artifacts, and test data before
  finishing.
- Review the final diff for accidental changes, whitespace errors, secrets, and
  incomplete migrations.

## Operational safety

- Treat deployments, GitHub writes, cluster changes, database changes, and
  destructive commands as separate actions requiring explicit user intent.
- Prefer reversible changes and preserve a clear rollback path.
- Do not commit, push, publish, deploy, or modify external systems unless the
  user explicitly requested that action.
- Account for the real production environment when changing health checks,
  persistence, proxies, worker concurrency, containers, or resource usage.

## Project knowledge and skills

Repository-specific information is stored under `.agents/`. Read
`.agents/project.md` before substantial work, then read only the skill files
relevant to the current task:

- `.agents/skills/flask-app.md` — Flask architecture, routes, templates, files,
  and view counters.
- `.agents/skills/assignment-solutions.md` — manual and executable assignment
  solutions, naming, and numerical verification.
- `.agents/skills/testing.md` — project test commands and test isolation rules.
- `.agents/skills/k3s-deployment.md` — Docker, GHCR, Traefik, Argo CD, Image
  Updater, probes, and persistent storage.

When a task crosses multiple areas, combine the applicable skill instructions.
If a skill conflicts with this file, this file takes precedence.
