from dataclasses import dataclass
from typing import List


@dataclass
class Schedule:
    block_id: str
    location: str
    date: str
    start_time: str
    end_time: str
    task_ids: List[str]
    departments: List[str]
    score: float