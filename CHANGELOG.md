# Changelog

All notable changes to Malaysia Realty Analyzer are documented in this file,
grouped by date. This project doesn't follow a formal version-number scheme,
so entries are ordered chronologically (newest first) based on commit history.

## 2026-08-10

### Fixed
- CI reliability: wrapped the SSH steps in `backup.yml` and `docker-cleanup.yml`
  with `Wandalen/wretry.action` (3 attempts, 10s backoff) after diagnosing
  intermittent scheduled-workflow failures caused by a transient TCP dial
  timeout between GitHub Actions and the VPS (not a reboot, firewall block, or
  fail2ban ban — traced to network conditions upstream of the VPS).

### Security
- Hardened VPS SSH: installed and enabled fail2ban for the `sshd` jail,
  changed the UFW SSH rule from `ALLOW` to `LIMIT` (rate-limiting), disabled
  password authentication, and restricted root login to key-only
  (`PermitRootLogin prohibit-password`).

## 2026-07-12

### Added
- `backup.yml` — nightly PostgreSQL backup workflow (SSH into VPS, `pg_dump`,
  retain last 7 backups).
- `docker-cleanup.yml` — weekly Docker build-cache pruning workflow.

## 2026-07-07 — Sprint 6 polish

### Added
- Condo-specialist ML model (GradientBoosting, R²=0.899, MAE≈MYR 129k) wired
  up via `POST /api/analytics/predict/condo` and `GET /api/analytics/predict/info`.
- `App\Http\Middleware\VerifyApiKey` guarding Laravel `import/*` routes and a
  `verify_etl_api_key` dependency guarding Python's `POST /etl/clean/properties`,
  both via shared-secret `X-API-Key` headers.
- Laravel Feature test coverage (`PropertyControllerTest`,
  `AnalyticsControllerTest`, `ImportApiKeyTest`) and Python pytest coverage
  (`test_etl.py`, `test_predictions_paths.py`), wired into `pr-checks.yml`.
- Local dev Docker Compose setup with hot reload.

### Fixed
- General ML model path resolution now checks `models/<file>` first, falling
  back to the legacy `python-service/<file>` root location with a one-time
  `DeprecationWarning`.
- Pinned the Laravel Vite dev server to port 5199.

### Changed
- Untracked `model_features.pkl` from git.

## 2026-05-05

### Added
- `pr-checks.yml` — CI workflow running Laravel and Python checks on pull requests.
- Health check endpoint plus a verify step in the deploy pipeline.

### Fixed
- Nginx security headers.
- `laravel-checks` now runs on PHP 8.4; PHP code style fixed with Pint.

### Changed
- Deploy pipeline steps given explicit names for clearer CI logs.

## 2026-04-22

### Fixed
- Map and property-listing index UI width/layout issues.

## 2026-04-09

### Added
- README screenshots.

### Fixed
- Chart rendering and model update issues.

### Changed
- Untracked `price_model.pkl` from git.

## 2026-04-06

### Fixed
- Dark input box and white-background number-input styling on the predict page.

## 2026-03-28 – 2026-03-29

### Added
- Initial Docker setup (PHP 8.4 CLI, production Nginx config) and the first
  CI/CD deploy workflow.

### Fixed
- Removed `@nuxtjs/tailwindcss` (was crashing the production build) and
  downgraded `@nuxt/ui` to v2 for Tailwind compatibility.
- Passed the API base URL as a Nuxt Docker build arg.
- Excluded `.env` from the Python Docker image, reading config from the VPS
  `env_file` instead.
- Added PostgreSQL support in `db.py`, updated CORS config, switched
  `DATE_FORMAT` to `TO_CHAR`, added `psycopg2-binary`.
- Persisted ML model files using a Docker named volume.

## 2026-03-26

### Added
- Initial commit, README, and the first version of the analytics page.
