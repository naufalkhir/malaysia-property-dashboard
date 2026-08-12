# Wire up prediction_logs (Recent Predictions widget) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire up the dead `prediction_logs` table by logging every `/predict` and `/predict/condo` call from Laravel, exposing the last 10 as `GET /api/analytics/predict/recent`, and showing them in a "Recent Predictions" widget on `predict.vue`.

**Architecture:** `AnalyticsController` writes a `PredictionLog` row synchronously (wrapped in try/catch so a DB failure never breaks the prediction response) right after it gets the Python service's response and before returning it to the frontend. A new read-only GET endpoint serves the last 10 rows; the Nuxt page fetches it on load and again after each successful prediction.

**Tech Stack:** Laravel 13 (Eloquent, PHPUnit Feature tests, sqlite in-memory for tests), Nuxt 3 (Composition API, `$fetch`).

**Spec:** `docs/superpowers/specs/2026-08-11-prediction-logs-wireup-design.md`

---

## File Structure

- Create: `laravel-api/app/Models/PredictionLog.php` — Eloquent model for the existing `prediction_logs` table (no new migration needed, table already exists).
- Modify: `laravel-api/app/Http/Controllers/AnalyticsController.php` — add logging to `predict()`/`predictCondo()`, add `recentPredictions()`.
- Modify: `laravel-api/routes/api.php` — register `GET /predict/recent`.
- Modify: `laravel-api/tests/Feature/AnalyticsControllerTest.php` — add `RefreshDatabase`, 4 new test methods.
- Modify: `nuxt-frontend/app/pages/dashboard/predict.vue` — add the Recent Predictions widget.

---

### Task 1: `PredictionLog` model

**Files:**
- Create: `laravel-api/app/Models/PredictionLog.php`

- [ ] **Step 1: Create the model**

The `prediction_logs` table (migrated 2026-03-25, already live) has `id`, `input_features` (json), `predicted_price` (decimal 15,2), `model_version` (string), and `created_at` only — no `updated_at`.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PredictionLog extends Model
{
    // Schema has created_at but no updated_at column.
    const UPDATED_AT = null;

    protected $fillable = [
        'input_features',
        'predicted_price',
        'model_version',
    ];

    protected $casts = [
        'input_features' => 'array',
        'predicted_price' => 'decimal:2',
    ];
}
```

There's no meaningful behavior to unit-test on a plain data model — it's exercised end-to-end by the Feature tests in Task 2.

- [ ] **Step 2: Commit**

```bash
git add laravel-api/app/Models/PredictionLog.php
git commit -m "feat: add PredictionLog model for the existing prediction_logs table"
```

---

### Task 2: Log every prediction to `prediction_logs`

**Files:**
- Modify: `laravel-api/tests/Feature/AnalyticsControllerTest.php`
- Modify: `laravel-api/app/Http/Controllers/AnalyticsController.php:1-28`

- [ ] **Step 1: Write the failing tests**

Replace the top of `laravel-api/tests/Feature/AnalyticsControllerTest.php` (the `use` imports and class declaration, lines 1-9) with:

```php
<?php

namespace Tests\Feature;

use App\Models\PredictionLog;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class AnalyticsControllerTest extends TestCase
{
    use RefreshDatabase;

```

Then add these two test methods inside the class (e.g. directly after `test_predict_forwards_request_body_to_python_service_and_returns_its_response`, before `test_trends_calls_python_service_with_state_in_the_url`):

```php
    public function test_predict_writes_a_prediction_log_row_with_correct_fields(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/predict' => Http::response([
                'predicted_price' => 500000,
                'low' => 425000,
                'high' => 575000,
                'model' => 'general',
            ], 200),
        ]);

        $payload = [
            'state' => 'Selangor',
            'property_type' => 'Condominium',
            'size_sqft' => 1000,
            'bedrooms' => 3,
        ];

        $this->postJson('/api/analytics/predict', $payload)->assertOk();

        $this->assertDatabaseHas('prediction_logs', [
            'predicted_price' => 500000,
            'model_version' => 'general',
        ]);

        $log = PredictionLog::first();
        $this->assertSame($payload, $log->input_features);
    }

    public function test_predict_condo_writes_a_prediction_log_row_with_condo_specialist_model_version(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/predict/condo' => Http::response([
                'predicted_price' => 620000,
                'low' => 540000,
                'high' => 700000,
                'model' => 'condo-specialist',
            ], 200),
        ]);

        $payload = [
            'state' => 'Kuala Lumpur',
            'size_sqft' => 850,
            'bedrooms' => 2,
        ];

        $this->postJson('/api/analytics/predict/condo', $payload)->assertOk();

        $this->assertDatabaseHas('prediction_logs', [
            'predicted_price' => 620000,
            'model_version' => 'condo-specialist',
        ]);
    }
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd laravel-api && php artisan test --filter=AnalyticsControllerTest`
Expected: the 2 new tests FAIL (`assertDatabaseHas` finds no `prediction_logs` row — the controller doesn't write anything yet). The 3 pre-existing tests in this file still PASS.

- [ ] **Step 3: Implement logging in the controller**

Replace `laravel-api/app/Http/Controllers/AnalyticsController.php:1-28` with:

```php
<?php

namespace App\Http\Controllers;

use App\Models\PredictionLog;
use App\Services\PythonAnalyticsService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class AnalyticsController extends Controller
{
    // PythonAnalyticsService is injected automatically by Laravel
    // This is called "dependency injection" — Laravel creates the service for us
    public function __construct(protected PythonAnalyticsService $python) {}

    // POST /api/analytics/predict
    public function predict(Request $request)
    {
        $result = $this->python->post('/predict', $request->all());

        $this->logPrediction($request->all(), $result);

        return response()->json($result);
    }

    // POST /api/analytics/predict/condo
    public function predictCondo(Request $request)
    {
        $result = $this->python->post('/predict/condo', $request->all());

        $this->logPrediction($request->all(), $result);

        return response()->json($result);
    }

    // Writes a prediction_logs row. Must never throw or block the
    // prediction response — a visitor waiting on a price estimate should
    // never see a failure because logging failed.
    private function logPrediction(array $inputFeatures, array $result): void
    {
        try {
            PredictionLog::create([
                'input_features' => $inputFeatures,
                'predicted_price' => $result['predicted_price'] ?? null,
                'model_version' => $result['model'] ?? 'v1',
            ]);
        } catch (\Throwable $e) {
            Log::warning('Failed to write prediction log: '.$e->getMessage());
        }
    }
```

Leave `modelInfo()` (line 30 onward in the original file) and everything below it unchanged — just make sure the class's closing brace still matches up.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd laravel-api && php artisan test --filter=AnalyticsControllerTest`
Expected: all 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add laravel-api/app/Http/Controllers/AnalyticsController.php laravel-api/tests/Feature/AnalyticsControllerTest.php
git commit -m "feat: log every prediction to prediction_logs"
```

---

### Task 3: `GET /api/analytics/predict/recent`

**Files:**
- Modify: `laravel-api/tests/Feature/AnalyticsControllerTest.php`
- Modify: `laravel-api/app/Http/Controllers/AnalyticsController.php` (add method after `modelInfo()`)
- Modify: `laravel-api/routes/api.php:20`

- [ ] **Step 1: Write the failing test**

Add this test method to `AnalyticsControllerTest.php` (anywhere in the class, e.g. after the two tests added in Task 2):

```php
    public function test_recent_predictions_returns_last_ten_rows_newest_first(): void
    {
        foreach (range(1, 12) as $i) {
            $log = PredictionLog::create([
                'input_features' => ['state' => 'Selangor'],
                'predicted_price' => 100000 + $i,
                'model_version' => 'general',
            ]);
            // forceFill bypasses mass-assignment protection so each row
            // gets a distinct, ordered created_at for a deterministic test.
            $log->forceFill(['created_at' => now()->addMinutes($i)])->save();
        }

        $response = $this->getJson('/api/analytics/predict/recent');

        $response->assertOk();
        $response->assertJsonCount(10);
        $response->assertJsonPath('0.predicted_price', '100012.00');
        $response->assertJsonPath('9.predicted_price', '100003.00');
    }
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd laravel-api && php artisan test --filter=AnalyticsControllerTest`
Expected: FAIL — `GET /api/analytics/predict/recent` 404s (route doesn't exist yet).

- [ ] **Step 3: Implement the endpoint and route**

Add this method to `AnalyticsController.php`, directly after `modelInfo()`:

```php
    // GET /api/analytics/predict/recent
    public function recentPredictions()
    {
        return response()->json(
            PredictionLog::orderByDesc('created_at')
                ->limit(10)
                ->get(['id', 'input_features', 'predicted_price', 'model_version', 'created_at'])
        );
    }
```

In `laravel-api/routes/api.php`, add a line directly after `Route::get('/predict/info', 'modelInfo');` (currently line 20):

```php
    Route::get('/predict/recent', 'recentPredictions');
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `cd laravel-api && php artisan test --filter=AnalyticsControllerTest`
Expected: all 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add laravel-api/app/Http/Controllers/AnalyticsController.php laravel-api/routes/api.php laravel-api/tests/Feature/AnalyticsControllerTest.php
git commit -m "feat: add GET /api/analytics/predict/recent endpoint"
```

---

### Task 4: Regression-guard test — logging failure must not break the prediction response

This is the design's core safety promise (see spec). It's already implemented by the try/catch in Task 2, so this test won't naturally go red before implementation exists. Instead, verify it actually catches a regression by temporarily breaking the code, confirming the test fails, then restoring it.

**Files:**
- Modify: `laravel-api/tests/Feature/AnalyticsControllerTest.php`

- [ ] **Step 1: Write the test**

Add `use Illuminate\Support\Facades\Schema;` to the imports at the top of `AnalyticsControllerTest.php` (alongside the other `use` statements from Task 2).

Add this test method:

```php
    public function test_predict_still_returns_200_when_prediction_log_write_fails(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/predict' => Http::response([
                'predicted_price' => 500000,
                'low' => 425000,
                'high' => 575000,
                'model' => 'general',
            ], 200),
        ]);

        // Simulate a DB failure on the logging write path.
        Schema::drop('prediction_logs');

        $response = $this->postJson('/api/analytics/predict', [
            'state' => 'Selangor',
            'property_type' => 'Condominium',
            'size_sqft' => 1000,
            'bedrooms' => 3,
        ]);

        $response->assertOk();
        $response->assertJson(['predicted_price' => 500000, 'model' => 'general']);
    }
```

- [ ] **Step 2: Run it — confirm it currently passes**

Run: `cd laravel-api && php artisan test --filter=AnalyticsControllerTest`
Expected: PASS (Task 2's try/catch already handles this).

- [ ] **Step 3: Prove the test actually guards the behavior**

In `AnalyticsController.php`, temporarily change `logPrediction()` to remove the try/catch (call `PredictionLog::create(...)` directly, no `try`/`catch`). Re-run:

Run: `cd laravel-api && php artisan test --filter=AnalyticsControllerTest`
Expected: `test_predict_still_returns_200_when_prediction_log_write_fails` now FAILS (the request throws a `QueryException` and the response is a 500), confirming the test would catch a future regression.

Then restore the try/catch exactly as it was in Task 2.

- [ ] **Step 4: Run the full suite to confirm everything passes again**

Run: `cd laravel-api && php artisan test --filter=AnalyticsControllerTest`
Expected: all 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add laravel-api/tests/Feature/AnalyticsControllerTest.php
git commit -m "test: guard that a prediction_logs write failure never breaks /predict"
```

---

### Task 5: Recent Predictions widget on `predict.vue`

There's no frontend test infrastructure in this project (no vitest/jest configured) — this task is implementation + manual verification, matching how the rest of the Nuxt frontend is built.

**Files:**
- Modify: `nuxt-frontend/app/pages/dashboard/predict.vue`

- [ ] **Step 1: Add the fetch logic and helper to the script**

In `predict.vue`, replace the `<script setup>` block's imports and add new reactive state. Change:

```js
import { ref, computed } from "vue";
import { useHead, useRuntimeConfig } from "#app";
```

to:

```js
import { ref, computed, onMounted } from "vue";
import { useHead, useRuntimeConfig } from "#app";
```

Then, directly after the `const loading = ref(false);` line, add:

```js
const recentPredictions = ref([]);

const fetchRecentPredictions = async () => {
  try {
    recentPredictions.value = await $fetch(`${apiBase}/api/analytics/predict/recent`);
  } catch {
    recentPredictions.value = [];
  }
};

const formatRelativeTime = (isoString) => {
  const diffMin = Math.round((Date.now() - new Date(isoString).getTime()) / 60000);
  if (diffMin < 1) return "just now";
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHr = Math.round(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h ago`;
  return `${Math.round(diffHr / 24)}d ago`;
};

onMounted(fetchRecentPredictions);
```

- [ ] **Step 2: Refetch after a successful prediction**

In the `predict()` function, find this line:

```js
    result.value = await $fetch(endpoint, {
      method: "POST",
      body: payload,
    });
```

and add a refetch directly after it:

```js
    result.value = await $fetch(endpoint, {
      method: "POST",
      body: payload,
    });
    fetchRecentPredictions();
```

- [ ] **Step 3: Add the widget to the template**

In the `<template>`, directly after the closing `</div>` of the two-column form/result grid (the `<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem">...</div>` block, currently ending at line 688) and before the outer container's closing `</div>` (line 689), add:

```html
      <!-- Recent Predictions -->
      <div style="margin-top: 2.5rem">
        <h2
          style="
            font-size: 1.4rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1rem;
          "
        >
          Recent Predictions
        </h2>
        <div
          v-if="recentPredictions.length === 0"
          style="color: #94a3b8; font-size: 0.95rem"
        >
          No predictions yet — be the first!
        </div>
        <div
          v-else
          style="
            background: white;
            border-radius: 1rem;
            border: 1px solid #e2e8f0;
            overflow: hidden;
          "
        >
          <table style="width: 100%; border-collapse: collapse">
            <thead>
              <tr style="background: #f8fafc; text-align: left">
                <th
                  style="
                    padding: 0.75rem 1rem;
                    font-size: 0.75rem;
                    color: #64748b;
                    text-transform: uppercase;
                  "
                >
                  State
                </th>
                <th
                  style="
                    padding: 0.75rem 1rem;
                    font-size: 0.75rem;
                    color: #64748b;
                    text-transform: uppercase;
                  "
                >
                  Model
                </th>
                <th
                  style="
                    padding: 0.75rem 1rem;
                    font-size: 0.75rem;
                    color: #64748b;
                    text-transform: uppercase;
                  "
                >
                  Size (sqft)
                </th>
                <th
                  style="
                    padding: 0.75rem 1rem;
                    font-size: 0.75rem;
                    color: #64748b;
                    text-transform: uppercase;
                  "
                >
                  Predicted Price
                </th>
                <th
                  style="
                    padding: 0.75rem 1rem;
                    font-size: 0.75rem;
                    color: #64748b;
                    text-transform: uppercase;
                  "
                >
                  When
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="log in recentPredictions"
                :key="log.id"
                style="border-top: 1px solid #f1f5f9"
              >
                <td style="padding: 0.75rem 1rem; color: #1e293b">
                  {{ log.input_features.state }}
                </td>
                <td style="padding: 0.75rem 1rem; color: #475569">
                  {{ log.model_version === "condo-specialist" ? "Condo" : "General" }}
                </td>
                <td style="padding: 0.75rem 1rem; color: #475569">
                  {{ log.input_features.size_sqft }}
                </td>
                <td style="padding: 0.75rem 1rem; font-weight: 700; color: #1e293b">
                  MYR {{ Number(log.predicted_price).toLocaleString() }}
                </td>
                <td style="padding: 0.75rem 1rem; color: #94a3b8; font-size: 0.85rem">
                  {{ formatRelativeTime(log.created_at) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
```

- [ ] **Step 4: Manual verification**

Start the stack (either `docker compose up` from the repo root, or `php artisan serve` + `uvicorn main:app --port 8001` in `python-service/` + `npm run dev` in `nuxt-frontend/` — whichever matches how you normally run local dev). Visit `/dashboard/predict`:

1. On load, confirm the Recent Predictions section renders (either the empty state or existing rows, depending on prior test data in your DB).
2. Submit a prediction (general model). Confirm the result card shows, and the Recent Predictions table updates to include the new row at the top within a second or two.
3. Switch to the condo model, submit again. Confirm the new row shows "Condo" in the Model column.
4. Refresh the page. Confirm the rows persist (proves they're coming from the DB, not local state).

- [ ] **Step 5: Commit**

```bash
git add nuxt-frontend/app/pages/dashboard/predict.vue
git commit -m "feat: add Recent Predictions widget to the predict page"
```

---

## Post-implementation

Update `CLAUDE.md`'s Sprint 6 "Still open" list: mark `prediction_logs dead schema` as done (wired up, not dropped), matching the pattern used for the other completed items (`~~strikethrough~~ — DONE (date): ...`).
