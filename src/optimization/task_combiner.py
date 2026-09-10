def can_combine(task1, task2):
    """
    Check whether two maintenance tasks are compatible
    for potential consolidation.
    """

    # Tasks must be at the same section
    if task1["section_id"] != task2["section_id"]:
        return False

    # A task cannot be combined with itself
    if task1["task_id"] == task2["task_id"]:
        return False

    # Tasks must have the same maintenance window
    if task1["window_date"] != task2["window_date"]:
        return False

    if task1["window_start"] != task2["window_start"]:
        return False

    if task1["window_end"] != task2["window_end"]:
        return False

    return True


def find_consolidation_opportunities(handoff):
    """
    Identify tasks that share the same section and
    maintenance window.

    Only tasks whose combined duration fits inside
    the available window are considered feasible.
    """

    opportunities = []

    grouped = handoff.groupby(
        [
            "section_id",
            "window_date",
            "window_start",
            "window_end"
        ]
    )

    for group_key, group in grouped:

        if len(group) < 2:
            continue

        section_id, date, start_time, end_time = group_key

        total_duration = group["maintenance_duration"].sum()
        window_duration = group["window_duration"].iloc[0]

        # Capacity check
        if total_duration > window_duration:
            continue

        opportunities.append({
            "section_id": section_id,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "tasks": group["task_id"].tolist(),
            "departments": group["department"].tolist(),
            "total_duration": total_duration,
            "window_duration": window_duration,
            "unused_minutes_after_consolidation":
                window_duration - total_duration
        })

    return opportunities