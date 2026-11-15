import { api } from '../lib/api'

export async function getHealthMetrics() {
  const response = await api.get('/health/metrics')
  return response.data
}