import pandas as pd


def time_to_minutes(time_value):
    """
    Convert HH:MM time into minutes from midnight.
    Example: 10:30 -> 630
    """
    hour, minute = map(int, str(time_value).split(":"))
    return hour * 60 + minute


def overlaps(start1, end1, start2, end2):
    """
    Check whether two time intervals overlap.

    Example:
    10:00-12:00 and 11:00-13:00 -> True
    10:00-12:00 and 12:00-14:00 -> False
    """

    start1 = time_to_minutes(start1)
    end1 = time_to_minutes(end1)

    start2 = time_to_minutes(start2)
    end2 = time_to_minutes(end2)

    return start1 < end2 and start2 < end1


def has_train_conflict(candidate, trains):
    """
    Check whether a maintenance candidate conflicts
    with a scheduled train.

    Matching is done using:
    - date
    - location / section
    - overlapping time
    """

    candidate_date = str(candidate["window_date"])

    # Current maintenance data uses section_id.
    # If a future handoff contains location, use it.
    if "location" in candidate:
        candidate_location = str(candidate["location"])
    else:
        candidate_location = str(candidate["section_id"])

    for _, train in trains.iterrows():

        train_date = str(train["date"])
        train_location = str(train["location"])

        # Different date -> no conflict
        if candidate_date != train_date:
            continue

        # Different location -> no conflict
        if candidate_location != train_location:
            continue

        # Same date + location -> check time overlap
        if overlaps(
            candidate["window_start"],
            candidate["window_end"],
            train["start_time"],
            train["end_time"]
        ):
            return True, train["train_id"]

    return False, None


def has_goods_forecast_conflict(
    candidate,
    goods_forecast,
    probability_threshold=0.70
):
    """
    Check whether a maintenance candidate conflicts
    with a high-probability goods movement forecast.

    probability_threshold is configurable.
    Default prototype value = 0.70.
    """

    candidate_date = str(candidate["window_date"])

    if "location" in candidate:
        candidate_location = str(candidate["location"])
    else:
        candidate_location = str(candidate["section_id"])

    for _, forecast in goods_forecast.iterrows():

        forecast_date = str(forecast["date"])
        forecast_location = str(forecast["location"])
        probability = float(forecast["probability"])

        # Different date -> no conflict
        if candidate_date != forecast_date:
            continue

        # Different location -> no conflict
        if candidate_location != forecast_location:
            continue

        # Low-probability forecast -> don't treat as hard conflict
        if probability < probability_threshold:
            continue

        # Same date + location -> check time overlap
        if overlaps(
            candidate["window_start"],
            candidate["window_end"],
            forecast["start_time"],
            forecast["end_time"]
        ):
            return True, forecast["forecast_id"], probability

    return False, None, None