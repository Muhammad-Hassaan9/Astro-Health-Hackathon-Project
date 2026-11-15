import { useState } from 'react'
import WelcomeSection from '../features/dashboard/components/WelcomeSection'
import MetricGrid from '../features/health-metrics/components/MetricGrid'
import HealthTrendChart from '../components/charts/HealthTrendChart'
import AlertList from '../features/alerts/components/AlertList'
import { Activity, ShieldCheck, RefreshCw } from 'lucide-react'
import { simulateHealthReading } from '../services/observationService'
import { getErrorMessage } from '../lib/api'

function Dashboard() {
  const [generating, setGenerating] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  async function handleGenerateReading() {
    try {
      setGenerating(true)
      setMessage('')
      setError('')

      await simulateHealthReading()

      setMessage('New simulated health reading generated successfully.')

      window.dispatchEvent(new Event('astrohealth:refresh-data'))
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="max-w-[1500px] mx-auto space-y-7">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <p className="text-xs text-teal-300 mb-1">
            LIVE HEALTH MONITORING
          </p>
          <h1 className="text-xl sm:text-2xl font-semibold text-white">
            Astronaut Dashboard
          </h1>
        </div>

        <button
          onClick={handleGenerateReading}
          disabled={generating}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-teal-500 px-4 py-2.5 text-sm font-medium text-[#06131b] hover:bg-teal-400 disabled:opacity-60 disabled:cursor-not-allowed transition"
        >
          <RefreshCw
            size={16}
            className={generating ? 'animate-spin' : ''}
          />
          {generating ? 'Generating...' : 'Generate Simulated Reading'}
        </button>
      </div>

      {message && (
        <p className="text-xs text-emerald-300">{message}</p>
      )}

      {error && (
        <p className="text-xs text-rose-300">{error}</p>
      )}

      <WelcomeSection />

      <MetricGrid />

      <div className="grid grid-cols-1 xl:grid-cols-[1.65fr_1fr] gap-4">
        <HealthTrendChart />
        <AlertList />
      </div>

      <div className="panel p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-teal-400/10 flex items-center justify-center">
            <ShieldCheck size={18} className="text-teal-300" />
          </div>

          <div>
            <p className="text-xs font-medium text-slate-200">
              AstroHealth monitoring prototype
            </p>
            <p className="text-[11px] text-slate-500 mt-1">
              Health information dashboard · Simulated data environment
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-[11px] text-slate-400">
          <Activity size={14} className="text-teal-300" />
          Personal monitoring
        </div>
      </div>
    </div>
  )
}

export default Dashboard