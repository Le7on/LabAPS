import axios from 'axios'

const TOKEN_KEY = 'labaps.token'

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token)
  else localStorage.removeItem(TOKEN_KEY)
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

// Shared Axios instance. The dev server proxies /api to the Flask backend
// (see vite.config.ts).
const client = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

// Attach the stored bearer token (ADR-013) to every request when present.
client.interceptors.request.use((config) => {
  const token = getToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// The backend uses a unified envelope {success, data, meta} (ADR-012).
// Unwrap it centrally so callers work with {data, meta} directly, and surface
// the stable error code/message on failures.
client.interceptors.response.use(
  (response) => {
    const body = response.data ?? {}
    return { data: body.data, meta: body.meta ?? {} }
  },
  (error) => {
    const envelope = error?.response?.data
    if (envelope?.error) {
      return Promise.reject({
        code: envelope.error.code,
        message: envelope.error.message,
        details: envelope.error.details ?? [],
      })
    }
    return Promise.reject({ code: 'NETWORK_ERROR', message: error.message, details: [] })
  }
)

export default client
