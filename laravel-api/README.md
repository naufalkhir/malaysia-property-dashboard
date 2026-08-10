# Malaysia Realty Analyzer — Laravel API

Laravel 13 API gateway for the [Malaysia Realty Analyzer](../README.md) — a
full-stack property analytics platform for the Malaysian real estate market.
This service exposes property listings and proxies analytics/ML predictions
from the Python FastAPI microservice, so the Nuxt frontend only ever talks to
Laravel directly.

Live at [propertyanalytics.naufaldev.cloud](https://propertyanalytics.naufaldev.cloud).

## Stack

- Laravel 13, PHP 8.4
- PostgreSQL 16 (production) / MySQL (local dev)
- Proxies to a Python FastAPI service for ML predictions, charts, and geodata

## API Routes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/properties` | List properties |
| GET | `/api/properties/stats/summary` | Summary stats |
| GET | `/api/properties/{id}` | Property details |
| GET | `/api/properties/{id}/similar` | Similar properties |
| POST | `/api/analytics/predict` | Price prediction (general model) |
| POST | `/api/analytics/predict/condo` | Price prediction (condo-specialist model) |
| GET | `/api/analytics/predict/info` | Model metadata |
| GET | `/api/analytics/trends/{state}` | Price trends by state |
| GET | `/api/analytics/distribution` | Price distribution |
| GET | `/api/analytics/affordability` | Affordability analysis |
| GET | `/api/analytics/correlation` | Feature correlation |
| GET | `/api/analytics/demographic` | Demographic breakdown |
| GET | `/api/analytics/map/choropleth` | Choropleth map data |
| GET | `/api/analytics/map/heatmap` | Heatmap data |
| GET | `/api/analytics/psf-by-state` | Price-per-sqft by state |
| GET | `/api/analytics/type-breakdown` | Property type breakdown |
| GET | `/api/analytics/affordability-bar` | Affordability bar chart data |
| POST | `/api/import/properties` | Import property CSV (requires `X-API-Key`) |
| POST | `/api/import/dosm` | Import DOSM demographic data (requires `X-API-Key`) |
| GET | `/api/import/status` | Import status (requires `X-API-Key`) |
| GET | `/api/health` | Health check |

`import/*` routes are protected by `App\Http\Middleware\VerifyApiKey`, which
checks the `X-API-Key` header against `IMPORT_API_KEY`.

## Local Setup

```bash
composer install
cp .env.example .env
php artisan key:generate
```

Set `DB_CONNECTION` (sqlite for a quick start, or mysql/pgsql — see
`.env.example`), and `PYTHON_SERVICE_URL` to point at the local Python
service (default `http://127.0.0.1:8001`).

```bash
php artisan migrate
php artisan serve
```

Or run the whole stack (server, queue listener, logs, Vite) together:

```bash
composer run dev
```

## Testing

```bash
php artisan test
```

Feature test coverage lives in `tests/Feature/` (`PropertyControllerTest`,
`AnalyticsControllerTest`, `ImportApiKeyTest`). Wired into `pr-checks.yml` CI.

## Code Style

```bash
./vendor/bin/pint
```
