import client from './client'

// Laboratory API calls. The client interceptor unwraps the envelope to {data, meta}.
export function listEquipment() {
  return client.get('/equipment')
}

export function createEquipment(payload) {
  return client.post('/equipment', payload).then((r) => r.data)
}

export function listStaff() {
  return client.get('/staff')
}

export function createStaff(payload) {
  return client.post('/staff', payload).then((r) => r.data)
}

export function listWorkflowDefinitions() {
  return client.get('/workflow-definitions')
}

export function createWorkflowDefinition(payload) {
  return client.post('/workflow-definitions', payload).then((r) => r.data)
}

export function listProjects() {
  return client.get('/projects')
}

export function createProject(payload) {
  return client.post('/projects', payload).then((r) => r.data)
}

// kind is 'equipment' | 'staff' | 'projects'; verb is 'deactivate' | 'activate'.
export function setResourceActive(kind, id, active) {
  const verb = active ? 'activate' : 'deactivate'
  return client.post(`/${kind}/${id}/${verb}`).then((r) => r.data)
}

export function updateProject(id, payload) {
  return client.put(`/projects/${id}`, payload).then((r) => r.data)
}
export function deleteProject(id) {
  return client.delete(`/projects/${id}`).then((r) => r.data)
}
export function updateEquipment(id, payload) {
  return client.put(`/equipment/${id}`, payload).then((r) => r.data)
}
export function deleteEquipment(id) {
  return client.delete(`/equipment/${id}`).then((r) => r.data)
}
export function updateStaff(id, payload) {
  return client.put(`/staff/${id}`, payload).then((r) => r.data)
}
export function deleteStaff(id) {
  return client.delete(`/staff/${id}`).then((r) => r.data)
}
export function deleteWorkflowDefinition(id) {
  return client.delete(`/workflow-definitions/${id}`).then((r) => r.data)
}

export function updateWorkflowDefinition(id, payload) {
  return client.put(`/workflow-definitions/${id}`, payload).then((r) => r.data)
}

// kind is 'equipment' | 'staff'; date arrays of "YYYY-MM-DD".
export function setUnavailableDates(kind, id, unavailableDates, overtimeDates = []) {
  return client
    .post(`/${kind}/${id}/unavailable-dates`, { unavailableDates, overtimeDates })
    .then((r) => r.data)
}
