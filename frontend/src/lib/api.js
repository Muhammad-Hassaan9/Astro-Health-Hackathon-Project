import axios from 'axios'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const SESSION_KEY = 'astrohealth_session'

export function getSession() {
  try {
    return JSON.parse(localStorage.getItem(SESSION_KEY))
  } catch {
    return null
  }
}

export function setSession(session) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(session))
}

export function clearSession() {
  localStorage.removeItem(SESSION_KEY)
}

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const session = getSession()

  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`
  }

  return config
})

let refreshPromise = null

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (
      error.response?.status !== 401 ||
      originalRequest?._retry ||
      originalRequest?.url?.includes('/auth/login') ||
      originalRequest?.url?.includes('/auth/signup') ||
      originalRequest?.url?.includes('/auth/refresh')
    ) {
      return Promise.reject(error)
    }

    const session = getSession()

    if (!session?.refresh_token) {
      clearSession()
      window.dispatchEvent(new Event('astrohealth:session-expired'))
      return Promise.reject(error)
    }

    originalRequest._retry = true

    try {
      if (!refreshPromise) {
        refreshPromise = axios
          .post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: session.refresh_token,
          })
          .then((response) => {
            const newSession = {
              ...session,
              ...response.data,
            }

            setSession(newSession)
            return newSession
          })
          .finally(() => {
            refreshPromise = null
          })
      }

      const newSession = await refreshPromise

      originalRequest.headers.Authorization =
        `Bearer ${newSession.access_token}`

      return api(originalRequest)
    } catch (refreshError) {
      clearSession()
      window.dispatchEvent(new Event('astrohealth:session-expired'))
      return Promise.reject(refreshError)
    }
  }
)

export function getErrorMessage(error) {
  return (
    error.response?.data?.detail ||
    error.response?.data?.message ||
    error.message ||
    'Something went wrong. Please try again.'
  )
}