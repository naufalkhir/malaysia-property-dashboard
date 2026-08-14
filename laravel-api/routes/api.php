<?php

use App\Http\Controllers\AnalyticsController;
use App\Http\Controllers\ImportController;
use App\Http\Controllers\PropertyController;
use Illuminate\Support\Facades\Route;

// ── Properties ────────────────────────────────────────────────────
Route::prefix('properties')->controller(PropertyController::class)->group(function () {
    Route::get('/', 'index');
    Route::get('/stats/summary', 'summary');
    Route::get('/{id}', 'show');
    Route::get('/{id}/similar', 'similar');
});

// ── Analytics (proxied to Python) ─────────────────────────────────
Route::prefix('analytics')->controller(AnalyticsController::class)->group(function () {
    Route::post('/predict', 'predict');
    Route::post('/predict/condo', 'predictCondo');
    Route::get('/predict/info', 'modelInfo');
    Route::get('/predict/recent', 'recentPredictions');
    Route::get('/trends/{state}', 'trends');
    Route::get('/distribution', 'distribution');
    Route::get('/affordability', 'affordability');
    Route::get('/correlation', 'correlation');
    Route::get('/demographic', 'demographic');
    Route::get('/map/choropleth', 'choropleth');
    Route::get('/map/heatmap', 'heatmap');

    // NEW: Add the missing Plotly chart endpoints!
    Route::get('/psf-by-state', 'psfByState');
    Route::get('/type-breakdown', 'typeBreakdown');
    Route::get('/affordability-bar', 'affordabilityBar');
});

// ── Import ────────────────────────────────────────────────────────
Route::prefix('import')->middleware('api.key')->controller(ImportController::class)->group(function () {
    Route::post('/properties', 'importProperties');
    Route::post('/dosm', 'importDosm');
    Route::get('/status', 'status');
});

// health check endpoint
Route::get('/health', function () {
    try {
        DB::connection()->getPdo();
        $db = 'connected';
    } catch (Throwable $e) {
        $db = 'down';
    }

    return response()->json([
        'status' => 'ok',
        'db' => $db,
        'timestamp' => now(),
    ]);
});
