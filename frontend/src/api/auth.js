import client from './client'

// Auth API (ADR-013). whoami validates the current bearer token and returns the
// user; createUser is an administrator-only bootstrap for issuing tokens.
export function whoami() {
  return client.get('/auth/whoami').then((r) => r.data)
}

export function createUser(payload) {
  return client.post('/users', payload).then((r) => r.data)
}
