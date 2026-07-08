import client from './client'

// Execution API calls. The client interceptor unwraps the envelope to {data, meta}.
function action(assignmentId, verb, body) {
  return client.post(`/executions/${assignmentId}/${verb}`, body).then((r) => r.data)
}

export function startAssignment(assignmentId) {
  return action(assignmentId, 'start')
}

export function completeAssignment(assignmentId) {
  return action(assignmentId, 'complete')
}

export function failAssignment(assignmentId, reason) {
  return action(assignmentId, 'fail', { reason })
}

export function cancelAssignment(assignmentId, reason) {
  return action(assignmentId, 'cancel', { reason })
}
