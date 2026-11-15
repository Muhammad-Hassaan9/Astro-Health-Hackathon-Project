import { Bell, Search, Menu } from 'lucide-react'

function Header({ onMenuClick, connected }) {
  return (
    <header className="sticky top-0 z-30 w-full border-b border-white/10 bg-[#080f1d]/90 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between gap-3 px-4 sm:px-6 lg:px-8">
        {/* Left side */}
        <div className="flex min-w-0 items-center gap-3">
          <button
            type="button"
            onClick={onMenuClick}
            className="rounded-lg p-2 text-slate-400 transition hover:bg-white/5 hover:text-white lg:hidden"
            aria-label="Open navigation menu"
          >
            <Menu size={21} />
          </button>

          <div className="min-w-0">
            <h1 className="truncate text-sm font-semibold text-white sm:text-base">
              AstroHealth
            </h1>
            <p className="hidden text-xs text-slate-500 sm:block">
              Astronaut Health Monitoring
            </p>
          </div>
        </div>

        {/* Right side controls */}
        <div className="flex items-center gap-2 sm:gap-4 shrink-0">
          {/* WebSocket connection status */}
          <div className="hidden sm:flex items-center gap-2 text-[10px]">
            <span
              className={`w-2 h-2 rounded-full ${
                connected ? 'bg-emerald-400' : 'bg-amber-400'
              }`}
            />
            <span className="text-slate-400">
              {connected ? 'Live connection' : 'Connecting...'}
            </span>
          </div>

          {/* Search */}
          <button
            type="button"
            className="rounded-lg p-2 text-slate-400 transition hover:bg-white/5 hover:text-white"
            aria-label="Search"
          >
            <Search size={19} />
          </button>

          {/* Notifications */}
          <button
            type="button"
            className="relative rounded-lg p-2 text-slate-400 transition hover:bg-white/5 hover:text-white"
            aria-label="Notifications"
          >
            <Bell size={19} />
            <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-cyan-400" />
          </button>

          {/* User avatar */}
          <div className="flex h-9 w-9 items-center justify-center rounded-full border border-cyan-400/20 bg-cyan-400/10 text-xs font-semibold text-cyan-300">
            A
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header