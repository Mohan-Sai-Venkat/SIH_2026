def time_to_minutes(time_string):
    hours, minutes = map(int, time_string.split(":"))
    return hours * 60 + minutes


def overlaps(start1, end1, start2, end2):
    return max(start1, start2) < min(end1, end2)