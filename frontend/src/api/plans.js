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

export function createVersion(planId) {
  return client.post(`/plans/${planId}/versions`).then((r) => r.data)
}

export function getPlanAvailability(planId) {
  return client.get(`/plans/${planId}/availability`).then((r) => r.data)
}

export function setPlanAvailability(planId, kind, resourceId, available) {
  return client
    .post(`/plans/${planId}/availability`, { kind, resourceId, available })
    .then((r) => r.data)
}

export function generateInstances(planId, versionId, workflowDefinitionId, runCounts = {}) {
  return client
    .post(`/plans/${planId}/versions/${versionId}/generate-instances`, {
      workflowDefinitionId,
      runCounts,
    })
    .then((r) => r.data)
}

export function scheduleInstances(planId, versionId, frozenUntil = 0) {
  return client
    .post(`/plans/${planId}/versions/${versionId}/schedule-instances`, { frozenUntil })
    .then((r) => ({ data: r.data, meta: r.meta }))
}

export function listAssignments(planId, versionId) {
  return client.get(`/plans/${planId}/versions/${versionId}/assignments`)
}

export function addDemand(planId, versionId, payload) {
  return client.post(`/plans/${planId}/versions/${versionId}/demands`, payload).then((r) => r.data)
}

export function listDemands(planId, versionId) {
  return client.get(`/plans/${planId}/versions/${versionId}/demands`)
}

export function reviewVersion(planId, versionId) {
  return client.post(`/plans/${planId}/versions/${versionId}/review`).then((r) => r.data)
}

export function publishVersion(planId, versionId) {
  return client.post(`/plans/${planId}/versions/${versionId}/publish`).then((r) => r.data)
}
