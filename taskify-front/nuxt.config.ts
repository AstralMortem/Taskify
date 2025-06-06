// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  modules: [
    '@nuxt/eslint',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/ui',
    'nuxt-api-party',
    '@pinia/nuxt'
  ],
  css: ['~/assets/main.css'],

  apiParty:{
    endpoints: {
      backend: {
        url: process.env.BACKEND_URL || 'https://taskify-backend-production-9eda.up.railway.app',
        cookies: true,
        schema: './assets/openapi.json'
      }
    }
  },
  colorMode: {
    fallback: 'light',
    preference: 'light'
  },
  runtimeConfig:{
    public:{
      AWSDomain: process.env.MEDIA_URL
    }
  }
})