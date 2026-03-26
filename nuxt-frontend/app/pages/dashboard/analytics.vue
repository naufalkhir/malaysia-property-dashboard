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

    <div style="max-width: 1280px; margin: 0 auto; padding: 2.5rem 1.5rem">
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
          Analytics
        </h1>
        <p style="color: #64748b; font-size: 1.05rem">
          Charts and trends powered by Python + Plotly
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
            background: #2563eb;
            color: white;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
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
            background: white;
            color: #475569;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            border: 1px solid #e2e8f0;
          "
          >Predict Price</NuxtLink
        >
      </div>

      <!-- State Selector -->
      <div
        style="
          background: white;
          border-radius: 1rem;
          padding: 1.5rem;
          margin-bottom: 2rem;
          border: 1px solid #e2e8f0;
          display: flex;
          align-items: center;
          gap: 1rem;
        "
      >
        <label style="font-weight: 700; color: #1e293b; font-size: 1rem"
          >Filter by State:</label
        >
        <select
          v-model="selectedState"
          @change="fetchCharts"
          style="
            padding: 0.6rem 1rem;
            border: 1.5px solid #e2e8f0;
            border-radius: 0.5rem;
            font-size: 1rem;
            color: #1e293b;
            min-width: 200px;
          "
        >
          <option v-for="state in states" :key="state" :value="state">
            {{ state }}
          </option>
        </select>
      </div>

      <!-- No data message -->
      <div
        v-if="noData"
        style="
          text-align: center;
          padding: 5rem;
          background: white;
          border-radius: 1rem;
          border: 1px solid #e2e8f0;
        "
      >
        <div style="font-size: 4rem; margin-bottom: 1rem">📊</div>
        <h3
          style="
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
          "
        >
          No data available yet
        </h3>
        <p style="color: #64748b; font-size: 1.05rem">
          Import your Kaggle CSV data first to see charts here.
        </p>
      </div>

      <div v-else>
        <!-- Charts Grid -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem">
          <!-- Price Trend -->
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 2rem;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            "
          >
            <h3
              style="
                font-size: 1.1rem;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 1.25rem;
              "
            >
              📈 Price Trend — {{ selectedState }}
            </h3>
            <div
              v-if="loadingTrend"
              style="
                height: 350px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #64748b;
              "
            >
              Loading...
            </div>
            <div
              v-show="!loadingTrend"
              ref="trendChart"
              style="width: 100%; min-height: 350px"
            ></div>
          </div>

          <!-- Distribution -->
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 2rem;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            "
          >
            <h3
              style="
                font-size: 1.1rem;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 1.25rem;
              "
            >
              📊 Price Distribution
            </h3>
            <div
              v-if="loadingDist"
              style="
                height: 350px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #64748b;
              "
            >
              Loading...
            </div>
            <div
              v-show="!loadingDist"
              ref="distChart"
              style="width: 100%; min-height: 350px"
            ></div>
          </div>

          <!-- PSF Box Plot -->
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 2rem;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            "
          >
            <h3
              style="
                font-size: 1.1rem;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 1.25rem;
              "
            >
              📦 Price per Sqft by State
            </h3>
            <div
              v-if="loadingPsf"
              style="
                height: 350px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #64748b;
              "
            >
              Loading...
            </div>
            <div
              v-show="!loadingPsf"
              ref="psfChart"
              style="width: 100%; min-height: 350px"
            ></div>
          </div>

          <!-- Type Breakdown -->
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 2rem;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            "
          >
            <h3
              style="
                font-size: 1.1rem;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 1.25rem;
              "
            >
              🥧 Property Type Breakdown
            </h3>
            <div
              v-if="loadingType"
              style="
                height: 350px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #64748b;
              "
            >
              Loading...
            </div>
            <div
              v-show="!loadingType"
              ref="typeChart"
              style="width: 100%; min-height: 350px"
            ></div>
          </div>

          <!-- Affordability Bar (full width) -->
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 2rem;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
              grid-column: 1 / -1;
            "
          >
            <h3
              style="
                font-size: 1.1rem;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 1.25rem;
              "
            >
              ⚖️ Affordability Ratio by State
            </h3>
            <div
              v-if="loadingAfford"
              style="
                height: 350px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #64748b;
              "
            >
              Loading...
            </div>
            <div
              v-show="!loadingAfford"
              ref="affordChart"
              style="width: 100%; min-height: 350px"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import { useHead, useRuntimeConfig } from "#app";

useHead({ title: "Analytics" });

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const selectedState = ref("Selangor");
const noData = ref(false);

const trendChart = ref(null);
const distChart = ref(null);
const psfChart = ref(null);
const typeChart = ref(null);
const affordChart = ref(null);

const loadingTrend = ref(true);
const loadingDist = ref(true);
const loadingPsf = ref(true);
const loadingType = ref(true);
const loadingAfford = ref(true);

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

const renderChart = (el, plotlyData) => {
  if (!el || !plotlyData || !window.Plotly) return;

  try {
    // If it comes through as a string (very rare in Nuxt $fetch but just in case)
    if (typeof plotlyData === "string") {
      plotlyData = JSON.parse(plotlyData.replace(/\bNaN\b/g, "null"));
    }

    if (plotlyData.data) {
      window.Plotly.newPlot(
        el,
        plotlyData.data,
        {
          ...(plotlyData.layout || {}),
          margin: { t: 40, r: 20, b: 60, l: 60 },
          paper_bgcolor: "transparent",
          plot_bgcolor: "transparent",
        },
        { responsive: true, displayModeBar: false },
      );
    }
  } catch (e) {
    console.error("Plotly failed to render this chart element:", e);
  }
};

const fetchCharts = async () => {
  loadingTrend.value = true;
  loadingDist.value = true;
  loadingPsf.value = true;
  loadingType.value = true;
  loadingAfford.value = true;
  noData.value = false;

  try {
    const trendReq = $fetch(
      `${apiBase}/api/analytics/trends/${selectedState.value}`,
    ).catch(() => null);
    const distReq = $fetch(`${apiBase}/api/analytics/distribution`).catch(
      () => null,
    );
    const psfReq = $fetch(`${apiBase}/api/analytics/psf-by-state`).catch(
      () => null,
    );
    const typeReq = $fetch(`${apiBase}/api/analytics/type-breakdown`).catch(
      () => null,
    );
    const affordReq = $fetch(
      `${apiBase}/api/analytics/affordability-bar`,
    ).catch(() => null);

    const [trend, dist, psf, type, afford] = await Promise.all([
      trendReq,
      distReq,
      psfReq,
      typeReq,
      affordReq,
    ]);

    // VERY IMPORTANT: wait for the loading... divs to disappear and chart divs to appear in the DOM
    await nextTick();

    // Now Plotly knows the divs exist and have height!
    loadingTrend.value = false;
    if (trend) renderChart(trendChart.value, trend);

    loadingDist.value = false;
    if (dist) renderChart(distChart.value, dist);

    loadingPsf.value = false;
    if (psf) renderChart(psfChart.value, psf);

    loadingType.value = false;
    if (type) renderChart(typeChart.value, type);

    loadingAfford.value = false;
    if (afford) renderChart(affordChart.value, afford);
  } catch (err) {
    console.error("Master fetch failed:", err);
    noData.value = true;
  }
};

onMounted(async () => {
  if (!window.Plotly) {
    const script = document.createElement("script");
    script.src = "https://cdn.plot.ly/plotly-2.27.0.min.js";
    script.onload = fetchCharts;
    document.head.appendChild(script);
  } else {
    fetchCharts();
  }
});
</script>
