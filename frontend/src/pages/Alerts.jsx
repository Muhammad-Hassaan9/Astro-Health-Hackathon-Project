import AlertList from '../features/alerts/components/AlertList'

function Alerts() {
  return (
    <div className="max-w-[1200px] mx-auto space-y-6">
      <div>
        <p className="text-xs text-teal-300 tracking-wide mb-2">
          NOTIFICATIONS CENTER
        </p>
        <h1 className="text-2xl font-semibold text-white">
          Health Alerts
        </h1>
        <p className="text-sm text-slate-400 mt-2">
          Review, acknowledge and resolve your health monitoring alerts.
        </p>
      </div>

      <AlertList showAll />
    </div>
  )
}

export default Alerts