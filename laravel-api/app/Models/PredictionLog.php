<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PredictionLog extends Model
{
    // Schema has created_at but no updated_at column.
    const UPDATED_AT = null;

    protected $fillable = [
        'input_features',
        'predicted_price',
        'model_version',
    ];

    protected $casts = [
        'input_features' => 'array',
        'predicted_price' => 'decimal:2',
    ];
}
