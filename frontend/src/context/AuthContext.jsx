import {
  createContext,
  useCallback,
  useEffect,
  useState,
} from 'react'

import {
  getSession,
  clearSession,
} from '../lib/api'

import {
  getCurrentUser,
  loginUser,
  signupUser,
  logoutUser,
} from '../services/authService'

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const refreshUser = useCallback(async () => {
    const session = getSession()

    if (!session?.access_token) {
      setUser(null)
      return null
    }

    const currentUser = await getCurrentUser()
    setUser(currentUser)

    return currentUser
  }, [])

  useEffect(() => {
    let mounted = true

    async function initializeAuth() {
      try {
        if (getSession()?.access_token) {
          const currentUser = await getCurrentUser()

          if (mounted) setUser(currentUser)
        }
      } catch {
        clearSession()

        if (mounted) setUser(null)
      } finally {
        if (mounted) setLoading(false)
      }
    }

    initializeAuth()

    const handleSessionExpired = () => {
      setUser(null)
    }

    window.addEventListener(
      'astrohealth:session-expired',
      handleSessionExpired
    )

    return () => {
      mounted = false

      window.removeEventListener(
        'astrohealth:session-expired',
        handleSessionExpired
      )
    }
  }, [])

  const login = async (credentials) => {
    const result = await loginUser(credentials)
    setUser(result.user)
    return result
  }

  const signup = async (credentials) => {
    const result = await signupUser(credentials)

    if (!result.pendingVerification) {
      setUser(result.user)
    }

    return result
  }

  const logout = () => {
    logoutUser()
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated: Boolean(user),
        login,
        signup,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}