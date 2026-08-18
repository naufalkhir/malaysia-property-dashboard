<?php

namespace App\Http\Controllers;

use App\Http\Requests\PropertyIndexRequest;
use App\Models\Property;

class PropertyController extends Controller
{
    // GET /api/properties — listing with filters + pagination
    public function index(PropertyIndexRequest $request)
    {
        $query = Property::query();

        // Apply filters only if they are present in the request
        if ($request->filled('state')) {
            $query->where('state', $request->state);
        }
        if ($request->filled('city')) {
            $query->where('city', $request->city);
        }
        if ($request->filled('property_type')) {
            $query->where('property_type', $request->property_type);
        }
        if ($request->filled('tenure')) {
            $query->where('tenure', $request->tenure);
        }
        if ($request->filled('bedrooms')) {
            $query->where('bedrooms', $request->bedrooms);
        }
        if ($request->filled('min_price')) {
            $query->where('price', '>=', $request->min_price);
        }
        if ($request->filled('max_price')) {
            $query->where('price', '<=', $request->max_price);
        }

        // Sorting — default to newest first — sort_by/sort_dir already
        // restricted to a safe allowlist by PropertyIndexRequest::rules()
        $sortBy = $request->input('sort_by', 'created_at');
        $sortDir = $request->input('sort_dir', 'desc');
        $query->orderBy($sortBy, $sortDir);

        // Paginate — 20 per page
        return response()->json($query->paginate(20));
    }

    // GET /api/properties/{id} — single property
    public function show($id)
    {
        $property = Property::findOrFail($id);

        return response()->json($property);
    }

    // GET /api/properties/stats/summary — KPI cards for dashboard
    public function summary()
    {
        $stats = [
            'total_listings' => Property::count(),
            'avg_price' => Property::avg('price'),
            'avg_price_psf' => Property::avg('price_per_sqft'),
            'states' => Property::distinct('state')->count('state'),
            'by_state' => Property::groupBy('state')
                ->selectRaw('state, count(*) as count, avg(price) as avg_price')
                ->orderByDesc('avg_price')
                ->get(),
        ];

        return response()->json($stats);
    }

    // GET /api/properties/similar/{id} — similar properties for detail page
    public function similar($id)
    {
        $property = Property::findOrFail($id);

        $similar = Property::where('state', $property->state)
            ->where('property_type', $property->property_type)
            ->where('id', '!=', $id)
            ->whereBetween('price', [
                $property->price * 0.7,  // 30% cheaper
                $property->price * 1.3,  // 30% more expensive
            ])
            ->limit(6)
            ->get();

        return response()->json($similar);
    }
}
