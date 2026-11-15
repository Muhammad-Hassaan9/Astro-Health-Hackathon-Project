import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Eye, EyeOff, LoaderCircle } from 'lucide-react'
import useAuth from '../../../hooks/useAuth'
import { getErrorMessage } from '../../../lib/api'

function LoginForm() {
  const { login } = useAuth()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      await login({ email, password })
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <p className="text-teal-300 text-xs font-semibold tracking-[2px] uppercase mb-3">
        Welcome back
      </p>

      <h1 className="text-3xl font-bold text-white">Sign in</h1>

      <p className="text-sm text-slate-400 mt-2 mb-8">
        Access your personal astronaut health dashboard.
      </p>

      {error && (
        <div className="mb-5 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm text-slate-300 mb-2">
            Email address
          </label>

          <input
            type="email"
            required
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="w-full rounded-lg border border-[#26364a] bg-[#111e30] px-4 py-3 text-sm text-white outline-none focus:border-teal-400"
          />
        </div>

        <div>
          <label className="block text-sm text-slate-300 mb-2">
            Password
          </label>

          <div className="relative">
            <input
              type={showPassword ? 'text' : 'password'}
              required
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              className="w-full rounded-lg border border-[#26364a] bg-[#111e30] px-4 py-3 pr-12 text-sm text-white outline-none focus:border-teal-400"
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-teal-300"
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full flex justify-center items-center gap-2 rounded-lg bg-teal-500 hover:bg-teal-400 disabled:opacity-60 py-3 text-sm font-semibold text-[#06121b] transition-colors"
        >
          {submitting && <LoaderCircle size={17} className="animate-spin" />}
          {submitting ? 'Signing in...' : 'Sign in'}
        </button>
      </form>

      <p className="text-sm text-center text-slate-400 mt-7">
        Don't have an account?{' '}
        <Link to="/signup" className="text-teal-300 hover:text-teal-200 font-medium">
          Create account
        </Link>
      </p>
    </div>
  )
}

export default LoginForm