import { api } from '../lib/api'

export async function getAlerts(params = {}) {
  const response = await api.get('/alerts', {
    params: {
      limit: 100,
      offset: 0,
      ...params,
    },
  })

  return response.data
}

export async function updateAlertStatus(alertId, status) {
  const response = await api.patch(`/alerts/${alertId}/status`, {
    status,
  })

  return response.data
}