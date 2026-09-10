from dataclasses import dataclass


@dataclass
class MaintenanceTask:
    task_id: str
    department: str
    location: str
    duration: int
    priority: int
    criticality: str
    deadline: str
    block_type: str