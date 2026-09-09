import { useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  Clock3,
  Gauge,
  Map,
  Route,
  TrainFront,
  Wrench,
  Zap,
} from "lucide-react";

const corridorData = [
  {
    code: "BZA-EE",
    name: "Vijayawada – Eluru",
    status: "Available",
    availability: 92,
    block: "10:00 – 12:30",
    trains: 18,
    distance: 65,
    utilization: 78,
    departments: ["Engineering", "Traction", "S&T"],
  },
  {
    code: "EE-TDD",
    name: "Eluru – Tadepalligudem",
    status: "Restricted",
    availability: 71,
    block: "14:00 – 16:00",
    trains: 14,
    distance: 54,
    utilization: 64,
    departments: ["Engineering"],
  },
  {
    code: "TDD-NDD",
    name: "Tadepalligudem – Nidadavolu",
    status: "Available",
    availability: 88,
    block: "11:30 – 13:00",
    trains: 11,
    distance: 38,
    utilization: 52,
    departments: ["S&T"],
  },
  {
    code: "NDD-RJY",
    name: "Nidadavolu – Rajahmundry",
    status: "Blocked",
    availability: 35,
    block: "18:00 – 20:00",
    trains: 16,
    distance: 42,
    utilization: 91,
    departments: ["Traction"],
  },
  {
    code: "RJY-DWP",
    name: "Rajahmundry – Dwarapudi",
    status: "Available",
    availability: 95,
    block: "09:00 – 11:00",
    trains: 12,
    distance: 48,
    utilization: 46,
    departments: ["Engineering"],
  },
  {
    code: "DWP-SLO",
    name: "Dwarapudi – Samalkot",
    status: "Available",
    availability: 89,
    block: "12:00 – 14:00",
    trains: 15,
    distance: 31,
    utilization: 58,
    departments: ["S&T", "Traction"],
  },
  {
    code: "SLO-ANV",
    name: "Samalkot – Annavaram",
    status: "Restricted",
    availability: 68,
    block: "15:00 – 17:00",
    trains: 17,
    distance: 46,
    utilization: 73,
    departments: ["Engineering", "Traction"],
  },
  {
    code: "ANV-TUNI",
    name: "Annavaram – Tuni",
    status: "Available",
    availability: 91,
    block: "10:30 – 12:00",
    trains: 10,
    distance: 29,
    utilization: 49,
    departments: ["Engineering"],
  },
  {
    code: "TUNI-ANAK",
    name: "Tuni – Anakapalle",
    status: "Available",
    availability: 86,
    block: "13:00 – 15:00",
    trains: 13,
    distance: 52,
    utilization: 61,
    departments: ["S&T"],
  },
  {
    code: "ANAK-VSKP",
    name: "Anakapalle – Visakhapatnam",
    status: "Restricted",
    availability: 74,
    block: "16:00 – 18:00",
    trains: 21,
    distance: 28,
    utilization: 81,
    departments: ["Engineering", "S&T"],
  },
  {
    code: "VSKP-KTV",
    name: "Visakhapatnam – Kottavalasa",
    status: "Available",
    availability: 93,
    block: "08:30 – 10:30",
    trains: 19,
    distance: 34,
    utilization: 55,
    departments: ["Traction"],
  },
  {
    code: "KTV-VZM",
    name: "Kottavalasa – Vizianagaram",
    status: "Available",
    availability: 90,
    block: "11:00 – 13:00",
    trains: 16,
    distance: 42,
    utilization: 59,
    departments: ["Engineering", "Traction"],
  },
];

const timeline = [
  {
    time: "08:00",
    title: "Routine Inspection",
    corridor: "BZA–EE",
    department: "Engineering",
    status: "Completed",
  },
  {
    time: "10:00",
    title: "Signal Relay Maintenance",
    corridor: "BZA–EE",
    department: "S&T",
    status: "Upcoming",
  },
  {
    time: "11:00",
    title: "Track + Transformer Work",
    corridor: "BZA–EE",
    department: "Engineering + Traction",
    status: "AI Optimized",
  },
  {
    time: "14:00",
    title: "Track Inspection",
    corridor: "EE–TDD",
    department: "Engineering",
    status: "Scheduled",
  },
  {
    time: "18:00",
    title: "Traction Maintenance Block",
    corridor: "NDD–RJY",
    department: "Traction",
    status: "Blocked",
  },
];

const networkNodes = [
  { code: "BZA", name: "Vijayawada", x: 5 },
  { code: "EE", name: "Eluru", x: 13 },
  { code: "TDD", name: "Tadepalligudem", x: 23 },
  { code: "NDD", name: "Nidadavolu", x: 33 },
  { code: "RJY", name: "Rajahmundry", x: 43 },
  { code: "DWP", name: "Dwarapudi", x: 53 },
  { code: "SLO", name: "Samalkot", x: 63 },
  { code: "ANV", name: "Annavaram", x: 73 },
  { code: "TUNI", name: "Tuni", x: 83 },
  { code: "ANAK", name: "Anakapalle", x: 93 },
];

const networkConnections = [
  { from: "BZA", to: "EE", status: "Available" },
  { from: "EE", to: "TDD", status: "Restricted" },
  { from: "TDD", to: "NDD", status: "Available" },
  { from: "NDD", to: "RJY", status: "Blocked" },
  { from: "RJY", to: "DWP", status: "Available" },
  { from: "DWP", to: "SLO", status: "Available" },
  { from: "SLO", to: "ANV", status: "Restricted" },
  { from: "ANV", to: "TUNI", status: "Available" },
  { from: "TUNI", to: "ANAK", status: "Available" },
];

function statusClasses(status) {
  if (status === "Available") {
    return "bg-emerald-50 text-emerald-700 border-emerald-200";
  }

  if (status === "Restricted") {
    return "bg-amber-50 text-amber-700 border-amber-200";
  }

  return "bg-red-50 text-red-700 border-red-200";
}

function statusDot(status) {
  if (status === "Available") return "bg-emerald-500";
  if (status === "Restricted") return "bg-amber-500";
  return "bg-red-500";
}

export default function Corridors() {
  const [selectedCorridor, setSelectedCorridor] = useState("BZA-EE");
  const [statusFilter, setStatusFilter] = useState("All");

  const filteredCorridors = useMemo(() => {
    if (statusFilter === "All") return corridorData;

    return corridorData.filter(
      (corridor) => corridor.status === statusFilter
    );
  }, [statusFilter]);

  const selected = corridorData.find(
    (corridor) => corridor.code === selectedCorridor
  );

  const total = corridorData.length;
  const available = corridorData.filter(
    (item) => item.status === "Available"
  ).length;
  const restricted = corridorData.filter(
    (item) => item.status === "Restricted"
  ).length;
  const blocked = corridorData.filter(
    (item) => item.status === "Blocked"
  ).length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-blue-600">
            <Route size={17} />
            Railway Corridor Control
          </div>

          <h1 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
            Corridor Status
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Monitor corridor availability, maintenance blocks and train
            movement impact.
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3">
          <Activity size={17} className="text-emerald-600" />
          <span className="text-sm font-semibold text-emerald-700">
            Network Operational
          </span>
        </div>
      </div>

      {/* Filter */}
      <div className="flex flex-wrap gap-2">
        {["All", "Available", "Restricted", "Blocked"].map((filter) => (
          <button
            key={filter}
            onClick={() => setStatusFilter(filter)}
            className={`rounded-xl border px-4 py-2 text-sm font-semibold transition ${
              statusFilter === filter
                ? "border-blue-600 bg-blue-600 text-white"
                : "border-slate-200 bg-white text-slate-600 hover:border-blue-300 hover:text-blue-600"
            }`}
          >
            {filter} Corridors
          </button>
        ))}
      </div>

      {/* Summary */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryCard
          title="Total Corridors"
          value={total}
          subtitle="Monitored"
          icon={Map}
          iconBg="bg-blue-50"
          iconColor="text-blue-600"
        />

        <SummaryCard
          title="Available"
          value={available}
          subtitle="Normal operation"
          icon={CheckCircle2}
          iconBg="bg-emerald-50"
          iconColor="text-emerald-600"
        />

        <SummaryCard
          title="Restricted"
          value={restricted}
          subtitle="Limited capacity"
          icon={AlertTriangle}
          iconBg="bg-amber-50"
          iconColor="text-amber-600"
        />

        <SummaryCard
          title="Blocked"
          value={blocked}
          subtitle="Maintenance block"
          icon={Wrench}
          iconBg="bg-red-50"
          iconColor="text-red-600"
        />
      </div>

      {/* Interactive Network */}
      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 p-5">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="flex items-center gap-2">
                <Map size={19} className="text-blue-600" />
                <h2 className="font-bold text-slate-900">
                  Live Railway Network
                </h2>
              </div>

              <p className="mt-1 text-xs text-slate-500">
                Corridor availability and operational flow
              </p>
            </div>

            <div className="flex flex-wrap gap-3 text-xs font-medium">
              <Legend color="bg-emerald-500" label="Available" />
              <Legend color="bg-amber-500" label="Restricted" />
              <Legend color="bg-red-500" label="Blocked" />
            </div>
          </div>
        </div>

        <div className="overflow-x-auto p-6">
          <div className="relative min-w-[850px] py-12">
            {/* Railway line */}
            <div className="absolute left-[5%] right-[7%] top-[77px] h-1 rounded-full bg-slate-200" />

            <div className="absolute left-[5%] right-[7%] top-[73px] h-0.5 border-t-2 border-dashed border-slate-400" />

            {/* Connections */}
            {networkConnections.map((connection) => {
              const from = networkNodes.find(
                (node) => node.code === connection.from
              );
              const to = networkNodes.find(
                (node) => node.code === connection.to
              );

              return (
                <div
                  key={`${connection.from}-${connection.to}`}
                  className="absolute top-[73px] h-2"
                  style={{
                    left: `${from.x}%`,
                    width: `${to.x - from.x}%`,
                  }}
                >
                  <div
                    className={`h-2 rounded-full ${
                      connection.status === "Available"
                        ? "bg-emerald-400"
                        : connection.status === "Restricted"
                        ? "bg-amber-400"
                        : "bg-red-500"
                    }`}
                  />
                </div>
              );
            })}

            {/* Nodes */}
            {networkNodes.map((node, index) => {
              const connection = networkConnections[index];
              const status = connection?.status || "Available";

              return (
                <button
                  key={node.code}
                  onClick={() => {
                    const matching = corridorData.find((item) =>
                      item.code.startsWith(node.code)
                    );

                    if (matching) {
                      setSelectedCorridor(matching.code);
                      window.scrollTo({ top: 0, behavior: "smooth" });
                    }
                  }}
                  className="absolute top-0 -translate-x-1/2 text-center"
                  style={{ left: `${node.x}%` }}
                >
                  <div
                    className={`mx-auto flex h-16 w-16 items-center justify-center rounded-full border-4 border-white shadow-lg ${
                      status === "Available"
                        ? "bg-emerald-500"
                        : status === "Restricted"
                        ? "bg-amber-500"
                        : "bg-red-500"
                    }`}
                  >
                    <span className="text-sm font-black text-white">
                      {node.code}
                    </span>
                  </div>

                  <p className="mt-2 whitespace-nowrap text-xs font-bold text-slate-700">
                    {node.name}
                  </p>
                </button>
              );
            })}

            {/* Train */}
            <div className="absolute left-[28%] top-[105px] flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-3 py-2 text-xs font-bold text-blue-700 shadow-sm">
              <TrainFront size={15} />
              12728 Express
              <ArrowRight size={14} />
            </div>

            {/* Conflict */}
            <div className="absolute left-[46%] top-[105px] flex items-center gap-2 rounded-full border border-red-200 bg-red-50 px-3 py-2 text-xs font-bold text-red-700 shadow-sm">
              <AlertTriangle size={14} />
              Conflict
            </div>
          </div>
        </div>

        {/* AI recommendation */}
        <div className="border-t border-blue-100 bg-blue-50/70 p-5">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-600 text-white">
                <BrainCircuit size={21} />
              </div>

              <div>
                <p className="text-sm font-bold text-slate-900">
                  AI Network Recommendation
                </p>

                <p className="mt-1 max-w-3xl text-sm leading-6 text-slate-600">
                  Combine Engineering, Traction and S&T maintenance activities
                  on the BZA–EE corridor during the 10:00–12:30 block window.
                  This reduces duplicate blocks and keeps train impact low.
                </p>
              </div>
            </div>

            <div className="shrink-0 rounded-xl border border-blue-200 bg-white px-4 py-3 text-center">
              <p className="text-xs font-semibold text-slate-500">
                AI Confidence
              </p>
              <p className="text-xl font-black text-blue-600">94%</p>
            </div>
          </div>
        </div>
      </section>

      {/* Corridor Cards */}
      <section>
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              Corridor Availability
            </h2>
            <p className="text-sm text-slate-500">
              Select a corridor to inspect operational details.
            </p>
          </div>

          <span className="text-xs font-semibold text-slate-400">
            {filteredCorridors.length} corridors
          </span>
        </div>

        <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
          {filteredCorridors.map((corridor) => {
            const selectedCard = selectedCorridor === corridor.code;

            return (
              <button
                key={corridor.code}
                onClick={() => setSelectedCorridor(corridor.code)}
                className={`text-left rounded-2xl border bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md ${
                  selectedCard
                    ? "border-blue-500 ring-2 ring-blue-100"
                    : "border-slate-200"
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-3">
                    <div
                      className={`mt-1 h-3 w-3 rounded-full ${statusDot(
                        corridor.status
                      )}`}
                    />

                    <div>
                      <p className="text-sm font-black tracking-wide text-slate-900">
                        {corridor.code}
                      </p>

                      <h3 className="mt-1 text-lg font-bold text-slate-800">
                        {corridor.name}
                      </h3>
                    </div>
                  </div>

                  <span
                    className={`rounded-full border px-3 py-1 text-xs font-bold ${statusClasses(
                      corridor.status
                    )}`}
                  >
                    {corridor.status}
                  </span>
                </div>

                <div className="mt-5">
                  <div className="mb-2 flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-500">
                      Corridor Availability
                    </span>

                    <span className="text-sm font-black text-slate-800">
                      {corridor.availability}%
                    </span>
                  </div>

                  <div className="h-2 overflow-hidden rounded-full bg-slate-100">
                    <div
                      className={`h-full rounded-full ${
                        corridor.availability >= 85
                          ? "bg-emerald-500"
                          : corridor.availability >= 60
                          ? "bg-amber-500"
                          : "bg-red-500"
                      }`}
                      style={{ width: `${corridor.availability}%` }}
                    />
                  </div>
                </div>

                <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
                  <InfoItem
                    icon={Clock3}
                    label="Next Block"
                    value={corridor.block}
                  />
                  <InfoItem
                    icon={TrainFront}
                    label="Trains"
                    value={`${corridor.trains}`}
                  />
                  <InfoItem
                    icon={Route}
                    label="Distance"
                    value={`${corridor.distance} km`}
                  />
                  <InfoItem
                    icon={Gauge}
                    label="Utilization"
                    value={`${corridor.utilization}%`}
                  />
                </div>

                <div className="mt-4 flex flex-wrap gap-2">
                  {corridor.departments.map((department) => (
                    <span
                      key={department}
                      className="rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600"
                    >
                      {department}
                    </span>
                  ))}
                </div>
              </button>
            );
          })}
        </div>
      </section>

      {/* Selected Corridor */}
      {selected && (
        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <div className="flex items-center gap-2 text-sm font-semibold text-blue-600">
                <Route size={17} />
                Selected Corridor
              </div>

              <h2 className="mt-2 text-2xl font-black text-slate-900">
                {selected.name}
              </h2>

              <p className="mt-1 text-xs text-slate-400">
                Corridor code: {selected.code}
              </p>
            </div>

            <span
              className={`w-fit rounded-full border px-4 py-2 text-sm font-bold ${statusClasses(
                selected.status
              )}`}
            >
              {selected.status}
            </span>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <DetailCard
              label="Availability"
              value={`${selected.availability}%`}
              subtitle="Infrastructure available"
              icon={Gauge}
            />

            <DetailCard
              label="Train Movement"
              value={selected.trains}
              subtitle="Scheduled trains"
              icon={TrainFront}
            />

            <DetailCard
              label="Next Block"
              value={selected.block}
              subtitle="Planned maintenance window"
              icon={Clock3}
            />
          </div>
        </section>
      )}

      {/* Timeline */}
      <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-6">
          <h2 className="text-lg font-bold text-slate-900">
            Today's Corridor Timeline
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Maintenance blocks and corridor activities
          </p>
        </div>

        <div className="relative">
          <div className="absolute bottom-0 left-[34px] top-0 w-px bg-slate-200" />

          <div className="space-y-5">
            {timeline.map((item) => (
              <div key={`${item.time}-${item.title}`} className="relative flex gap-4">
                <div className="relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border-4 border-white bg-blue-600 text-[10px] font-black text-white shadow-sm">
                  {item.time}
                </div>

                <div className="flex-1 rounded-xl border border-slate-200 bg-slate-50 p-4">
                  <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                      <p className="text-sm font-bold text-slate-900">
                        {item.title}
                      </p>

                      <p className="mt-1 text-xs text-slate-500">
                        {item.corridor} · {item.department}
                      </p>
                    </div>

                    <span className="w-fit rounded-full bg-white px-3 py-1 text-xs font-bold text-slate-600 shadow-sm">
                      {item.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Insight */}
      <section className="rounded-2xl border border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 p-5 shadow-sm">
        <div className="flex gap-4">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm">
            <BrainCircuit size={22} />
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-3">
              <h2 className="font-bold text-slate-900">
                AI Corridor Insight
              </h2>

              <span className="rounded-full bg-white px-3 py-1 text-xs font-black text-blue-600">
                94% Confidence
              </span>
            </div>

            <p className="mt-2 max-w-5xl text-sm leading-6 text-slate-600">
              The Vijayawada–Eluru corridor currently provides the best
              opportunity for coordinated maintenance. Combining Engineering,
              Traction and S&T activities in the 10:00–12:30 window can reduce
              duplicate blocks while maintaining low train-operation impact.
            </p>

            <div className="mt-4 flex flex-wrap gap-3">
              <InsightBadge
                icon={Clock3}
                text="2.4 hrs block saving"
              />
              <InsightBadge
                icon={TrainFront}
                text="Low train impact"
              />
              <InsightBadge
                icon={Zap}
                text="Multi-department"
              />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function SummaryCard({
  title,
  value,
  subtitle,
  icon: Icon,
  iconBg,
  iconColor,
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="mt-2 text-3xl font-black text-slate-900">{value}</p>
          <p className="mt-1 text-xs text-slate-400">{subtitle}</p>
        </div>

        <div
          className={`flex h-11 w-11 items-center justify-center rounded-xl ${iconBg} ${iconColor}`}
        >
          <Icon size={21} />
        </div>
      </div>
    </div>
  );
}

function InfoItem({ icon: Icon, label, value }) {
  return (
    <div className="rounded-xl bg-slate-50 p-3">
      <Icon size={16} className="text-slate-400" />
      <p className="mt-2 text-[11px] font-medium text-slate-400">{label}</p>
      <p className="mt-0.5 text-xs font-bold text-slate-700">{value}</p>
    </div>
  );
}

function DetailCard({ label, value, subtitle, icon: Icon }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
      <div className="flex items-center gap-2 text-slate-400">
        <Icon size={17} />
        <span className="text-xs font-semibold">{label}</span>
      </div>

      <p className="mt-3 text-2xl font-black text-slate-900">{value}</p>
      <p className="mt-1 text-xs text-slate-500">{subtitle}</p>
    </div>
  );
}

function Legend({ color, label }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className={`h-2.5 w-2.5 rounded-full ${color}`} />
      {label}
    </div>
  );
}

function InsightBadge({ icon: Icon, text }) {
  return (
    <div className="flex items-center gap-2 rounded-lg border border-blue-100 bg-white px-3 py-2 text-xs font-semibold text-slate-600">
      <Icon size={14} className="text-blue-600" />
      {text}
    </div>
  );
}