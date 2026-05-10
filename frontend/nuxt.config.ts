export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ["~/assets/css/main.css"],
  modules: ["@nuxtjs/tailwindcss"],
  typescript: {
    strict: true,
    typeCheck: true
  },
  runtimeConfig: {
    public: {
      backendBaseUrl: process.env.NUXT_PUBLIC_BACKEND_BASE_URL ?? "http://localhost:8000"
    }
  },
  compatibilityDate: "2026-05-10"
})
