import { Navigate } from 'react-router-dom'
import SignupForm from '../features/auth/components/SignupForm'
import useAuth from '../hooks/useAuth'

function Signup() {
  const { isAuthenticated } = useAuth()

  if (isAuthenticated) {
    return <Navigate to="/app" replace />
  }

  return <SignupForm />
}

export default Signup