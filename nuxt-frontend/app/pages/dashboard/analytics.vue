<template>
  <div class="dashboard-root">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-inner">
        <NuxtLink to="/" class="nav-brand">
          <span class="brand-icon">🏠</span>
          <span class="brand-name">Malaysia Realty</span>
        </NuxtLink>
        <div class="nav-links">
          <NuxtLink to="/listings" class="nav-link">Listings</NuxtLink>
          <NuxtLink to="/dashboard" class="nav-link">Dashboard</NuxtLink>
          <NuxtLink to="/dashboard/predict" class="nav-cta"
            >Try Prediction →</NuxtLink
          >
        </div>
      </div>
    </nav>

    <div class="page-wrapper">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-left">
          <div class="header-badge">Live Data</div>
          <h1 class="page-title">Analytics</h1>
          <p class="page-sub">Real estate trends powered by Python + Plotly</p>
        </div>
      </div>

      <!-- Dashboard Sub-Nav -->
      <div class="subnav">
        <NuxtLink to="/dashboard" class="subnav-item">Overview</NuxtLink>
        <NuxtLink to="/dashboard/analytics" class="subnav-item active"
          >Analytics</NuxtLink
        >
        <NuxtLink to="/dashboard/map" class="subnav-item">Map</NuxtLink>
        <NuxtLink to="/dashboard/predict" class="subnav-item"
          >Predict Price</NuxtLink
        >
      </div>

      <!-- Filter Bar -->
      <div class="filter-bar">
        <div class="filter-label">
          <span class="filter-icon">📍</span>
          <span>State</span>
        </div>
        <div class="select-wrapper">
          <select
            v-model="selectedState"
            @change="fetchCharts"
            class="state-select"
          >
            <option v-for="state in states" :key="state" :value="state">
              {{ state }}
            </option>
          </select>
          <span class="select-arrow">▾</span>
        </div>
        <div class="filter-divider"></div>
        <div class="filter-info">
          Showing data for <strong>{{ selectedState }}</strong>
        </div>
      </div>

      <!-- No Data State -->
      <div v-if="noData" class="empty-state">
        <div class="empty-icon">📊</div>
        <h3 class="empty-title">No data available yet</h3>
        <p class="empty-sub">
          Import your Kaggle CSV data first to see charts here.
        </p>
      </div>

      <div v-else class="charts-layout">
        <!-- Row 1: Two charts side by side -->
        <div class="chart-row">
          <!-- Price Trend -->
          <div class="chart-card accent-blue">
            <div class="card-header">
              <div class="card-icon-wrap blue">📈</div>
              <div>
                <div class="card-title">Price Trend</div>
                <div class="card-sub">{{ selectedState }} · Avg. over time</div>
              </div>
            </div>
            <div v-if="loadingTrend" class="skeleton-chart"></div>
            <div
              v-show="!loadingTrend"
              ref="trendChart"
              class="chart-area"
            ></div>
          </div>

          <!-- Distribution -->
          <div class="chart-card accent-violet">
            <div class="card-header">
              <div class="card-icon-wrap violet">📊</div>
              <div>
                <div class="card-title">Price Distribution</div>
                <div class="card-sub">All states · Frequency histogram</div>
              </div>
            </div>
            <div v-if="loadingDist" class="skeleton-chart"></div>
            <div v-show="!loadingDist" ref="distChart" class="chart-area"></div>
          </div>
        </div>

        <!-- Row 2: Two charts side by side -->
        <div class="chart-row">
          <!-- PSF Box Plot -->
          <div class="chart-card accent-amber">
            <div class="card-header">
              <div class="card-icon-wrap amber">📦</div>
              <div>
                <div class="card-title">Price per Sqft</div>
                <div class="card-sub">By state · Box plot spread</div>
              </div>
            </div>
            <div v-if="loadingPsf" class="skeleton-chart"></div>
            <div v-show="!loadingPsf" ref="psfChart" class="chart-area"></div>
          </div>

          <!-- Type Breakdown -->
          <div class="chart-card accent-green">
            <div class="card-header">
              <div class="card-icon-wrap green">🥧</div>
              <div>
                <div class="card-title">Property Types</div>
                <div class="card-sub">All states · Market share</div>
              </div>
            </div>
            <div v-if="loadingType" class="skeleton-chart"></div>
            <div v-show="!loadingType" ref="typeChart" class="chart-area"></div>
          </div>
        </div>

        <!-- Row 3: Full width -->
        <div class="chart-card full-width accent-rose">
          <div class="card-header">
            <div class="card-icon-wrap rose">⚖️</div>
            <div>
              <div class="card-title">Affordability Ratio by State</div>
              <div class="card-sub">
                Higher = less affordable · Based on median income vs. median
                price
              </div>
            </div>
            <div class="card-badge">All States</div>
          </div>
          <div v-if="loadingAfford" class="skeleton-chart tall"></div>
          <div
            v-show="!loadingAfford"
            ref="affordChart"
            class="chart-area tall"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import { useHead, useRuntimeConfig } from "#app";

useHead({
  title: "Analytics — Malaysia Realty",
  link: [
    { rel: "preconnect", href: "https://fonts.googleapis.com" },
    { rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "" },
    {
      rel: "stylesheet",
      href: "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap",
    },
  ],
});

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

const plotlyLayout = (overrides = {}) => {
  const safeOverrides = {
    ...overrides,
    xaxis: {
      gridcolor: "#f1f5f9",
      linecolor: "#e2e8f0",
      tickcolor: "#e2e8f0",
      ...(overrides.xaxis || {}),
    },
    yaxis: {
      gridcolor: "#f1f5f9",
      linecolor: "#e2e8f0",
      tickcolor: "#e2e8f0",
      ...(overrides.yaxis || {}),
    },
  };

  return {
    margin: { t: 24, r: 16, b: 48, l: 56 },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    font: { family: "'DM Sans', sans-serif", color: "#64748b", size: 12 },
    legend: { bgcolor: "transparent", borderwidth: 0 },
    ...safeOverrides,
  };
};

const renderChart = (el, plotlyData) => {
  if (!el || !plotlyData || !window.Plotly) return;
  try {
    if (typeof plotlyData === "string") {
      plotlyData = JSON.parse(plotlyData.replace(/\\bNaN\\b/g, "null"));
    }
    if (plotlyData.data) {
      window.Plotly.newPlot(
        el,
        plotlyData.data,
        plotlyLayout(plotlyData.layout || {}),
        { responsive: true, displayModeBar: false },
      );
    }
  } catch (e) {
    console.error("Plotly render error:", e);
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
    const [trend, dist, psf, type, afford] = await Promise.all([
      $fetch(`${apiBase}/api/analytics/trends/${selectedState.value}`).catch(
        () => null,
      ),
      $fetch(`${apiBase}/api/analytics/distribution`).catch(() => null),
      $fetch(`${apiBase}/api/analytics/psf-by-state`).catch(() => null),
      $fetch(`${apiBase}/api/analytics/type-breakdown`).catch(() => null),
      $fetch(`${apiBase}/api/analytics/affordability-bar`).catch(() => null),
    ]);

    await nextTick();

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
    console.error("Fetch failed:", err);
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

<style scoped>
/* ── Reset & Root ── */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.dashboard-root {
  min-height: 100vh;
  background: #f8fafc;
  font-family: "DM Sans", sans-serif;
}

/* ── Navbar ── */
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid #e2e8f0;
}

.nav-inner {
  max-width: 1360px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.brand-icon {
  font-size: 1.5rem;
}

.brand-name {
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.4px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  color: #64748b;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #0f172a;
}

.nav-cta {
  background: #2563eb;
  color: white;
  padding: 0.5rem 1.2rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 700;
  font-size: 0.88rem;
  transition:
    background 0.2s,
    transform 0.15s;
}

.nav-cta:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
}

/* ── Page Wrapper ── */
.page-wrapper {
  max-width: 1360px;
  margin: 0 auto;
  padding: 2rem 2rem 4rem;
}

/* ── Page Header ── */
.page-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1.75rem;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #dcfce7;
  color: #16a34a;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  margin-bottom: 0.6rem;
}

.header-badge::before {
  content: "";
  width: 6px;
  height: 6px;
  background: #16a34a;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
}

.page-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.8px;
  line-height: 1;
  margin-bottom: 0.35rem;
}

.page-sub {
  font-size: 0.95rem;
  color: #94a3b8;
  font-weight: 500;
}

/* ── Sub Nav ── */
.subnav {
  display: flex;
  gap: 0.375rem;
  margin-bottom: 1.75rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 0.375rem;
  width: fit-content;
}

.subnav-item {
  padding: 0.5rem 1.1rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.875rem;
  color: #64748b;
  transition: all 0.2s;
}

.subnav-item:hover {
  color: #0f172a;
  background: #f8fafc;
}

.subnav-item.active {
  background: #2563eb;
  color: white;
}

/* ── Filter Bar ── */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.875rem;
  padding: 0.875rem 1.5rem;
  margin-bottom: 1.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 700;
  font-size: 0.875rem;
  color: #0f172a;
}

.filter-icon {
  font-size: 1rem;
}

.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.state-select {
  appearance: none;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 0.45rem 2.2rem 0.45rem 0.85rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #0f172a;
  font-family: "DM Sans", sans-serif;
  cursor: pointer;
  min-width: 180px;
  transition: border-color 0.2s;
}

.state-select:focus {
  outline: none;
  border-color: #2563eb;
}

.select-arrow {
  position: absolute;
  right: 0.7rem;
  font-size: 0.75rem;
  color: #94a3b8;
  pointer-events: none;
}

.filter-divider {
  width: 1px;
  height: 20px;
  background: #e2e8f0;
}

.filter-info {
  font-size: 0.875rem;
  color: #94a3b8;
  font-weight: 500;
}

.filter-info strong {
  color: #0f172a;
}

/* ── Empty State ── */
.empty-state {
  text-align: center;
  padding: 5rem 2rem;
  background: white;
  border-radius: 1.25rem;
  border: 1px solid #e2e8f0;
}

.empty-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.empty-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.empty-sub {
  color: #94a3b8;
  font-size: 0.95rem;
}

/* ── Charts Layout ── */
.charts-layout {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

/* ── Chart Cards ── */
.chart-card {
  background: white;
  border-radius: 1.25rem;
  padding: 1.75rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.chart-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  border-radius: 1.25rem 1.25rem 0 0;
}

.chart-card.accent-blue::before {
  background: linear-gradient(90deg, #2563eb, #60a5fa);
}
.chart-card.accent-violet::before {
  background: linear-gradient(90deg, #7c3aed, #a78bfa);
}
.chart-card.accent-amber::before {
  background: linear-gradient(90deg, #d97706, #fbbf24);
}
.chart-card.accent-green::before {
  background: linear-gradient(90deg, #16a34a, #4ade80);
}
.chart-card.accent-rose::before {
  background: linear-gradient(90deg, #e11d48, #fb7185);
}

.chart-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  margin-bottom: 1.25rem;
}

.card-icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: 0.625rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.card-icon-wrap.blue {
  background: #eff6ff;
}
.card-icon-wrap.violet {
  background: #f5f3ff;
}
.card-icon-wrap.amber {
  background: #fffbeb;
}
.card-icon-wrap.green {
  background: #f0fdf4;
}
.card-icon-wrap.rose {
  background: #fff1f2;
}

.card-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.2px;
}

.card-sub {
  font-size: 0.78rem;
  color: #94a3b8;
  font-weight: 500;
  margin-top: 0.15rem;
}

.card-badge {
  margin-left: auto;
  background: #f1f5f9;
  color: #64748b;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
}

/* ── Chart Areas ── */
.chart-area {
  width: 100%;
  min-height: 300px;
}

.chart-area.tall {
  min-height: 340px;
}

/* ── Skeleton Loading ── */
.skeleton-chart {
  width: 100%;
  height: 300px;
  border-radius: 0.75rem;
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: shimmer 1.6s infinite;
}

.skeleton-chart.tall {
  height: 340px;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* ── Responsive ── */
@media (max-width: 900px) {
  .chart-row {
    grid-template-columns: 1fr;
  }
  .page-title {
    font-size: 1.75rem;
  }
  .nav-links {
    gap: 1rem;
  }
}
</style>
