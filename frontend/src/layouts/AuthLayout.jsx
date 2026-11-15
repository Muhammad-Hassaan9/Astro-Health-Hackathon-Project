import { Orbit } from 'lucide-react'
import { Link, Outlet } from 'react-router-dom'

function AuthLayout() {
  return (
    <div className="min-h-screen bg-[#080f1d] text-white flex">
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-[#0b1524] border-r border-[#1c2b3d] flex-col justify-between p-12">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-teal-500/15 border border-teal-400/20 flex items-center justify-center">
            <Orbit size={25} className="text-teal-300" />
          </div>
          <span className="text-xl font-bold tracking-wide">AstroHealth</span>
        </div>

        <div className="relative z-10 max-w-lg">
          <p className="text-teal-300 text-xs tracking-[3px] uppercase mb-5">
            Astronaut wellness platform
          </p>

          <h1 className="text-5xl font-semibold leading-tight">
            Your health.
            <br />
            Your mission.
            <br />
            <span className="text-teal-300">Our priority.</span>
          </h1>

          <p className="text-slate-400 mt-6 leading-7">
            Monitor health indicators, review alerts and access
            AI-powered wellness guidance through your personal
            astronaut dashboard.
          </p>
        </div>

        <p className="text-xs text-slate-600">
          AstroHealth · Astronaut Health Monitoring Prototype
        </p>

        <div className="absolute w-96 h-96 rounded-full border border-teal-400/10 -right-32 top-1/4" />
        <div className="absolute w-72 h-72 rounded-full border border-teal-400/10 -right-20 top-[30%]" />
      </div>

      <div className="flex-1 flex flex-col min-h-screen">
        <div className="lg:hidden flex items-center gap-3 p-6">
          <Orbit className="text-teal-300" size={26} />
          <span className="font-bold text-lg">AstroHealth</span>
        </div>

        <main className="flex-1 flex items-center justify-center p-5 sm:p-8">
          <div className="w-full max-w-md">
            <Outlet />
          </div>
        </main>

        <footer className="text-center text-xs text-slate-600 p-5">
          AstroHealth · Prototype project
        </footer>
      </div>
    </div>
  )
}

export default AuthLayout