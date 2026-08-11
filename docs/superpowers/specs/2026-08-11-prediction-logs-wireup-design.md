# Wire up `prediction_logs` — Recent Predictions widget

Date: 2026-08-11
Status: Approved

## Context

`prediction_logs` (`laravel-api/database/migrations/2026_03_25_145735_create_prediction_logs_table.php`)
has existed since 2026-03-25 with no `PredictionLog` model and nothing writing
to it — flagged as dead schema in `CLAUDE.md` Sprint 6 open items. This spec
decides to wire it up rather than drop it.

Schema (already migrated, no changes needed):
- `id`
- `input_features` (json)
- `predicted_price` (decimal 15,2)
- `model_version` (string, default `'v1'`)
- `created_at` (timestamp, `useCurrent()`) — no `updated_at` column

## Goal

A "Recent Predictions" widget on `nuxt-frontend/app/pages/dashboard/predict.vue`
showing the last 10 predictions made by any site visitor (global feed, not
session-scoped) — a lightweight portfolio feature demonstrating real usage of
the ML prediction tool. No PII is stored or displayed, only property
attributes and predicted price.

## Approaches considered (write path)

1. **Synchronous log-then-respond in Laravel (chosen).** `AnalyticsController`
   writes a `PredictionLog` row right after receiving the Python response,
   before returning JSON to the frontend. Wrapped in try/catch so a logging
   failure never breaks the prediction response.
2. **Queued job.** Rejected — no queue worker exists in
   `docker-compose.prod.yml` today; standing up queue infra just to avoid one
   cheap synchronous INSERT is not worth it.
3. **Log from the Python service.** Rejected — `prediction_logs` is a
   Laravel-owned table (migration lives in `laravel-api/`), and Laravel
   already sees the full response before returning to the frontend. No
   reason to give Python a second write path into a table it doesn't
   otherwise touch.

## Design

### Backend (Laravel)

**Model** — new `App\Models\PredictionLog`:
- `input_features` cast to `array`
- `fillable`: `input_features`, `predicted_price`, `model_version`
- `const UPDATED_AT = null;` (schema has `created_at` only, no `updated_at`
  — this is Laravel's supported way to disable just the one timestamp
  rather than `$timestamps = false`, which would also drop `created_at`
  auto-population)

**Write path** — in `AnalyticsController::predict` and `predictCondo`
(`laravel-api/app/Http/Controllers/AnalyticsController.php:14-28`), after the
Python call succeeds, write one row:
- `input_features` = the request payload (`$request->all()`)
- `predicted_price` = `$result['predicted_price']`
- `model_version` = `$result['model']`

Verified against `python-service/routers/predictions.py`:
- line 201 (`predict`, general model): `"model": "general"`
- line 236 (`predict_condo`): `"model": "condo-specialist"`

Wrapped in try/catch; failures logged via `Log::warning(...)`, never
surfaced to the client and never block the JSON response.

**Read path** — new `AnalyticsController::recentPredictions`:
`GET /api/analytics/predict/recent` → last 10 `PredictionLog` rows ordered
`created_at` desc, returned as plain JSON
(`id`, `input_features`, `predicted_price`, `model_version`, `created_at`).

**Route registration** — add to the existing `analytics` prefix group in
`laravel-api/routes/api.php`, directly after the `predict/info` line
(currently `routes/api.php:20`):
```php
Route::get('/predict/recent', 'recentPredictions');
```

### Frontend (Nuxt)

`nuxt-frontend/app/pages/dashboard/predict.vue`: below the existing
form/result two-column grid, a "Recent Predictions" widget.
- Fetches `GET /api/analytics/predict/recent` on page load.
- Renders a small table/list: state, property type or model badge
  (general/condo-specialist), size, predicted price, relative time.
- After a successful prediction (`predict()` resolves), refetch the recent
  list so the visitor's own guess appears.

### Error handling

- Backend: logging never blocks or fails the prediction response
  (try/catch around the `PredictionLog::create()` call).
- Frontend: if the recent-predictions fetch fails, the widget silently
  shows nothing (or an empty state) — never blocks or errors the predict
  form itself.

### Testing

Laravel Feature tests (extending `AnalyticsControllerTest.php`):
1. POST `/api/analytics/predict` creates a `prediction_logs` row with the
   correct `input_features`, `predicted_price`, `model_version`.
2. GET `/api/analytics/predict/recent` returns rows newest-first, capped
   at 10.
3. **Resilience test**: force `PredictionLog::create()` to throw (e.g. mock
   the model or the DB connection), POST to `/predict`, assert the response
   is still `200` with the correct `predicted_price` — directly covers the
   "a logging failure never breaks the prediction response" guarantee
   rather than just the happy path.

## Out of scope

- Session-scoped/private feed — rejected in favor of the global feed per
  user decision.
- Pagination beyond the last 10 rows.
- Any auth/rate-limiting on the new `/predict/recent` GET endpoint (it's
  read-only and mirrors the existing public `/predict/info` endpoint's
  posture).
