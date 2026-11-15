import { useEffect, useState } from 'react'
import { Activity, CalendarDays } from 'lucide-react'
import { getAstronautProfile } from '../../../services/astronautService'

function WelcomeSection() {
  const [profile, setProfile] = useState(null)

  useEffect(() => {
    let active = true

    getAstronautProfile()
      .then((data) => {
        if (active) setProfile(data)
      })
      .catch((error) => {
        if (error.response?.status !== 404) {
          console.error('Profile loading failed:', error)
        }
      })

    return () => {
      active = false
    }
  }, [])

  return (
    <section className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <p className="text-xs text-teal-300 font-medium tracking-wide mb-2">
          PERSONAL HEALTH OVERVIEW
        </p>

        <h1 className="text-2xl sm:text-[28px] font-semibold text-white tracking-tight">
          Welcome back{profile?.display_name
            ? `, ${profile.display_name}`
            : ''}
        </h1>

        <p className="text-sm text-slate-400 mt-2">
          Here's a snapshot of your health and wellness data.
        </p>

        {profile?.mission_name && (
          <p className="text-xs text-slate-500 mt-2">
            Mission: {profile.mission_name}
            {profile.mission_role ? ` · ${profile.mission_role}` : ''}
          </p>
        )}
      </div>

      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 bg-[#111e30] border border-[#26384b] rounded-lg px-3 py-2.5">
          <CalendarDays size={15} className="text-teal-300" />
          <span className="text-xs text-slate-300">
            {new Date().toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric',
              year: 'numeric',
            })}
          </span>
        </div>

        <div className="flex items-center gap-2 bg-amber-400/10 border border-amber-400/20 rounded-lg px-3 py-2.5">
          <Activity size={14} className="text-amber-300" />
          <span className="text-xs text-amber-200">Simulated data</span>
        </div>
      </div>
    </section>
  )
}

export default WelcomeSection