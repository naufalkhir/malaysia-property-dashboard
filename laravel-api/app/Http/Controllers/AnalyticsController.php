<?php

namespace App\Http\Controllers;

use App\Services\PythonAnalyticsService;
use Illuminate\Http\Request;

class AnalyticsController extends Controller
{
    // PythonAnalyticsService is injected automatically by Laravel
    // This is called "dependency injection" — Laravel creates the service for us
    public function __construct(protected PythonAnalyticsService $python) {}

    // POST /api/analytics/predict
    public function predict(Request $request)
    {
        return response()->json(
            $this->python->post('/predict', $request->all())
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
