import client from './client'

// Plans API calls. The client interceptor unwraps the envelope to {data, meta}.
export function listPlans() {
  // data is the plan array; meta carries total/pagination.
  return client.get('/plans')
}

export function createPlan(payload) {
  return client.post('/plans', payload).then((r) => r.data)
}

export function getPlan(planId) {
  return client.get(`/plans/${planId}`).then((r) => r.data)
}
