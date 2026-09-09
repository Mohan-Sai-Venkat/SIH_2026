import { useMemo, useState } from "react";
import {
  BarChart3,
  TrendingUp,
  Wrench,
  Clock3,
  TrainFront,
  Activity,
  BrainCircuit,
  Zap,
  ShieldCheck,
  ArrowUpRight,
  ArrowDownRight,
  Download,
} from "lucide-react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const utilizationData = [
  {
    department: "Engineering",
    current: 61,
    optimized: 78,
  },
  {
    department: "Traction",
    current: 52,
    optimized: 64,
  },
  {
    department: "S&T",
    current: 43,
    optimized: 52,
  },
];

const trendData = [
  { week: "W1", tasks: 24, completed: 18 },
  { week: "W2", tasks: 27, completed: 21 },
  { week: "W3", tasks: 22, completed: 19 },
  { week: "W4", tasks: 18, completed: 17 },
];

const trainImpactData = [
  {
    name: "Low Impact",
    value: 68,
  },
  {
    name: "Medium Impact",
    value: 23,
  },
  {
    name: "High Impact",
    value: 9,
  },
];

const workloadData = [
  {
    department: "Engineering",
    tasks: 34,
    blocks: 14,
    utilization: 76,
  },
  {
    department: "Traction",
    tasks: 29,
    blocks: 13,
    utilization: 65,
  },
  {
    department: "S&T",
    tasks: 28,
    blocks: 11,
    utilization: 58,
  },
];

function KPI({
  icon: Icon,
  title,
  value,
  description,
  change,
  positive = true,
  style,
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>

          <h3 className="mt-2 text-2xl font-bold text-slate-900">
            {value}
          </h3>

          <p className="mt-1 text-xs text-slate-400">
            {description}
          </p>
        </div>

        <div className={`rounded-xl p-3 ${style}`}>
          <Icon size={21} />
        </div>
      </div>

      <div
        className={`mt-4 flex items-center gap-1 text-xs font-bold ${
          positive ? "text-emerald-600" : "text-red-600"
        }`}
      >
        {positive ? (
          <ArrowUpRight size={15} />
        ) : (
          <ArrowDownRight size={15} />
        )}

        {change}
      </div>
    </div>
  );
}

function SectionHeader({ icon: Icon, title, description }) {
  return (
    <div className="mb-5 flex items-start gap-3">
      <div className="rounded-xl bg-blue-50 p-2.5 text-blue-600">
        <Icon size={20} />
      </div>

      <div>
        <h2 className="font-bold text-slate-900">{title}</h2>

        <p className="mt-1 text-sm text-slate-500">
          {description}
        </p>
      </div>
    </div>
  );
}

export default function Analytics() {
  const [period, setPeriod] = useState("Monthly");
  const [selectedDepartment, setSelectedDepartment] =
    useState("All");

  const filteredWorkload = useMemo(() => {
    if (selectedDepartment === "All") {
      return workloadData;
    }

    return workloadData.filter(
      (item) => item.department === selectedDepartment
    );
  }, [selectedDepartment]);

  const exportReport = () => {
    alert(
      "Analytics report prepared successfully. Backend export will be connected later."
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
        <div>
          <div className="mb-2 flex items-center gap-2">
            <BarChart3 size={22} className="text-blue-600" />

            <span className="text-sm font-semibold text-blue-600">
              OPERATIONS INTELLIGENCE
            </span>
          </div>

          <h1 className="text-2xl font-bold text-slate-900 sm:text-3xl">
            Analytics & Performance
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Measure maintenance efficiency and AI optimization impact
          </p>
        </div>

        <button
          onClick={exportReport}
          className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 shadow-sm transition hover:bg-slate-50"
        >
          <Download size={18} />
          Export Report
        </button>
      </div>

      {/* Controls */}
      <div className="flex flex-col justify-between gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Analysis Period
          </p>

          <div className="mt-2 flex gap-2">
            {["Weekly", "Monthly", "Quarterly"].map((item) => (
              <button
                key={item}
                onClick={() => setPeriod(item)}
                className={`rounded-lg px-4 py-2 text-xs font-semibold transition ${
                  period === item
                    ? "bg-blue-600 text-white"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Department
          </p>

          <select
            value={selectedDepartment}
            onChange={(e) => setSelectedDepartment(e.target.value)}
            className="mt-2 rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 outline-none focus:border-blue-500"
          >
            <option>All</option>
            <option>Engineering</option>
            <option>Traction</option>
            <option>S&T</option>
          </select>
        </div>
      </div>

      {/* KPI */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <KPI
          icon={Activity}
          title="Block Utilization"
          value="84%"
          description="Corridor block utilization"
          change="+23% vs manual planning"
          style="bg-blue-50 text-blue-600"
        />

        <KPI
          icon={Clock3}
          title="Asset Downtime"
          value="15%"
          description="Average infrastructure downtime"
          change="-18% after AI optimization"
          style="bg-emerald-50 text-emerald-600"
        />

        <KPI
          icon={Zap}
          title="Block Hours Saved"
          value="14.5h"
          description="Estimated monthly savings"
          change="+14.5 hours optimized"
          style="bg-violet-50 text-violet-600"
        />

        <KPI
          icon={TrainFront}
          title="Train Impact"
          value="-50%"
          description="Maintenance-related disruption"
          change="-50% predicted impact"
          style="bg-orange-50 text-orange-600"
        />
      </div>

      {/* AI Performance */}
      <div className="rounded-2xl border border-violet-200 bg-gradient-to-r from-violet-50 to-blue-50 p-5">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-violet-600 text-white shadow-lg">
              <BrainCircuit size={24} />
            </div>

            <div>
              <div className="flex items-center gap-2">
                <h2 className="font-bold text-slate-900">
                  AI Planning Performance
                </h2>

                <span className="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-bold text-emerald-700">
                  94% CONFIDENCE
                </span>
              </div>

              <p className="mt-1 max-w-3xl text-sm leading-6 text-slate-600">
                AI coordination is improving block utilization by combining
                compatible maintenance activities while selecting lower
                train-density windows.
              </p>
            </div>
          </div>

          <div className="rounded-xl bg-white px-5 py-4 shadow-sm">
            <p className="text-xs text-slate-400">
              Overall Efficiency
            </p>

            <p className="mt-1 text-3xl font-bold text-emerald-600">
              +23%
            </p>
          </div>
        </div>
      </div>

      {/* Utilization chart */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <SectionHeader
          icon={TrendingUp}
          title="Block Utilization: Manual vs AI"
          description="Comparison of corridor block utilization before and after AI optimization."
        />

        <div className="h-[360px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={utilizationData}
              margin={{
                top: 10,
                right: 20,
                left: 0,
                bottom: 10,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="department" />

              <YAxis
                domain={[0, 100]}
                tickFormatter={(value) => `${value}%`}
              />

              <Tooltip
                formatter={(value) => `${value}%`}
              />

              <Legend />

              <Bar
                dataKey="current"
                name="Manual Planning"
                fill="#94a3b8"
                radius={[5, 5, 0, 0]}
              />

              <Bar
                dataKey="optimized"
                name="AI Optimized"
                fill="#2563eb"
                radius={[5, 5, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Trend + Train Impact */}
      <div className="grid gap-6 xl:grid-cols-[1.4fr_0.6fr]">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <SectionHeader
            icon={Activity}
            title="Maintenance Completion Trend"
            description="Weekly planned activities compared with completed work."
          />

          <div className="h-[320px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={trendData}
                margin={{
                  top: 10,
                  right: 20,
                  left: 0,
                  bottom: 10,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="week" />

                <YAxis />

                <Tooltip />

                <Legend />

                <Line
                  type="monotone"
                  dataKey="tasks"
                  name="Planned Tasks"
                  stroke="#64748b"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                />

                <Line
                  type="monotone"
                  dataKey="completed"
                  name="Completed Tasks"
                  stroke="#16a34a"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <SectionHeader
            icon={TrainFront}
            title="Train Impact"
            description="Predicted operational impact."
          />

          <div className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={trainImpactData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={90}
                  paddingAngle={3}
                >
                  {trainImpactData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={
                        index === 0
                          ? "#16a34a"
                          : index === 1
                          ? "#f59e0b"
                          : "#ef4444"
                      }
                    />
                  ))}
                </Pie>

                <Tooltip formatter={(value) => `${value}%`} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-3">
            {trainImpactData.map((item, index) => (
              <div
                key={item.name}
                className="flex items-center justify-between"
              >
                <div className="flex items-center gap-2">
                  <span
                    className={`h-3 w-3 rounded-full ${
                      index === 0
                        ? "bg-emerald-500"
                        : index === 1
                        ? "bg-amber-500"
                        : "bg-red-500"
                    }`}
                  />

                  <span className="text-sm text-slate-600">
                    {item.name}
                  </span>
                </div>

                <span className="text-sm font-bold text-slate-800">
                  {item.value}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Department Workload */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <SectionHeader
          icon={BarChart3}
          title="Department Workload"
          description="Maintenance workload and block utilization by department."
        />

        <div className="overflow-x-auto">
          <table className="w-full min-w-[650px] text-left">
            <thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-500">
              <tr>
                <th className="rounded-l-lg px-5 py-4">
                  Department
                </th>
                <th className="px-5 py-4">Tasks</th>
                <th className="px-5 py-4">Blocks</th>
                <th className="px-5 py-4">Utilization</th>
                <th className="rounded-r-lg px-5 py-4">
                  Performance
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">
              {filteredWorkload.map((item) => (
                <tr key={item.department}>
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">
                      <div className="rounded-lg bg-blue-50 p-2 text-blue-600">
                        <WrenchIcon
                          department={item.department}
                        />
                      </div>

                      <span className="text-sm font-bold text-slate-800">
                        {item.department}
                      </span>
                    </div>
                  </td>

                  <td className="px-5 py-4 text-sm font-semibold text-slate-700">
                    {item.tasks}
                  </td>

                  <td className="px-5 py-4 text-sm font-semibold text-slate-700">
                    {item.blocks}
                  </td>

                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">
                      <div className="h-2 w-28 overflow-hidden rounded-full bg-slate-100">
                        <div
                          className="h-full rounded-full bg-blue-600"
                          style={{
                            width: `${item.utilization}%`,
                          }}
                        />
                      </div>

                      <span className="text-sm font-bold text-slate-700">
                        {item.utilization}%
                      </span>
                    </div>
                  </td>

                  <td className="px-5 py-4">
                    <span className="inline-flex items-center gap-1 text-xs font-bold text-emerald-600">
                      <ArrowUpRight size={14} />
                      Optimized
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Key Results */}
      <div>
        <div className="mb-4">
          <h2 className="text-lg font-bold text-slate-900">
            Key Results
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Measurable outcomes from coordinated maintenance planning.
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-emerald-600 p-3 text-white">
                <Clock3 size={20} />
              </div>

              <div>
                <p className="text-xs font-semibold uppercase text-emerald-700">
                  Block Efficiency
                </p>

                <p className="text-2xl font-bold text-emerald-800">
                  +23%
                </p>
              </div>
            </div>

            <p className="mt-4 text-sm leading-6 text-emerald-800">
              More maintenance activities are completed within shared
              corridor block windows.
            </p>
          </div>

          <div className="rounded-2xl border border-blue-200 bg-blue-50 p-5">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-blue-600 p-3 text-white">
                <Activity size={20} />
              </div>

              <div>
                <p className="text-xs font-semibold uppercase text-blue-700">
                  Asset Availability
                </p>

                <p className="text-2xl font-bold text-blue-800">
                  +11%
                </p>
              </div>
            </div>

            <p className="mt-4 text-sm leading-6 text-blue-800">
              Reduced downtime improves the availability of critical
              fixed railway infrastructure.
            </p>
          </div>

          <div className="rounded-2xl border border-violet-200 bg-violet-50 p-5">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-violet-600 p-3 text-white">
                <BrainCircuit size={20} />
              </div>

              <div>
                <p className="text-xs font-semibold uppercase text-violet-700">
                  AI Confidence
                </p>

                <p className="text-2xl font-bold text-violet-800">
                  94%
                </p>
              </div>
            </div>

            <p className="mt-4 text-sm leading-6 text-violet-800">
              Recommendations are evaluated using safety, urgency,
              asset impact and train movement.
            </p>
          </div>
        </div>
      </div>

      {/* Safety / Governance */}
      <div className="flex flex-col gap-4 rounded-2xl border border-emerald-200 bg-emerald-50 p-5 sm:flex-row sm:items-center">
        <div className="rounded-xl bg-emerald-600 p-3 text-white">
          <ShieldCheck size={23} />
        </div>

        <div>
          <h2 className="font-bold text-emerald-900">
            Analytics support operational decisions
          </h2>

          <p className="mt-1 text-sm leading-6 text-emerald-800">
            AI metrics are intended to assist planners in evaluating
            maintenance efficiency. Final block approval remains under
            authorized railway operational control.
          </p>
        </div>
      </div>
    </div>
  );
}

function WrenchIcon({ department }) {
  if (department === "Traction") {
    return <Zap size={17} />;
  }

  if (department === "S&T") {
    return <Activity size={17} />;
  }

  return <Wrench size={17} />;
}