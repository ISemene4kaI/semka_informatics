# k3s deployment skill

Use this file for Docker, CI, health checks, persistence, proxy, or GitOps work.

## Production topology

- The application runs in k3s behind Traefik.
- Gunicorn binds to `0.0.0.0:8000`.
- Traefik forwards proxy headers; Flask uses `ProxyFix` with the expected proxy
  count.
- `/health` must remain an inexpensive liveness check.
- `/ready` must report whether required directories and persistent state are
  usable.

## Container constraints

- Run as a non-root user and retain dropped Linux capabilities,
  `allowPrivilegeEscalation: false`, and the runtime-default seccomp profile.
- Keep the production image free of NumPy, Matplotlib, test tools, caches, and
  generated assignment artifacts.
- Keep stdout/stderr suitable for Kubernetes logs.
- Do not hardcode credentials or cluster-specific secrets in the image.

## Persistence

- `VIEWS_FILE` is `/data/views.json` in production.
- `/data` is a PVC mounted with a pod `fsGroup` compatible with the container
  user.
- Changes to persistence must account for concurrent workers, atomicity,
  permissions, pod restarts, and rollback.

## GitOps flow

- CI tests the application, builds the image, and publishes `latest` plus the
  commit SHA to GHCR.
- Argo CD Image Updater follows the mutable `latest` tag using the `digest`
  strategy so a changed image triggers a Deployment rollout.
- Argo CD automated sync uses `prune: true` and `selfHeal: true`.
- Kubernetes manifests and Helm values live in the separate
  `ISemene4kaI/sites_kubernetes` repository.

## Verification

- Render Helm changes before deployment with `helm lint` and `helm template`.
- Verify probes, security context, environment variables, service ports, and
  PVC mounts in the rendered Deployment.
- Applying manifests, pushing Git changes, or touching the cluster requires an
  explicit user request; local validation does not authorize deployment.
