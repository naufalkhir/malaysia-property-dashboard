<template>
  <div
    style="
      min-height: 100vh;
      background: #f1f5f9;
      width: 100%;
      box-sizing: border-box;
    "
  >
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
              color: #2563eb;
              text-decoration: none;
              font-weight: 700;
              font-size: 1rem;
            "
            >Listings</NuxtLink
          >
          <NuxtLink
            to="/dashboard"
            style="
              color: #475569;
              text-decoration: none;
              font-weight: 600;
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

    <div
      style="
        max-width: 1200px;
        margin: 0 auto;
        padding: 2.5rem 2rem;
        width: 100%;
        box-sizing: border-box;
      "
    >
      <!-- Page Header -->
      <div style="margin-bottom: 2rem">
        <h1
          style="
            font-size: 2.5rem;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 0.5rem;
          "
        >
          Property Listings
        </h1>
        <p style="color: #64748b; font-size: 1.05rem">
          Browse and filter Malaysian property listings
        </p>
      </div>

      <!-- Filters -->
      <div
        style="
          background: white;
          border-radius: 1rem;
          padding: 2rem;
          margin-bottom: 2rem;
          box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
          border: 1px solid #e2e8f0;
          width: 100%;
          box-sizing: border-box;
        "
      >
        <div
          style="
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1.25rem;
          "
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
              >State</label
            >
            <select
              v-model="filters.state"
              style="
                width: 100%;
                padding: 0.75rem 0.9rem;
                border: 1.5px solid #e2e8f0;
                border-radius: 0.5rem;
                font-size: 1rem;
                color: #1e293b;
                background: white;
                box-sizing: border-box;
              "
            >
              <option value="">All States</option>
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
              >Type</label
            >
            <select
              v-model="filters.property_type"
              style="
                width: 100%;
                padding: 0.75rem 0.9rem;
                border: 1.5px solid #e2e8f0;
                border-radius: 0.5rem;
                font-size: 1rem;
                color: #1e293b;
                background: white;
                box-sizing: border-box;
              "
            >
              <option value="">All Types</option>
              <option value="Condominium">Condominium</option>
              <option value="Apartment">Apartment</option>
              <option value="Terrace">Terrace</option>
              <option value="Semi-D">Semi-D</option>
              <option value="Bungalow">Bungalow</option>
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
              >Bedrooms</label
            >
            <select
              v-model="filters.bedrooms"
              style="
                width: 100%;
                padding: 0.75rem 0.9rem;
                border: 1.5px solid #e2e8f0;
                border-radius: 0.5rem;
                font-size: 1rem;
                color: #1e293b;
                background: white;
                box-sizing: border-box;
              "
            >
              <option value="">Any</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4+</option>
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
              >Min Price</label
            >
            <input
              v-model="filters.min_price"
              type="number"
              placeholder="e.g. 200,000"
              style="
                width: 100%;
                padding: 0.75rem 0.9rem;
                border: 1.5px solid #e2e8f0;
                border-radius: 0.5rem;
                font-size: 1rem;
                color: #1e293b;
                box-sizing: border-box;
              "
            >
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
              >Max Price</label
            >
            <input
              v-model="filters.max_price"
              type="number"
              placeholder="e.g. 1,000,000"
              style="
                width: 100%;
                padding: 0.75rem 0.9rem;
                border: 1.5px solid #e2e8f0;
                border-radius: 0.5rem;
                font-size: 1rem;
                color: #1e293b;
                box-sizing: border-box;
              "
            >
          </div>
        </div>
        <div
          style="
            margin-top: 1.5rem;
            display: flex;
            gap: 0.75rem;
            align-items: center;
          "
        >
          <button
            style="
              background: #2563eb;
              color: white;
              padding: 0.75rem 1.75rem;
              border-radius: 0.5rem;
              border: none;
              cursor: pointer;
              font-weight: 700;
              font-size: 1rem;
            "
            @click="applyFilters"
          >
            Search
          </button>
          <button
            style="
              padding: 0.75rem 1.25rem;
              border: 1.5px solid #e2e8f0;
              border-radius: 0.5rem;
              background: white;
              cursor: pointer;
              font-weight: 600;
              color: #64748b;
              font-size: 1rem;
            "
            @click="resetFilters"
          >
            Reset
          </button>
          <span
            style="
              margin-left: auto;
              color: #64748b;
              font-size: 1rem;
              font-weight: 500;
            "
          >
            {{ pagination.total ?? 0 }} properties found
          </span>
        </div>
      </div>

      <!-- Loading -->
      <div
        v-if="loading"
        style="text-align: center; padding: 5rem; color: #64748b"
      >
        <div style="font-size: 2.5rem; margin-bottom: 1rem">⏳</div>
        <p style="font-size: 1.1rem">Loading properties...</p>
      </div>

      <!-- Empty state -->
      <div
        v-else-if="properties.length === 0"
        style="
          text-align: center;
          padding: 5rem;
          background: white;
          border-radius: 1rem;
          border: 1px solid #e2e8f0;
        "
      >
        <div style="font-size: 4rem; margin-bottom: 1rem">🏠</div>
        <h3
          style="
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
          "
        >
          No properties found
        </h3>
        <p style="color: #64748b; font-size: 1.05rem">
          Try adjusting your filters or import some data first.
        </p>
      </div>

      <!-- Property Grid — fixed: width 100% + box-sizing so it fills the container properly -->
      <div
        v-else
        style="
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
          gap: 1.75rem;
          width: 100%;
          box-sizing: border-box;
        "
      >
        <NuxtLink
          v-for="property in properties"
          :key="property.id"
          :to="`/listings/${property.id}`"
          style="text-decoration: none; color: inherit"
        >
          <div
            style="
              background: white;
              border-radius: 1rem;
              overflow: hidden;
              border: 1px solid #e2e8f0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
              cursor: pointer;
              transition:
                box-shadow 0.2s,
                transform 0.2s;
            "
            @mouseenter="
              (e) =>
                (e.currentTarget.style.cssText +=
                  'box-shadow: 0 8px 24px rgba(0,0,0,0.1); transform: translateY(-2px);')
            "
            @mouseleave="
              (e) =>
                (e.currentTarget.style.cssText +=
                  'box-shadow: 0 1px 4px rgba(0,0,0,0.06); transform: translateY(0);')
            "
          >
            <!-- Image placeholder with property-type color -->
            <div
              style="
                height: 200px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 4rem;
                position: relative;
              "
              :style="{ background: cardGradient(property.property_type) }"
            >
              {{ cardIcon(property.property_type) }}
              <span
                style="
                  position: absolute;
                  top: 0.75rem;
                  right: 0.75rem;
                  background: white;
                  padding: 0.3rem 0.85rem;
                  border-radius: 999px;
                  font-size: 0.8rem;
                  font-weight: 700;
                  color: #2563eb;
                "
              >
                {{ simplifyType(property.property_type) }}
              </span>
            </div>
            <div style="padding: 1.5rem">
              <div
                style="
                  font-size: 1.5rem;
                  font-weight: 800;
                  color: #2563eb;
                  margin-bottom: 0.5rem;
                "
              >
                MYR {{ formatPrice(property.price) }}
              </div>
              <div
                style="
                  font-weight: 600;
                  color: #1e293b;
                  margin-bottom: 0.4rem;
                  white-space: nowrap;
                  overflow: hidden;
                  text-overflow: ellipsis;
                  font-size: 1rem;
                "
              >
                {{ property.title }}
              </div>
              <div
                style="color: #64748b; font-size: 0.9rem; margin-bottom: 1rem"
              >
                📍 {{ property.city }}, {{ property.state }}
              </div>
              <div
                style="
                  display: flex;
                  gap: 1.25rem;
                  font-size: 0.9rem;
                  color: #475569;
                  padding-top: 1rem;
                  border-top: 1px solid #f1f5f9;
                "
              >
                <span>🛏 {{ property.bedrooms ?? "-" }} bed</span>
                <span>🚿 {{ property.bathrooms ?? "-" }} bath</span>
                <span
                  >📐
                  {{
                    property.size_sqft
                      ? Number(property.size_sqft).toLocaleString()
                      : "-"
                  }}
                  sqft</span
                >
              </div>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- Pagination -->
      <div
        v-if="pagination.last_page > 1"
        style="
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 0.75rem;
          margin-top: 3rem;
        "
      >
        <button
          :disabled="pagination.current_page === 1"
          style="
            padding: 0.75rem 1.5rem;
            border: 1.5px solid #e2e8f0;
            border-radius: 0.5rem;
            background: white;
            cursor: pointer;
            font-weight: 600;
            color: #475569;
            font-size: 1rem;
          "
          @click="goToPage(pagination.current_page - 1)"
        >
          Prev
        </button>
        <span style="padding: 0.75rem 1rem; color: #64748b; font-size: 1rem">
          Page {{ pagination.current_page }} of {{ pagination.last_page }}
        </span>
        <button
          :disabled="pagination.current_page === pagination.last_page"
          style="
            padding: 0.75rem 1.5rem;
            border: 1.5px solid #e2e8f0;
            border-radius: 0.5rem;
            background: white;
            cursor: pointer;
            font-weight: 600;
            color: #475569;
            font-size: 1rem;
          "
          @click="goToPage(pagination.current_page + 1)"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({
  title: "Property Listings",
  meta: [
    {
      name: "description",
      content:
        "Browse Malaysian property listings with filters by state, type, price and bedrooms.",
    },
  ],
});

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const properties = ref([]);
const loading = ref(false);
const pagination = ref({});

const filters = ref({
  state: "",
  property_type: "",
  bedrooms: "",
  min_price: "",
  max_price: "",
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

const formatPrice = (price) => Number(price).toLocaleString("en-MY");

// Simplify messy property type strings for the badge
const simplifyType = (t) => {
  const s = (t || "").toLowerCase();
  if (
    s.includes("condominium") ||
    s.includes("service residence") ||
    s.includes("apartment") ||
    s.includes("flat")
  )
    return "Condo/Apt";
  if (s.includes("terrace") || s.includes("link") || s.includes("town house"))
    return "Terrace";
  if (s.includes("semi d") || s.includes("cluster")) return "Semi-D";
  if (s.includes("bungalow") || s.includes("villa")) return "Bungalow";
  return t?.split(" ").slice(0, 2).join(" ") || "Property";
};

// Different gradient per property category — makes cards visually distinct
const cardGradient = (t) => {
  const s = (t || "").toLowerCase();
  if (
    s.includes("condominium") ||
    s.includes("apartment") ||
    s.includes("service residence") ||
    s.includes("flat")
  )
    return "linear-gradient(135deg, #dbeafe 0%, #ede9fe 100%)";
  if (s.includes("terrace") || s.includes("link"))
    return "linear-gradient(135deg, #dcfce7 0%, #d1fae5 100%)";
  if (s.includes("semi d") || s.includes("cluster"))
    return "linear-gradient(135deg, #fef9c3 0%, #fde68a 100%)";
  if (s.includes("bungalow") || s.includes("villa"))
    return "linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)";
  return "linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%)";
};

// Different emoji per property category
const cardIcon = (t) => {
  const s = (t || "").toLowerCase();
  if (
    s.includes("condominium") ||
    s.includes("apartment") ||
    s.includes("service residence") ||
    s.includes("flat")
  )
    return "🏢";
  if (s.includes("terrace") || s.includes("link")) return "🏘";
  if (s.includes("semi d") || s.includes("cluster")) return "🏡";
  if (s.includes("bungalow") || s.includes("villa")) return "🏰";
  return "🏠";
};

const fetchProperties = async (page = 1) => {
  loading.value = true;
  try {
    const params = new URLSearchParams();
    params.append("page", page);
    Object.entries(filters.value).forEach(([key, val]) => {
      if (val !== "") params.append(key, val);
    });
    const data = await $fetch(`${apiBase}/api/properties?${params}`);
    properties.value = data.data;
    pagination.value = {
      current_page: data.current_page,
      last_page: data.last_page,
      total: data.total,
    };
  } catch (err) {
    console.error("Failed to fetch properties:", err);
  } finally {
    loading.value = false;
  }
};

const applyFilters = () => fetchProperties(1);
const resetFilters = () => {
  filters.value = {
    state: "",
    property_type: "",
    bedrooms: "",
    min_price: "",
    max_price: "",
  };
  fetchProperties(1);
};
const goToPage = (page) => fetchProperties(page);

onMounted(() => fetchProperties());
</script>
