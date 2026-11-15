import { useEffect, useState } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import Dashboard from '../pages/Dashboard'
import HealthMonitoring from '../pages/HealthMonitoring'
import Alerts from '../pages/Alerts'
import AIAssistant from '../pages/AIAssistant'
import Profile from '../pages/Profile'
import useWebSocket from '../hooks/useWebSocket'

function DashboardLayout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { connected } = useWebSocket(true)

  const navigate = useNavigate()
  const location = useLocation()

  const currentPage = location.pathname.split('/')[2] || 'overview'

  const pageMap = {
    overview: <Dashboard />,
    health: <HealthMonitoring />,
    alerts: <Alerts />,
    ai: <AIAssistant />,
    profile: <Profile />,
  }

  function handleNavigate(page) {
    navigate(`/app/${page}`)
    setMobileMenuOpen(false)
  }

  useEffect(() => {
    const handleCustomNavigation = (event) => {
      if (event.detail) handleNavigate(event.detail)
    }

    window.addEventListener('astrohealth:navigate', handleCustomNavigation)

    return () => {
      window.removeEventListener('astrohealth:navigate', handleCustomNavigation)
    }
  }, [])

  if (!pageMap[currentPage]) {
    return <Navigate to="/app/overview" replace />
  }

  return (
    <div className="min-h-screen w-full overflow-x-hidden bg-[#080f1d] text-white flex">
      <Sidebar
        activePage={currentPage}
        onNavigate={handleNavigate}
      />

      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 md:hidden">
          <button
            aria-label="Close navigation"
            onClick={() => setMobileMenuOpen(false)}
            className="absolute inset-0 w-full h-full bg-black/65"
          />

          <div className="relative z-10 h-full w-[280px] max-w-[85vw]">
            <Sidebar
              mobile
              activePage={currentPage}
              onNavigate={handleNavigate}
              onClose={() => setMobileMenuOpen(false)}
            />
          </div>
        </div>
      )}

      <div className="flex-1 min-w-0">
        <Header
          onMenuClick={() => setMobileMenuOpen(true)}
          connected={connected}
        />

        <main className="dashboard-main w-full min-w-0 p-4 sm:p-5 lg:p-8">
          {pageMap[currentPage]}
        </main>
      </div>
    </div>
  )
}

export default DashboardLayout