import pandas as pd
from ortools.sat.python import cp_model

from src.optimization.constraints import (
    has_train_conflict,
    has_goods_forecast_conflict
)

from src.optimization.scoring import (
    calculate_window_score,
    calculate_deadline_urgency
)


# ============================================================
# CONFIGURATION
# ============================================================

SOLVER_TIME_LIMIT = 30
NUM_WORKERS = 8


# ============================================================
# MAIN OPTIMIZER
# ============================================================

def optimize_with_cp_sat(
    candidate_windows,
    trains=None,
    goods_forecast=None,
    goods_probability_threshold=0.70
):
    """
    Railway Maintenance Block Optimization.

    The optimizer considers:

    1. Maintenance priority
    2. Criticality
    3. Data Engineering matching score
    4. Block utilization
    5. Unused block time
    6. Deadline urgency
    7. Train conflicts
    8. Goods forecast conflicts
    9. One window per task
    10. Shared block capacity

    NOTE:
    Multi-department consolidation is intentionally
    NOT included in this optimizer.
    """

    # ========================================================
    # 1. VALIDATE INPUT
    # ========================================================

    required_columns = [
        "task_id",
        "department",
        "section_id",
        "priority_score",
        "priority_level",
        "maintenance_duration",
        "window_date",
        "window_start",
        "window_end",
        "window_duration"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in candidate_windows.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    candidates = candidate_windows.copy()

    # ========================================================
    # 2. OPTIONAL INPUTS
    # ========================================================

    if trains is None:
        trains = pd.DataFrame()

    if goods_forecast is None:
        goods_forecast = pd.DataFrame()

    # ========================================================
    # 3. NORMALIZE NUMERIC COLUMNS
    # ========================================================

    numeric_columns = [
        "priority_score",
        "maintenance_duration",
        "window_duration"
    ]

    if "matching_score" in candidates.columns:
        numeric_columns.append(
            "matching_score"
        )

    for column in numeric_columns:

        candidates[column] = pd.to_numeric(
            candidates[column],
            errors="coerce"
        )

    candidates = candidates.dropna(
        subset=[
            "priority_score",
            "maintenance_duration",
            "window_duration"
        ]
    ).copy()

    # matching_score is optional
    if "matching_score" not in candidates.columns:

        candidates["matching_score"] = 0.0

    candidates["matching_score"] = (
        candidates["matching_score"]
        .fillna(0.0)
    )

    # ========================================================
    # 4. REMOVE IMPOSSIBLE WINDOWS
    # ========================================================

    candidates = candidates[
        candidates["maintenance_duration"]
        <= candidates["window_duration"]
    ].copy()

    candidates = candidates.reset_index(
        drop=True
    )

    print(
        "\n===== OPTIMIZATION INPUT ====="
    )

    print(
        f"Candidate windows received: "
        f"{len(candidates)}"
    )

    print(
        f"Tasks received: "
        f"{candidates['task_id'].nunique()}"
    )

    print(
        f"Departments received: "
        f"{candidates['department'].nunique()}"
    )

    # ========================================================
    # 5. CONFLICT FILTERING
    # ========================================================

    feasible_rows = []
    conflict_rows = []

    for index, row in candidates.iterrows():

        # ----------------------------------------------------
        # TRAIN CONFLICT
        # ----------------------------------------------------

        train_conflict = False
        train_id = None

        if not trains.empty:

            (
                train_conflict,
                train_id
            ) = has_train_conflict(
                row,
                trains
            )

        if train_conflict:

            conflict_rows.append({

                "task_id":
                    row["task_id"],

                "reason":
                    "Train conflict with "
                    + str(train_id),

                "window_date":
                    row["window_date"],

                "window_start":
                    row["window_start"],

                "window_end":
                    row["window_end"]
            })

            continue

        # ----------------------------------------------------
        # GOODS FORECAST CONFLICT
        # ----------------------------------------------------

        goods_conflict = False
        forecast_id = None
        probability = None

        if not goods_forecast.empty:

            (
                goods_conflict,
                forecast_id,
                probability
            ) = has_goods_forecast_conflict(

                row,
                goods_forecast,

                probability_threshold=
                    goods_probability_threshold
            )

        if goods_conflict:

            conflict_rows.append({

                "task_id":
                    row["task_id"],

                "reason":
                    "Goods forecast conflict with "
                    + str(forecast_id)
                    + " "
                    + "(probability="
                    + str(probability)
                    + ")",

                "window_date":
                    row["window_date"],

                "window_start":
                    row["window_start"],

                "window_end":
                    row["window_end"]
            })

            continue

        # ----------------------------------------------------
        # FEASIBLE
        # ----------------------------------------------------

        feasible_rows.append(index)

    feasible_candidates = candidates.loc[
        feasible_rows
    ].copy()

    feasible_candidates = (
        feasible_candidates.reset_index(
            drop=True
        )
    )

    conflict_df = pd.DataFrame(
        conflict_rows
    )

    print(
        f"Train/goods conflicts: "
        f"{len(conflict_df)}"
    )

    print(
        f"Feasible windows: "
        f"{len(feasible_candidates)}"
    )

    # ========================================================
    # 6. NO FEASIBLE WINDOWS
    # ========================================================

    if feasible_candidates.empty:

        print(
            "\nNo feasible maintenance "
            "windows available."
        )

        unscheduled_rows = []

        for task_id in candidates[
            "task_id"
        ].unique():

            task_conflicts = conflict_df[
                conflict_df[
                    "task_id"
                ].astype(str)
                ==
                str(task_id)
            ]

            if not task_conflicts.empty:

                reason = "; ".join(
                    task_conflicts[
                        "reason"
                    ].astype(str).tolist()
                )

            else:

                reason = (
                    "No feasible maintenance "
                    "window available"
                )

            unscheduled_rows.append({

                "task_id":
                    task_id,

                "reason":
                    reason
            })

        return (
            pd.DataFrame(),
            pd.DataFrame(
                unscheduled_rows
            )
        )

    # ========================================================
    # 7. CREATE CP-SAT MODEL
    # ========================================================

    model = cp_model.CpModel()

    variables = []

    for index in range(
        len(feasible_candidates)
    ):

        variable = model.NewBoolVar(
            f"select_{index}"
        )

        variables.append(
            variable
        )

    # ========================================================
    # 8. CONSTRAINT:
    # AT MOST ONE WINDOW PER TASK
    # ========================================================

    task_to_indices = {}

    for index, row in feasible_candidates.iterrows():

        task_id = str(
            row["task_id"]
        )

        if task_id not in task_to_indices:

            task_to_indices[
                task_id
            ] = []

        task_to_indices[
            task_id
        ].append(index)

    for task_id, indices in task_to_indices.items():

        model.Add(
            sum(
                variables[index]
                for index in indices
            )
            <= 1
        )

    # ========================================================
    # 9. CONSTRAINT:
    # SHARED BLOCK CAPACITY
    # ========================================================

    block_groups = feasible_candidates.groupby(
        [
            "section_id",
            "window_date",
            "window_start",
            "window_end"
        ]
    )

    for block_key, group in block_groups:

        indices = group.index.tolist()

        capacity = int(
            group[
                "window_duration"
            ].iloc[0]
        )

        model.Add(

            sum(

                int(
                    feasible_candidates.loc[
                        index,
                        "maintenance_duration"
                    ]
                )
                *
                variables[index]

                for index in indices

            )

            <= capacity
        )

    # ========================================================
    # 10. OBJECTIVE FUNCTION
    # ========================================================

    objective_terms = []

    for index, row in feasible_candidates.iterrows():

        deadline = row.get(
            "deadline",
            None
        )

        window_date = row.get(
            "window_date",
            None
        )

        score = calculate_window_score(

            priority_score=float(
                row[
                    "priority_score"
                ]
            ),

            priority_level=str(
                row[
                    "priority_level"
                ]
            ),

            matching_score=float(
                row[
                    "matching_score"
                ]
            ),

            maintenance_duration=float(
                row[
                    "maintenance_duration"
                ]
            ),

            window_duration=float(
                row[
                    "window_duration"
                ]
            ),

            deadline=deadline,

            window_date=window_date
        )

        # CP-SAT requires integer objective values.
        scaled_score = int(
            round(
                score * 100
            )
        )

        objective_terms.append(

            scaled_score
            *
            variables[index]
        )

    # ========================================================
    # 11. MAXIMIZE OBJECTIVE
    # ========================================================

    model.Maximize(
        sum(
            objective_terms
        )
    )

    # ========================================================
    # 12. SOLVER
    # ========================================================

    solver = cp_model.CpSolver()

    solver.parameters.max_time_in_seconds = (
        SOLVER_TIME_LIMIT
    )

    solver.parameters.num_search_workers = (
        NUM_WORKERS
    )

    status = solver.Solve(
        model
    )

    print(
        "\n===== CP-SAT RESULT ====="
    )

    print(
        "Solver status:",
        solver.StatusName(
            status
        )
    )

    # ========================================================
    # 13. SOLVER FAILURE
    # ========================================================

    if status not in [
        cp_model.OPTIMAL,
        cp_model.FEASIBLE
    ]:

        print(
            "Optimizer could not find "
            "a valid schedule."
        )

        unscheduled_rows = []

        for task_id in candidates[
            "task_id"
        ].unique():

            unscheduled_rows.append({

                "task_id":
                    task_id,

                "reason":
                    "No feasible schedule "
                    "found by optimizer"
            })

        return (
            pd.DataFrame(),
            pd.DataFrame(
                unscheduled_rows
            )
        )

    # ========================================================
    # 14. EXTRACT SELECTED WINDOWS
    # ========================================================

    selected_rows = []

    for index, row in feasible_candidates.iterrows():

        if solver.Value(
            variables[index]
        ) != 1:

            continue

        # ----------------------------------------------------
        # DEADLINE
        # ----------------------------------------------------

        deadline = row.get(
            "deadline",
            None
        )

        window_date = row.get(
            "window_date",
            None
        )

        # ----------------------------------------------------
        # FINAL SCORE
        # ----------------------------------------------------

        score = calculate_window_score(

            priority_score=float(
                row[
                    "priority_score"
                ]
            ),

            priority_level=str(
                row[
                    "priority_level"
                ]
            ),

            matching_score=float(
                row[
                    "matching_score"
                ]
            ),

            maintenance_duration=float(
                row[
                    "maintenance_duration"
                ]
            ),

            window_duration=float(
                row[
                    "window_duration"
                ]
            ),

            deadline=deadline,

            window_date=window_date
        )

        # ----------------------------------------------------
        # BLOCK UTILIZATION
        # ----------------------------------------------------

        window_duration = float(
            row[
                "window_duration"
            ]
        )

        maintenance_duration = float(
            row[
                "maintenance_duration"
            ]
        )

        if window_duration > 0:

            utilization = (

                maintenance_duration
                /
                window_duration

            ) * 100

        else:

            utilization = 0

        # ----------------------------------------------------
        # DEADLINE URGENCY
        # ----------------------------------------------------

        deadline_urgency = 0

        if (
            "deadline" in row.index
            and
            pd.notna(
                row[
                    "deadline"
                ]
            )
        ):

            try:

                deadline_urgency = (
                    calculate_deadline_urgency(

                        row[
                            "deadline"
                        ],

                        row[
                            "window_date"
                        ]
                    )
                )

            except Exception:

                deadline_urgency = 0

        # ----------------------------------------------------
        # OPTIMIZATION RANK
        # ----------------------------------------------------

        optimization_rank = row.get(
            "optimization_rank",
            None
        )

        # ----------------------------------------------------
        # SELECTED ROW
        # ----------------------------------------------------

        selected_rows.append({

            # Original identifiers
            "task_id":
                row[
                    "task_id"
                ],

            "department":
                row[
                    "department"
                ],

            "section_id":
                row[
                    "section_id"
                ],

            # Original window fields
            "window_date":
                row[
                    "window_date"
                ],

            "window_start":
                row[
                    "window_start"
                ],

            "window_end":
                row[
                    "window_end"
                ],

            # Fields expected by main.py
            "date":
                row[
                    "window_date"
                ],

            "start_time":
                row[
                    "window_start"
                ],

            "end_time":
                row[
                    "window_end"
                ],

            # Maintenance
            "maintenance_duration":
                row[
                    "maintenance_duration"
                ],

            "window_duration":
                row[
                    "window_duration"
                ],

            # Priority
            "priority_score":
                row[
                    "priority_score"
                ],

            "priority_level":
                row[
                    "priority_level"
                ],

            # Data Engineering
            "matching_score":
                row[
                    "matching_score"
                ],

            "optimization_rank":
                optimization_rank,

            # Deadline
            "deadline":
                deadline,

            "deadline_urgency":
                deadline_urgency,

            # Block efficiency
            "block_utilization":
                round(
                    utilization,
                    2
                ),

            "unused_window_minutes":
                max(
                    int(
                        window_duration
                        -
                        maintenance_duration
                    ),
                    0
                ),

            # Final optimization score
            "optimization_score":
                score
        })

    selected = pd.DataFrame(
        selected_rows
    )

    # ========================================================
    # 15. SORT FINAL SCHEDULE
    # ========================================================

    if not selected.empty:

        selected = selected.sort_values(

            by=[
                "date",
                "start_time"
            ]

        ).reset_index(
            drop=True
        )

    # ========================================================
    # 16. FIND UNSCHEDULED TASKS
    # ========================================================

    scheduled_task_ids = set()

    if not selected.empty:

        scheduled_task_ids = set(

            selected[
                "task_id"
            ].astype(str)

        )

    all_task_ids = set(

        candidates[
            "task_id"
        ].astype(str)

    )

    unscheduled_rows = []

    for task_id in sorted(
        all_task_ids
    ):

        if task_id in scheduled_task_ids:

            continue

        # ----------------------------------------------------
        # CHECK CONFLICT REASONS
        # ----------------------------------------------------

        task_conflicts = conflict_df[

            conflict_df[
                "task_id"
            ].astype(str)

            ==
            str(task_id)
        ]

        if not task_conflicts.empty:

            reason = "; ".join(

                task_conflicts[
                    "reason"
                ]
                .astype(str)
                .tolist()
            )

        else:

            task_candidates = (

                feasible_candidates[

                    feasible_candidates[
                        "task_id"
                    ].astype(str)

                    ==

                    str(task_id)
                ]
            )

            if task_candidates.empty:

                reason = (
                    "No feasible window available"
                )

            else:

                reason = (
                    "Another higher-value "
                    "window was selected for "
                    "the available block capacity"
                )

        unscheduled_rows.append({

            "task_id":
                task_id,

            "reason":
                reason
        })

    unscheduled = pd.DataFrame(
        unscheduled_rows
    )

    # ========================================================
    # 17. FINAL SCHEDULE DISPLAY
    # ========================================================

    print(
        "\n===== FINAL SCHEDULE ====="
    )

    if selected.empty:

        print(
            "No tasks scheduled."
        )

    else:

        for _, row in selected.iterrows():

            print(

                f"{row['task_id']} | "
                f"{row['department']} | "
                f"{row['section_id']} | "
                f"{row['date']} | "
                f"{row['start_time']}-"
                f"{row['end_time']} | "
                f"Score="
                f"{row['optimization_score']}"
            )

    # ========================================================
    # 18. FINAL METRICS
    # ========================================================

    print(
        "\n===== FINAL METRICS ====="
    )

    print(
        "Scheduled tasks:",
        len(selected)
    )

    print(
        "Unscheduled tasks:",
        len(unscheduled)
    )

    if not selected.empty:

        # ----------------------------------------------------
        # TOTAL MAINTENANCE
        # ----------------------------------------------------

        total_maintenance = selected[
            "maintenance_duration"
        ].sum()

        print(

            "Total maintenance time:",

            int(
                total_maintenance
            ),

            "minutes"
        )

        # ----------------------------------------------------
        # CRITICAL TASKS
        # ----------------------------------------------------

        critical_candidates = candidates[

            candidates[
                "priority_level"
            ]
            .astype(str)
            .str.lower()
            ==
            "critical"
        ]

        critical_selected = selected[

            selected[
                "priority_level"
            ]
            .astype(str)
            .str.lower()
            ==
            "critical"
        ]

        critical_total = (

            critical_candidates[
                "task_id"
            ]
            .nunique()
        )

        critical_scheduled = (

            critical_selected[
                "task_id"
            ]
            .nunique()
        )

        print(

            "Critical tasks scheduled:",

            f"{critical_scheduled} / "
            f"{critical_total}"
        )

        # ----------------------------------------------------
        # DEPARTMENTS
        # ----------------------------------------------------

        print(

            "Departments scheduled:",

            selected[
                "department"
            ].nunique()
        )

        # ----------------------------------------------------
        # SECTIONS
        # ----------------------------------------------------

        print(

            "Sections scheduled:",

            selected[
                "section_id"
            ].nunique()
        )

        # ----------------------------------------------------
        # AVERAGE UTILIZATION
        # ----------------------------------------------------

        print(

            "Average block utilization:",

            round(

                selected[
                    "block_utilization"
                ].mean(),

                2
            ),

            "%"
        )

        # ----------------------------------------------------
        # DEADLINE URGENCY
        # ----------------------------------------------------

        print(

            "Total deadline urgency:",

            round(

                selected[
                    "deadline_urgency"
                ].sum(),

                2
            )
        )

    # ========================================================
    # 19. RETURN RESULTS
    # ========================================================

    return (
        selected,
        unscheduled
    )
