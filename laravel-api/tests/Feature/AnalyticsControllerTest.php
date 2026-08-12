<?php

namespace Tests\Feature;

use App\Models\PredictionLog;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class AnalyticsControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_predict_forwards_request_body_to_python_service_and_returns_its_response(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/predict' => Http::response([
                'predicted_price' => 500000,
                'currency' => 'MYR',
            ], 200),
        ]);

        $payload = [
            'state' => 'Selangor',
            'property_type' => 'Condominium',
            'size_sqft' => 1000,
            'bedrooms' => 3,
        ];

        $response = $this->postJson('/api/analytics/predict', $payload);

        $response->assertOk();
        $response->assertJson(['predicted_price' => 500000, 'currency' => 'MYR']);

        Http::assertSent(function ($request) use ($payload) {
            return $request->url() === 'http://127.0.0.1:8001/predict'
                && $request['state'] === $payload['state']
                && $request['size_sqft'] === $payload['size_sqft'];
        });
    }

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

    public function test_trends_calls_python_service_with_state_in_the_url(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/charts/trends/Selangor' => Http::response(['data' => [], 'layout' => []], 200),
        ]);

        $response = $this->getJson('/api/analytics/trends/Selangor');

        $response->assertOk();
        Http::assertSent(fn ($request) => $request->url() === 'http://127.0.0.1:8001/charts/trends/Selangor');
    }

    public function test_affordability_proxies_get_request_to_python_service(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/stats/affordability' => Http::response(['index' => 1.2], 200),
        ]);

        $response = $this->getJson('/api/analytics/affordability');

        $response->assertOk();
        $response->assertJson(['index' => 1.2]);
    }
}
