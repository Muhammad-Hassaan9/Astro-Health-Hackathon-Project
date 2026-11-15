import MetricGrid from '../features/health-metrics/components/MetricGrid'
import HealthTrendChart from '../components/charts/HealthTrendChart'

function HealthMonitoring() {
  return (
    <div className="max-w-[1400px] mx-auto space-y-6">
      <div>
        <p className="text-xs text-teal-300 mb-2">HEALTH DATA</p>
        <h1 className="text-2xl font-semibold text-white">Health Monitoring</h1>
        <p className="text-sm text-slate-400 mt-2">
          Monitor your recorded health indicators and trends.
        </p>
      </div>
      <MetricGrid />
      <HealthTrendChart />
    </div>
  )
}

export default HealthMonitoring