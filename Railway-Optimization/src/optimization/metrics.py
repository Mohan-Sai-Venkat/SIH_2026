import pandas as pd


def calculate_metrics(schedule, handoff):

    metrics = {}

    # Basic task metrics
    total_tasks = handoff["task_id"].nunique()
    scheduled_tasks = len(schedule)
    unscheduled_tasks = total_tasks - scheduled_tasks

    metrics["total_tasks"] = total_tasks
    metrics["scheduled_tasks"] = scheduled_tasks
    metrics["unscheduled_tasks"] = unscheduled_tasks

    # Maintenance time
    if scheduled_tasks > 0:
        total_maintenance = int(
            schedule["maintenance_duration"].sum()
        )
    else:
        total_maintenance = 0

    metrics["total_maintenance_minutes"] = (
        total_maintenance
    )

    # Critical task metrics
    critical_tasks = handoff[
        handoff["priority_level"]
        .astype(str)
        .str.lower()
        == "critical"
    ]["task_id"].nunique()

    scheduled_critical = schedule[
        schedule["priority_level"]
        .astype(str)
        .str.lower()
        == "critical"
    ]["task_id"].nunique()

    metrics["critical_tasks"] = critical_tasks
    metrics["scheduled_critical_tasks"] = (
        scheduled_critical
    )

    if critical_tasks > 0:
        critical_rate = (
            scheduled_critical
            / critical_tasks
            * 100
        )
    else:
        critical_rate = 0

    metrics["critical_task_schedule_rate"] = (
        round(critical_rate, 2)
    )

    # Department coverage
    if scheduled_tasks > 0:
        departments = schedule[
            "department"
        ].nunique()
    else:
        departments = 0

    metrics["departments_covered"] = departments

    # Section coverage
    if scheduled_tasks > 0:
        sections = schedule[
            "section_id"
        ].nunique()
    else:
        sections = 0

    metrics["sections_covered"] = sections

    return metrics


def print_metrics(metrics):

    print(
        "\n===== OPTIMIZATION METRICS =====\n"
    )

    print(
        f"Total tasks: "
        f"{metrics['total_tasks']}"
    )

    print(
        f"Scheduled tasks: "
        f"{metrics['scheduled_tasks']}"
    )

    print(
        f"Unscheduled tasks: "
        f"{metrics['unscheduled_tasks']}"
    )

    print(
        f"Total maintenance time: "
        f"{metrics['total_maintenance_minutes']} "
        f"minutes"
    )

    print(
        f"Critical tasks: "
        f"{metrics['critical_tasks']}"
    )

    print(
        f"Critical tasks scheduled: "
        f"{metrics['scheduled_critical_tasks']}"
    )

    print(
        f"Critical task schedule rate: "
        f"{metrics['critical_task_schedule_rate']}%"
    )

    print(
        f"Departments covered: "
        f"{metrics['departments_covered']}"
    )

    print(
        f"Sections covered: "
        f"{metrics['sections_covered']}"
    )