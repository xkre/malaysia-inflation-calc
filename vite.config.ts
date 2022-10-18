import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}']
      },
      manifest: {
        name: 'Malaysia Inflation Calculator',
        short_name: 'InflationCalc',
        description: 'Simple calculator that calculates the equivalent purchasing power between two time periods',
        icons: [
          {
            src: 'logo.png',
            sizes: '160x160',
            type: 'image/png'
          },
        ]
      }
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
