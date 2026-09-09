import { useMemo, useState } from "react";
import {
  BrainCircuit,
  CalendarDays,
  CheckCircle2,
  Clock3,
  Filter,
  Gauge,
  MapPin,
  TrainFront,
  Wrench,
  Zap,
} from "lucide-react";

const days = [
  { key: "Mon", date: "07 Sep" },
  { key: "Tue", date: "08 Sep" },
  { key: "Wed", date: "09 Sep" },
  { key: "Thu", date: "10 Sep" },
  { key: "Fri", date: "11 Sep" },
  { key: "Sat", date: "12 Sep" },
  { key: "Sun", date: "13 Sep" },
];

const tasks = [
  {
    id: "MT-1042",
    title: "Rail Track Inspection",
    asset: "Track KM 428/6",
    department: "Engineering",
    priority: "Critical",
    day: "Thu",
    date: "10 Sep",
    corridor: "BZA-EE",
    start: "10:00",
    end: "11:00",
    duration: "1 hr",
    status: "AI Optimized",
    impact: "Low",
    score: 96,
  },
  {
    id: "MT-1038",
    title: "Transformer Maintenance",
    asset: "TSS-14",
    department: "Traction",
    priority: "High",
    day: "Thu",
    date: "10 Sep",
    corridor: "BZA-EE",
    start: "11:00",
    end: "12:30",
    duration: "1.5 hrs",
    status: "AI Optimized",
    impact: "Low",
    score: 93,
  },
  {
    id: "MT-1029",
    title: "Signal Relay Replacement",
    asset: "Signal BZA-22",
    department: "S&T",
    priority: "Medium",
    day: "Thu",
    date: "10 Sep",
    corridor: "BZA-EE",
    start: "10:00",
    end: "11:00",
    duration: "1 hr",
    status: "AI Optimized",
    impact: "Low",
    score: 91,
  },
  {
    id: "MT-1021",
    title: "Overhead Equipment Inspection",
    asset: "OHE KM 431",
    department: "Traction",
    priority: "High",
    day: "Fri",
    date: "11 Sep",
    corridor: "EE-TDD",
    start: "14:00",
    end: "16:00",
    duration: "2 hrs",
    status: "Scheduled",
    impact: "Medium",
    score: 84,
  },
  {
    id: "MT-1017",
    title: "Track Geometry Inspection",
    asset: "Track KM 452",
    department: "Engineering",
    priority: "Medium",
    day: "Sat",
    date: "12 Sep",
    corridor: "TDD-NDD",
    start: "11:30",
    end: "13:00",
    duration: "1.5 hrs",
    status: "Scheduled",
    impact: "Low",
    score: 81,
  },
  {
    id: "MT-1011",
    title: "Point Machine Inspection",
    asset: "Point NDD-17",
    department: "S&T",
    priority: "Medium",
    day: "Sun",
    date: "13 Sep",
    corridor: "NDD-RJY",
    start: "18:00",
    end: "20:00",
    duration: "2 hrs",
    status: "Blocked",
    impact: "High",
    score: 72,
  },
];

const departmentColors = {
  Engineering: "bg-blue-50 text-blue-700 border-blue-200",
  Traction: "bg-orange-50 text-orange-700 border-orange-200",
  "S&T": "bg-purple-50 text-purple-700 border-purple-200",
};

function priorityClasses(priority) {
  if (priority === "Critical") {
    return "bg-red-50 text-red-700 border-red-200";
  }

  if (priority === "High") {
    return "bg-orange-50 text-orange-700 border-orange-200";
  }

  return "bg-yellow-50 text-yellow-700 border-yellow-200";
}

export default function WeeklyPlan() {
  const [selectedDay, setSelectedDay] = useState("All");
  const [department, setDepartment] = useState("All");

  const filteredTasks = useMemo(() => {
    return tasks.filter((task) => {
      const dayMatch = selectedDay === "All" || task.day === selectedDay;
      const departmentMatch =
        department === "All" || task.department === department;

      return dayMatch && departmentMatch;
    });
  }, [selectedDay, department]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-blue-600">
            <CalendarDays size={17} />
            Maintenance Scheduling
          </div>

          <h1 className="text-2xl font-black tracking-tight text-slate-900 sm:text-3xl">
            Weekly Maintenance Plan
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            AI-optimized maintenance schedule coordinated across departments,
            corridors and train movements.
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-xl border border-blue-200 bg-blue-50 px-4 py-3">
          <BrainCircuit size={18} className="text-blue-600" />
          <div>
            <p className="text-xs font-bold text-blue-700">
              AI PLAN ACTIVE
            </p>
            <p className="text-[11px] text-blue-600">
              Updated 09 Sep 2026 · 08:30
            </p>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Kpi
          title="Planned Tasks"
          value="24"
          subtitle="This week"
          icon={Wrench}
          bg="bg-blue-50"
          color="text-blue-600"
        />

        <Kpi
          title="AI Optimized"
          value="18"
          subtitle="75% of tasks"
          icon={BrainCircuit}
          bg="bg-purple-50"
          color="text-purple-600"
        />

        <Kpi
          title="Block Saving"
          value="6.8 hrs"
          subtitle="Compared with manual plan"
          icon={Clock3}
          bg="bg-emerald-50"
          color="text-emerald-600"
        />

        <Kpi
          title="Train Impact"
          value="Low"
          subtitle="82% of planned blocks"
          icon={TrainFront}
          bg="bg-orange-50"
          color="text-orange-600"
        />
      </div>

      {/* Filters */}
      <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <div className="mb-3 flex items-center gap-2">
          <Filter size={17} className="text-slate-500" />
          <p className="text-sm font-bold text-slate-800">
            Schedule Filters
          </p>
        </div>

        <div className="flex flex-col gap-3 lg:flex-row">
          <div className="flex flex-1 flex-wrap gap-2">
            <button
              onClick={() => setSelectedDay("All")}
              className={`rounded-lg px-3 py-2 text-xs font-bold ${
                selectedDay === "All"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-100 text-slate-600"
              }`}
            >
              All Week
            </button>

            {days.map((day) => (
              <button
                key={day.key}
                onClick={() => setSelectedDay(day.key)}
                className={`rounded-lg px-3 py-2 text-xs font-bold ${
                  selectedDay === day.key
                    ? "bg-blue-600 text-white"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >
                {day.key}
              </button>
            ))}
          </div>

          <select
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700 outline-none focus:border-blue-500"
          >
            <option value="All">All Departments</option>
            <option value="Engineering">Engineering</option>
            <option value="Traction">Traction</option>
            <option value="S&T">Signal & Telecom</option>
          </select>
        </div>
      </section>

      {/* Week strip */}
      <section className="overflow-x-auto rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <div className="grid min-w-[760px] grid-cols-7 gap-2">
          {days.map((day) => {
            const count = tasks.filter((task) => task.day === day.key).length;
            const active = selectedDay === day.key;

            return (
              <button
                key={day.key}
                onClick={() => setSelectedDay(day.key)}
                className={`rounded-xl border p-4 text-center transition ${
                  active
                    ? "border-blue-500 bg-blue-50"
                    : "border-slate-200 bg-slate-50 hover:border-blue-200"
                }`}
              >
                <p
                  className={`text-xs font-bold ${
                    active ? "text-blue-600" : "text-slate-500"
                  }`}
                >
                  {day.key}
                </p>

                <p className="mt-1 text-lg font-black text-slate-900">
                  {day.date.split(" ")[0]}
                </p>

                <p className="mt-1 text-[11px] text-slate-400">
                  {count} tasks
                </p>
              </button>
            );
          })}
        </div>
      </section>

      {/* AI Optimization Banner */}
      <section className="rounded-2xl border border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex gap-3">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-600 text-white">
              <BrainCircuit size={22} />
            </div>

            <div>
              <h2 className="font-black text-slate-900">
                AI Optimization Summary
              </h2>

              <p className="mt-1 max-w-3xl text-sm leading-6 text-slate-600">
                The planner grouped 3 activities on the BZA–EE corridor into
                one coordinated maintenance window. This avoids duplicate
                corridor blocks and reduces train-operation disruption.
              </p>
            </div>
          </div>

          <div className="flex shrink-0 gap-3">
            <Metric value="2.4 hrs" label="Block saved" />
            <Metric value="94%" label="Confidence" />
          </div>
        </div>
      </section>

      {/* Schedule */}
      <section className="rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="flex flex-col gap-3 border-b border-slate-200 p-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-black text-slate-900">
              Optimized Work Schedule
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              {filteredTasks.length} maintenance activities displayed
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-600">
            <CheckCircle2 size={15} />
            AI schedule validated
          </div>
        </div>

        <div className="divide-y divide-slate-100">
          {filteredTasks.map((task) => (
            <div
              key={task.id}
              className="p-5 transition hover:bg-slate-50"
            >
              <div className="flex flex-col gap-5 xl:flex-row xl:items-center">
                {/* Time */}
                <div className="w-full shrink-0 xl:w-28">
                  <p className="text-sm font-black text-slate-900">
                    {task.start}
                  </p>
                  <p className="text-xs text-slate-400">to {task.end}</p>

                  <div className="mt-2 flex items-center gap-1 text-xs text-slate-500">
                    <Clock3 size={13} />
                    {task.duration}
                  </div>
                </div>

                {/* Task */}
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="rounded-md bg-slate-100 px-2 py-1 text-[11px] font-black text-slate-500">
                      {task.id}
                    </span>

                    <span
                      className={`rounded-full border px-2.5 py-1 text-[11px] font-bold ${priorityClasses(
                        task.priority
                      )}`}
                    >
                      {task.priority}
                    </span>

                    <span className="rounded-full border border-blue-200 bg-blue-50 px-2.5 py-1 text-[11px] font-bold text-blue-700">
                      {task.status}
                    </span>
                  </div>

                  <h3 className="mt-2 text-base font-black text-slate-900">
                    {task.title}
                  </h3>

                  <p className="mt-1 text-sm text-slate-500">
                    {task.asset}
                  </p>

                  <div className="mt-3 flex flex-wrap gap-2">
                    <span
                      className={`rounded-lg border px-2.5 py-1 text-xs font-bold ${
                        departmentColors[task.department]
                      }`}
                    >
                      {task.department}
                    </span>

                    <span className="flex items-center gap-1 rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">
                      <MapPin size={13} />
                      {task.corridor}
                    </span>

                    <span className="flex items-center gap-1 rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">
                      <TrainFront size={13} />
                      {task.impact} train impact
                    </span>
                  </div>
                </div>

                {/* AI Score */}
                <div className="w-full rounded-xl border border-slate-200 bg-slate-50 p-4 xl:w-44">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-500">
                      AI Priority
                    </span>

                    <Gauge size={15} className="text-blue-600" />
                  </div>

                  <p className="mt-2 text-2xl font-black text-blue-600">
                    {task.score}
                  </p>

                  <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-200">
                    <div
                      className="h-full rounded-full bg-blue-600"
                      style={{ width: `${task.score}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}

          {filteredTasks.length === 0 && (
            <div className="p-10 text-center">
              <CalendarDays className="mx-auto text-slate-300" size={35} />
              <p className="mt-3 font-bold text-slate-700">
                No maintenance tasks found
              </p>
              <p className="mt-1 text-sm text-slate-400">
                Change the selected day or department.
              </p>
            </div>
          )}
        </div>
      </section>

      {/* AI Logic */}
      <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <ReasonCard
          icon={Zap}
          title="Shared Corridor"
          text="Multiple departments are coordinated inside the same block window."
        />

        <ReasonCard
          icon={TrainFront}
          title="Train Impact"
          text="Maintenance is shifted away from high-density train movement periods."
        />

        <ReasonCard
          icon={Gauge}
          title="Criticality"
          text="Critical assets receive higher priority based on safety and availability risk."
        />
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
          <p className="mt-2 text-3xl font-black text-slate-900">{value}</p>
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
      <p className="text-[11px] font-semibold text-slate-400">{label}</p>
    </div>
  );
}

function ReasonCard({ icon: Icon, title, text }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
        <Icon size={19} />
      </div>

      <h3 className="mt-4 font-black text-slate-900">{title}</h3>

      <p className="mt-2 text-sm leading-6 text-slate-500">{text}</p>
    </div>
  );
}