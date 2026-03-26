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
          Dashboard
        </h1>
        <p style="color: #64748b; font-size: 1.05rem">
          Malaysian property market overview
        </p>
      </div>

      <!-- Dashboard Nav -->
      <div style="display: flex; gap: 0.5rem; margin-bottom: 2rem">
        <NuxtLink
          to="/dashboard"
          style="
            padding: 0.6rem 1.25rem;
            background: #2563eb;
            color: white;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
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

      <!-- Loading -->
      <div
        v-if="loading"
        style="text-align: center; padding: 5rem; color: #64748b"
      >
        <div style="font-size: 2.5rem; margin-bottom: 1rem">⏳</div>
        <p style="font-size: 1.1rem">Loading dashboard data...</p>
      </div>

      <div v-else>
        <!-- KPI Cards -->
        <div
          style="
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
          "
        >
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 1.75rem;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            "
          >
            <div
              style="
                font-size: 0.8rem;
                font-weight: 700;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.75rem;
              "
            >
              Total Listings
            </div>
            <div style="font-size: 2.25rem; font-weight: 800; color: #1e293b">
              {{ summary.total_listings?.toLocaleString() ?? "-" }}
            </div>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem">
              Properties in database
            </div>
          </div>
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 1.75rem;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            "
          >
            <div
              style="
                font-size: 0.8rem;
                font-weight: 700;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.75rem;
              "
            >
              Avg Price
            </div>
            <div style="font-size: 2.25rem; font-weight: 800; color: #2563eb">
              MYR
              {{
                summary.avg_price
                  ? Math.round(summary.avg_price).toLocaleString()
                  : "-"
              }}
            </div>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem">
              Across all listings
            </div>
          </div>
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 1.75rem;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            "
          >
            <div
              style="
                font-size: 0.8rem;
                font-weight: 700;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.75rem;
              "
            >
              Avg Price/Sqft
            </div>
            <div style="font-size: 2.25rem; font-weight: 800; color: #7c3aed">
              MYR
              {{
                summary.avg_price_psf
                  ? Math.round(summary.avg_price_psf).toLocaleString()
                  : "-"
              }}
            </div>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem">
              Per square foot
            </div>
          </div>
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 1.75rem;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            "
          >
            <div
              style="
                font-size: 0.8rem;
                font-weight: 700;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.75rem;
              "
            >
              States Covered
            </div>
            <div style="font-size: 2.25rem; font-weight: 800; color: #059669">
              {{ summary.states ?? "-" }}
            </div>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem">
              Malaysian states
            </div>
          </div>
        </div>

        <!-- By State Table -->
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
            Average Price by State
          </h2>
          <div v-if="summary.by_state && summary.by_state.length > 0">
            <div
              style="
                display: grid;
                grid-template-columns: 2fr 1fr 1fr;
                gap: 0;
                border-bottom: 2px solid #f1f5f9;
                padding-bottom: 0.75rem;
                margin-bottom: 0.5rem;
              "
            >
              <span
                style="
                  font-size: 0.8rem;
                  font-weight: 700;
                  color: #64748b;
                  text-transform: uppercase;
                "
                >State</span
              >
              <span
                style="
                  font-size: 0.8rem;
                  font-weight: 700;
                  color: #64748b;
                  text-transform: uppercase;
                "
                >Listings</span
              >
              <span
                style="
                  font-size: 0.8rem;
                  font-weight: 700;
                  color: #64748b;
                  text-transform: uppercase;
                "
                >Avg Price</span
              >
            </div>
            <div
              v-for="(row, i) in summary.by_state"
              :key="row.state"
              style="
                display: grid;
                grid-template-columns: 2fr 1fr 1fr;
                gap: 0;
                padding: 0.875rem 0;
                border-bottom: 1px solid #f8fafc;
              "
              :style="
                i % 2 === 0
                  ? ''
                  : 'background: #fafafa; border-radius: 0.5rem; padding: 0.875rem 0.75rem;'
              "
            >
              <span
                style="font-weight: 600; color: #1e293b; font-size: 0.95rem"
                >{{ row.state }}</span
              >
              <span style="color: #64748b; font-size: 0.95rem">{{
                Number(row.count).toLocaleString()
              }}</span>
              <span style="font-weight: 700; color: #2563eb; font-size: 0.95rem"
                >MYR {{ Math.round(row.avg_price).toLocaleString() }}</span
              >
            </div>
          </div>
          <div v-else style="text-align: center; padding: 3rem; color: #64748b">
            <p>No data yet — import your CSV to see stats here.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({ title: "Dashboard" });

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const summary = ref({});
const loading = ref(true);

const fetchSummary = async () => {
  loading.value = true;
  try {
    summary.value = await $fetch(`${apiBase}/api/properties/stats/summary`);
  } catch (err) {
    console.error("Failed to fetch summary:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => fetchSummary());
</script>
