import { Navigate, useLocation } from 'react-router-dom'
import LoginForm from '../features/auth/components/LoginForm'
import useAuth from '../hooks/useAuth'

function Login() {
  const { isAuthenticated } = useAuth()
  const location = useLocation()

  if (isAuthenticated) {
    return <Navigate to="/app" replace />
  }

  return (
    <>
      {location.state?.message && (
        <div className="mb-6 rounded-lg border border-teal-500/30 bg-teal-500/10 p-3 text-sm text-teal-200">
          {location.state.message}
        </div>
      )}

      <LoginForm />
    </>
  )
}

export default Login