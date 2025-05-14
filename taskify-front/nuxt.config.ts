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
        url: process.env.BASE_URL || 'http://localhost:8000',
        cookies: true,
        schema: '~/assets/openapi.json'
      }
    }
  },
  colorMode: {
    'fallback': 'light'
  },
  runtimeConfig:{
    public:{
      AWSDomain: process.env.MEDIA_URL || 'http://localhost:9000'
    }
  }
})