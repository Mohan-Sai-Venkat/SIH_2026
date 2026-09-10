import pandas as pd


def explain_decisions(schedule, unscheduled, candidate_windows):
    """
    Generate human-readable explanations for optimizer decisions.

    Parameters
    ----------
    schedule : pandas.DataFrame
        Tasks selected by the optimizer.

    unscheduled : pandas.DataFrame
        Tasks that could not be scheduled.

    candidate_windows : pandas.DataFrame
        All candidate maintenance windows.

    Returns
    -------
    pandas.DataFrame
        Decision explanations.
    """

    explanations = []

    # ============================================================
    # SCHEDULED TASKS
    # ============================================================

    if schedule is not None and not schedule.empty:

        for _, task in schedule.iterrows():

            task_id = task.get("task_id", "UNKNOWN")

            priority = task.get("priority_score", 0)
            priority_level = str(
                task.get("priority_level", "")
            )

            matching_score = task.get(
                "matching_score", 0
            )

            utilization = task.get(
                "block_utilization", None
            )

            if pd.isna(utilization):
                utilization = None

            # Convert numeric values safely
            try:
                priority = float(priority)
            except (ValueError, TypeError):
                priority = 0.0

            try:
                matching_score = float(matching_score)
            except (ValueError, TypeError):
                matching_score = 0.0

            # ----------------------------------------------------
            # Explanation based on priority
            # ----------------------------------------------------

            if priority_level.lower() == "critical":

                reason = (
                    f"Scheduled because the task has Critical "
                    f"priority ({priority:.1f}) and a strong "
                    f"matching score ({matching_score:.2f})."
                )

            elif priority_level.lower() == "high":

                reason = (
                    f"Scheduled because the task has High "
                    f"priority ({priority:.1f}) with a suitable "
                    f"maintenance window and matching score "
                    f"({matching_score:.2f})."
                )

            else:

                reason = (
                    "Scheduled because a feasible maintenance "
                    "window was available and selected by the "
                    "optimizer."
                )

            # ----------------------------------------------------
            # Add utilization information
            # ----------------------------------------------------

            if utilization is not None:

                try:
                    reason += (
                        f" Block utilization is "
                        f"{float(utilization):.2f}%."
                    )
                except (ValueError, TypeError):
                    pass

            explanations.append(
                {
                    "task_id": task_id,
                    "decision": "Scheduled",
                    "reason": reason
                }
            )

    # ============================================================
    # UNSCHEDULED TASKS
    # ============================================================

    if unscheduled is not None and not unscheduled.empty:

        for _, task in unscheduled.iterrows():

            task_id = task.get(
                "task_id",
                "UNKNOWN"
            )

            original_reason = str(
                task.get(
                    "reason",
                    "No feasible window available."
                )
            )

            reason_lower = original_reason.lower()

            # ----------------------------------------------------
            # Train conflict
            # ----------------------------------------------------

            if "train conflict" in reason_lower:

                explanation = (
                    "Not scheduled because the available "
                    "maintenance window conflicts with a train "
                    "movement."
                )

                if original_reason:
                    explanation += f" {original_reason}"

            # ----------------------------------------------------
            # Goods forecast conflict
            # ----------------------------------------------------

            elif (
                "goods forecast" in reason_lower
                or "forecast conflict" in reason_lower
            ):

                explanation = (
                    "Not scheduled because the available "
                    "maintenance window conflicts with a "
                    "high-probability goods movement."
                )

                if original_reason:
                    explanation += f" {original_reason}"

            # ----------------------------------------------------
            # Capacity conflict
            # ----------------------------------------------------

            elif "capacity" in reason_lower:

                explanation = (
                    "Not scheduled because the available block "
                    "capacity could not accommodate the "
                    "maintenance requirement."
                )

                if original_reason:
                    explanation += f" {original_reason}"

            # ----------------------------------------------------
            # No feasible window
            # ----------------------------------------------------

            elif (
                "no feasible" in reason_lower
                or "no window" in reason_lower
            ):

                explanation = (
                    "Not scheduled because no feasible "
                    "maintenance window was available."
                )

                if original_reason:
                    explanation += f" {original_reason}"

            # ----------------------------------------------------
            # Other reason
            # ----------------------------------------------------

            else:

                explanation = (
                    f"Not scheduled by the optimizer. "
                    f"Reason: {original_reason}"
                )

            explanations.append(
                {
                    "task_id": task_id,
                    "decision": "Not Scheduled",
                    "reason": explanation
                }
            )

    # ============================================================
    # RETURN RESULT
    # ============================================================

    return pd.DataFrame(
        explanations,
        columns=[
            "task_id",
            "decision",
            "reason"
        ]
    )


def print_decisions(explanations):

    print("\n===== OPTIMIZATION DECISIONS =====")

    if explanations is None or explanations.empty:

        print("No optimization decisions available.")

        return

    for _, row in explanations.iterrows():

        print(
            f"\nTask: {row['task_id']}"
        )

        print(
            f"Decision: {row['decision']}"
        )

        print(
            f"Reason: {row['reason']}"
        )

        print(
            "------------------------------------------------------------"
        )