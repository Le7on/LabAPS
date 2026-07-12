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

// Merge the selected plans' demand lines into one scheduling run (ADR-020).
export function schedulePlans(planIds, shiftMode = 'single') {
  return client
    .post('/schedule', { planIds, shiftMode })
    .then((r) => ({ data: r.data, meta: r.meta }))
}

export function addDemandLine(planId, payload) {
  return client.post(`/plans/${planId}/demand-lines`, payload).then((r) => r.data)
}

export function removeDemandLine(planId, lineId) {
  return client.delete(`/plans/${planId}/demand-lines/${lineId}`).then((r) => r.data)
}
