<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

class PythonAnalyticsService
{
    private string $baseUrl;

    public function __construct()
    {
        // Reads PYTHON_SERVICE_URL from .env
        // Default: http://127.0.0.1:8001 (where FastAPI runs locally)
        $this->baseUrl = config('services.python.url', 'http://127.0.0.1:8001');
    }

    // Make a GET request to Python service
    public function get(string $endpoint): array
    {
        $response = Http::timeout(10)->get($this->baseUrl . $endpoint);
        return $response->json();
    }

    // Make a POST request to Python service
    public function post(string $endpoint, array $data): array
    {
        $response = Http::timeout(30)->post($this->baseUrl . $endpoint, $data);
        return $response->json();
    }
}
