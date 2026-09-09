import { useMemo, useState } from "react";
import {
  Search,
  Filter,
  Wrench,
  AlertTriangle,
  Clock3,
  CheckCircle2,
  X,
} from "lucide-react";

const maintenanceData = [
  {
    id: "MT-1042",
    asset: "Rail Track - KM 428/6",
    department: "Engineering",
    corridor: "BZA–EE",
    priority: "Critical",
    status: "Overdue",
    due: "08 Sep 2026",
  },
  {
    id: "MT-1038",
    asset: "Transformer - TSS 14",
    department: "Traction",
    corridor: "BZA–EE",
    priority: "High",
    status: "Scheduled",
    due: "09 Sep 2026",
  },
  {
    id: "MT-1029",
    asset: "Signal Relay - BZA-22",
    department: "S&T",
    corridor: "BZA–EE",
    priority: "Medium",
    status: "Scheduled",
    due: "12 Sep 2026",
  },
  {
    id: "MT-1021",
    asset: "Overhead Equipment - KM 431",
    department: "Traction",
    corridor: "BZA–EE",
    priority: "High",
    status: "Pending",
    due: "13 Sep 2026",
  },
  {
    id: "MT-1018",
    asset: "Rail Joint - KM 425/2",
    department: "Engineering",
    corridor: "EE–TDD",
    priority: "Critical",
    status: "Overdue",
    due: "07 Sep 2026",
  },
  {
    id: "MT-1015",
    asset: "Signal Cable - KM 452",
    department: "S&T",
    corridor: "EE–TDD",
    priority: "Low",
    status: "Completed",
    due: "06 Sep 2026",
  },
  {
    id: "MT-1009",
    asset: "OHE Insulator - KM 438",
    department: "Traction",
    corridor: "TDD–NDD",
    priority: "Medium",
    status: "Pending",
    due: "15 Sep 2026",
  },
  {
    id: "MT-1004",
    asset: "Track Geometry - KM 417",
    department: "Engineering",
    corridor: "BZA–EE",
    priority: "High",
    status: "Scheduled",
    due: "16 Sep 2026",
  },
];

function Maintenance() {
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("All");
  const [priority, setPriority] = useState("All");
  const [status, setStatus] = useState("All");

  const filteredTasks = useMemo(() => {
    return maintenanceData.filter((task) => {
      const searchText = search.toLowerCase();

      const matchesSearch =
        task.id.toLowerCase().includes(searchText) ||
        task.asset.toLowerCase().includes(searchText) ||
        task.corridor.toLowerCase().includes(searchText);

      const matchesDepartment =
        department === "All" || task.department === department;

      const matchesPriority =
        priority === "All" || task.priority === priority;

      const matchesStatus =
        status === "All" || task.status === status;

      return (
        matchesSearch &&
        matchesDepartment &&
        matchesPriority &&
        matchesStatus
      );
    });
  }, [search, department, priority, status]);

  const clearFilters = () => {
    setSearch("");
    setDepartment("All");
    setPriority("All");
    setStatus("All");
  };

  const totalTasks = maintenanceData.length;

  const criticalTasks = maintenanceData.filter(
    (task) => task.priority === "Critical"
  ).length;

  const overdueTasks = maintenanceData.filter(
    (task) => task.status === "Overdue"
  ).length;

  const scheduledTasks = maintenanceData.filter(
    (task) => task.status === "Scheduled"
  ).length;

  return (
    <div className="space-y-6">

      {/* ================= HEADER ================= */}
      <div>
        <div className="flex items-center gap-2 text-sm font-medium text-blue-600">
          <Wrench size={18} />
          Maintenance Management
        </div>

        <h1 className="mt-1 text-2xl font-bold text-slate-900">
          Maintenance Tasks
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Monitor defects, maintenance activities and scheduling priorities
          across railway infrastructure.
        </p>
      </div>

      {/* ================= SUMMARY CARDS ================= */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">

        <SummaryCard
          title="Total Tasks"
          value={totalTasks}
          icon={Wrench}
          iconBg="bg-blue-50"
          iconColor="text-blue-600"
        />

        <SummaryCard
          title="Critical Tasks"
          value={criticalTasks}
          icon={AlertTriangle}
          iconBg="bg-red-50"
          iconColor="text-red-600"
        />

        <SummaryCard
          title="Overdue"
          value={overdueTasks}
          icon={Clock3}
          iconBg="bg-orange-50"
          iconColor="text-orange-600"
        />

        <SummaryCard
          title="Scheduled"
          value={scheduledTasks}
          icon={CheckCircle2}
          iconBg="bg-emerald-50"
          iconColor="text-emerald-600"
        />

      </div>

      {/* ================= FILTER SECTION ================= */}
      <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">

        <div className="flex flex-col gap-4">

          {/* Search */}
          <div className="relative">

            <Search
              size={18}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
            />

            <input
              type="text"
              placeholder="Search task ID, asset or corridor..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full rounded-lg border border-slate-200 py-3 pl-10 pr-4 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
            />

          </div>

          {/* Filters */}
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">

            <FilterSelect
              label="Department"
              value={department}
              onChange={setDepartment}
              options={[
                "All",
                "Engineering",
                "Traction",
                "S&T",
              ]}
            />

            <FilterSelect
              label="Priority"
              value={priority}
              onChange={setPriority}
              options={[
                "All",
                "Critical",
                "High",
                "Medium",
                "Low",
              ]}
            />

            <FilterSelect
              label="Status"
              value={status}
              onChange={setStatus}
              options={[
                "All",
                "Overdue",
                "Scheduled",
                "Pending",
                "Completed",
              ]}
            />

            <button
              onClick={clearFilters}
              className="flex items-center justify-center gap-2 rounded-lg border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50"
            >
              <X size={16} />
              Clear Filters
            </button>

          </div>

        </div>
      </div>

      {/* ================= RESULT COUNT ================= */}
      <div className="flex items-center justify-between">

        <div className="flex items-center gap-2">

          <Filter size={17} className="text-slate-400" />

          <p className="text-sm text-slate-500">
            Showing{" "}
            <span className="font-bold text-slate-800">
              {filteredTasks.length}
            </span>{" "}
            of{" "}
            <span className="font-bold text-slate-800">
              {totalTasks}
            </span>{" "}
            maintenance tasks
          </p>

        </div>

        {(search ||
          department !== "All" ||
          priority !== "All" ||
          status !== "All") && (
          <button
            onClick={clearFilters}
            className="text-sm font-semibold text-blue-600 hover:text-blue-700"
          >
            Reset
          </button>
        )}

      </div>

      {/* ================= TASK TABLE ================= */}
      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">

        <div className="overflow-x-auto">

          <table className="w-full min-w-[950px] text-left text-sm">

            <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">

              <tr>

                <th className="px-6 py-4">
                  Task ID
                </th>

                <th className="px-6 py-4">
                  Asset
                </th>

                <th className="px-6 py-4">
                  Department
                </th>

                <th className="px-6 py-4">
                  Corridor
                </th>

                <th className="px-6 py-4">
                  Priority
                </th>

                <th className="px-6 py-4">
                  Status
                </th>

                <th className="px-6 py-4">
                  Due Date
                </th>

              </tr>

            </thead>

            <tbody>

              {filteredTasks.length > 0 ? (

                filteredTasks.map((task) => (

                  <tr
                    key={task.id}
                    className="border-t border-slate-100 transition hover:bg-slate-50"
                  >

                    <td className="px-6 py-5 font-bold text-slate-800">
                      {task.id}
                    </td>

                    <td className="px-6 py-5">

                      <p className="font-medium text-slate-700">
                        {task.asset}
                      </p>

                    </td>

                    <td className="px-6 py-5">

                      <DepartmentBadge department={task.department} />

                    </td>

                    <td className="px-6 py-5 font-medium text-slate-600">
                      {task.corridor}
                    </td>

                    <td className="px-6 py-5">

                      <PriorityBadge priority={task.priority} />

                    </td>

                    <td className="px-6 py-5">

                      <StatusBadge status={task.status} />

                    </td>

                    <td className="px-6 py-5 text-slate-600">
                      {task.due}
                    </td>

                  </tr>

                ))

              ) : (

                <tr>

                  <td
                    colSpan="7"
                    className="px-6 py-16 text-center"
                  >

                    <div className="flex flex-col items-center">

                      <div className="rounded-full bg-slate-100 p-4">
                        <Search
                          size={24}
                          className="text-slate-400"
                        />
                      </div>

                      <h3 className="mt-4 font-bold text-slate-800">
                        No maintenance tasks found
                      </h3>

                      <p className="mt-1 text-sm text-slate-500">
                        Try changing your search or filters.
                      </p>

                      <button
                        onClick={clearFilters}
                        className="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
                      >
                        Clear Filters
                      </button>

                    </div>

                  </td>

                </tr>

              )}

            </tbody>

          </table>

        </div>
      </div>

      {/* ================= AI PRIORITY NOTICE ================= */}
      <div className="rounded-xl border border-blue-200 bg-blue-50 p-5">

        <div className="flex items-start gap-3">

          <div className="rounded-lg bg-blue-600 p-2 text-white">
            <AlertTriangle size={19} />
          </div>

          <div>

            <h3 className="font-bold text-slate-900">
              AI Priority Analysis
            </h3>

            <p className="mt-1 text-sm leading-6 text-slate-600">
              Critical and overdue maintenance tasks are automatically
              prioritized by the AI Block Planner based on safety criticality,
              urgency, asset impact and train operation impact.
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}

/* ================= SUMMARY CARD ================= */

function SummaryCard({
  title,
  value,
  icon: Icon,
  iconBg,
  iconColor,
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-md">

      <div className="flex items-center justify-between">

        <div>
          <p className="text-sm font-medium text-slate-500">
            {title}
          </p>

          <p className="mt-2 text-3xl font-bold text-slate-900">
            {value}
          </p>
        </div>

        <div className={`rounded-lg p-3 ${iconBg} ${iconColor}`}>
          <Icon size={22} />
        </div>

      </div>

    </div>
  );
}

/* ================= FILTER ================= */

function FilterSelect({
  label,
  value,
  onChange,
  options,
}) {
  return (
    <div>

      <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-400">
        {label}
      </label>

      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-lg border border-slate-200 bg-white px-3 py-3 text-sm font-medium text-slate-700 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
      >

        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}

      </select>

    </div>
  );
}

/* ================= DEPARTMENT BADGE ================= */

function DepartmentBadge({ department }) {
  const styles = {
    Engineering: "bg-blue-50 text-blue-700",
    Traction: "bg-indigo-50 text-indigo-700",
    "S&T": "bg-purple-50 text-purple-700",
  };

  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-semibold ${
        styles[department] || "bg-slate-100 text-slate-600"
      }`}
    >
      {department}
    </span>
  );
}

/* ================= PRIORITY BADGE ================= */

function PriorityBadge({ priority }) {
  const styles = {
    Critical: "bg-red-100 text-red-700",
    High: "bg-orange-100 text-orange-700",
    Medium: "bg-yellow-100 text-yellow-700",
    Low: "bg-slate-100 text-slate-600",
  };

  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-bold ${
        styles[priority]
      }`}
    >
      {priority}
    </span>
  );
}

/* ================= STATUS BADGE ================= */

function StatusBadge({ status }) {
  const styles = {
    Overdue: "bg-red-50 text-red-700",
    Scheduled: "bg-blue-50 text-blue-700",
    Pending: "bg-orange-50 text-orange-700",
    Completed: "bg-emerald-50 text-emerald-700",
  };

  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-bold ${
        styles[status]
      }`}
    >
      {status}
    </span>
  );
}

export default Maintenance;