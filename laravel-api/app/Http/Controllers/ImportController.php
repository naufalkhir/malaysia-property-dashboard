<?php

namespace App\Http\Controllers;

use App\Models\Property;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class ImportController extends Controller
{
    // POST /api/import/properties — upload Kaggle CSV
    public function importProperties(Request $request)
    {
        $request->validate(['file' => 'required|file|mimes:csv,txt']);

        $file = $request->file('file');
        $rows = array_map('str_getcsv', file($file->getRealPath()));
        $header = array_map('trim', array_shift($rows));

        $imported = 0;
        $skipped = 0;

        DB::transaction(function () use ($rows, $header, &$imported, &$skipped) {
            foreach (array_chunk($rows, 500) as $chunk) {
                $batch = [];
                foreach ($chunk as $row) {
                    if (count($row) < count($header)) {
                        $skipped++;
                        continue;
                    }
                    $data = array_combine($header, $row);

                    // Skip rows with no price or state
                    $price = (float) ($data['Median_Price'] ?? $data['price'] ?? 0);
                    $state = trim($data['State'] ?? $data['state'] ?? '');
                    if (!$price || !$state) {
                        $skipped++;
                        continue;
                    }

                    $township = trim($data['Township'] ?? $data['title'] ?? '');
                    $area = trim($data['Area'] ?? $data['area'] ?? '');
                    $type = trim($data['Type'] ?? $data['property_type'] ?? '');
                    $tenure = trim($data['Tenure'] ?? $data['tenure'] ?? '');
                    $psf = (float) ($data['Median_PSF'] ?? $data['price_per_sqft'] ?? 0);

                    $batch[] = [
                        'title' => $township ?: 'Property in ' . $state,
                        'state' => $state,
                        'city' => $area ?: $state,
                        'area' => $area ?: null,
                        'property_type' => $type ?: 'Unknown',
                        'tenure' => $tenure ?: null,
                        'price' => $price,
                        'price_per_sqft' => $psf ?: null,
                        'size_sqft' => null,
                        'bedrooms' => null,
                        'bathrooms' => null,
                        'car_parks' => null,
                        'furnishing' => null,
                        'lat' => null,
                        'lng' => null,
                        'listed_at' => null,
                        'created_at' => now(),
                        'updated_at' => now(),
                    ];
                    $imported++;
                }
                if (!empty($batch))
                    Property::insert($batch);
            }
        });

        return response()->json([
            'message' => 'Import complete',
            'imported' => $imported,
            'skipped' => $skipped,
        ]);
    }

    // POST /api/import/dosm — upload DOSM demographics CSV
    public function importDosm(Request $request)
    {
        $request->validate(['file' => 'required|file|mimes:csv,txt']);

        $file = $request->file('file');
        $rows = array_map('str_getcsv', file($file->getRealPath()));
        $header = array_map('trim', array_shift($rows));

        $imported = 0;
        $skipped = 0;

        DB::transaction(function () use ($rows, $header, &$imported, &$skipped) {
            foreach (array_chunk($rows, 500) as $chunk) {
                $batch = [];
                foreach ($chunk as $row) {
                    if (count($row) < count($header)) {
                        $skipped++;
                        continue;
                    }
                    $data = array_combine($header, $row);

                    $state = trim($data['state'] ?? '');
                    if (!$state) {
                        $skipped++;
                        continue;
                    }

                    // Extract year from date column e.g. "1970-01-01" → 1970
                    $date = $data['date'] ?? '';
                    $year = $date ? (int) substr($date, 0, 4) : date('Y');

                    $batch[] = [
                        'state' => $state,
                        'district' => null,
                        'year' => $year,
                        'population' => null,
                        'median_household_income' => (float) ($data['income_median'] ?? 0) ?: null,
                        'mean_household_income' => (float) ($data['income_mean'] ?? 0) ?: null,
                        'unemployment_rate' => null,
                        'urbanisation_rate' => null,
                        'population_density' => null,
                        'created_at' => now(),
                        'updated_at' => now(),
                    ];
                    $imported++;
                }
                if (!empty($batch))
                    DB::table('dosm_demographics')->insert($batch);
            }
        });

        return response()->json([
            'message' => 'Import complete',
            'imported' => $imported,
            'skipped' => $skipped,
        ]);
    }

    // GET /api/import/status — how much data is in the DB
    public function status()
    {
        return response()->json([
            'properties' => Property::count(),
            'demographics' => DB::table('dosm_demographics')->count(),
        ]);
    }
}
