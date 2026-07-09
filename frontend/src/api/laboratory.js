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
