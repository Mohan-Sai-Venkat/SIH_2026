def generate_explanation(task):
    reasons = []

    severity = task.get("severity_score", 0)
    urgency = task.get("urgency_score", 0)
    train_activity = task.get("train_activity_score", 0)
    high_priority_train = task.get("high_priority_train_score", 0)
    days_to_due = task.get("days_to_due", 0)
    is_overdue = task.get("is_overdue", 0)

    # Severity
    if severity >= 0.75:
        reasons.append("High maintenance severity")

    # Urgency
    if urgency >= 0.75:
        reasons.append("High maintenance urgency")

    # Overdue
    if is_overdue == 1 or days_to_due <= 0:
        reasons.append("Maintenance task is overdue")

    # Train activity
    if train_activity >= 0.75:
        reasons.append("High train activity in the affected section")

    # High-priority trains
    if high_priority_train >= 0.50:
        reasons.append("High-priority train activity may be affected")

    # Maintenance duration
    if task.get("maintenance_duration", 0) >= 3:
        reasons.append("Long maintenance duration")

    # Default explanation
    if not reasons:
        reasons.append("Low maintenance risk factors")

    return reasons