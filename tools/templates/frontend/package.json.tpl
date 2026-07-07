{
  "name": "lab-aps-frontend",
  "version": "{{VERSION}}",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --fix",
    "lint:check": "eslint .",
    "format": "prettier --write \"src/**/*.{js,ts,vue,css,html}\" \"*.{js,ts,json,html}\"",
    "format:check": "prettier --check \"src/**/*.{js,ts,vue,css,html}\" \"*.{js,ts,json,html}\""
  },
  "dependencies": {
    "axios": "^1.7.0",
    "pinia": "^2.2.0",
    "vue": "^3.5.0",
    "vue-router": "^4.4.0"
  },
  "devDependencies": {
    "@eslint/js": "^9.9.0",
    "@vitejs/plugin-vue": "^5.1.0",
    "eslint": "^9.9.0",
    "eslint-config-prettier": "^9.1.0",
    "eslint-plugin-vue": "^9.27.0",
    "prettier": "^3.3.0",
    "vite": "^5.4.0"
  }
}
