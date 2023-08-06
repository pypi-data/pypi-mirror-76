from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    method: str

    max_requests: int = None
    max_clients: int = None
    interval: int = 1
