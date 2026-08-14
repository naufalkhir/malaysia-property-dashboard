<template>
  <div>
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
        <!-- Left: Logo -->
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

        <!-- Right: Nav links + CTA -->
        <div style="display: flex; align-items: center; gap: 2.5rem">
          <NuxtLink
            to="/listings"
            style="
              color: #475569;
              text-decoration: none;
              font-weight: 600;
              font-size: 1rem;
              letter-spacing: 0.01em;
            "
          >
            Listings
          </NuxtLink>
          <NuxtLink
            to="/dashboard"
            style="
              color: #475569;
              text-decoration: none;
              font-weight: 600;
              font-size: 1rem;
              letter-spacing: 0.01em;
            "
          >
            Dashboard
          </NuxtLink>
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
          >
            Try Prediction →
          </NuxtLink>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="relative overflow-hidden bg-[#050807] px-6 py-24 text-center md:py-32">
      <!-- Aurora glow layers (pure CSS, no canvas/WebGL) -->
      <div class="pointer-events-none absolute inset-0 flex items-center justify-center">
        <div class="absolute h-[220px] w-[140%] rounded-full bg-emerald-500/25 blur-[90px] mix-blend-screen" />
        <div class="absolute h-[140px] w-[90%] rounded-full bg-cyan-400/40 blur-[70px] mix-blend-screen" />
        <div class="absolute h-[60px] w-[55%] rounded-full bg-amber-300/40 blur-[60px] mix-blend-screen" />
        <div class="absolute h-[24px] w-[30%] rounded-full bg-white/80 blur-[40px] mix-blend-screen" />
      </div>

      <div class="relative z-10 mx-auto max-w-3xl">
        <BlurText
          text="Malaysia Property Analytics"
          :delay="120"
          animate-by="words"
          direction="top"
          class="mb-6 justify-center text-4xl font-extrabold leading-tight text-white md:text-5xl"
        />
        <p class="mb-10 text-lg leading-relaxed text-slate-300">
          Explore real Malaysian property listings with affordability analysis,
          interactive maps, and ML-powered price predictions.
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <NuxtLink to="/listings" class="btn-primary">
            Browse Listings →
          </NuxtLink>
          <NuxtLink
            to="/dashboard"
            class="rounded-lg border-2 border-white px-6 py-3 font-semibold text-white no-underline"
          >
            View Analytics
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- Stats Bar -->
    <section
      style="
        background: white;
        border-bottom: 1px solid #e2e8f0;
        padding: 2rem 1.5rem;
      "
    >
      <div
        style="
          max-width: 1280px;
          margin: 0 auto;
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 2rem;
          text-align: center;
        "
      >
        <div>
          <div style="font-size: 2rem; font-weight: 800; color: #2563eb">
            50,000+
          </div>
          <div style="color: #64748b; font-size: 0.9rem">Property Listings</div>
        </div>
        <div>
          <div style="font-size: 2rem; font-weight: 800; color: #2563eb">
            16
          </div>
          <div style="color: #64748b; font-size: 0.9rem">Malaysian States</div>
        </div>
        <div>
          <div style="font-size: 2rem; font-weight: 800; color: #2563eb">
            ML
          </div>
          <div style="color: #64748b; font-size: 0.9rem">Price Predictions</div>
        </div>
        <div>
          <div style="font-size: 2rem; font-weight: 800; color: #2563eb">
            DOSM
          </div>
          <div style="color: #64748b; font-size: 0.9rem">Official Data</div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section style="padding: 5rem 1.5rem; background: #f8fafc">
      <div style="max-width: 1280px; margin: 0 auto">
        <h2
          style="
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 3rem;
            color: #1e293b;
          "
        >
          Everything you need to understand the Malaysian property market
        </h2>
        <div
          style="
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
          "
        >
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 2rem;
              box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            "
          >
            <div style="font-size: 2.5rem; margin-bottom: 1rem">🗺️</div>
            <h3
              style="
                font-size: 1.25rem;
                font-weight: 700;
                margin-bottom: 0.75rem;
                color: #1e293b;
              "
            >
              Interactive Map
            </h3>
            <p style="color: #64748b; line-height: 1.7">
              Choropleth maps showing average prices and affordability ratios by
              state across Malaysia.
            </p>
          </div>
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 2rem;
              box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            "
          >
            <div style="font-size: 2.5rem; margin-bottom: 1rem">📊</div>
            <h3
              style="
                font-size: 1.25rem;
                font-weight: 700;
                margin-bottom: 0.75rem;
                color: #1e293b;
              "
            >
              Analytics Dashboard
            </h3>
            <p style="color: #64748b; line-height: 1.7">
              Price trends, distribution charts, and demographic cross-analysis
              using official DOSM data.
            </p>
          </div>
          <div
            style="
              background: white;
              border-radius: 1rem;
              padding: 2rem;
              box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            "
          >
            <div style="font-size: 2.5rem; margin-bottom: 1rem">🤖</div>
            <h3
              style="
                font-size: 1.25rem;
                font-weight: 700;
                margin-bottom: 0.75rem;
                color: #1e293b;
              "
            >
              ML Price Prediction
            </h3>
            <p style="color: #64748b; line-height: 1.7">
              Random Forest model trained on real Malaysian property data to
              predict property prices.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer
      style="
        background: #1e293b;
        color: #94a3b8;
        text-align: center;
        padding: 2rem;
        font-size: 0.9rem;
      "
    >
      Built with Laravel · Python FastAPI · Nuxt.js · PostgreSQL · Scikit-learn
    </footer>
  </div>
</template>
