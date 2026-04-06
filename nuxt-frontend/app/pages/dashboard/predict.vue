<template>
  <div style="min-height: 100vh; background: #f1f5f9">
    <!-- Navbar -->
    <nav
      style="
        background: white;
        border-bottom: 1px solid #e2e8f0;
        padding: 1.25rem 2.5rem;
      "
    >
      <div
        style="
          max-width: 1280px;
          margin: 0 auto;
          display: flex;
          align-items: center;
          justify-content: space-between;
        "
      >
        <NuxtLink
          to="/"
          style="
            display: flex;
            align-items: center;
            gap: 0.6rem;
            text-decoration: none;
          "
        >
          <span style="font-size: 1.75rem">🏠</span>
          <span
            style="
              font-size: 1.3rem;
              font-weight: 800;
              color: #1e293b;
              letter-spacing: -0.5px;
            "
            >Malaysia Realty</span
          >
        </NuxtLink>
        <div style="display: flex; align-items: center; gap: 2.5rem">
          <NuxtLink
            to="/listings"
            style="
              color: #475569;
              text-decoration: none;
              font-weight: 600;
              font-size: 1rem;
            "
            >Listings</NuxtLink
          >
          <NuxtLink
            to="/dashboard"
            style="
              color: #2563eb;
              text-decoration: none;
              font-weight: 700;
              font-size: 1rem;
            "
            >Dashboard</NuxtLink
          >
          <NuxtLink
            to="/dashboard/predict"
            style="
              background: #2563eb;
              color: white;
              padding: 0.6rem 1.4rem;
              border-radius: 0.5rem;
              text-decoration: none;
              font-weight: 700;
              font-size: 0.95rem;
            "
            >Try Prediction →</NuxtLink
          >
        </div>
      </div>
    </nav>

    <div style="max-width: 900px; margin: 0 auto; padding: 2.5rem 1.5rem">
      <!-- Header -->
      <div style="margin-bottom: 2rem">
        <h1
          style="
            font-size: 2.5rem;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 0.5rem;
          "
        >
          ML Price Prediction
        </h1>
        <p style="color: #64748b; font-size: 1.05rem">
          Powered by Random Forest trained on real Malaysian property data
        </p>
      </div>

      <!-- Dashboard Nav -->
      <div style="display: flex; gap: 0.5rem; margin-bottom: 2rem">
        <NuxtLink
          to="/dashboard"
          style="
            padding: 0.6rem 1.25rem;
            background: white;
            color: #475569;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            border: 1px solid #e2e8f0;
          "
          >Overview</NuxtLink
        >
        <NuxtLink
          to="/dashboard/analytics"
          style="
            padding: 0.6rem 1.25rem;
            background: white;
            color: #475569;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            border: 1px solid #e2e8f0;
          "
          >Analytics</NuxtLink
        >
        <NuxtLink
          to="/dashboard/map"
          style="
            padding: 0.6rem 1.25rem;
            background: white;
            color: #475569;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            border: 1px solid #e2e8f0;
          "
          >Map</NuxtLink
        >
        <NuxtLink
          to="/dashboard/predict"
          style="
            padding: 0.6rem 1.25rem;
            background: #2563eb;
            color: white;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
          "
          >Predict Price</NuxtLink
        >
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem">
        <!-- Form -->
        <div
          style="
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
          "
        >
          <h2
            style="
              font-size: 1.25rem;
              font-weight: 700;
              color: #1e293b;
              margin-bottom: 1.5rem;
            "
          >
            Property Details
          </h2>

          <div style="display: flex; flex-direction: column; gap: 1.25rem">
            <div>
              <label
                style="
                  font-size: 0.8rem;
                  font-weight: 700;
                  color: #64748b;
                  display: block;
                  margin-bottom: 0.5rem;
                  text-transform: uppercase;
                  letter-spacing: 0.05em;
                "
                >State</label
              >
              <select
                v-model="form.state"
                style="
                  width: 100%;
                  padding: 0.75rem;
                  border: 1.5px solid #e2e8f0;
                  border-radius: 0.5rem;
                  font-size: 1rem;
                  color: #1e293b;
                  background: white;
                "
              >
                <option value="" disabled>Select state...</option>
                <option v-for="state in states" :key="state" :value="state">
                  {{ state }}
                </option>
              </select>
            </div>

            <div>
              <label
                style="
                  font-size: 0.8rem;
                  font-weight: 700;
                  color: #64748b;
                  display: block;
                  margin-bottom: 0.5rem;
                  text-transform: uppercase;
                  letter-spacing: 0.05em;
                "
                >Property Type</label
              >
              <select
                v-model="form.property_type"
                style="
                  width: 100%;
                  padding: 0.75rem;
                  border: 1.5px solid #e2e8f0;
                  border-radius: 0.5rem;
                  font-size: 1rem;
                  color: #1e293b;
                  background: white;
                "
              >
                <option value="" disabled>Select type...</option>
                <option value="Condominium">Condominium</option>
                <option value="Apartment">Apartment</option>
                <option value="Terrace">Terrace</option>
                <option value="Semi-D">Semi-D</option>
                <option value="Bungalow">Bungalow</option>
                <option value="Studio">Studio</option>
              </select>
            </div>

            <!-- FIX 1: Size input — added background: white -->
            <div>
              <label
                style="
                  font-size: 0.8rem;
                  font-weight: 700;
                  color: #64748b;
                  display: block;
                  margin-bottom: 0.5rem;
                  text-transform: uppercase;
                  letter-spacing: 0.05em;
                "
                >Size (sqft)</label
              >
              <input
                v-model.number="form.size_sqft"
                type="number"
                placeholder="e.g. 1200"
                style="
                  width: 100%;
                  padding: 0.75rem;
                  border: 1.5px solid #e2e8f0;
                  border-radius: 0.5rem;
                  font-size: 1rem;
                  color: #1e293b;
                  background: white;
                  box-sizing: border-box;
                "
              />
            </div>

            <div
              style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem"
            >
              <!-- FIX 2: Bedrooms input — added background: white -->
              <div>
                <label
                  style="
                    font-size: 0.8rem;
                    font-weight: 700;
                    color: #64748b;
                    display: block;
                    margin-bottom: 0.5rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                  "
                  >Bedrooms</label
                >
                <input
                  v-model.number="form.bedrooms"
                  type="number"
                  placeholder="3"
                  min="1"
                  max="10"
                  style="
                    width: 100%;
                    padding: 0.75rem;
                    border: 1.5px solid #e2e8f0;
                    border-radius: 0.5rem;
                    font-size: 1rem;
                    color: #1e293b;
                    background: white;
                    box-sizing: border-box;
                  "
                />
              </div>
              <!-- FIX 3: Bathrooms input — added background: white -->
              <div>
                <label
                  style="
                    font-size: 0.8rem;
                    font-weight: 700;
                    color: #64748b;
                    display: block;
                    margin-bottom: 0.5rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                  "
                  >Bathrooms</label
                >
                <input
                  v-model.number="form.bathrooms"
                  type="number"
                  placeholder="2"
                  min="1"
                  max="10"
                  style="
                    width: 100%;
                    padding: 0.75rem;
                    border: 1.5px solid #e2e8f0;
                    border-radius: 0.5rem;
                    font-size: 1rem;
                    color: #1e293b;
                    background: white;
                    box-sizing: border-box;
                  "
                />
              </div>
            </div>

            <div
              style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem"
            >
              <div>
                <label
                  style="
                    font-size: 0.8rem;
                    font-weight: 700;
                    color: #64748b;
                    display: block;
                    margin-bottom: 0.5rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                  "
                  >Tenure</label
                >
                <select
                  v-model="form.tenure"
                  style="
                    width: 100%;
                    padding: 0.75rem;
                    border: 1.5px solid #e2e8f0;
                    border-radius: 0.5rem;
                    font-size: 1rem;
                    color: #1e293b;
                    background: white;
                  "
                >
                  <option value="freehold">Freehold</option>
                  <option value="leasehold">Leasehold</option>
                </select>
              </div>
              <div>
                <label
                  style="
                    font-size: 0.8rem;
                    font-weight: 700;
                    color: #64748b;
                    display: block;
                    margin-bottom: 0.5rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                  "
                  >Furnishing</label
                >
                <select
                  v-model="form.furnishing"
                  style="
                    width: 100%;
                    padding: 0.75rem;
                    border: 1.5px solid #e2e8f0;
                    border-radius: 0.5rem;
                    font-size: 1rem;
                    color: #1e293b;
                    background: white;
                  "
                >
                  <option value="unfurnished">Unfurnished</option>
                  <option value="partially furnished">
                    Partially Furnished
                  </option>
                  <option value="fully furnished">Fully Furnished</option>
                </select>
              </div>
            </div>

            <button
              @click="predict"
              :disabled="loading || !isFormValid"
              :style="{
                width: '100%',
                padding: '0.9rem',
                background: '#2563eb',
                color: 'white',
                border: 'none',
                borderRadius: '0.5rem',
                fontSize: '1.1rem',
                fontWeight: '700',
                cursor: 'pointer',
                marginTop: '0.5rem',
                opacity: !isFormValid || loading ? '0.6' : '1',
              }"
            >
              {{ loading ? "Predicting..." : "Predict Price" }}
            </button>
          </div>
        </div>

        <!-- Result Section -->
        <div>
          <!-- Placeholder when no result -->
          <div
            v-if="!result && !error"
            style="
              background: white;
              border-radius: 1rem;
              padding: 2rem;
              border: 1px solid #e2e8f0;
              text-align: center;
              height: 100%;
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
            "
          >
            <div style="font-size: 4rem; margin-bottom: 1rem">🤖</div>
            <h3
              style="
                font-size: 1.25rem;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 0.75rem;
              "
            >
              AI Price Estimator
            </h3>
            <p style="color: #64748b; line-height: 1.7">
              Fill in the property details and click "Predict Price" to get an
              ML-powered estimate based on real Malaysian market data.
            </p>
          </div>

          <!-- Error -->
          <div
            v-if="error"
            style="
              background: #fef2f2;
              border-radius: 1rem;
              padding: 2rem;
              border: 1px solid #fecaca;
            "
          >
            <div style="font-size: 2rem; margin-bottom: 1rem">⚠️</div>
            <h3 style="font-weight: 700; color: #dc2626; margin-bottom: 0.5rem">
              Prediction Failed
            </h3>
            <p style="color: #64748b; font-size: 0.95rem">{{ error }}</p>
          </div>

          <!-- Result -->
          <div
            v-if="result"
            style="
              background: white;
              border-radius: 1rem;
              padding: 2rem;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            "
          >
            <div
              style="
                text-align: center;
                padding: 1.5rem;
                background: linear-gradient(135deg, #eff6ff, #dbeafe);
                border-radius: 0.75rem;
                margin-bottom: 1.5rem;
              "
            >
              <div
                style="
                  font-size: 0.85rem;
                  font-weight: 700;
                  color: #2563eb;
                  text-transform: uppercase;
                  letter-spacing: 0.05em;
                  margin-bottom: 0.5rem;
                "
              >
                Predicted Price
              </div>
              <div style="font-size: 2.75rem; font-weight: 800; color: #1e293b">
                MYR {{ Number(result.predicted_price).toLocaleString() }}
              </div>
            </div>

            <!-- Confidence Range -->
            <div style="margin-bottom: 1.5rem">
              <div
                style="
                  font-size: 0.8rem;
                  font-weight: 700;
                  color: #64748b;
                  text-transform: uppercase;
                  margin-bottom: 0.75rem;
                "
              >
                Confidence Range
              </div>
              <div
                style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem"
              >
                <div
                  style="
                    padding: 1rem;
                    background: #f0fdf4;
                    border-radius: 0.5rem;
                    text-align: center;
                  "
                >
                  <div
                    style="
                      font-size: 0.75rem;
                      color: #16a34a;
                      font-weight: 700;
                      margin-bottom: 0.25rem;
                    "
                  >
                    LOW ESTIMATE
                  </div>
                  <div
                    style="font-size: 1.25rem; font-weight: 800; color: #15803d"
                  >
                    MYR {{ Number(result.low).toLocaleString() }}
                  </div>
                </div>
                <div
                  style="
                    padding: 1rem;
                    background: #fff7ed;
                    border-radius: 0.5rem;
                    text-align: center;
                  "
                >
                  <div
                    style="
                      font-size: 0.75rem;
                      color: #ea580c;
                      font-weight: 700;
                      margin-bottom: 0.25rem;
                    "
                  >
                    HIGH ESTIMATE
                  </div>
                  <div
                    style="font-size: 1.25rem; font-weight: 800; color: #c2410c"
                  >
                    MYR {{ Number(result.high).toLocaleString() }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Disclaimer -->
            <p
              style="
                font-size: 0.8rem;
                color: #94a3b8;
                text-align: center;
                line-height: 1.6;
              "
            >
              ⚠️ This is an indicative estimate only, not a professional
              valuation. Based on Random Forest model trained on historical
              Malaysian property data.
            </p>

            <button
              @click="
                result = null;
                error = null;
              "
              style="
                width: 100%;
                margin-top: 1.25rem;
                padding: 0.75rem;
                border: 1.5px solid #e2e8f0;
                border-radius: 0.5rem;
                background: white;
                cursor: pointer;
                font-weight: 600;
                color: #64748b;
                font-size: 0.95rem;
              "
            >
              Try Another Prediction
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useHead, useRuntimeConfig } from "#app";

useHead({ title: "Price Prediction" });

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const result = ref(null);
const error = ref(null);
const loading = ref(false);

const form = ref({
  state: "",
  property_type: "",
  size_sqft: null,
  bedrooms: null,
  bathrooms: null,
  car_parks: 0,
  tenure: "freehold",
  furnishing: "unfurnished",
});

const states = [
  "Selangor",
  "Kuala Lumpur",
  "Johor",
  "Penang",
  "Perak",
  "Sabah",
  "Sarawak",
  "Kedah",
  "Kelantan",
  "Melaka",
  "Negeri Sembilan",
  "Pahang",
  "Perlis",
  "Terengganu",
  "Putrajaya",
];

const isFormValid = computed(() => {
  return (
    form.value.state &&
    form.value.property_type &&
    form.value.size_sqft > 0 &&
    form.value.bedrooms > 0
  );
});

const predict = async () => {
  loading.value = true;
  result.value = null;
  error.value = null;

  try {
    const payload = {
      state: form.value.state,
      property_type: form.value.property_type,
      size_sqft: Number(form.value.size_sqft),
      bedrooms: Number(form.value.bedrooms),
    };

    result.value = await $fetch(`${apiBase}/api/analytics/predict`, {
      method: "POST",
      body: payload,
    });
  } catch (err) {
    error.value =
      err?.data?.detail ||
      "Prediction failed. Make sure the ML model is trained and running.";
  } finally {
    loading.value = false;
  }
};
</script>
