<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('properties', function (Blueprint $table) {
            $table->id();
            $table->string('title');
            $table->string('state');
            $table->string('city');
            $table->string('area')->nullable();
            $table->string('property_type');
            $table->string('tenure')->nullable();        // freehold / leasehold
            $table->decimal('price', 15, 2);
            $table->decimal('price_per_sqft', 10, 2)->nullable();
            $table->integer('size_sqft')->nullable();
            $table->integer('bedrooms')->nullable();
            $table->integer('bathrooms')->nullable();
            $table->integer('car_parks')->nullable();
            $table->string('furnishing')->nullable();    // furnished / unfurnished
            $table->decimal('lat', 10, 7)->nullable();
            $table->decimal('lng', 10, 7)->nullable();
            $table->date('listed_at')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('properties');
    }
};
