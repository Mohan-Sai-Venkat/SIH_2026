import { useState } from "react";

import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import BlockPlanner from "./pages/BlockPlanner";
import Maintenance from "./pages/Maintenance";
import Corridors from "./pages/Corridors";
import WeeklyPlan from "./pages/WeeklyPlan";
import MonthlyPlan from "./pages/MonthlyPlan";
import AIInsights from "./pages/AIInsights";
import Analytics from "./pages/Analytics";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const renderPage = () => {
    switch (activePage) {
      case "Dashboard":
        return <Dashboard setActivePage={setActivePage} />;

      case "AI Block Planner":
        return <BlockPlanner />;

      case "Maintenance":
        return <Maintenance />;

      case "Corridors":
        return <Corridors />;

      case "Weekly Plan":
        return <WeeklyPlan />;

      case "Monthly Plan":
        return <MonthlyPlan />;

      case "AI Insights":
        return <AIInsights />;

      case "Analytics":
        return <Analytics />;

      default:
        return <Dashboard setActivePage={setActivePage} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
        isOpen={isSidebarOpen}
        setIsOpen={setIsSidebarOpen}
      />

      <div className="lg:ml-64">
        <Navbar
          activePage={activePage}
          setIsSidebarOpen={setIsSidebarOpen}
        />

        <main className="p-4 sm:p-6 lg:p-8">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}

export default App;