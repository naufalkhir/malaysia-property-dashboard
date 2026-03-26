<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('dosm_demographics', function (Blueprint $table) {
            $table->id();
            $table->string('state');
            $table->string('district')->nullable();
            $table->integer('year');
            $table->bigInteger('population')->nullable();
            $table->decimal('median_household_income', 10, 2)->nullable();
            $table->decimal('mean_household_income', 10, 2)->nullable();
            $table->decimal('unemployment_rate', 5, 2)->nullable();
            $table->decimal('urbanisation_rate', 5, 2)->nullable();
            $table->decimal('population_density', 10, 2)->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('dosm_demographics');
    }
};
