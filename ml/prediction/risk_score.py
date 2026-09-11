def calculate_risk_score(
    severity_score,
    urgency_score,
    train_activity_score,
    days_to_due,
    high_priority_train_score
):
    """
    Calculate maintenance risk using Data Engineering features.
    Returns a score between 0 and 1.
    """

    # Normalize days_to_due.
    # Negative values mean the task is overdue.
    overdue_factor = 1.0 if days_to_due <= 0 else max(
        0.0,
        1.0 - (days_to_due / 30.0)
    )

    # Keep all feature values between 0 and 1
    severity = min(max(severity_score, 0), 1)
    urgency = min(max(urgency_score, 0), 1)
    train_activity = min(max(train_activity_score, 0), 1)
    high_priority_train = min(max(high_priority_train_score, 0), 1)

    # Weighted railway maintenance risk
    risk_score = (
        0.30 * severity
        + 0.25 * urgency
        + 0.20 * train_activity
        + 0.15 * high_priority_train
        + 0.10 * overdue_factor
    )

    return round(min(max(risk_score, 0), 1), 2)