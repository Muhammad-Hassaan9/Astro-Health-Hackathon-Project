import {
  Activity,
  LayoutDashboard,
  HeartPulse,
  Bell,
  UserRound,
  Orbit,
  PanelLeftClose,
  PanelLeftOpen,
  X,
  Bot,
} from 'lucide-react'
import { useState } from 'react'

const navigation = [
  { label: 'Overview', icon: LayoutDashboard, path: 'overview' },
  { label: 'Health Monitoring', icon: HeartPulse, path: 'health' },
  { label: 'Alerts', icon: Bell, path: 'alerts' },
  { label: 'AI Assistant', icon: Bot, path: 'ai' },
  { label: 'My Profile', icon: UserRound, path: 'profile' },
]

function Sidebar({ activePage, onNavigate, mobile = false, onClose }) {
  const [collapsed, setCollapsed] = useState(false)
  const isCollapsed = mobile ? false : collapsed

  return (
    <aside
      className={`${
        mobile
          ? 'flex w-[280px] max-w-[85vw] h-full'
          : `${collapsed ? 'w-[76px]' : 'w-[250px]'} hidden md:flex min-h-screen`
      } flex-col shrink-0 bg-[#0b1524] border-r border-[#1c2b3d] transition-all duration-300`}
    >
      {/* Sidebar Header */}
      <div
        className={`h-[76px] min-h-[76px] px-4 flex items-center ${
          isCollapsed ? 'justify-center' : 'justify-between'
        } gap-3 border-b border-[#1c2b3d]`}
      >
        {/* Logo and Brand */}
        <div
          className={`flex items-center ${
            isCollapsed ? 'justify-center' : 'gap-3'
          } min-w-0`}
        >
          <div
            className={`relative w-10 h-10 shrink-0 rounded-xl bg-teal-500/15 border border-teal-400/20 flex items-center justify-center ${
              isCollapsed ? 'group' : ''
            }`}
          >
            <Orbit
              size={23}
              className={`text-teal-300 transition-opacity ${
                isCollapsed ? 'group-hover:opacity-0' : ''
              }`}
            />

            {/* Hover Toggle in Collapsed State */}
            {isCollapsed && (
              <button
                    onClick={() => setCollapsed(false)}
                    aria-label="Expand sidebar"
                    className="absolute inset-0 flex items-center justify-center rounded-xl text-teal-300 opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 hover:bg-teal-400/10 transition-opacity"
                >
                    <PanelLeftOpen size={21} />
                    <span className="pointer-events-none absolute left-full top-1/2 z-50 ml-3 whitespace-nowrap -translate-y-1/2 rounded-md border border-[#2b4055] bg-[#17283a] px-3 py-2 text-xs text-white opacity-0 group-hover:opacity-100 shadow-xl">
                        Expand sidebar
                    </span>
                </button>
            )}
          </div>

          {!isCollapsed && (
            <div className="min-w-0">
              <h1 className="font-bold text-[17px] tracking-wide text-white">
                AstroHealth
              </h1>
              <p className="text-[10px] tracking-[2px] text-slate-500 uppercase">
                Astronaut wellness
              </p>
            </div>
          )}
        </div>

        {/* Expanded Desktop Toggle */}
        {!mobile && !isCollapsed && (
          <button
                onClick={() => setCollapsed(true)}
                aria-label="Collapse sidebar"
                className="group relative shrink-0 p-2 rounded-lg text-slate-400 hover:text-teal-300 hover:bg-[#17283a] transition-colors"
            >
                <PanelLeftClose size={19} />
                <span className="pointer-events-none absolute right-0 top-full z-50 mt-2 whitespace-nowrap rounded-md border border-[#2b4055] bg-[#17283a] px-3 py-2 text-xs text-white opacity-0 group-hover:opacity-100 shadow-xl">
                    Collapse sidebar
                </span>
            </button>
        )}

        {/* Mobile Close */}
        {mobile && (
          <button
            onClick={onClose}
            aria-label="Close sidebar"
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-[#17283a]"
          >
            <X size={19} />
          </button>
        )}
      </div>

      {/* Navigation */}
      <div className="px-3 pt-8">
        {!isCollapsed && (
          <p className="text-[10px] font-semibold tracking-[1.8px] text-slate-500 uppercase px-3 mb-3">
            Workspace
          </p>
        )}

        <nav className="space-y-1">
          {navigation.map(({ label, icon: Icon, path }) => (
            <button
              key={path}
              onClick={() => {
                onNavigate(path)
                if (mobile) onClose()
              }}
              aria-label={label}
              className={`nav-item ${
                activePage === path ? 'active' : 'text-slate-400'
              } group relative w-full flex items-center ${
                isCollapsed ? 'justify-center' : 'gap-3'
              } px-3 py-3 rounded-lg text-sm text-left`}
            >
              <Icon size={19} className="shrink-0" />

              {!isCollapsed && <span>{label}</span>}

              {/* Single Custom Tooltip */}
              {isCollapsed && (
                <span
                  role="tooltip"
                  className="pointer-events-none absolute left-full top-1/2 z-50 ml-3 -translate-y-1/2 whitespace-nowrap rounded-md border border-[#2b4055] bg-[#17283a] px-3 py-2 text-xs text-white opacity-0 shadow-xl transition-opacity duration-150 group-hover:opacity-100 group-focus-visible:opacity-100"
                >
                  {label}
                </span>
              )}
            </button>
          ))}
        </nav>
      </div>

      {/* System Status */}
      {!mobile && !isCollapsed && (
        <div className="mt-auto p-3">
          <div className="bg-[#112638] border border-[#1e4050] rounded-xl p-3">
            <div className="flex items-center gap-2 mb-2">
              <Activity size={15} className="text-teal-300" />
              <span className="text-xs font-medium text-teal-200">
                System status
              </span>
            </div>

            <p className="text-[11px] text-slate-400">
              Dashboard prototype active
            </p>

            <div className="flex items-center gap-2 mt-3">
              <span className="w-2 h-2 rounded-full bg-amber-400" />
              <span className="text-[10px] text-slate-400">
                Simulated data mode
              </span>
            </div>
          </div>
        </div>
      )}
    </aside>
  )
}

export default Sidebar