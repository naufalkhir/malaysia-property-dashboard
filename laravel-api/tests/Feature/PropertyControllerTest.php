<?php

namespace Tests\Feature;

use App\Models\Property;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PropertyControllerTest extends TestCase
{
    use RefreshDatabase;

    private function makeProperty(array $overrides = []): Property
    {
        return Property::create(array_merge([
            'title' => 'Test Property',
            'state' => 'Selangor',
            'city' => 'Shah Alam',
            'area' => 'Section 13',
            'property_type' => 'Condominium',
            'tenure' => 'Freehold',
            'price' => 500000,
            'price_per_sqft' => 500,
            'size_sqft' => 1000,
            'bedrooms' => 3,
            'bathrooms' => 2,
            'car_parks' => 1,
            'furnishing' => 'Partially Furnished',
        ], $overrides));
    }

    public function test_index_returns_only_properties_matching_state_filter(): void
    {
        $this->makeProperty(['state' => 'Selangor']);
        $this->makeProperty(['state' => 'Johor']);

        $response = $this->getJson('/api/properties?state=Selangor');

        $response->assertOk();
        $response->assertJsonCount(1, 'data');
        $this->assertSame('Selangor', $response->json('data.0.state'));
    }

    public function test_index_filters_by_price_range(): void
    {
        $this->makeProperty(['price' => 300000]);
        $this->makeProperty(['price' => 900000]);

        $response = $this->getJson('/api/properties?min_price=500000&max_price=1000000');

        $response->assertOk();
        $response->assertJsonCount(1, 'data');
        $this->assertSame('900000.00', $response->json('data.0.price'));
    }

    public function test_show_returns_a_single_property(): void
    {
        $property = $this->makeProperty();

        $response = $this->getJson("/api/properties/{$property->id}");

        $response->assertOk();
        $response->assertJsonPath('id', $property->id);
    }

    public function test_show_returns_404_for_missing_property(): void
    {
        $response = $this->getJson('/api/properties/999');

        $response->assertNotFound();
    }

    public function test_similar_excludes_the_original_property_and_matches_state_and_type(): void
    {
        $property = $this->makeProperty(['state' => 'Selangor', 'property_type' => 'Condominium', 'price' => 500000]);
        $this->makeProperty(['state' => 'Selangor', 'property_type' => 'Condominium', 'price' => 520000]); // within ±30%
        $this->makeProperty(['state' => 'Selangor', 'property_type' => 'Condominium', 'price' => 900000]); // outside ±30%
        $this->makeProperty(['state' => 'Johor', 'property_type' => 'Condominium', 'price' => 510000]); // wrong state

        $response = $this->getJson("/api/properties/{$property->id}/similar");

        $response->assertOk();
        $ids = collect($response->json())->pluck('id');
        $this->assertNotContains($property->id, $ids);
        $this->assertCount(1, $ids);
    }
}
