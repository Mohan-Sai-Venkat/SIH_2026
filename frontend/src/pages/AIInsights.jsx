import {
  BarChart3,
  TrendingDown,
  Clock3,
  TrainFront,
  ShieldCheck,
  BrainCircuit,
  Activity,
  ArrowDownRight,
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

const beforeAfterData = [
  {
    metric: "Block Utilization",
    Before: 61,
    After: 89,
  },
  {
    metric: "Asset Availability",
    Before: 78,
    After: 93,
  },
  {
    metric: "Train Impact",
    Before: 24,
    After: 8,
  },
  {
    metric: "Coordination",
    Before: 52,
    After: 91,
  },
];

const weeklyData = [
  { week: "W1", Planned: 38, Optimized: 34 },
  { week: "W2", Planned: 47, Optimized: 42 },
  { week: "W3", Planned: 41, Optimized: 37 },
  { week: "W4", Planned: 36, Optimized: 32 },
  { week: "W5", Planned: 20, Optimized: 18 },
];

const departmentData = [
  { name: "Engineering", value: 78 },
  { name: "Traction", value: 64 },
  { name: "S&T", value: 52 },
];

const savingsData = [
  { month: "Apr", saving: 8.2 },
  { month: "May", saving: 11.4 },
  { month: "Jun", saving: 13.8 },
  { month: "Jul", saving: 16.1 },
  { month: "Aug", saving: 18.7 },
  { month: "Sep", saving: 20.5 },
];

const pieData = [
  { name: "Engineering", value: 42 },
  { name: "Traction", value: 31 },
  { name: "S&T", value: 27 },
];

const COLORS = ["#2563eb", "#7c3aed", "#0891b2"];

function StatCard({ icon: Icon, label, value, description }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
      <div className="flex items-start justify-between">
        <div className="rounded-xl bg-blue-50 p-3 text-blue-600">
          <Icon size={22} />
        </div>

        <span className="flex items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-bold text-emerald-700">
          <ArrowDownRight size={13} />
          Improved
        </span>
      </div>

      <p className="mt-4 text-sm font-medium text-slate-500">{label}</p>

      <h3 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
        {value}
      </h3>

      <p className="mt-1 text-xs text-slate-400">{description}</p>
    </div>
  );
}

function ChartCard({ title, description, children }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-5">
        <h3 className="font-bold text-slate-900">{title}</h3>
        <p className="mt-1 text-xs text-slate-500">{description}</p>
      </div>

      {children}
    </div>
  );
}

function Analytics() {
  return (
    <div className="space-y-6">
      {/* HEADER */}
      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <div className="rounded-xl bg-blue-100 p-2 text-blue-700">
              <BarChart3 size={22} />
            </div>

            <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-blue-700">
              Performance Intelligence
            </span>
          </div>

          <h1 className="mt-3 text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
            Analytics & AI Impact
          </h1>

          <p className="mt-1 max-w-3xl text-sm text-slate-500">
            Measure how AI-assisted maintenance planning improves block
            utilization, asset availability, coordination and train
            operations.
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3">
          <Activity size={18} className="text-emerald-600" />

          <div>
            <p className="text-xs font-semibold text-emerald-700">
              AI PERFORMANCE
            </p>
            <p className="text-sm font-bold text-emerald-800">
              Optimization Active
            </p>
          </div>
        </div>
      </div>

      {/* KPI CARDS */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          icon={Clock3}
          label="Block Time Saved"
          value="20.5 hrs"
          description="Compared with manual planning"
        />

        <StatCard
          icon={TrendingDown}
          label="Train Impact"
          value="8%"
          description="Reduced operational disruption"
        />

        <StatCard
          icon={ShieldCheck}
          label="Asset Availability"
          value="93%"
          description="Critical infrastructure availability"
        />

        <StatCard
          icon={BrainCircuit}
          label="AI Optimization"
          value="94%"
          description="Average planning confidence"
        />
      </div>

      {/* BEFORE VS AFTER */}
      <ChartCard
        title="Manual Planning vs AI-Optimized Planning"
        description="Key operational indicators before and after AI-assisted coordination."
      >
        <div className="h-[360px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={beforeAfterData}
              margin={{
                top: 10,
                right: 10,
                left: 0,
                bottom: 10,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" vertical={false} />

              <XAxis
                dataKey="metric"
                tick={{ fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />

              <YAxis
                domain={[0, 100]}
                tick={{ fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />

              <Tooltip />

              <Legend />

              <Bar
                dataKey="Before"
                fill="#94a3b8"
                radius={[6, 6, 0, 0]}
                barSize={28}
              />

              <Bar
                dataKey="After"
                fill="#2563eb"
                radius={[6, 6, 0, 0]}
                barSize={28}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </ChartCard>

      {/* TWO CHARTS */}
      <div className="grid gap-6 xl:grid-cols-2">
        <ChartCard
          title="Weekly Planning Efficiency"
          description="Number of maintenance tasks handled through optimized scheduling."
        >
          <div className="h-[310px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />

                <XAxis
                  dataKey="week"
                  tick={{ fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                />

                <YAxis
                  tick={{ fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                />

                <Tooltip />

                <Legend />

                <Bar
                  dataKey="Planned"
                  fill="#cbd5e1"
                  radius={[5, 5, 0, 0]}
                />

                <Bar
                  dataKey="Optimized"
                  fill="#2563eb"
                  radius={[5, 5, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard
          title="Block Saving Trend"
          description="Cumulative block hours saved through AI-assisted planning."
        >
          <div className="h-[310px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={savingsData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />

                <XAxis
                  dataKey="month"
                  tick={{ fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                />

                <YAxis
                  tick={{ fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="saving"
                  stroke="#2563eb"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* DEPARTMENT + PIE */}
      <div className="grid gap-6 xl:grid-cols-3">
        <ChartCard
          title="Department Block Utilization"
          description="Current utilization across maintenance departments."
        >
          <div className="space-y-5">
            {departmentData.map((department) => (
              <div key={department.name}>
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-sm font-semibold text-slate-700">
                    {department.name}
                  </span>

                  <span className="text-sm font-bold text-slate-900">
                    {department.value}%
                  </span>
                </div>

                <div className="h-3 overflow-hidden rounded-full bg-slate-100">
                  <div
                    className="h-full rounded-full bg-blue-600 transition-all"
                    style={{ width: `${department.value}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </ChartCard>

        <div className="xl:col-span-2">
          <ChartCard
            title="Maintenance Workload Distribution"
            description="Distribution of planned maintenance activities by department."
          >
            <div className="grid items-center gap-4 md:grid-cols-2">
              <div className="h-[250px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={pieData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius={90}
                      innerRadius={52}
                      paddingAngle={3}
                    >
                      {pieData.map((entry, index) => (
                        <Cell
                          key={entry.name}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Pie>

                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="space-y-4">
                {pieData.map((item, index) => (
                  <div
                    key={item.name}
                    className="flex items-center justify-between rounded-xl bg-slate-50 px-4 py-3"
                  >
                    <div className="flex items-center gap-3">
                      <span
                        className="h-3 w-3 rounded-full"
                        style={{
                          backgroundColor: COLORS[index],
                        }}
                      />

                      <span className="text-sm font-semibold text-slate-700">
                        {item.name}
                      </span>
                    </div>

                    <span className="text-sm font-bold text-slate-900">
                      {item.value}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </ChartCard>
        </div>
      </div>

      {/* AI IMPACT SUMMARY */}
      <div className="overflow-hidden rounded-2xl bg-slate-900 text-white shadow-lg">
        <div className="grid gap-0 lg:grid-cols-[1.4fr_1fr_1fr_1fr]">
          <div className="p-6">
            <div className="flex items-center gap-2">
              <div className="rounded-lg bg-blue-500/20 p-2 text-blue-300">
                <BrainCircuit size={20} />
              </div>

              <span className="text-xs font-bold uppercase tracking-wider text-blue-300">
                AI Impact Summary
              </span>
            </div>

            <h2 className="mt-4 text-xl font-bold">
              Smarter blocks. Less disruption.
            </h2>

            <p className="mt-2 max-w-xl text-sm leading-6 text-slate-400">
              The AI planner combines maintenance urgency, asset criticality,
              corridor availability and train movement forecasts to create
              coordinated maintenance blocks.
            </p>
          </div>

          <div className="border-t border-slate-700 p-6 lg:border-l lg:border-t-0">
            <p className="text-xs font-semibold uppercase text-slate-500">
              Block Waste Reduced
            </p>

            <p className="mt-2 text-3xl font-bold text-white">28%</p>

            <p className="mt-1 text-xs text-emerald-400">
              More efficient corridor usage
            </p>
          </div>

          <div className="border-t border-slate-700 p-6 lg:border-l lg:border-t-0">
            <p className="text-xs font-semibold uppercase text-slate-500">
              Asset Downtime
            </p>

            <p className="mt-2 text-3xl font-bold text-white">−19%</p>

            <p className="mt-1 text-xs text-emerald-400">
              Faster coordinated maintenance
            </p>
          </div>

          <div className="border-t border-slate-700 p-6 lg:border-l lg:border-t-0">
            <p className="text-xs font-semibold uppercase text-slate-500">
              Train Reliability
            </p>

            <p className="mt-2 text-3xl font-bold text-white">+12%</p>

            <p className="mt-1 text-xs text-emerald-400">
              Lower maintenance-related impact
            </p>
          </div>
        </div>
      </div>

      {/* FOOTER INSIGHT */}
      <div className="flex flex-col gap-3 rounded-2xl border border-blue-100 bg-blue-50 p-5 sm:flex-row sm:items-center">
        <div className="rounded-xl bg-white p-3 text-blue-600 shadow-sm">
          <TrainFront size={22} />
        </div>

        <div>
          <p className="text-sm font-bold text-blue-900">
            AI-generated operational insight
          </p>

          <p className="mt-1 text-sm text-blue-700">
            Coordinating Engineering, Traction and S&T activities within the
            same corridor block can save approximately{" "}
            <strong>2.4 hours</strong> while maintaining low train impact.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Analytics;