from dataclasses import dataclass


@dataclass
class Train:
    train_id: str
    date: str
    start_time: str
    end_time: str
    location: str
    train_type: str