import client from './client'

// Reporting API calls. The client interceptor unwraps the envelope to {data, meta}.
export function getDashboard() {
  return client.get('/reports/dashboard').then((r) => r.data)
}
