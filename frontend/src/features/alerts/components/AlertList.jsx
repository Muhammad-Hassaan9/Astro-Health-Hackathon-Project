import { useCallback, useEffect, useState } from 'react'
import {
  AlertTriangle,
  Info,
  ShieldAlert,
  ChevronRight,
  CheckCircle2,
  Clock,
} from 'lucide-react'
import {
  getAlerts,
  updateAlertStatus,
} from '../../../services/alertService'

const severityStyles = {
  WARNING: 'text-amber-300 bg-amber-400/10 border-amber-400/20',
  CRITICAL: 'text-rose-300 bg-rose-400/10 border-rose-400/20',
  INFO: 'text-sky-300 bg-sky-400/10 border-sky-400/20',
}

function getItems(response) {
  if (Array.isArray(response)) return response
  return response?.items || response?.alerts || response?.results || []
}

function AlertList({ showAll = false }) {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [updatingId, setUpdatingId] = useState(null)

  const loadAlerts = useCallback(async () => {
    try {
      setError('')
      const response = await getAlerts({ limit: 100 })
      setAlerts(getItems(response))
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Unable to load alerts.'
      )
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadAlerts()

    const handleNewAlert = (event) => {
      if (event.detail) {
        setAlerts((current) => [
          event.detail,
          ...current.filter((item) => item.id !== event.detail.id),
        ])
      } else {
        loadAlerts()
      }
    }

    window.addEventListener('astrohealth:new-alert', handleNewAlert)
    window.addEventListener('astrohealth:refresh-data', loadAlerts)

    return () => {
      window.removeEventListener('astrohealth:new-alert', handleNewAlert)
      window.removeEventListener('astrohealth:refresh-data', loadAlerts)
    }
  }, [loadAlerts])

  async function handleStatusChange(alertId, status) {
    try {
      setUpdatingId(alertId)
      const updated = await updateAlertStatus(alertId, status)

      setAlerts((current) =>
        current.map((alert) =>
          alert.id === alertId
            ? { ...alert, ...updated, status }
            : alert
        )
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Unable to update alert.'
      )
    } finally {
      setUpdatingId(null)
    }
  }

  const visibleAlerts = showAll ? alerts : alerts.slice(0, 4)

  return (
    <section className="panel p-5 min-w-0">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="text-sm font-semibold text-white">
            {showAll ? 'All Alerts' : 'Recent Alerts'}
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Health and system notifications
          </p>
        </div>

        {!showAll && (
          <button
            onClick={() => window.dispatchEvent(
              new CustomEvent('astrohealth:navigate', {
                detail: 'alerts',
              })
            )}
            className="text-xs text-teal-300 hover:text-teal-200 flex items-center gap-1"
          >
            View all <ChevronRight size={14} />
          </button>
        )}
      </div>

      {loading ? (
        <p className="text-xs text-slate-400 py-6 text-center">
          Loading alerts...
        </p>
      ) : error ? (
        <p className="text-xs text-rose-300 py-4">{error}</p>
      ) : visibleAlerts.length === 0 ? (
        <div className="py-8 text-center">
          <CheckCircle2 className="mx-auto text-emerald-400 mb-2" size={25} />
          <p className="text-sm text-slate-300">No alerts found</p>
          <p className="text-xs text-slate-500 mt-1">
            Your current monitoring alerts will appear here.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {visibleAlerts.map((alert) => {
            const severity = String(alert.severity || 'INFO').toUpperCase()
            const Icon = severity === 'CRITICAL'
              ? ShieldAlert
              : severity === 'WARNING'
                ? AlertTriangle
                : Info

            const style = severityStyles[severity] || severityStyles.INFO
            const status = String(alert.status || 'NEW').toUpperCase()

            return (
              <div
                key={alert.id}
                className="flex gap-3 p-3 rounded-lg bg-[#0c1726] border border-[#1d3044]"
              >
                <div className={`w-9 h-9 shrink-0 rounded-lg border flex items-center justify-center ${style}`}>
                  <Icon size={17} />
                </div>

                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <p className="text-xs font-medium text-slate-200">
                      {alert.title}
                    </p>
                    <span className={`text-[9px] px-1.5 py-0.5 rounded border ${style}`}>
                      {severity}
                    </span>
                  </div>

                  <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">
                    {alert.message}
                  </p>

                  {alert.recommended_action && (
                    <p className="text-[11px] text-teal-300 mt-2">
                      Action: {alert.recommended_action}
                    </p>
                  )}

                  <div className="flex flex-wrap items-center gap-2 mt-3">
                    <span className="text-[10px] text-slate-500 flex items-center gap-1">
                      <Clock size={11} />
                      {alert.created_at
                        ? new Date(alert.created_at).toLocaleString()
                        : 'Recent'}
                    </span>

                    <span className="text-[9px] text-slate-400 border border-slate-700 rounded px-1.5 py-0.5">
                      {status}
                    </span>
                  </div>

                  {status !== 'RESOLVED' && (
                    <div className="flex flex-wrap gap-2 mt-3">
                      {status === 'NEW' && (
                        <button
                          disabled={updatingId === alert.id}
                          onClick={() => handleStatusChange(alert.id, 'ACKNOWLEDGED')}
                          className="text-[10px] px-2.5 py-1.5 rounded-md border border-amber-400/20 text-amber-300 hover:bg-amber-400/10 disabled:opacity-50"
                        >
                          Acknowledge
                        </button>
                      )}

                      <button
                        disabled={updatingId === alert.id}
                        onClick={() => handleStatusChange(alert.id, 'RESOLVED')}
                        className="text-[10px] px-2.5 py-1.5 rounded-md border border-emerald-400/20 text-emerald-300 hover:bg-emerald-400/10 disabled:opacity-50"
                      >
                        Resolve
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </section>
  )
}

export default AlertList