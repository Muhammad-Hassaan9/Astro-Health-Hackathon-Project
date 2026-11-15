import { api } from '../lib/api'

export async function getAstronautProfile() {
  const response = await api.get('/astronaut/profile')
  return response.data
}

export async function createAstronautProfile(profile) {
  const response = await api.post('/astronaut/profile', profile)
  return response.data
}

export async function updateAstronautProfile(profile) {
  const response = await api.patch('/astronaut/profile', profile)
  return response.data
}