import { api, setSession, clearSession } from '../lib/api'

export async function signupUser(credentials) {
  const response = await api.post('/auth/signup', credentials)

  // Email verification pending: backend returns HTTP 202.
  if (response.status === 202) {
    return {
      pendingVerification: true,
      message: response.data.message,
    }
  }

  setSession(response.data)

  return {
    pendingVerification: false,
    user: await getCurrentUser(),
  }
}

export async function loginUser(credentials) {
  const response = await api.post('/auth/login', credentials)

  setSession(response.data)

  try {
    const user = await getCurrentUser()

    return { user }
  } catch (error) {
    clearSession()
    throw error
  }
}

export async function getCurrentUser() {
  const response = await api.get('/auth/me')
  return response.data
}

export function logoutUser() {
  clearSession()
}