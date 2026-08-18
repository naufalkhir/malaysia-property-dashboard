<?php

namespace App\Http\Controllers;

use App\Http\Requests\PredictCondoRequest;
use App\Http\Requests\PredictRequest;
use App\Models\PredictionLog;
use App\Services\PythonAnalyticsService;
use Illuminate\Support\Facades\Log;

class AnalyticsController extends Controller
{
    // PythonAnalyticsService is injected automatically by Laravel
    // This is called "dependency injection" — Laravel creates the service for us
    public function __construct(protected PythonAnalyticsService $python) {}

    // POST /api/analytics/predict
    public function predict(PredictRequest $request)
    {
        $result = $this->python->post('/predict', $request->validated());

        $this->logPrediction($request->validated(), $result);

        return response()->json($result);
    }

    // POST /api/analytics/predict/condo
    public function predictCondo(PredictCondoRequest $request)
    {
        $result = $this->python->post('/predict/condo', $request->validated());

        $this->logPrediction($request->validated(), $result);

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

    // GET /api/analytics/predict/info
    public function modelInfo()
    {
        return response()->json(
            $this->python->get('/predict/info')
        );
    }

    // GET /api/analytics/predict/recent
    public function recentPredictions()
    {
        return response()->json(
            PredictionLog::orderByDesc('created_at')
                ->orderByDesc('id')
                ->limit(10)
                ->get(['id', 'input_features', 'predicted_price', 'model_version', 'created_at'])
        );
    }

    // GET /api/analytics/trends/{state}
    public function trends($state)
    {
        return response()->json(
            $this->python->get("/charts/trends/{$state}")
        );
    }

    // GET /api/analytics/distribution
    public function distribution()
    {
        return response()->json(
            $this->python->get('/charts/distribution')
        );
    }

    // GET /api/analytics/affordability
    public function affordability()
    {
        return response()->json(
            $this->python->get('/stats/affordability')
        );
    }

    // GET /api/analytics/correlation
    public function correlation()
    {
        return response()->json(
            $this->python->get('/stats/correlation')
        );
    }

    // GET /api/analytics/demographic
    public function demographic()
    {
        return response()->json(
            $this->python->get('/stats/demographic')
        );
    }

    // GET /api/analytics/map/choropleth
    public function choropleth()
    {
        return response()->json(
            $this->python->get('/geodata/choropleth')
        );
    }

    // GET /api/analytics/map/heatmap
    public function heatmap()
    {
        return response()->json(
            $this->python->get('/geodata/heatmap')
        );
    }

    // GET /api/analytics/psf-by-state
    public function psfByState()
    {
        return response()->json(
            $this->python->get('/charts/psf-by-state')
        );
    }

    // GET /api/analytics/type-breakdown
    public function typeBreakdown()
    {
        return response()->json(
            $this->python->get('/charts/type-breakdown')
        );
    }

    // GET /api/analytics/affordability-bar
    public function affordabilityBar()
    {
        return response()->json(
            $this->python->get('/charts/affordability-bar')
        );
    }
}
