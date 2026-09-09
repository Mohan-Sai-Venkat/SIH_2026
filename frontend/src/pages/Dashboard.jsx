import { useEffect, useState } from "react";
import api from "../services/api";

import {
  Activity,
  AlertTriangle,
  Clock3,
  TrainFront,
  Wrench,
  ArrowUpRight,
  ArrowDownRight,
  RefreshCw,
  BrainCircuit,
  ShieldCheck,
  Zap,
  ChevronRight,
} from "lucide-react";

const stats = [
  {
    title: "Active Blocks",
    value: "18",
    change: "+3 today",
    positive: true,
    icon: TrainFront,
    iconStyle: "bg-blue-50 text-blue-600",
  },
  {
    title: "Pending Maintenance",
    value: "47",
    change: "12 critical",
    positive: false,
    icon: Wrench,
    iconStyle: "bg-amber-50 text-amber-600",
  },
  {
    title: "Critical Defects",
    value: "08",
    change: "Requires attention",
    positive: false,
    icon: AlertTriangle,
    iconStyle: "bg-red-50 text-red-600",
  },
  {
    title: "Corridor Availability",
    value: "92%",
    change: "+4.2% this week",
    positive: true,
    icon: Activity,
    iconStyle: "bg-emerald-50 text-emerald-600",
  },
];

const maintenanceTasks = [
  {
    id: "MT-1042",
    asset: "Rail Track - KM 428/6",
    department: "Engineering",
    priority: "Critical",
    due: "Today",
  },
  {
    id: "MT-1038",
    asset: "Transformer - TSS 14",
    department: "Traction",
    priority: "High",
    due: "Tomorrow",
  },
  {
    id: "MT-1029",
    asset: "Signal Relay - BZA-22",
    department: "S&T",
    priority: "Medium",
    due: "12 Sep",
  },
  {
    id: "MT-1021",
    asset: "Overhead Equipment - KM 431",
    department: "Traction",
    priority: "High",
    due: "13 Sep",
  },
];

const utilization = [
  {
    name: "Engineering",
    value: 78,
    blocks: 14,
    style: "bg-blue-600",
  },
  {
    name: "Traction",
    value: 64,
    blocks: 11,
    style: "bg-indigo-500",
  },
  {
    name: "Signal & Telecom",
    value: 52,
    blocks: 9,
    style: "bg-purple-500",
  },
];

function Dashboard({ setActivePage }) {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [isRefreshing, setIsRefreshing] = useState(false);

  const checkBackend = async () => {
    try {
      setIsRefreshing(true);

      await api.get("/health");

      setBackendStatus("Connected");
    } catch (error) {
      setBackendStatus("Demo Mode");
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    checkBackend();
  }, []);

  const statusColor =
    backendStatus === "Connected"
      ? "bg-emerald-500"
      : backendStatus === "Demo Mode"
      ? "bg-amber-500"
      : "bg-blue-500";

  return (
    <div className="space-y-6">
      {/* ================= PAGE HEADER ================= */}
      <section>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2">
              <span className="relative flex h-2.5 w-2.5">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500"></span>
              </span>

              <span className="text-xs font-bold uppercase tracking-wider text-emerald-600">
                Live Operations
              </span>
            </div>

            <h1 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
              Railway Operations Dashboard
            </h1>

            <p className="mt-1 max-w-2xl text-sm leading-6 text-slate-500">
              AI-powered maintenance block coordination and infrastructure
              monitoring.
            </p>
          </div>

          {/* Backend status */}
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-2 shadow-sm">
              <span
                className={`h-2.5 w-2.5 rounded-full ${statusColor} ${
                  backendStatus === "Checking..." ? "animate-pulse" : ""
                }`}
              />

              <span className="text-xs font-semibold text-slate-600">
                Backend: {backendStatus}
              </span>
            </div>

            <button
              onClick={checkBackend}
              disabled={isRefreshing}
              className="rounded-lg border border-slate-200 bg-white p-2 text-slate-500 shadow-sm transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-600 disabled:cursor-not-allowed"
              title="Refresh backend status"
            >
              <RefreshCw
                size={16}
                className={isRefreshing ? "animate-spin" : ""}
              />
            </button>
          </div>
        </div>
      </section>

      {/* ================= KPI CARDS ================= */}
      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon;

          return (
            <div
              key={stat.title}
              className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition duration-200 hover:-translate-y-1 hover:border-slate-300 hover:shadow-lg"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-500">
                    {stat.title}
                  </p>

                  <h2 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
                    {stat.value}
                  </h2>
                </div>

                <div
                  className={`rounded-xl p-3 transition group-hover:scale-105 ${stat.iconStyle}`}
                >
                  <Icon size={21} />
                </div>
              </div>

              <div className="mt-4 flex items-center gap-1.5 text-xs font-medium">
                {stat.positive ? (
                  <ArrowUpRight
                    size={14}
                    className="text-emerald-500"
                  />
                ) : (
                  <ArrowDownRight
                    size={14}
                    className="text-amber-500"
                  />
                )}

                <span className="text-slate-500">{stat.change}</span>
              </div>
            </div>
          );
        })}
      </section>

      {/* ================= OPERATIONS OVERVIEW ================= */}
      <section className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        {/* BLOCK UTILIZATION */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm xl:col-span-2">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="flex items-center gap-2">
                <div className="rounded-lg bg-blue-50 p-2 text-blue-600">
                  <Activity size={18} />
                </div>

                <h2 className="font-bold text-slate-900">
                  Block Utilization
                </h2>
              </div>

              <p className="mt-1 text-sm text-slate-500">
                Current maintenance block allocation by department
              </p>
            </div>

            <button className="w-fit rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-600 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-600">
              This Week
            </button>
          </div>

          <div className="mt-7 space-y-6">
            {utilization.map((item) => (
              <div key={item.name}>
                <div className="mb-2 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-slate-700">
                      {item.name}
                    </span>

                    <span className="text-xs text-slate-400">
                      {item.blocks} blocks
                    </span>
                  </div>

                  <span className="text-sm font-bold text-slate-700">
                    {item.value}%
                  </span>
                </div>

                <div className="h-3 overflow-hidden rounded-full bg-slate-100">
                  <div
                    className={`h-full rounded-full ${item.style} transition-all duration-1000`}
                    style={{ width: `${item.value}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Utilization footer */}
          <div className="mt-7 grid grid-cols-2 gap-3 border-t border-slate-100 pt-5 sm:grid-cols-3">
            <div>
              <p className="text-xs text-slate-400">Total Blocks</p>
              <p className="mt-1 text-lg font-bold text-slate-800">34</p>
            </div>

            <div>
              <p className="text-xs text-slate-400">Avg. Utilization</p>
              <p className="mt-1 text-lg font-bold text-slate-800">65%</p>
            </div>

            <div className="col-span-2 sm:col-span-1">
              <p className="text-xs text-slate-400">AI Optimization</p>
              <p className="mt-1 text-lg font-bold text-emerald-600">
                +23%
              </p>
            </div>
          </div>
        </div>

        {/* AI RECOMMENDATION */}
        <div className="relative overflow-hidden rounded-2xl bg-slate-950 p-6 text-white shadow-lg">
          {/* Decorative background */}
          <div className="absolute -right-12 -top-12 h-40 w-40 rounded-full bg-blue-600/20 blur-3xl" />
          <div className="absolute -bottom-12 -left-12 h-40 w-40 rounded-full bg-indigo-600/20 blur-3xl" />

          <div className="relative">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="rounded-xl bg-blue-600 p-2.5 shadow-lg shadow-blue-900/40">
                  <BrainCircuit size={20} />
                </div>

                <div>
                  <h2 className="font-bold">AI Recommendation</h2>
                  <p className="text-xs text-slate-400">
                    Decision engine
                  </p>
                </div>
              </div>

              <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-emerald-400">
                94% Confidence
              </span>
            </div>

            <div className="mt-6">
              <p className="text-sm leading-6 text-slate-300">
                Combine{" "}
                <span className="font-bold text-white">
                  3 maintenance activities
                </span>{" "}
                in the{" "}
                <span className="font-bold text-white">
                  Vijayawada–Eluru
                </span>{" "}
                corridor during the same block window.
              </p>

              <div className="mt-5 grid grid-cols-2 gap-3">
                <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                  <div className="flex items-center gap-2 text-slate-400">
                    <Zap size={14} />
                    <span className="text-xs">Block Saving</span>
                  </div>

                  <p className="mt-2 text-xl font-bold text-emerald-400">
                    2.4 hrs
                  </p>
                </div>

                <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                  <div className="flex items-center gap-2 text-slate-400">
                    <TrainFront size={14} />
                    <span className="text-xs">Train Impact</span>
                  </div>

                  <p className="mt-2 text-xl font-bold text-emerald-400">
                    Low
                  </p>
                </div>
              </div>

              <div className="mt-4 flex items-start gap-2 rounded-lg border border-blue-500/20 bg-blue-500/10 p-3">
                <ShieldCheck
                  size={16}
                  className="mt-0.5 shrink-0 text-blue-400"
                />

                <p className="text-xs leading-5 text-slate-300">
                  AI prioritizes safety criticality, urgency, asset impact,
                  and train movement forecasts.
                </p>
              </div>

              <button
  onClick={() => setActivePage("AI Block Planner")}
  className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 py-3 text-sm font-bold transition hover:bg-blue-500"
>
  View AI Plan
  <ChevronRight size={17} />
</button>
            </div>
          </div>
        </div>
      </section>

      {/* ================= MAINTENANCE TABLE ================= */}
      <section className="rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="flex flex-col justify-between gap-3 border-b border-slate-200 p-6 sm:flex-row sm:items-center">
          <div>
            <div className="flex items-center gap-2">
              <div className="rounded-lg bg-red-50 p-2 text-red-600">
                <AlertTriangle size={18} />
              </div>

              <h2 className="font-bold text-slate-900">
                Priority Maintenance Tasks
              </h2>
            </div>

            <p className="mt-1 text-sm text-slate-500">
              Tasks requiring upcoming maintenance blocks
            </p>
          </div>

          <button className="flex items-center gap-1 text-sm font-bold text-blue-600 transition hover:text-blue-700">
            View All
            <ChevronRight size={16} />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full min-w-[760px] text-left text-sm">
            <thead className="bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-500">
              <tr>
                <th className="px-6 py-4">Task ID</th>
                <th className="px-6 py-4">Asset</th>
                <th className="px-6 py-4">Department</th>
                <th className="px-6 py-4">Priority</th>
                <th className="px-6 py-4">Due</th>
              </tr>
            </thead>

            <tbody>
              {maintenanceTasks.map((task) => (
                <tr
                  key={task.id}
                  className="border-t border-slate-100 transition hover:bg-slate-50"
                >
                  <td className="px-6 py-4">
                    <span className="font-bold text-blue-600">
                      {task.id}
                    </span>
                  </td>

                  <td className="px-6 py-4 font-medium text-slate-700">
                    {task.asset}
                  </td>

                  <td className="px-6 py-4">
                    <span className="rounded-full bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-600">
                      {task.department}
                    </span>
                  </td>

                  <td className="px-6 py-4">
                    <span
                      className={`rounded-full px-3 py-1.5 text-xs font-bold ${
                        task.priority === "Critical"
                          ? "bg-red-100 text-red-700"
                          : task.priority === "High"
                          ? "bg-orange-100 text-orange-700"
                          : "bg-yellow-100 text-yellow-700"
                      }`}
                    >
                      {task.priority}
                    </span>
                  </td>

                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2 font-medium text-slate-600">
                      <Clock3 size={15} />
                      {task.due}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Table footer */}
        <div className="border-t border-slate-100 bg-slate-50/70 px-6 py-4">
          <div className="flex flex-col gap-2 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
            <span>
              Showing <strong className="text-slate-700">4</strong> priority
              tasks
            </span>

            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-red-500" />
              <span>Critical tasks require immediate attention</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
