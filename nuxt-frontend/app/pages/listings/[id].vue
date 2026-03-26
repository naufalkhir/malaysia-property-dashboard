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
            >Try Prediction →</NuxtLink
          >
        </div>
      </div>
    </nav>

    <div style="max-width: 1280px; margin: 0 auto; padding: 2.5rem 1.5rem">
      <!-- Back button -->
      <NuxtLink
        to="/listings"
        style="
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          color: #64748b;
          text-decoration: none;
          font-weight: 600;
          margin-bottom: 1.5rem;
          font-size: 1rem;
        "
      >
        ← Back to Listings
      </NuxtLink>

      <!-- Loading -->
      <div
        v-if="loading"
        style="text-align: center; padding: 5rem; color: #64748b"
      >
        <div style="font-size: 2.5rem; margin-bottom: 1rem">⏳</div>
        <p style="font-size: 1.1rem">Loading property...</p>
      </div>

      <!-- Not found -->
      <div
        v-else-if="!property"
        style="
          text-align: center;
          padding: 5rem;
          background: white;
          border-radius: 1rem;
        "
      >
        <div style="font-size: 4rem; margin-bottom: 1rem">😕</div>
        <h3
          style="
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
          "
        >
          Property not found
        </h3>
        <NuxtLink to="/listings" style="color: #2563eb; font-weight: 600"
          >Back to listings</NuxtLink
        >
      </div>

      <!-- Property Detail -->
      <div v-else>
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem">
          <!-- Left Column -->
          <div>
            <!-- Image -->
            <div
              style="
                background: linear-gradient(135deg, #dbeafe 0%, #ede9fe 100%);
                height: 350px;
                border-radius: 1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 6rem;
                margin-bottom: 1.5rem;
                position: relative;
              "
            >
              🏠
              <span
                style="
                  position: absolute;
                  top: 1rem;
                  right: 1rem;
                  background: white;
                  padding: 0.4rem 1rem;
                  border-radius: 999px;
                  font-size: 0.9rem;
                  font-weight: 700;
                  color: #2563eb;
                "
              >
                {{ property.property_type }}
              </span>
            </div>

            <!-- Title & Location -->
            <div
              style="
                background: white;
                border-radius: 1rem;
                padding: 2rem;
                margin-bottom: 1.5rem;
                border: 1px solid #e2e8f0;
              "
            >
              <h1
                style="
                  font-size: 1.75rem;
                  font-weight: 800;
                  color: #1e293b;
                  margin-bottom: 0.75rem;
                "
              >
                {{ property.title }}
              </h1>
              <p
                style="
                  color: #64748b;
                  font-size: 1.05rem;
                  margin-bottom: 1.5rem;
                "
              >
                📍 {{ property.area ? property.area + ", " : ""
                }}{{ property.city }}, {{ property.state }}
              </p>

              <!-- Key stats -->
              <div
                style="
                  display: grid;
                  grid-template-columns: repeat(4, 1fr);
                  gap: 1rem;
                  padding-top: 1.5rem;
                  border-top: 1px solid #f1f5f9;
                "
              >
                <div
                  style="
                    text-align: center;
                    padding: 1rem;
                    background: #f8fafc;
                    border-radius: 0.75rem;
                  "
                >
                  <div style="font-size: 1.75rem; margin-bottom: 0.25rem">
                    🛏
                  </div>
                  <div
                    style="font-size: 1.25rem; font-weight: 800; color: #1e293b"
                  >
                    {{ property.bedrooms ?? "-" }}
                  </div>
                  <div style="font-size: 0.8rem; color: #64748b">Bedrooms</div>
                </div>
                <div
                  style="
                    text-align: center;
                    padding: 1rem;
                    background: #f8fafc;
                    border-radius: 0.75rem;
                  "
                >
                  <div style="font-size: 1.75rem; margin-bottom: 0.25rem">
                    🚿
                  </div>
                  <div
                    style="font-size: 1.25rem; font-weight: 800; color: #1e293b"
                  >
                    {{ property.bathrooms ?? "-" }}
                  </div>
                  <div style="font-size: 0.8rem; color: #64748b">Bathrooms</div>
                </div>
                <div
                  style="
                    text-align: center;
                    padding: 1rem;
                    background: #f8fafc;
                    border-radius: 0.75rem;
                  "
                >
                  <div style="font-size: 1.75rem; margin-bottom: 0.25rem">
                    🚗
                  </div>
                  <div
                    style="font-size: 1.25rem; font-weight: 800; color: #1e293b"
                  >
                    {{ property.car_parks ?? "-" }}
                  </div>
                  <div style="font-size: 0.8rem; color: #64748b">Car Parks</div>
                </div>
                <div
                  style="
                    text-align: center;
                    padding: 1rem;
                    background: #f8fafc;
                    border-radius: 0.75rem;
                  "
                >
                  <div style="font-size: 1.75rem; margin-bottom: 0.25rem">
                    📐
                  </div>
                  <div
                    style="font-size: 1.25rem; font-weight: 800; color: #1e293b"
                  >
                    {{
                      property.size_sqft
                        ? property.size_sqft.toLocaleString()
                        : "-"
                    }}
                  </div>
                  <div style="font-size: 0.8rem; color: #64748b">Sqft</div>
                </div>
              </div>
            </div>

            <!-- Details -->
            <div
              style="
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
                  margin-bottom: 1.25rem;
                "
              >
                Property Details
              </h2>
              <div
                style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem"
              >
                <div
                  style="
                    padding: 1rem;
                    background: #f8fafc;
                    border-radius: 0.75rem;
                  "
                >
                  <div
                    style="
                      font-size: 0.8rem;
                      font-weight: 700;
                      color: #64748b;
                      text-transform: uppercase;
                      margin-bottom: 0.4rem;
                    "
                  >
                    Tenure
                  </div>
                  <div
                    style="
                      font-size: 1rem;
                      font-weight: 600;
                      color: #1e293b;
                      text-transform: capitalize;
                    "
                  >
                    {{ property.tenure ?? "N/A" }}
                  </div>
                </div>
                <div
                  style="
                    padding: 1rem;
                    background: #f8fafc;
                    border-radius: 0.75rem;
                  "
                >
                  <div
                    style="
                      font-size: 0.8rem;
                      font-weight: 700;
                      color: #64748b;
                      text-transform: uppercase;
                      margin-bottom: 0.4rem;
                    "
                  >
                    Furnishing
                  </div>
                  <div
                    style="
                      font-size: 1rem;
                      font-weight: 600;
                      color: #1e293b;
                      text-transform: capitalize;
                    "
                  >
                    {{ property.furnishing ?? "N/A" }}
                  </div>
                </div>
                <div
                  style="
                    padding: 1rem;
                    background: #f8fafc;
                    border-radius: 0.75rem;
                  "
                >
                  <div
                    style="
                      font-size: 0.8rem;
                      font-weight: 700;
                      color: #64748b;
                      text-transform: uppercase;
                      margin-bottom: 0.4rem;
                    "
                  >
                    Price per Sqft
                  </div>
                  <div
                    style="font-size: 1rem; font-weight: 600; color: #1e293b"
                  >
                    MYR
                    {{
                      property.price_per_sqft
                        ? Number(property.price_per_sqft).toLocaleString()
                        : "N/A"
                    }}
                  </div>
                </div>
                <div
                  style="
                    padding: 1rem;
                    background: #f8fafc;
                    border-radius: 0.75rem;
                  "
                >
                  <div
                    style="
                      font-size: 0.8rem;
                      font-weight: 700;
                      color: #64748b;
                      text-transform: uppercase;
                      margin-bottom: 0.4rem;
                    "
                  >
                    Listed Date
                  </div>
                  <div
                    style="font-size: 1rem; font-weight: 600; color: #1e293b"
                  >
                    {{ property.listed_at ?? "N/A" }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column — Price Card -->
          <div>
            <div
              style="
                background: white;
                border-radius: 1rem;
                padding: 2rem;
                border: 1px solid #e2e8f0;
                position: sticky;
                top: 2rem;
              "
            >
              <div
                style="
                  font-size: 2rem;
                  font-weight: 800;
                  color: #2563eb;
                  margin-bottom: 0.5rem;
                "
              >
                MYR {{ formatPrice(property.price) }}
              </div>
              <div
                style="color: #64748b; font-size: 0.9rem; margin-bottom: 2rem"
              >
                {{
                  property.price_per_sqft
                    ? "MYR " +
                      Number(property.price_per_sqft).toLocaleString() +
                      " per sqft"
                    : ""
                }}
              </div>

              <div
                style="
                  display: flex;
                  flex-direction: column;
                  gap: 0.75rem;
                  margin-bottom: 2rem;
                "
              >
                <div
                  style="
                    display: flex;
                    justify-content: space-between;
                    padding: 0.75rem 0;
                    border-bottom: 1px solid #f1f5f9;
                  "
                >
                  <span style="color: #64748b; font-size: 0.95rem">Type</span>
                  <span
                    style="font-weight: 600; color: #1e293b; font-size: 0.95rem"
                    >{{ property.property_type }}</span
                  >
                </div>
                <div
                  style="
                    display: flex;
                    justify-content: space-between;
                    padding: 0.75rem 0;
                    border-bottom: 1px solid #f1f5f9;
                  "
                >
                  <span style="color: #64748b; font-size: 0.95rem">State</span>
                  <span
                    style="font-weight: 600; color: #1e293b; font-size: 0.95rem"
                    >{{ property.state }}</span
                  >
                </div>
                <div
                  style="
                    display: flex;
                    justify-content: space-between;
                    padding: 0.75rem 0;
                    border-bottom: 1px solid #f1f5f9;
                  "
                >
                  <span style="color: #64748b; font-size: 0.95rem">City</span>
                  <span
                    style="font-weight: 600; color: #1e293b; font-size: 0.95rem"
                    >{{ property.city }}</span
                  >
                </div>
                <div
                  style="
                    display: flex;
                    justify-content: space-between;
                    padding: 0.75rem 0;
                  "
                >
                  <span style="color: #64748b; font-size: 0.95rem">Tenure</span>
                  <span
                    style="
                      font-weight: 600;
                      color: #1e293b;
                      font-size: 0.95rem;
                      text-transform: capitalize;
                    "
                    >{{ property.tenure ?? "N/A" }}</span
                  >
                </div>
              </div>

              <NuxtLink
                to="/dashboard/predict"
                style="
                  display: block;
                  background: #2563eb;
                  color: white;
                  padding: 1rem;
                  border-radius: 0.5rem;
                  text-decoration: none;
                  font-weight: 700;
                  font-size: 1rem;
                  text-align: center;
                "
              >
                🤖 Predict Similar Price
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Similar Properties -->
        <div v-if="similar.length > 0" style="margin-top: 3rem">
          <h2
            style="
              font-size: 1.5rem;
              font-weight: 800;
              color: #1e293b;
              margin-bottom: 1.5rem;
            "
          >
            Similar Properties
          </h2>
          <div
            style="
              display: grid;
              grid-template-columns: repeat(3, 1fr);
              gap: 1.5rem;
            "
          >
            <NuxtLink
              v-for="item in similar"
              :key="item.id"
              :to="`/listings/${item.id}`"
              style="text-decoration: none; color: inherit"
            >
              <div
                style="
                  background: white;
                  border-radius: 1rem;
                  overflow: hidden;
                  border: 1px solid #e2e8f0;
                  cursor: pointer;
                "
              >
                <div
                  style="
                    background: linear-gradient(
                      135deg,
                      #dbeafe 0%,
                      #ede9fe 100%
                    );
                    height: 140px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 3rem;
                  "
                >
                  🏠
                </div>
                <div style="padding: 1.25rem">
                  <div
                    style="
                      font-size: 1.25rem;
                      font-weight: 800;
                      color: #2563eb;
                      margin-bottom: 0.4rem;
                    "
                  >
                    MYR {{ formatPrice(item.price) }}
                  </div>
                  <div
                    style="
                      color: #1e293b;
                      font-weight: 600;
                      font-size: 0.9rem;
                      margin-bottom: 0.4rem;
                      white-space: nowrap;
                      overflow: hidden;
                      text-overflow: ellipsis;
                    "
                  >
                    {{ item.title }}
                  </div>
                  <div style="color: #64748b; font-size: 0.85rem">
                    📍 {{ item.city }}, {{ item.state }}
                  </div>
                </div>
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const route = useRoute();
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const property = ref(null);
const similar = ref([]);
const loading = ref(true);

const formatPrice = (price) => Number(price).toLocaleString("en-MY");

// Fetch property details
const fetchProperty = async () => {
  loading.value = true;
  try {
    property.value = await $fetch(
      `${apiBase}/api/properties/${route.params.id}`,
    );

    useHead({
      title: property.value.title,
      meta: [
        {
          name: "description",
          content: `${property.value.property_type} in ${property.value.city}, ${property.value.state} — MYR ${formatPrice(property.value.price)}`,
        },
      ],
    });

    // Fetch similar properties
    const similarData = await $fetch(
      `${apiBase}/api/properties/${route.params.id}/similar`,
    );
    similar.value = similarData;
  } catch (err) {
    console.error("Failed to fetch property:", err);
    property.value = null;
  } finally {
    loading.value = false;
  }
};

onMounted(() => fetchProperty());
</script>
