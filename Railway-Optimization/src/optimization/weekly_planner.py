import pandas as pd


def generate_weekly_plan(schedule):

    if schedule.empty:
        return pd.DataFrame()

    plan = schedule.copy()

    plan["date"] = pd.to_datetime(
        plan["date"]
    )

    plan["day"] = plan["date"].dt.day_name()

    weekly_plan = (
        plan.groupby(
            [
                "date",
                "day",
                "department"
            ]
        )
        .agg(
            tasks=("task_id", "count"),
            maintenance_minutes=(
                "maintenance_duration",
                "sum"
            ),
            sections=(
                "section_id",
                "nunique"
            )
        )
        .reset_index()
    )

    weekly_plan = weekly_plan.sort_values(
        by=["date", "department"]
    )

    return weekly_plan


def save_weekly_plan(
    weekly_plan
):

    output_path = (
        "data/output/weekly_plan.csv"
    )

    weekly_plan.to_csv(
        output_path,
        index=False
    )

    print(
        f"\nWeekly plan saved to: "
        f"{output_path}"
    )


def print_weekly_plan(
    weekly_plan
):

    print(
        "\n===== WEEKLY MAINTENANCE PLAN =====\n"
    )

    if weekly_plan.empty:
        print("No scheduled tasks.")
        return

    print(
        weekly_plan.to_string(
            index=False
        )
    )