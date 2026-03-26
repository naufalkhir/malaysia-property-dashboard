export default defineNuxtConfig({
  modules: ["@pinia/nuxt", "@nuxt/ui"],

  routeRules: {
    "/": { prerender: true },
    "/listings": { ssr: true },
    "/listings/**": { ssr: true },
    "/dashboard/**": { ssr: false },
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },

  app: {
    head: {
      titleTemplate: "%s — Malaysia Realty Analyzer",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
      ],
      // Add Leaflet CSS from CDN
      link: [
        {
          rel: "stylesheet",
          href: "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
        },
      ],
    },
  },

  vite: {
    optimizeDeps: {
      include: ["leaflet", "@vue/devtools-core", "@vue/devtools-kit"],
    },
  },

  devtools: { enabled: true },
  compatibilityDate: "2024-04-03",
});
