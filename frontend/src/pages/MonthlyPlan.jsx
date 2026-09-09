import { useMemo, useState } from "react";
import {
  BrainCircuit,
  CalendarRange,
  CheckCircle2,
  Clock3,
  Gauge,
  Route,
  TrainFront,
  Wrench,
  Zap,
} from "lucide-react";

const weeks = [
  {
    id: "W1",
    label: "Week 1",
    dates: "01 – 06 Sep",
    tasks: 42,
    blocks: 11,
    utilization: 76,
    saving: "3.2 hrs",
  },
  {
    id: "W2",
    label: "Week 2",
    dates: "07 – 13 Sep",
    tasks: 47,
    blocks: 14,
    utilization: 82,
    saving: "6.8 hrs",
  },
  {
    id: "W3",
    label: "Week 3",
    dates: "14 – 20 Sep",
    tasks: 39,
    blocks: 12,
    utilization: 79,
    saving: "4.5 hrs",
  },
  {
    id: "W4",
    label: "Week 4",
    dates: "21 – 27 Sep",
    tasks: 36,
    blocks: 10,
    utilization: 74,
    saving: "3.9 hrs",
  },
  {
    id: "W5",
    label: "Week 5",
    dates: "28 – 30 Sep",
    tasks: 18,
    blocks: 6,
    utilization: 71,
    saving: "2.1 hrs",
  },
];

const monthlyTasks = [
  {
    id: "MT-1042",
    date: "10 Sep",
    day: "Thu",
    title: "Rail Track Inspection",
    asset: "Track KM 428/6",
    department: "Engineering",
    corridor: "BZA-EE",
    priority: "Critical",
    start: "10:00",
    end: "11:00",
    status: "AI Optimized",
  },
  {
    id: "MT-1038",
    date: "10 Sep",
    day: "Thu",
    title: "Transformer Maintenance",
    asset: "TSS-14",
    department: "Traction",
    corridor: "BZA-EE",
    priority: "High",
    start: "11:00",
    end: "12:30",
    status: "AI Optimized",
  },
  {
    id: "MT-1029",
    date: "10 Sep",
    day: "Thu",
    title: "Signal Relay Replacement",
    asset: "Signal BZA-22",
    department: "S&T",
    corridor: "BZA-EE",
    priority: "Medium",
    start: "10:00",
    end: "11:00",
    status: "AI Optimized",
  },
  {
    id: "MT-1021",
    date: "11 Sep",
    day: "Fri",
    title: "Overhead Equipment Inspection",
    asset: "OHE KM 431",
    department: "Traction",
    corridor: "EE-TDD",
    priority: "High",
    start: "14:00",
    end: "16:00",
    status: "Scheduled",
  },
  {
    id: "MT-1017",
    date: "12 Sep",
    day: "Sat",
    title: "Track Geometry Inspection",
    asset: "Track KM 452",
    department: "Engineering",
    corridor: "TDD-NDD",
    priority: "Medium",
    start: "11:30",
    end: "13:00",
    status: "Scheduled",
  },
  {
    id: "MT-1011",
    date: "13 Sep",
    day: "Sun",
    title: "Point Machine Inspection",
    asset: "Point NDD-17",
    department: "S&T",
    corridor: "NDD-RJY",
    priority: "Medium",
    start: "18:00",
    end: "20:00",
    status: "Blocked",
  },
  {
    id: "MT-1008",
    date: "16 Sep",
    day: "Wed",
    title: "Rail Welding Inspection",
    asset: "Track KM 467",
    department: "Engineering",
    corridor: "RJY-DWP",
    priority: "High",
    start: "09:00",
    end: "11:00",
    status: "Scheduled",
  },
  {
    id: "MT-1004",
    date: "18 Sep",
    day: "Fri",
    title: "OHE Preventive Maintenance",
    asset: "OHE SLO-14",
    department: "Traction",
    corridor: "SLO-ANV",
    priority: "High",
    start: "15:00",
    end: "17:00",
    status: "AI Optimized",
  },
  {
    id: "MT-0998",
    date: "22 Sep",
    day: "Tue",
    title: "Signal Equipment Testing",
    asset: "Relay Room ANV",
    department: "S&T",
    corridor: "ANV-TUNI",
    priority: "Medium",
    start: "10:30",
    end: "12:00",
    status: "Scheduled",
  },
  {
    id: "MT-0992",
    date: "25 Sep",
    day: "Fri",
    title: "Track Drainage Inspection",
    asset: "Track KM 512",
    department: "Engineering",
    corridor: "TUNI-ANAK",
    priority: "Medium",
    start: "13:00",
    end: "15:00",
    status: "Scheduled",
  },
];

const departmentData = [
  {
    name: "Engineering",
    tasks: 18,
    blocks: 8,
    utilization: 84,
    icon: Wrench,
  },
  {
    name: "Traction",
    tasks: 15,
    blocks: 6,
    utilization: 76,
    icon: Zap,
  },
  {
    name: "S&T",
    tasks: 14,
    blocks: 5,
    utilization: 69,
    icon: Gauge,
  },
];

function priorityClasses(priority) {
  if (priority === "Critical") {
    return "bg-red-50 text-red-700 border-red-200";
  }

  if (priority === "High") {
    return "bg-orange-50 text-orange-700 border-orange-200";
  }

  return "bg-yellow-50 text-yellow-700 border-yellow-200";
}

function statusClasses(status) {
  if (status === "AI Optimized") {
    return "bg-blue-50 text-blue-700 border-blue-200";
  }

  if (status === "Blocked") {
    return "bg-red-50 text-red-700 border-red-200";
  }

  return "bg-emerald-50 text-emerald-700 border-emerald-200";
}

export default function MonthlyPlan() {
  const [selectedWeek, setSelectedWeek] = useState("All");
  const [department, setDepartment] = useState("All");

  const filteredTasks = useMemo(() => {
    const weekDates = {
      W1: ["01", "02", "03", "04", "05", "06"],
      W2: ["07", "08", "09", "10", "11", "12", "13"],
      W3: ["14", "15", "16", "17", "18", "19", "20"],
      W4: ["21", "22", "23", "24", "25", "26", "27"],
      W5: ["28", "29", "30"],
    };

    return monthlyTasks.filter((task) => {
      const dateNumber = task.date.split(" ")[0];

      const weekMatch =
        selectedWeek === "All" ||
        weekDates[selectedWeek]?.includes(dateNumber);

      const departmentMatch =
        department === "All" || task.department === department;

      return weekMatch && departmentMatch;
    });
  }, [selectedWeek, department]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-blue-600">
            <CalendarRange size={17} />
            Long-Term Maintenance Planning
          </div>

          <h1 className="text-2xl font-black tracking-tight text-slate-900 sm:text-3xl">
            Monthly Maintenance Plan
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            AI-assisted monthly planning for maintenance workload, corridor
            blocks and train-operation impact.
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-xl border border-blue-200 bg-blue-50 px-4 py-3">
          <BrainCircuit size={18} className="text-blue-600" />

          <div>
            <p className="text-xs font-black text-blue-700">
              SEPTEMBER 2026
            </p>
            <p className="text-[11px] text-blue-600">
              AI Planning Cycle Active
            </p>
          </div>
        </div>
      </div>

      {/* Monthly KPI */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Kpi
          title="Monthly Tasks"
          value="182"
          subtitle="Maintenance activities"
          icon={Wrench}
          bg="bg-blue-50"
          color="text-blue-600"
        />

        <Kpi
          title="Planned Blocks"
          value="53"
          subtitle="Corridor blocks"
          icon={Route}
          bg="bg-purple-50"
          color="text-purple-600"
        />

        <Kpi
          title="AI Optimized"
          value="137"
          subtitle="75% of activities"
          icon={BrainCircuit}
          bg="bg-emerald-50"
          color="text-emerald-600"
        />

        <Kpi
          title="Block Saving"
          value="20.5 hrs"
          subtitle="Estimated monthly saving"
          icon={Clock3}
          bg="bg-orange-50"
          color="text-orange-600"
        />
      </div>

      {/* AI Overview */}
      <section className="rounded-2xl border border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 p-5">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex gap-3">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-600 text-white">
              <BrainCircuit size={22} />
            </div>

            <div>
              <h2 className="font-black text-slate-900">
                AI Monthly Optimization
              </h2>

              <p className="mt-1 max-w-4xl text-sm leading-6 text-slate-600">
                The AI planner evaluates maintenance criticality, corridor
                availability and train density to distribute work across the
                month while maximizing block utilization.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            <Metric value="20.5h" label="Block saved" />
            <Metric value="94%" label="Confidence" />
            <Metric value="8%" label="Train impact" />
          </div>
        </div>
      </section>

      {/* Week Overview */}
      <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-5">
          <h2 className="text-lg font-black text-slate-900">
            Monthly Workload Distribution
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            AI-distributed maintenance workload by week
          </p>
        </div>

        <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-5">
          {weeks.map((week) => {
            const active = selectedWeek === week.id;

            return (
              <button
                key={week.id}
                onClick={() =>
                  setSelectedWeek(active ? "All" : week.id)
                }
                className={`rounded-2xl border p-4 text-left transition hover:-translate-y-0.5 hover:shadow-md ${
                  active
                    ? "border-blue-500 bg-blue-50 ring-2 ring-blue-100"
                    : "border-slate-200 bg-white"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-black text-slate-900">
                    {week.label}
                  </span>

                  <span className="rounded-lg bg-slate-100 px-2 py-1 text-[10px] font-bold text-slate-500">
                    {week.dates}
                  </span>
                </div>

                <p className="mt-4 text-2xl font-black text-slate-900">
                  {week.tasks}
                </p>

                <p className="text-xs text-slate-400">
                  maintenance tasks
                </p>

                <div className="mt-4">
                  <div className="mb-1 flex justify-between text-[11px]">
                    <span className="font-semibold text-slate-400">
                      Block utilization
                    </span>

                    <span className="font-bold text-slate-700">
                      {week.utilization}%
                    </span>
                  </div>

                  <div className="h-2 rounded-full bg-slate-100">
                    <div
                      className="h-full rounded-full bg-blue-600"
                      style={{ width: `${week.utilization}%` }}
                    />
                  </div>
                </div>

                <div className="mt-4 flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-500">
                    {week.blocks} blocks
                  </span>

                  <span className="text-xs font-black text-emerald-600">
                    -{week.saving}
                  </span>
                </div>
              </button>
            );
          })}
        </div>
      </section>

      {/* Filters */}
      <section className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p className="text-sm font-black text-slate-900">
            Planned Maintenance
          </p>

          <p className="mt-1 text-xs text-slate-400">
            Showing {filteredTasks.length} activities
          </p>
        </div>

        <div className="flex flex-col gap-2 sm:flex-row">
          <select
            value={selectedWeek}
            onChange={(e) => setSelectedWeek(e.target.value)}
            className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 outline-none focus:border-blue-500"
          >
            <option value="All">All Weeks</option>
            {weeks.map((week) => (
              <option key={week.id} value={week.id}>
                {week.label} · {week.dates}
              </option>
            ))}
          </select>

          <select
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 outline-none focus:border-blue-500"
          >
            <option value="All">All Departments</option>
            <option value="Engineering">Engineering</option>
            <option value="Traction">Traction</option>
            <option value="S&T">Signal & Telecom</option>
          </select>
        </div>
      </section>

      {/* Monthly Task List */}
      <section className="rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 p-5">
          <h2 className="text-lg font-black text-slate-900">
            Monthly Execution Schedule
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Coordinated maintenance activities generated by the planning
            engine.
          </p>
        </div>

        <div className="divide-y divide-slate-100">
          {filteredTasks.map((task) => (
            <div
              key={task.id}
              className="p-5 transition hover:bg-slate-50"
            >
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center">
                {/* Date */}
                <div className="flex w-full items-center gap-3 lg:w-28">
                  <div className="flex h-11 w-11 shrink-0 flex-col items-center justify-center rounded-xl bg-blue-50">
                    <span className="text-sm font-black text-blue-700">
                      {task.date.split(" ")[0]}
                    </span>

                    <span className="text-[9px] font-bold uppercase text-blue-400">
                      Sep
                    </span>
                  </div>

                  <div className="lg:hidden">
                    <p className="text-sm font-bold text-slate-800">
                      {task.day}
                    </p>
                  </div>
                </div>

                {/* Time */}
                <div className="w-full lg:w-32">
                  <div className="flex items-center gap-2 text-sm font-black text-slate-800">
                    <Clock3 size={15} className="text-slate-400" />
                    {task.start} – {task.end}
                  </div>

                  <p className="mt-1 text-xs text-slate-400">
                    {task.day}
                  </p>
                </div>

                {/* Task */}
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap gap-2">
                    <span className="rounded-md bg-slate-100 px-2 py-1 text-[10px] font-black text-slate-500">
                      {task.id}
                    </span>

                    <span
                      className={`rounded-full border px-2.5 py-1 text-[10px] font-bold ${priorityClasses(
                        task.priority
                      )}`}
                    >
                      {task.priority}
                    </span>

                    <span
                      className={`rounded-full border px-2.5 py-1 text-[10px] font-bold ${statusClasses(
                        task.status
                      )}`}
                    >
                      {task.status}
                    </span>
                  </div>

                  <h3 className="mt-2 font-black text-slate-900">
                    {task.title}
                  </h3>

                  <p className="mt-1 text-sm text-slate-500">
                    {task.asset}
                  </p>

                  <div className="mt-3 flex flex-wrap gap-2">
                    <span className="rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">
                      {task.department}
                    </span>

                    <span className="flex items-center gap-1 rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">
                      <Route size={13} />
                      {task.corridor}
                    </span>
                  </div>
                </div>

                {/* AI indicator */}
                <div className="flex shrink-0 items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2">
                  <CheckCircle2 size={16} className="text-emerald-600" />

                  <div>
                    <p className="text-[10px] font-black text-emerald-700">
                      PLAN STATUS
                    </p>
                    <p className="text-xs font-semibold text-emerald-600">
                      Validated
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}

          {filteredTasks.length === 0 && (
            <div className="p-10 text-center">
              <CalendarRange
                size={36}
                className="mx-auto text-slate-300"
              />

              <p className="mt-3 font-bold text-slate-700">
                No activities found
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Department workload */}
      <section>
        <div className="mb-4">
          <h2 className="text-lg font-black text-slate-900">
            Department Workload
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Monthly maintenance distribution across departments.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          {departmentData.map((item) => {
            const Icon = item.icon;

            return (
              <div
                key={item.name}
                className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                      <Icon size={19} />
                    </div>

                    <div>
                      <p className="font-black text-slate-900">
                        {item.name}
                      </p>

                      <p className="text-xs text-slate-400">
                        {item.tasks} tasks · {item.blocks} blocks
                      </p>
                    </div>
                  </div>

                  <span className="text-lg font-black text-blue-600">
                    {item.utilization}%
                  </span>
                </div>

                <div className="mt-5 h-2 rounded-full bg-slate-100">
                  <div
                    className="h-full rounded-full bg-blue-600"
                    style={{ width: `${item.utilization}%` }}
                  />
                </div>

                <p className="mt-2 text-xs text-slate-400">
                  Planned resource utilization
                </p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Final AI insight */}
      <section className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
        <div className="flex gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-600 text-white">
            <BrainCircuit size={20} />
          </div>

          <div>
            <h2 className="font-black text-slate-900">
              Planning Recommendation
            </h2>

            <p className="mt-1 max-w-5xl text-sm leading-6 text-slate-600">
              September maintenance demand is within available corridor
              capacity. The AI planner recommends prioritizing critical
              Engineering assets during low-density train windows and
              combining compatible Traction and S&T activities wherever
              possible.
            </p>

            <div className="mt-4 flex flex-wrap gap-3">
              <Badge icon={TrainFront} text="Low train disruption" />
              <Badge icon={Route} text="53 planned blocks" />
              <Badge icon={Zap} text="20.5 hrs saved" />
              <Badge icon={Gauge} text="94% AI confidence" />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function Kpi({ title, value, subtitle, icon: Icon, bg, color }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="mt-2 text-3xl font-black text-slate-900">
            {value}
          </p>
          <p className="mt-1 text-xs text-slate-400">{subtitle}</p>
        </div>

        <div
          className={`flex h-11 w-11 items-center justify-center rounded-xl ${bg} ${color}`}
        >
          <Icon size={21} />
        </div>
      </div>
    </div>
  );
}

function Metric({ value, label }) {
  return (
    <div className="rounded-xl border border-blue-100 bg-white px-4 py-3 text-center shadow-sm">
      <p className="text-lg font-black text-blue-600">{value}</p>
      <p className="text-[11px] font-semibold text-slate-400">
        {label}
      </p>
    </div>
  );
}

function Badge({ icon: Icon, text }) {
  return (
    <div className="flex items-center gap-2 rounded-lg border border-emerald-100 bg-white px-3 py-2 text-xs font-semibold text-slate-600">
      <Icon size={14} className="text-emerald-600" />
      {text}
    </div>
  );
}