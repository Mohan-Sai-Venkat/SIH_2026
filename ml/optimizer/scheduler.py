from ortools.sat.python import cp_model
import pandas as pd
import math


AI_FILE = "data/prioritized_tasks.csv"
MAINTENANCE_FILE = "data/integrated_maintenance.csv"
OUTPUT_FILE = "data/final_schedule.csv"


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    ai_data = pd.read_csv(AI_FILE)

    maintenance_data = pd.read_csv(
        MAINTENANCE_FILE
    )

    data = maintenance_data.merge(
        ai_data[
            [
                "task_id",
                "rank",
                "priority_level",
                "priority_score"
            ]
        ],
        on="task_id",
        how="inner"
    )

    print()
    print("=" * 70)
    print("RAILWAY AUTOMATIC BLOCK PLANNING & OPTIMIZATION")
    print("=" * 70)

    print()
    print("Maintenance tasks:", len(maintenance_data))
    print("AI priority tasks:", len(ai_data))
    print("Tasks for optimization:", len(data))

    return data


# ============================================================
# TIME CONVERSION
# ============================================================

def time_to_minutes(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    try:
        hour, minute = value.split(":")[:2]

        return int(hour) * 60 + int(minute)

    except Exception:
        return None


def minutes_to_time(minutes):

    hour = minutes // 60
    minute = minutes % 60

    return f"{hour:02d}:{minute:02d}"


# ============================================================
# PREPARE TASKS
# ============================================================

def prepare_tasks(data):

    tasks = []

    for _, row in data.iterrows():

        duration_minutes = int(
            row["maintenance_duration"]
        )

        duration_minutes = max(
            duration_minutes,
            30
        )

        requested_start = time_to_minutes(
            row["requested_start"]
        )

        requested_end = time_to_minutes(
            row["requested_end"]
        )

        # If a valid requested window exists,
        # use it as the preferred time.
        if (
            requested_start is not None
            and requested_end is not None
        ):
            preferred_start = requested_start

        else:
            # Default planning start
            preferred_start = 8 * 60

        task = {

            "task_id":
                row["task_id"],

            "department":
                row["department"],

            "section_id":
                row["section_id"],

            "maintenance_type":
                row["maintenance_type"],

            "duration":
                duration_minutes,

            "priority_level":
                row["priority_level"],

            "priority_score":
                float(row["priority_score"]),

            "rank":
                int(row["rank"]),

            "requested_start":
                requested_start,

            "requested_end":
                requested_end,

            "preferred_start":
                preferred_start,

            "start_location":
                row["start_location"],

            "end_location":
                row["end_location"],

            "train_count":
                0
                if pd.isna(row["train_count"])
                else float(row["train_count"]),

            "high_priority_train_count":
                0
                if pd.isna(
                    row["high_priority_train_count"]
                )
                else float(
                    row["high_priority_train_count"]
                )
        }

        tasks.append(task)

    return tasks


# ============================================================
# OPTIMIZATION
# ============================================================

def generate_schedule():

    data = load_data()

    tasks = prepare_tasks(data)

    model = cp_model.CpModel()

    start_vars = {}
    end_vars = {}

    # Planning horizon:
    # 00:00 to 24:00
    DAY_START = 0
    DAY_END = 24 * 60

    # --------------------------------------------------------
    # CREATE VARIABLES
    # --------------------------------------------------------

    for task in tasks:

        task_id = task["task_id"]

        duration = task["duration"]

        start_vars[task_id] = model.NewIntVar(
            DAY_START,
            DAY_END - duration,
            f"start_{task_id}"
        )

        end_vars[task_id] = model.NewIntVar(
            DAY_START + duration,
            DAY_END,
            f"end_{task_id}"
        )

        model.Add(
            end_vars[task_id]
            ==
            start_vars[task_id] + duration
        )

    # --------------------------------------------------------
    # SAME SECTION = NO OVERLAP
    # --------------------------------------------------------

    sections = {}

    for task in tasks:

        section = task["section_id"]

        if section not in sections:
            sections[section] = []

        sections[section].append(
            task
        )

    print()
    print("Sections found:", len(sections))

    for section, section_tasks in sections.items():

        print(
            f"Section {section}: "
            f"{len(section_tasks)} tasks"
        )

        for i in range(
            len(section_tasks)
        ):

            for j in range(
                i + 1,
                len(section_tasks)
            ):

                task1 = section_tasks[i]
                task2 = section_tasks[j]

                id1 = task1["task_id"]
                id2 = task2["task_id"]

                before_1 = model.NewBoolVar(
                    f"{id1}_before_{id2}"
                )

                before_2 = model.NewBoolVar(
                    f"{id2}_before_{id1}"
                )

                model.AddBoolOr([
                    before_1,
                    before_2
                ])

                model.Add(
                    end_vars[id1]
                    <= start_vars[id2]
                ).OnlyEnforceIf(
                    before_1
                )

                model.Add(
                    end_vars[id2]
                    <= start_vars[id1]
                ).OnlyEnforceIf(
                    before_2
                )

    # --------------------------------------------------------
    # OBJECTIVE
    # --------------------------------------------------------
    #
    # Priority tasks should be scheduled earlier.
    #
    # We also keep tasks reasonably close to their
    # requested start time when possible.
    # --------------------------------------------------------

    objective_terms = []

    for task in tasks:

        task_id = task["task_id"]

        priority_weight = max(
            1,
            int(
                task["priority_score"] * 100
            )
        )

        # Higher priority gets stronger
        # preference for earlier scheduling.
        objective_terms.append(
            priority_weight
            * start_vars[task_id]
        )

        # Small penalty for moving away
        # from requested/preferred time.
        preferred = task[
            "preferred_start"
        ]

        deviation = model.NewIntVar(
            0,
            DAY_END,
            f"deviation_{task_id}"
        )

        model.AddAbsEquality(
            deviation,
            start_vars[task_id]
            - preferred
        )

        objective_terms.append(
            deviation
        )

    model.Minimize(
        sum(objective_terms)
    )

    # --------------------------------------------------------
    # SOLVE
    # --------------------------------------------------------

    print()
    print(
        "Starting OR-Tools optimization..."
    )

    solver = cp_model.CpSolver()

    solver.parameters.max_time_in_seconds = 30

    solver.parameters.num_search_workers = 8

    status = solver.Solve(model)

    print()
    print(
        "Solver status:",
        solver.StatusName(status)
    )

    if status not in [
        cp_model.OPTIMAL,
        cp_model.FEASIBLE
    ]:

        print()
        print(
            "No feasible schedule found."
        )

        return None

    # --------------------------------------------------------
    # CREATE RESULT
    # --------------------------------------------------------

    final_schedule = []

    print()
    print("=" * 70)
    print("OPTIMIZED MAINTENANCE SCHEDULE")
    print("=" * 70)

    for task in tasks:

        task_id = task["task_id"]

        start = solver.Value(
            start_vars[task_id]
        )

        end = solver.Value(
            end_vars[task_id]
        )

        result = {

            "task_id":
                task_id,

            "department":
                task["department"],

            "section_id":
                task["section_id"],

            "maintenance_type":
                task["maintenance_type"],

            "start_location":
                task["start_location"],

            "end_location":
                task["end_location"],

            "block_id":
                f"BLOCK-{task['section_id']}",

            "start_time":
                minutes_to_time(start),

            "end_time":
                minutes_to_time(end),

            "duration_minutes":
                task["duration"],

            "priority_level":
                task["priority_level"],

            "priority_score":
                round(
                    task["priority_score"],
                    2
                ),

            "train_count":
                task["train_count"],

            "high_priority_train_count":
                task[
                    "high_priority_train_count"
                ]
        }

        final_schedule.append(
            result
        )

        print(
            f"{task_id:8} | "
            f"{task['section_id']:3} | "
            f"{result['block_id']:10} | "
            f"{result['start_time']} - "
            f"{result['end_time']} | "
            f"{task['priority_level']:8} | "
            f"{task['priority_score']:.2f}"
        )

    # --------------------------------------------------------
    # SORT BY START TIME
    # --------------------------------------------------------

    final_schedule = sorted(
        final_schedule,
        key=lambda x: (
            x["start_time"],
            x["section_id"]
        )
    )

    schedule_df = pd.DataFrame(
        final_schedule
    )

    schedule_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("=" * 70)
    print("SCHEDULE GENERATION SUCCESSFUL")
    print("=" * 70)

    print()
    print(
        "Tasks scheduled:",
        len(schedule_df)
    )

    print(
        "Output:",
        OUTPUT_FILE
    )

    return final_schedule


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    generate_schedule()