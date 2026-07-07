import client from './client'

// Plans API calls. Mirrors the backend planning endpoints.
export function listPlans() {
  return client.get('/plans').then((r) => r.data)
}

export function createPlan(payload) {
  return client.post('/plans', payload).then((r) => r.data)
}

export function getPlan(planId) {
  return client.get(`/plans/${planId}`).then((r) => r.data)
}
