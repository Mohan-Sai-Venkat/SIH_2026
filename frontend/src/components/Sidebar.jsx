import {
  LayoutDashboard,
  BrainCircuit,
  Wrench,
  Route,
  CalendarDays,
  CalendarRange,
  Lightbulb,
  BarChart3,
  X,
} from "lucide-react";

const menuItems = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "AI Block Planner",
    icon: BrainCircuit,
  },
  {
    name: "Maintenance",
    icon: Wrench,
  },
  {
    name: "Corridors",
    icon: Route,
  },
  {
    name: "Weekly Plan",
    icon: CalendarDays,
  },
  {
    name: "Monthly Plan",
    icon: CalendarRange,
  },
  {
    name: "AI Insights",
    icon: Lightbulb,
  },
  {
    name: "Analytics",
    icon: BarChart3,
  },
];

export default function Sidebar({
  activePage,
  setActivePage,
  isOpen,
  setIsOpen,
}) {
  const handleClick = (page) => {
    setActivePage(page);
    setIsOpen(false);
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      <aside
        className={`fixed left-0 top-0 z-50 flex h-screen w-64 flex-col bg-slate-900 text-white transition-transform duration-300 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } lg:translate-x-0`}
      >
        {/* Logo */}
        <div className="flex h-20 items-center justify-between border-b border-slate-700 px-5">
          <div>
            <h1 className="text-lg font-bold">RailOps AI</h1>
            <p className="text-xs text-slate-400">
              Maintenance Control Center
            </p>
          </div>

          <button
            onClick={() => setIsOpen(false)}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white lg:hidden"
          >
            <X size={20} />
          </button>
        </div>

        {/* Operations */}
        <div className="px-4 py-5">
          <p className="mb-3 px-2 text-xs font-semibold uppercase tracking-wider text-slate-500">
            Operations
          </p>

          <nav className="space-y-1">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const active = activePage === item.name;

              return (
                <button
                  key={item.name}
                  onClick={() => handleClick(item.name)}
                  className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-medium transition ${
                    active
                      ? "bg-blue-600 text-white shadow-lg shadow-blue-900/30"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }`}
                >
                  <Icon size={19} strokeWidth={2} />

                  <span>{item.name}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* System Status */}
        <div className="mt-auto border-t border-slate-700 p-4">
          <div className="rounded-xl bg-slate-800 p-4">
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />

              <span className="text-sm font-semibold">
                SYSTEM STATUS
              </span>
            </div>

            <p className="mt-2 text-xs text-slate-400">
              All systems operational
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}