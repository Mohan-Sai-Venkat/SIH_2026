import { useState } from "react";
import {
  BrainCircuit,
  CheckCircle2,
  Clock3,
  Route,
  ShieldAlert,
  Sparkles,
  TrainFront,
  Wrench,
  Zap,
  Loader2,
  AlertTriangle,
  MapPin,
} from "lucide-react";

const tasks = [
  {
    id: "MT-1042",
    asset: "Rail Track KM 428/6",
    department: "Engineering",
    corridor: "BZA–EE",
    duration: "2 hrs",
    priority: 96,
    reason: "Safety critical + overdue",
  },
  {
    id: "MT-1038",
    asset: "Transformer TSS-14",
    department: "Traction",
    corridor: "BZA–EE",
    duration: "1.5 hrs",
    priority: 88,
    reason: "High asset impact",
  },
  {
    id: "MT-1029",
    asset: "Signal Relay BZA-22",
    department: "S&T",
    corridor: "BZA–EE",
    duration: "1 hr",
    priority: 79,
    reason: "Upcoming deadline",
  },
];

const generatedSchedule = [
  {
    time: "10:00 – 11:00",
    task: "Signal Relay BZA-22",
    department: "S&T",
    icon: Route,
  },
  {
    time: "11:00 – 12:30",
    task: "Rail Track KM 428/6",
    department: "Engineering",
    icon: Wrench,
  },
  {
    time: "11:00 – 12:30",
    task: "Transformer TSS-14",
    department: "Traction",
    icon: Zap,
  },
];

const timelineItems = [
  {
    time: "09:30",
    title: "Express 12728",
    type: "train",
    status: "Passed",
  },
  {
    time: "10:00",
    title: "AI Maintenance Block",
    type: "block",
    status: "Active",
  },
  {
    time: "11:00",
    title: "Freight Movement",
    type: "conflict",
    status: "Rerouted",
  },
  {
    time: "12:30",
    title: "Block Released",
    type: "release",
    status: "Scheduled",
  },
  {
    time: "13:00",
    title: "Express 17210",
    type: "train",
    status: "Clear",
  },
];

function BlockPlanner() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [planGenerated, setPlanGenerated] = useState(false);

  const generatePlan = () => {
    setIsGenerating(true);
    setPlanGenerated(false);

    setTimeout(() => {
      setIsGenerating(false);
      setPlanGenerated(true);
    }, 1800);
  };

  return (
    <div className="space-y-6">

      {/* HEADER */}
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
        <div>
          <div className="flex items-center gap-2 text-sm font-medium text-blue-600">
            <BrainCircuit size={18} />
            AI Optimization Engine
          </div>

          <h1 className="mt-1 text-2xl font-bold text-slate-900">
            AI Block Planner
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Optimize maintenance activities, corridor blocks and train impact
            using AI-driven scheduling.
          </p>
        </div>

        <button
          onClick={generatePlan}
          disabled={isGenerating}
          className="flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-200 transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {isGenerating ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              Generating Plan...
            </>
          ) : (
            <>
              <Sparkles size={18} />
              Generate AI Plan
            </>
          )}
        </button>
      </div>

      {/* AI STATUS */}
      <div className="rounded-xl border border-blue-200 bg-blue-50 p-5">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-blue-600 p-3 text-white">
              <BrainCircuit size={22} />
            </div>

            <div>
              <h2 className="font-bold text-slate-900">
                AI Decision Engine
              </h2>

              <p className="text-sm text-slate-600">
                Analyzing maintenance urgency, safety, asset impact and train
                movement.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 rounded-full bg-white px-4 py-2 shadow-sm">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-500"></span>

            <span className="text-xs font-bold text-slate-600">
              AI ENGINE ACTIVE
            </span>
          </div>
        </div>
      </div>

      {/* MAINTENANCE ACTIVITIES */}
      <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 p-6">
          <h2 className="font-bold text-slate-900">
            Maintenance Activities
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            High-priority tasks selected for block optimization
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full min-w-[800px] text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-6 py-4">Task</th>
                <th className="px-6 py-4">Asset</th>
                <th className="px-6 py-4">Department</th>
                <th className="px-6 py-4">Corridor</th>
                <th className="px-6 py-4">Duration</th>
                <th className="px-6 py-4">AI Priority</th>
              </tr>
            </thead>

            <tbody>
              {tasks.map((task) => (
                <tr
                  key={task.id}
                  className="border-t border-slate-100 hover:bg-slate-50"
                >
                  <td className="px-6 py-4">
                    <p className="font-bold text-slate-800">
                      {task.id}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      {task.reason}
                    </p>
                  </td>

                  <td className="px-6 py-4 font-medium text-slate-700">
                    {task.asset}
                  </td>

                  <td className="px-6 py-4">
                    <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
                      {task.department}
                    </span>
                  </td>

                  <td className="px-6 py-4 font-medium text-slate-600">
                    {task.corridor}
                  </td>

                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2 text-slate-600">
                      <Clock3 size={15} />
                      {task.duration}
                    </div>
                  </td>

                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-16 overflow-hidden rounded-full bg-slate-100">
                        <div
                          className="h-full rounded-full bg-blue-600"
                          style={{ width: `${task.priority}%` }}
                        />
                      </div>

                      <span className="font-bold text-blue-600">
                        {task.priority}
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* DECISION FACTORS */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">

        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <ShieldAlert className="text-red-500" size={22} />

            <div>
              <p className="text-xs text-slate-500">
                Safety Criticality
              </p>

              <p className="text-xl font-bold text-slate-900">
                35%
              </p>
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <Clock3 className="text-orange-500" size={22} />

            <div>
              <p className="text-xs text-slate-500">
                Urgency
              </p>

              <p className="text-xl font-bold text-slate-900">
                25%
              </p>
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <Wrench className="text-blue-500" size={22} />

            <div>
              <p className="text-xs text-slate-500">
                Asset Impact
              </p>

              <p className="text-xl font-bold text-slate-900">
                20%
              </p>
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <TrainFront className="text-purple-500" size={22} />

            <div>
              <p className="text-xs text-slate-500">
                Train Impact
              </p>

              <p className="text-xl font-bold text-slate-900">
                20%
              </p>
            </div>
          </div>
        </div>

      </div>

      {/* GENERATED PLAN */}
      {planGenerated && (
        <div className="space-y-6">

          {/* SUCCESS */}
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-5">
            <div className="flex items-start gap-3">
              <CheckCircle2
                size={24}
                className="mt-0.5 text-emerald-600"
              />

              <div>
                <h2 className="font-bold text-emerald-900">
                  AI Plan Generated Successfully
                </h2>

                <p className="mt-1 text-sm text-emerald-700">
                  The AI engine found an optimized maintenance window with
                  minimal impact on train operations.
                </p>
              </div>
            </div>
          </div>

          {/* RESULT CARDS */}
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">

            <div className="rounded-xl bg-slate-950 p-6 text-white shadow-sm">
              <p className="text-sm text-slate-400">
                Optimization Score
              </p>

              <div className="mt-3 flex items-end gap-2">
                <span className="text-5xl font-bold">
                  94
                </span>

                <span className="mb-2 text-slate-400">
                  / 100
                </span>
              </div>

              <div className="mt-5 h-3 rounded-full bg-slate-800">
                <div className="h-3 w-[94%] rounded-full bg-blue-500"></div>
              </div>

              <p className="mt-3 text-xs text-slate-400">
                High-confidence optimization
              </p>
            </div>

            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-emerald-100 p-3 text-emerald-600">
                  <Zap size={22} />
                </div>

                <div>
                  <p className="text-sm text-slate-500">
                    Estimated Block Saving
                  </p>

                  <p className="text-3xl font-bold text-slate-900">
                    2.4 hrs
                  </p>
                </div>
              </div>

              <p className="mt-4 text-sm text-slate-500">
                Maintenance activities are combined into a shared corridor
                block.
              </p>
            </div>

            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-blue-100 p-3 text-blue-600">
                  <TrainFront size={22} />
                </div>

                <div>
                  <p className="text-sm text-slate-500">
                    Train Operation Impact
                  </p>

                  <p className="text-3xl font-bold text-emerald-600">
                    Low
                  </p>
                </div>
              </div>

              <p className="mt-4 text-sm text-slate-500">
                Selected window avoids major train movement periods.
              </p>
            </div>

          </div>

          {/* RECOMMENDED BLOCK */}
          <div className="rounded-xl border border-blue-200 bg-white shadow-sm">
            <div className="border-b border-blue-100 bg-blue-50 p-6">
              <div className="flex items-center gap-3">
                <Route className="text-blue-600" size={24} />

                <div>
                  <h2 className="font-bold text-slate-900">
                    Recommended Block
                  </h2>

                  <p className="text-sm text-slate-500">
                    AI-optimized corridor maintenance window
                  </p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-6 p-6 md:grid-cols-3">
              <div>
                <p className="text-xs uppercase text-slate-400">
                  Corridor
                </p>

                <p className="mt-1 text-lg font-bold text-slate-900">
                  Vijayawada – Eluru
                </p>

                <p className="text-sm text-slate-500">
                  BZA–EE
                </p>
              </div>

              <div>
                <p className="text-xs uppercase text-slate-400">
                  Date
                </p>

                <p className="mt-1 text-lg font-bold text-slate-900">
                  10 Sep 2026
                </p>
              </div>

              <div>
                <p className="text-xs uppercase text-slate-400">
                  Block Window
                </p>

                <p className="mt-1 text-lg font-bold text-blue-600">
                  10:00 – 12:30
                </p>
              </div>
            </div>
          </div>

          {/* 🚆 NEW RAILWAY TIMELINE */}
          <div className="rounded-xl border border-slate-200 bg-white shadow-sm">

            <div className="border-b border-slate-200 p-6">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

                <div>
                  <div className="flex items-center gap-2">
                    <TrainFront className="text-blue-600" size={22} />

                    <h2 className="font-bold text-slate-900">
                      Corridor & Train Conflict Timeline
                    </h2>
                  </div>

                  <p className="mt-1 text-sm text-slate-500">
                    AI analysis of train movements against the selected
                    maintenance block.
                  </p>
                </div>

                <div className="flex items-center gap-4 text-xs font-medium">
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-blue-500"></span>
                    Train
                  </div>

                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-amber-500"></span>
                    Maintenance
                  </div>

                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-red-500"></span>
                    Conflict
                  </div>
                </div>

              </div>
            </div>

            <div className="p-6">

              {/* Corridor */}
              <div className="mb-7">
                <div className="mb-3 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <MapPin size={17} className="text-slate-500" />

                    <span className="text-sm font-bold text-slate-800">
                      BZA
                    </span>
                  </div>

                  <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-700">
                    Corridor Available
                  </span>

                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-slate-800">
                      EE
                    </span>

                    <MapPin size={17} className="text-slate-500" />
                  </div>
                </div>

                <div className="relative h-4 rounded-full bg-slate-200">

                  <div className="absolute left-0 top-0 h-4 w-full rounded-full bg-emerald-200"></div>

                  <div className="absolute left-[28%] top-[-4px] h-6 w-[43%] rounded-full border-2 border-amber-500 bg-amber-100"></div>

                  <div className="absolute left-[48%] top-[-8px] h-8 w-1 rounded-full bg-red-500"></div>

                  <div className="absolute left-[47%] top-[-30px] -translate-x-1/2 whitespace-nowrap rounded-md bg-red-500 px-2 py-1 text-[10px] font-bold text-white">
                    Train Conflict
                  </div>

                </div>

                <div className="mt-2 flex justify-between text-[10px] text-slate-400">
                  <span>KM 0</span>
                  <span>KM 25</span>
                  <span>KM 50</span>
                  <span>KM 75</span>
                  <span>KM 100</span>
                </div>
              </div>

              {/* Time scale */}
              <div className="mb-2 grid grid-cols-6 text-center text-[11px] font-semibold text-slate-400">
                <span>09:00</span>
                <span>10:00</span>
                <span>11:00</span>
                <span>12:00</span>
                <span>13:00</span>
                <span>14:00</span>
              </div>

              {/* Timeline */}
              <div className="relative rounded-xl bg-slate-50 p-5">

                <div className="absolute left-5 right-5 top-[50%] h-px bg-slate-200"></div>

                <div className="relative space-y-5">

                  {timelineItems.map((item, index) => {

                    const isTrain = item.type === "train";
                    const isConflict = item.type === "conflict";
                    const isBlock = item.type === "block";

                    return (
                      <div
                        key={index}
                        className="relative flex items-center gap-4"
                      >

                        <div className="w-16 text-xs font-bold text-slate-500">
                          {item.time}
                        </div>

                        <div
                          className={`flex h-11 flex-1 items-center gap-3 rounded-xl border px-4 ${
                            isTrain
                              ? "border-blue-200 bg-blue-50"
                              : isConflict
                              ? "border-red-200 bg-red-50"
                              : isBlock
                              ? "border-amber-200 bg-amber-50"
                              : "border-emerald-200 bg-emerald-50"
                          }`}
                        >

                          <div
                            className={`rounded-lg p-2 ${
                              isTrain
                                ? "bg-blue-600 text-white"
                                : isConflict
                                ? "bg-red-500 text-white"
                                : isBlock
                                ? "bg-amber-500 text-white"
                                : "bg-emerald-500 text-white"
                            }`}
                          >
                            {isTrain ? (
                              <TrainFront size={17} />
                            ) : isConflict ? (
                              <AlertTriangle size={17} />
                            ) : isBlock ? (
                              <Wrench size={17} />
                            ) : (
                              <CheckCircle2 size={17} />
                            )}
                          </div>

                          <div className="flex-1">
                            <p className="text-sm font-bold text-slate-800">
                              {item.title}
                            </p>

                            <p className="text-[11px] text-slate-500">
                              {item.type === "train"
                                ? "Scheduled train movement"
                                : item.type === "block"
                                ? "AI maintenance window"
                                : item.type === "conflict"
                                ? "AI rerouting applied"
                                : "Corridor returned to operations"}
                            </p>
                          </div>

                          <span
                            className={`rounded-full px-2.5 py-1 text-[10px] font-bold ${
                              isConflict
                                ? "bg-red-100 text-red-700"
                                : isBlock
                                ? "bg-amber-100 text-amber-700"
                                : "bg-emerald-100 text-emerald-700"
                            }`}
                          >
                            {item.status}
                          </span>

                        </div>

                      </div>
                    );
                  })}

                </div>
              </div>

              {/* Conflict Summary */}
              <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-3">

                <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 size={18} className="text-emerald-600" />

                    <p className="text-sm font-bold text-emerald-900">
                      0 Critical Conflicts
                    </p>
                  </div>

                  <p className="mt-1 text-xs text-emerald-700">
                    No major passenger train is blocked.
                  </p>
                </div>

                <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
                  <div className="flex items-center gap-2">
                    <AlertTriangle size={18} className="text-amber-600" />

                    <p className="text-sm font-bold text-amber-900">
                      1 Reroute Applied
                    </p>
                  </div>

                  <p className="mt-1 text-xs text-amber-700">
                    Freight movement shifted outside the block window.
                  </p>
                </div>

                <div className="rounded-xl border border-blue-200 bg-blue-50 p-4">
                  <div className="flex items-center gap-2">
                    <BrainCircuit size={18} className="text-blue-600" />

                    <p className="text-sm font-bold text-blue-900">
                      AI Confidence: 94%
                    </p>
                  </div>

                  <p className="mt-1 text-xs text-blue-700">
                    Schedule satisfies safety and operational constraints.
                  </p>
                </div>

              </div>

            </div>
          </div>

          {/* GENERATED SCHEDULE */}
          <div className="rounded-xl border border-slate-200 bg-white shadow-sm">

            <div className="border-b border-slate-200 p-6">
              <h2 className="font-bold text-slate-900">
                Optimized Maintenance Sequence
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                AI-generated execution order for the selected block
              </p>
            </div>

            <div className="divide-y divide-slate-100">
              {generatedSchedule.map((item, index) => {
                const Icon = item.icon;

                return (
                  <div
                    key={index}
                    className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center"
                  >
                    <div className="w-32 text-sm font-bold text-blue-600">
                      {item.time}
                    </div>

                    <div className="flex flex-1 items-center gap-3">
                      <div className="rounded-lg bg-slate-100 p-2 text-slate-600">
                        <Icon size={19} />
                      </div>

                      <div>
                        <p className="font-semibold text-slate-800">
                          {item.task}
                        </p>

                        <p className="text-xs text-slate-500">
                          {item.department}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 text-xs font-semibold text-emerald-600">
                      <CheckCircle2 size={16} />
                      Optimized
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* AI REASONING */}
          <div className="rounded-xl bg-slate-950 p-6 text-white shadow-sm">

            <div className="flex items-center gap-3">
              <Sparkles className="text-blue-400" size={22} />

              <h2 className="font-bold">
                Why AI Selected This Plan
              </h2>
            </div>

            <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-3">

              <div className="rounded-xl bg-slate-900 p-4">
                <p className="text-sm font-semibold">
                  01. Safety First
                </p>

                <p className="mt-2 text-xs leading-5 text-slate-400">
                  The safety-critical rail track defect receives the highest
                  priority.
                </p>
              </div>

              <div className="rounded-xl bg-slate-900 p-4">
                <p className="text-sm font-semibold">
                  02. Shared Corridor
                </p>

                <p className="mt-2 text-xs leading-5 text-slate-400">
                  Three departmental activities are coordinated within the same
                  corridor block.
                </p>
              </div>

              <div className="rounded-xl bg-slate-900 p-4">
                <p className="text-sm font-semibold">
                  03. Low Train Impact
                </p>

                <p className="mt-2 text-xs leading-5 text-slate-400">
                  The selected time window minimizes disruption to scheduled
                  train operations.
                </p>
              </div>

            </div>
          </div>

        </div>
      )}

    </div>
  );
}

export default BlockPlanner;
