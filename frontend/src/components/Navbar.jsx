import { Bell, Menu, UserCircle } from "lucide-react";

function Navbar({ activePage, setIsSidebarOpen }) {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div className="flex h-20 items-center justify-between px-4 sm:px-6">

        {/* LEFT */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsSidebarOpen(true)}
            className="rounded-lg p-2 text-slate-600 transition hover:bg-slate-100 lg:hidden"
          >
            <Menu size={24} />
          </button>

          <div>
            <p className="text-xs text-slate-400">
              RailOps AI • Control Room
            </p>

            <h2 className="text-sm font-bold text-slate-800 sm:text-base">
              {activePage}
            </h2>
          </div>
        </div>

        {/* RIGHT */}
        <div className="flex items-center gap-2 sm:gap-4">

          {/* SYSTEM STATUS */}
          <div className="hidden items-center gap-2 rounded-full bg-amber-50 px-3 py-2 sm:flex">
  <span className="h-2 w-2 rounded-full bg-amber-500" />

  <span className="text-xs font-semibold text-amber-700">
    Demo Mode
  </span>
</div>

          {/* NOTIFICATION */}
          <button
            className="relative rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 hover:text-slate-800"
            title="Notifications"
          >
            <Bell size={20} />

            <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-red-500" />
          </button>

          {/* USER */}
          <div className="flex items-center gap-2 border-l border-slate-200 pl-3">
            <div className="hidden text-right sm:block">
              <p className="text-sm font-semibold text-slate-800">
                Control Room
              </p>

              <p className="text-xs text-slate-400">
                Operations Division
              </p>
            </div>

            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-600 text-white">
              <UserCircle size={21} />
            </div>
          </div>

        </div>
      </div>
    </header>
  );
}

export default Navbar;