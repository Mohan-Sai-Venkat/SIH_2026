from dataclasses import dataclass


@dataclass
class Block:
    block_id: str
    date: str
    start_time: str
    end_time: str
    location: str
    block_type: str