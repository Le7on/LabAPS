import axios from 'axios'

// Shared Axios instance. The dev server proxies /api to the Flask backend
// (see vite.config.ts).
const client = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

export default client
