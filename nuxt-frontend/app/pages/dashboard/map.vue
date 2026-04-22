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
            >Try Prediction -></NuxtLink
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
          Interactive Map
        </h1>
        <p style="color: #64748b; font-size: 1.05rem">
          Malaysia property heatmap powered by Leaflet.js
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
            background: #2563eb;
            color: white;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
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

      <!-- Map Container -->
      <div
        style="
          background: white;
          border-radius: 1rem;
          overflow: hidden;
          border: 1px solid #e2e8f0;
          box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
        "
      >
        <div ref="mapContainer" style="height: 600px; width: 100%"></div>
      </div>

      <!-- State Stats -->
      <div
        style="
          margin-top: 2rem;
          background: white;
          border-radius: 1rem;
          padding: 2rem;
          border: 1px solid #e2e8f0;
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
          Property Density by State
        </h2>
        <div
          v-if="stateData.length > 0"
          style="
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
          "
        >
          <div
            v-for="state in stateData"
            :key="state.state"
            style="
              padding: 1rem;
              background: #f8fafc;
              border-radius: 0.75rem;
              border: 1px solid #e2e8f0;
            "
          >
            <div
              style="
                font-weight: 700;
                color: #1e293b;
                font-size: 0.95rem;
                margin-bottom: 0.4rem;
              "
            >
              {{ state.state }}
            </div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #2563eb">
              MYR {{ Math.round(state.avg_price).toLocaleString() }}
            </div>
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.25rem">
              {{ Number(state.listing_count).toLocaleString() }} listings
            </div>
          </div>
        </div>
        <div v-else style="text-align: center; padding: 2rem; color: #64748b">
          <p>No data yet - import your CSV to see state stats here.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({ title: "Property Map" });

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const mapContainer = ref(null);
const stateData = ref([]);
let map = null;

const MALAYSIA_CENTER = [4.2105, 108.9758];
const MALAYSIA_ZOOM = 6;

const initMap = async () => {
  if (!mapContainer.value) return;

  const L = await import("leaflet");

  delete L.Icon.Default.prototype._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl:
      "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  });

  map = L.map(mapContainer.value).setView(MALAYSIA_CENTER, MALAYSIA_ZOOM);

  // Street layer
  const streetLayer = L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
      attribution: "© OpenStreetMap contributors",
      maxZoom: 18,
    },
  );

  // Satellite layer (ESRI — free, no API key needed)
  const satelliteLayer = L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    {
      attribution: "Tiles &copy; Esri",
      maxZoom: 18,
    },
  );

  // Start with satellite
  satelliteLayer.addTo(map);

  // Layer switcher — top right corner
  L.control
    .layers({
      Street: streetLayer,
      Satellite: satelliteLayer,
    })
    .addTo(map);

  try {
    const states = await $fetch(`${apiBase}/api/analytics/map/choropleth`);
    stateData.value = states;

    const stateCenters = {
      Selangor: [3.0738, 101.5183],
      "Kuala Lumpur": [3.139, 101.6869],
      Johor: [1.9344, 103.3587],
      Penang: [5.4141, 100.3288],
      Perak: [4.5921, 101.0901],
      Sabah: [5.9788, 116.0753],
      Sarawak: [1.5533, 110.3592],
      Kedah: [6.1184, 100.3685],
      Kelantan: [6.1254, 102.2381],
      Melaka: [2.1896, 102.2501],
      "Negeri Sembilan": [2.7258, 101.9424],
      Pahang: [3.8126, 103.3256],
      Perlis: [6.4449, 100.2048],
      Terengganu: [5.3117, 103.1324],
      Putrajaya: [2.9264, 101.6964],
    };

    states.forEach((state) => {
      const coords = stateCenters[state.state];
      if (!coords) return;

      const marker = L.circleMarker(coords, {
        radius: Math.min(30, Math.max(8, state.listing_count / 100)),
        fillColor: "#2563eb",
        color: "#ffffff",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.75,
      }).addTo(map);

      marker.bindPopup(`
        <div style="font-family: sans-serif; min-width: 160px;">
          <div style="font-weight: 700; font-size: 1rem; margin-bottom: 0.5rem;">${state.state}</div>
          <div style="color: #2563eb; font-weight: 700;">MYR ${Math.round(state.avg_price).toLocaleString()}</div>
          <div style="color: #64748b; font-size: 0.85rem;">${Number(state.listing_count).toLocaleString()} listings</div>
          ${state.affordability_ratio ? `<div style="color: #64748b; font-size: 0.85rem;">Affordability: ${Number(state.affordability_ratio).toFixed(1)}x</div>` : ""}
        </div>
      `);
    });
  } catch (err) {
    console.error("Failed to fetch map data:", err);
  }
};

onMounted(() => {
  initMap();
});

onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
  }
});
</script>
