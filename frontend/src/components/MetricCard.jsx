import {
  Activity,
  HeartPulse,
  Droplets,
  Thermometer,
  Moon,
} from 'lucide-react'

const iconMap = {
  heart_rate: HeartPulse,
  spo2: Droplets,
  body_temperature: Thermometer,
  physical_activity: Activity,
  sleep_duration: Moon,
}

function MetricCard({ metric }) {
  const Icon = iconMap[metric.key] || Activity
  const hasValue = metric.value !== '--'

  return (
    <div className="panel metric-card p-4 sm:p-5 min-w-0">
      <div className="flex items-center justify-between">
        <div className="w-10 h-10 rounded-xl bg-teal-400/10 flex items-center justify-center">
          <Icon size={19} className="text-teal-300" />
        </div>

        <span className="text-[10px] text-teal-300 bg-teal-400/10 border border-teal-400/15 px-2 py-1 rounded-full">
          SIMULATED
        </span>
      </div>

      <p className="text-xs text-slate-400 mt-4">{metric.label}</p>

      <div className="flex items-baseline gap-1.5 mt-1">
        <span className="text-[26px] font-semibold tracking-tight text-white">
          {metric.value}
        </span>
        <span className="text-xs text-slate-500">{metric.unit}</span>
      </div>

      <p className="text-[11px] text-slate-500 mt-2">
        {hasValue ? metric.description : 'No recorded data'}
      </p>
    </div>
  )
}

export default MetricCard