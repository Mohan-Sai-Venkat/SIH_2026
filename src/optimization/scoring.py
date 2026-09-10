def calculate_deadline_urgency(deadline, window_date):
    """
    Calculate urgency based on how close the maintenance
    window is to the task deadline.

    Higher urgency = deadline is closer.

    Returns a prototype urgency score from 0 to 30.
    """

    if deadline is None or window_date is None:
        return 0

    try:
        deadline_date = str(deadline)
        window_date = str(window_date)

        deadline_obj = __import__("pandas").to_datetime(deadline_date)
        window_obj = __import__("pandas").to_datetime(window_date)

        days_remaining = (deadline_obj - window_obj).days

        if days_remaining <= 0:
            return 30
        elif days_remaining == 1:
            return 25
        elif days_remaining == 2:
            return 20
        elif days_remaining == 3:
            return 15
        elif days_remaining <= 5:
            return 10
        else:
            return 5

    except Exception:
        return 0


def calculate_window_score(
    priority_score,
    priority_level,
    matching_score,
    maintenance_duration,
    window_duration,
    deadline=None,
    window_date=None
):
    """
    Calculate the optimization value of a maintenance window.

    Higher score = better candidate window.

    Factors:
    1. Priority
    2. Criticality
    3. Data Engineering matching score
    4. Block utilization
    5. Unused block time
    6. Deadline urgency
    """

    priority_score = float(priority_score)
    matching_score = float(matching_score)
    maintenance_duration = float(maintenance_duration)
    window_duration = float(window_duration)

    # ----------------------------------------------------------
    # PRIORITY
    # ----------------------------------------------------------

    priority_component = priority_score * 40

    # ----------------------------------------------------------
    # CRITICALITY
    # ----------------------------------------------------------

    priority_level = str(priority_level).lower()

    if priority_level == "critical":
        criticality_component = 40
    elif priority_level == "high":
        criticality_component = 25
    elif priority_level == "medium":
        criticality_component = 15
    else:
        criticality_component = 5

    # ----------------------------------------------------------
    # DATA ENGINEERING MATCHING SCORE
    # ----------------------------------------------------------

    matching_component = matching_score * 0.30

    # ----------------------------------------------------------
    # BLOCK UTILIZATION
    # ----------------------------------------------------------

    if window_duration > 0:
        utilization = (
            maintenance_duration / window_duration
        ) * 100
    else:
        utilization = 0

    utilization_component = utilization * 0.20

    # ----------------------------------------------------------
    # UNUSED TIME PENALTY
    # ----------------------------------------------------------

    unused_time = max(
        window_duration - maintenance_duration,
        0
    )

    unused_time_penalty = unused_time * 0.10

    # ----------------------------------------------------------
    # DEADLINE URGENCY
    # ----------------------------------------------------------

    deadline_urgency = calculate_deadline_urgency(
        deadline,
        window_date
    )

    # ----------------------------------------------------------
    # FINAL SCORE
    # ----------------------------------------------------------

    final_score = (
        priority_component
        + criticality_component
        + matching_component
        + utilization_component
        + deadline_urgency
        - unused_time_penalty
    )

    return round(final_score, 2)


def explain_score(
    priority_score,
    priority_level,
    matching_score,
    maintenance_duration,
    window_duration,
    deadline=None,
    window_date=None
):
    if window_duration > 0:
        utilization = round(
            (maintenance_duration / window_duration) * 100,
            2
        )
    else:
        utilization = 0

    deadline_urgency = calculate_deadline_urgency(
        deadline,
        window_date
    )

    score = calculate_window_score(
        priority_score,
        priority_level,
        matching_score,
        maintenance_duration,
        window_duration,
        deadline,
        window_date
    )

    return {
        "score": score,
        "priority": priority_score,
        "priority_level": priority_level,
        "matching_score": matching_score,
        "block_utilization": utilization,
        "deadline_urgency": deadline_urgency
    }