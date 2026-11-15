import { useCallback, useEffect, useState } from 'react'
import MetricCard from '../../../components/MetricCard'
import { getHealthMetrics } from '../../../services/metricService'
import { getHealthObservations } from '../../../services/observationService'

const metricDefinitions = [
  {
    key: 'heart_rate',
    label: 'Heart Rate',
    aliases: ['HEART_RATE', 'HEART RATE'],
    unit: 'bpm',
    description: 'Latest recorded reading',
  },
  {
    key: 'spo2',
    label: 'Blood Oxygen',
    aliases: ['SPO2', 'OXYGEN', 'BLOOD_OXYGEN', 'BLOOD OXYGEN'],
    unit: '%',
    description: 'Latest recorded reading',
  },
  {
    key: 'body_temperature',
    label: 'Body Temperature',
    aliases: ['BODY_TEMPERATURE', 'BODY TEMPERATURE', 'TEMPERATURE'],
    unit: '°C',
    description: 'Latest recorded reading',
  },
  {
    key: 'physical_activity',
    label: 'Physical Activity',
    aliases: ['ACTIVITY_DURATION', 'PHYSICAL_ACTIVITY', 'PHYSICAL ACTIVITY', 'ACTIVITY'],
    unit: 'min',
    description: 'Recorded activity duration',
  },
  {
    key: 'sleep_duration',
    label: 'Sleep Duration',
    aliases: ['SLEEP_DURATION', 'SLEEP DURATION', 'SLEEP'],
    unit: 'hrs',
    description: 'Recorded sleep duration',
  },
]

function getArray(data) {
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.items)) return data.items
  if (Array.isArray(data?.results)) return data.results
  if (Array.isArray(data?.observations)) return data.observations
  if (Array.isArray(data?.metrics)) return data.metrics
  return []
}

function MetricGrid() {
  const [metrics, setMetrics] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadMetrics = useCallback(async () => {
    try {
      setError('')

      const [metricResponse, observationResponse] = await Promise.all([
        getHealthMetrics(),
        getHealthObservations({ limit: 100 }),
      ])

      const availableMetrics = getArray(metricResponse)
      const observations = getArray(observationResponse)

      const formatted = metricDefinitions.map((definition) => {
        const matchedMetric = availableMetrics.find((metric) => {
          const code = String(metric.code || '').toUpperCase()
          const name = String(metric.name || '').toUpperCase()

          return definition.aliases.includes(code) ||
            definition.aliases.includes(name)
        })

        const matchingObservations = observations
          .filter((observation) => {
            if (!matchedMetric) return false

            return String(observation.metric_id) === String(matchedMetric.id)
          })
          .sort((a, b) => {
            return new Date(b.observed_at || b.recorded_at || 0) -
              new Date(a.observed_at || a.recorded_at || 0)
          })

        const latest = matchingObservations[0]
        const value = latest?.numeric_value ?? latest?.text_value ?? null

        return {
          ...definition,
          value: value === null ? '--' : Number.isFinite(Number(value))
            ? Number(value).toFixed(definition.key === 'body_temperature' || definition.key === 'sleep_duration' ? 1 : 0)
            : String(value),
          unit: latest?.unit || matchedMetric?.unit || definition.unit,
          description: latest
            ? 'Latest recorded reading'
            : 'No reading available yet',
        }
      })

      setMetrics(formatted)
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Unable to load health metrics.'
      )
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadMetrics()

    const handleUpdate = () => loadMetrics()

    window.addEventListener('astrohealth:health-update', handleUpdate)
    window.addEventListener('astrohealth:refresh-data', handleUpdate)

    return () => {
      window.removeEventListener('astrohealth:health-update', handleUpdate)
      window.removeEventListener('astrohealth:refresh-data', handleUpdate)
    }
  }, [loadMetrics])

  return (
    <section>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-base font-semibold text-white">Health Metrics</h2>
          <p className="text-xs text-slate-500 mt-1">
            Your latest health indicators
          </p>
        </div>
        <span className="text-[10px] text-slate-500">5 tracked metrics</span>
      </div>

      {loading ? (
        <p className="text-sm text-slate-400 py-8 text-center">
          Loading health readings...
        </p>
      ) : (
        <>
          {error && (
            <p className="text-xs text-rose-300 mb-3">{error}</p>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-3">
            {metrics.map((metric) => (
              <MetricCard key={metric.key} metric={metric} />
            ))}
          </div>
        </>
      )}
    </section>
  )
}

export default MetricGrid