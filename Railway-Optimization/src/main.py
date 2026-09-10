import pandas as pd

from src.optimization.optimizer import (
    optimize_with_cp_sat
)

from src.optimization.metrics import (
    calculate_metrics,
    print_metrics
)

from src.optimization.weekly_planner import (
    generate_weekly_plan,
    save_weekly_plan,
    print_weekly_plan
)

from src.optimization.decision_explainer import (
    explain_decisions,
    print_decisions
)


# ============================================================
# INPUT FILES
# ============================================================

CANDIDATE_PATH = (
    "data/input/task_window_matches.csv"
)

HANDOFF_PATH = (
    "data/input/optimization_handoff.csv"
)

TRAIN_PATH = (
    "data/input/trains.csv"
)

GOODS_PATH = (
    "data/input/goods_forecast.csv"
)


# ============================================================
# OUTPUT FILES
# ============================================================

SCHEDULE_OUTPUT_PATH = (
    "data/output/optimized_schedule.csv"
)

WEEKLY_OUTPUT_PATH = (
    "data/output/weekly_plan.csv"
)

EXPLANATION_OUTPUT_PATH = (
    "data/output/decision_explanations.csv"
)


# ============================================================
# LOAD + ENRICH CANDIDATE WINDOWS
# ============================================================

def load_enriched_candidates():

    candidates = pd.read_csv(
        CANDIDATE_PATH
    )

    handoff = pd.read_csv(
        HANDOFF_PATH
    )

    handoff_scores = handoff[
        [
            "task_id",
            "matching_score",
            "optimization_rank"
        ]
    ].drop_duplicates(
        subset=["task_id"]
    )

    candidates = candidates.merge(
        handoff_scores,
        on="task_id",
        how="left"
    )

    candidates[
        "matching_score"
    ] = candidates[
        "matching_score"
    ].fillna(0)

    candidates[
        "optimization_rank"
    ] = candidates[
        "optimization_rank"
    ].fillna(0)

    return candidates


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n" + "=" * 70
    )

    print(
        "       RAILWAY AUTOMATIC BLOCK PLANNING & OPTIMIZATION"
    )

    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # LOAD CANDIDATE WINDOWS
    # --------------------------------------------------------

    print(
        "\n===== LOADING ENRICHED CANDIDATE WINDOWS =====\n"
    )

    candidate_windows = (
        load_enriched_candidates()
    )

    print(
        "Candidate file:",
        CANDIDATE_PATH
    )

    print(
        "Data Engineering handoff:",
        HANDOFF_PATH
    )

    print(
        "Candidate records:",
        len(candidate_windows)
    )

    print(
        "Tasks received:",
        candidate_windows[
            "task_id"
        ].nunique()
    )

    print(
        "\nEnriched Candidate Windows:"
    )

    print(
        candidate_windows[
            [
                "task_id",
                "department",
                "section_id",
                "priority_level",
                "priority_score",
                "maintenance_duration",
                "window_date",
                "window_start",
                "window_end",
                "window_duration",
                "matching_score",
                "optimization_rank"
            ]
        ].to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # LOAD TRAINS
    # --------------------------------------------------------

    print(
        "\n===== LOADING TRAIN DATA ====="
    )

    trains = pd.read_csv(
        TRAIN_PATH
    )

    print(
        "Train file:",
        TRAIN_PATH
    )

    print(
        "Train records:",
        len(trains)
    )

    print(
        trains.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # LOAD GOODS FORECAST
    # --------------------------------------------------------

    print(
        "\n===== LOADING GOODS FORECAST ====="
    )

    goods_forecast = pd.read_csv(
        GOODS_PATH
    )

    print(
        "Goods forecast file:",
        GOODS_PATH
    )

    print(
        "Goods forecast records:",
        len(goods_forecast)
    )

    print(
        goods_forecast.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # RUN OPTIMIZER
    # --------------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "             RUNNING MULTIPLE-WINDOW OPTIMIZER"
    )

    print(
        "=" * 70
    )

    selected, unscheduled = (
        optimize_with_cp_sat(
            candidate_windows,
            trains,
            goods_forecast,
            goods_probability_threshold=0.70
        )
    )

    # --------------------------------------------------------
    # CREATE SCHEDULE DATAFRAME
    # --------------------------------------------------------

    schedule = pd.DataFrame(
        selected
    )

    print(
        "\n===== OPTIMIZED MAINTENANCE SCHEDULE =====\n"
    )

    if schedule.empty:

        print(
            "No tasks were scheduled."
        )

    else:

        print(
            schedule[
                [
                    "task_id",
                    "department",
                    "section_id",
                    "date",
                    "start_time",
                    "end_time",
                    "maintenance_duration",
                    "priority_level",
                    "priority_score",
                    "matching_score",
                    "optimization_rank"
                ]
            ].to_string(
                index=False
            )
        )

        schedule.to_csv(
            SCHEDULE_OUTPUT_PATH,
            index=False
        )

        print(
            "\nOptimized schedule saved to:",
            SCHEDULE_OUTPUT_PATH
        )

    # --------------------------------------------------------
    # UNSCHEDULED TASKS
    # --------------------------------------------------------

    print(
        "\n===== UNSCHEDULED TASKS =====\n"
    )

    if isinstance(unscheduled, pd.DataFrame):

        if unscheduled.empty:

            print(
                "All tasks were scheduled successfully."
            )

        else:

            print(
                unscheduled.to_string(
                    index=False
                )
            )

    elif not unscheduled:

        print(
            "All tasks were scheduled successfully."
        )

    else:

        for task in unscheduled:

            print(
                f"Task: {task['task_id']} | "
                f"Section: {task['section_id']} | "
                f"Reason: {task['reason']}"
            )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    metrics = calculate_metrics(
        schedule,
        candidate_windows
    )

    print_metrics(
        metrics
    )

    # --------------------------------------------------------
    # WEEKLY PLAN
    # --------------------------------------------------------

    weekly_plan = generate_weekly_plan(
        schedule
    )

    print_weekly_plan(
        weekly_plan
    )

    save_weekly_plan(
        weekly_plan
    )

    # --------------------------------------------------------
    # DECISION EXPLANATIONS
    # --------------------------------------------------------

    explanations = explain_decisions(
        schedule,
        unscheduled,
        candidate_windows
    )

    print_decisions(
        explanations
    )

    if not explanations.empty:

        explanations.to_csv(
            EXPLANATION_OUTPUT_PATH,
            index=False
        )

        print(
            "\nDecision explanations saved to:",
            EXPLANATION_OUTPUT_PATH
        )

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "                     FINAL SUMMARY"
    )

    print(
        "=" * 70
    )

    print(
        f"\nTotal tasks received      : "
        f"{metrics['total_tasks']}"
    )

    print(
        f"Tasks scheduled           : "
        f"{metrics['scheduled_tasks']}"
    )

    print(
        f"Tasks not scheduled       : "
        f"{metrics['unscheduled_tasks']}"
    )

    print(
        f"Critical tasks scheduled  : "
        f"{metrics['scheduled_critical_tasks']} / "
        f"{metrics['critical_tasks']}"
    )

    print(
        f"Departments covered       : "
        f"{metrics['departments_covered']}"
    )

    print(
        f"Sections covered          : "
        f"{metrics['sections_covered']}"
    )

    print(
        f"Maintenance time          : "
        f"{metrics['total_maintenance_minutes']} minutes"
    )

    print(
        "\nOptimization completed successfully."
    )

    print(
        "\n" + "=" * 70
    )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()