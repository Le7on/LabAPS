import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// {{PROJECT_NAME}} frontend build configuration.
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://127.0.0.1:5000',
    },
  },
  build: {
    outDir: 'dist',
  },
})
