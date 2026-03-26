<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Property extends Model
{
    // These fields can be mass-assigned (e.g. when importing CSV data)
    protected $fillable = [
        'title',
        'state',
        'city',
        'area',
        'property_type',
        'tenure',
        'price',
        'price_per_sqft',
        'size_sqft',
        'bedrooms',
        'bathrooms',
        'car_parks',
        'furnishing',
        'lat',
        'lng',
        'listed_at',
    ];

    // Tell Laravel what data type each column is
    protected $casts = [
        'price' => 'decimal:2',
        'price_per_sqft' => 'decimal:2',
        'lat' => 'decimal:7',
        'lng' => 'decimal:7',
        'listed_at' => 'date',
    ];

    // ── Query Scopes ──────────────────────────────────────────────
    // Scopes are reusable query filters. Usage: Property::state('Selangor')->get()

    public function scopeState($query, $state)
    {
        return $query->where('state', $state);
    }

    public function scopePropertyType($query, $type)
    {
        return $query->where('property_type', $type);
    }

    public function scopePriceRange($query, $min, $max)
    {
        return $query->whereBetween('price', [$min, $max]);
    }

    public function scopeBedrooms($query, $bedrooms)
    {
        return $query->where('bedrooms', $bedrooms);
    }
}
