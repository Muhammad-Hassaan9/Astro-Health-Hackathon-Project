
import Sidebar from './Sidebar'
import Header from './Header'
import Dashboard from '../pages/Dashboard'

function DashboardLayout() {
  return (
    <div className="min-h-screen bg-[#080d1a] text-white flex">
      <Sidebar />

      <div className="flex-1 min-w-0">
        <Header />

        <main className="p-6">
          <Dashboard />
        </main>
      </div>
    </div>
  )
}

export default DashboardLayout
