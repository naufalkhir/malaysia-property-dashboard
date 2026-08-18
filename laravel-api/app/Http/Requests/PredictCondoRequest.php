<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class PredictCondoRequest extends FormRequest
{
    private const MALAYSIA_STATES = [
        'Johor', 'Kedah', 'Kelantan', 'Kuala Lumpur', 'Labuan', 'Melaka',
        'Negeri Sembilan', 'Pahang', 'Penang', 'Perak', 'Perlis', 'Putrajaya',
        'Sabah', 'Sarawak', 'Selangor', 'Terengganu',
    ];

    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'state' => ['required', 'string', Rule::in(self::MALAYSIA_STATES)],
            'city' => ['nullable', 'string', 'max:100'],
            'size_sqft' => ['required', 'numeric', 'min:100', 'max:50000'],
            'bedrooms' => ['required', 'integer', 'min:0', 'max:20'],
            'bathrooms' => ['nullable', 'integer', 'min:0', 'max:20'],
            'car_parks' => ['nullable', 'integer', 'min:0', 'max:20'],
        ];
    }
}
