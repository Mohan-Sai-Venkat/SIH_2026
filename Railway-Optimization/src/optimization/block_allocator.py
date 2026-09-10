from src.util.time_utils import time_to_minutes


def block_can_fit_task(block, task):
    block_start = time_to_minutes(block["start_time"])
    block_end = time_to_minutes(block["end_time"])

    block_duration = block_end - block_start

    return block_duration >= task["duration"]