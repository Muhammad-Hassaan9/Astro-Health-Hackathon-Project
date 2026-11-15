import { useCallback, useEffect, useState } from 'react'
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts'
import { getHealthMetrics } from '../../services/metricService'
import { getHealthObservations } from '../../services/observationService'

function HealthTrendChart() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  const loadChart = useCallback(async () => {
    try {
      const [metricResponse, observationResponse] = await Promise.all([
        getHealthMetrics(),
        getHealthObservations({ limit: 100 }),
      ])

      const metrics = Array.isArray(metricResponse)
        ? metricResponse
        : metricResponse?.items || []

      const observations = Array.isArray(observationResponse)
        ? observationResponse
        : observationResponse?.items || observationResponse?.observations || []

      const heartMetric = metrics.find((metric) => {
        const code = String(metric.code || '').toUpperCase()
        const name = String(metric.name || '').toUpperCase()

        return code === 'HEART_RATE' || name === 'HEART RATE'
      })

      if (!heartMetric) {
        setData([])
        return
      }

      const readings = observations
        .filter((item) =>
          String(item.metric_id) === String(heartMetric.id) &&
          item.numeric_value !== null &&
          item.numeric_value !== undefined
        )
        .sort((a, b) =>
          new Date(a.observed_at || a.recorded_at) -
          new Date(b.observed_at || b.recorded_at)
        )
        .slice(-20)

      setData(readings.map((item) => ({
        time: new Date(item.observed_at || item.recorded_at).toLocaleTimeString(
          [],
          { hour: '2-digit', minute: '2-digit' }
        ),
        heartRate: Number(item.numeric_value),
      })))
    } catch (error) {
      console.error('Chart loading error:', error)
      setData([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadChart()

    window.addEventListener('astrohealth:health-update', loadChart)
    window.addEventListener('astrohealth:refresh-data', loadChart)

    return () => {
      window.removeEventListener('astrohealth:health-update', loadChart)
      window.removeEventListener('astrohealth:refresh-data', loadChart)
    }
  }, [loadChart])

  return (
    <section className="panel p-5 min-w-0">
      <div className="flex flex-wrap items-start justify-between gap-3 mb-6">
        <div>
          <h2 className="text-sm font-semibold text-white">
            Heart Rate Trends
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Historical recorded readings
          </p>
        </div>

        <span className="text-[10px] text-teal-300 bg-teal-400/10 border border-teal-400/20 rounded-md px-2.5 py-1.5">
          SIMULATED DATA
        </span>
      </div>

      <div className="h-[250px] w-full">
        {loading ? (
          <div className="h-full flex items-center justify-center text-xs text-slate-500">
            Loading chart...
          </div>
        ) : data.length === 0 ? (
          <div className="h-full flex items-center justify-center text-xs text-slate-500">
            No heart rate readings available. Generate a simulated reading.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={data}
              margin={{ top: 5, right: 8, left: -22, bottom: 0 }}
            >
              <defs>
                <linearGradient id="heartRateFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#2dd4bf" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#2dd4bf" stopOpacity={0} />
                </linearGradient>
              </defs>

              <CartesianGrid
                stroke="#243448"
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="time"
                tick={{ fill: '#718096', fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />

              <YAxis
                domain={['auto', 'auto']}
                tick={{ fill: '#718096', fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />

              <Tooltip
                contentStyle={{
                  background: '#101e30',
                  border: '1px solid #294054',
                  borderRadius: '9px',
                  color: '#e5edf7',
                  fontSize: '12px',
                }}
                formatter={(value) => [`${value} bpm`, 'Heart rate']}
              />

              <Area
                type="monotone"
                dataKey="heartRate"
                stroke="#2dd4bf"
                strokeWidth={2.5}
                fill="url(#heartRateFill)"
                activeDot={{
                  r: 5,
                  fill: '#2dd4bf',
                  stroke: '#0b1524',
                  strokeWidth: 2,
                }}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </section>
  )
}

export default HealthTrendChart