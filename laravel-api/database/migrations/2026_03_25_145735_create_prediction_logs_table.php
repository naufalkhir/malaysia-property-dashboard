<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('prediction_logs', function (Blueprint $table) {
            $table->id();
            // JSON column stores all the input fields as one object
            // e.g. {"state":"Selangor","bedrooms":3,"sqft":1200}
            $table->json('input_features');
            $table->decimal('predicted_price', 15, 2);
            $table->string('model_version')->default('v1');
            $table->timestamp('created_at')->useCurrent();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('prediction_logs');
    }
};
