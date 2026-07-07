<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ImportApiKeyTest extends TestCase
{
    use RefreshDatabase;

    public function test_import_properties_rejects_request_without_api_key(): void
    {
        $response = $this->postJson('/api/import/properties', []);

        $response->assertStatus(401);
    }

    public function test_import_properties_rejects_request_with_wrong_api_key(): void
    {
        $response = $this->postJson('/api/import/properties', [], [
            'X-API-Key' => 'wrong-key',
        ]);

        $response->assertStatus(401);
    }

    public function test_import_properties_accepts_request_with_correct_api_key(): void
    {
        $response = $this->postJson('/api/import/properties', [], [
            'X-API-Key' => config('services.import.api_key'),
        ]);

        // No file provided, so validation fails — but it must get PAST the auth
        // check first. 401 here would mean the middleware is blocking valid keys.
        $response->assertStatus(422);
    }

    public function test_import_status_rejects_request_without_api_key(): void
    {
        $response = $this->getJson('/api/import/status');

        $response->assertStatus(401);
    }

    public function test_import_status_accepts_request_with_correct_api_key(): void
    {
        $response = $this->getJson('/api/import/status', [
            'X-API-Key' => config('services.import.api_key'),
        ]);

        $response->assertOk();
    }
}
