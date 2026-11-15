import { api } from '../lib/api'

export async function getHealthObservations(params = {}) {
  const response = await api.get('/health/observations', {
    params: {
      limit: 100,
      offset: 0,
      ...params,
    },
  })

  return response.data
}

export async function createHealthObservation(data) {
  const response = await api.post('/health/observations', data)
  return response.data
}

export async function simulateHealthReading() {
  const response = await api.post('/health/simulate')
  return response.data
}