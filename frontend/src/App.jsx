import { Navigate, Route, Routes } from 'react-router-dom'

import AuthLayout from './layouts/AuthLayout'
import DashboardLayout from './layouts/DashboardLayout'
import Login from './pages/Login'
import Signup from './pages/Signup'
import useAuth from './hooks/useAuth'

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen bg-[#080f1d] flex items-center justify-center">
        <div className="text-center">
          <div className="w-9 h-9 border-2 border-teal-400 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm text-slate-400 mt-4">
            Restoring your session...
          </p>
        </div>
      </div>
    )
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />
}

function App() {
  const { loading, isAuthenticated } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen bg-[#080f1d] flex items-center justify-center">
        <div className="w-9 h-9 border-2 border-teal-400 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <Routes>
      <Route element={<AuthLayout />}>
        <Route
          path="/login"
          element={
            isAuthenticated ? <Navigate to="/app" replace /> : <Login />
          }
        />

        <Route
          path="/signup"
          element={
            isAuthenticated ? <Navigate to="/app" replace /> : <Signup />
          }
        />
      </Route>

      <Route
        path="/app/*"
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      />

      <Route
        path="/"
        element={
          <Navigate to={isAuthenticated ? '/app' : '/login'} replace />
        }
      />

      <Route
        path="*"
        element={
          <Navigate to={isAuthenticated ? '/app' : '/login'} replace />
        }
      />
    </Routes>
  )
}

export default App