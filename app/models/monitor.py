from dataclasses import dataclass
from time import time


@dataclass
class Monitor:
    id: str
    timeout: int
    alert_email: str
    expires_at: float
    status: str = "active"
    paused: bool = False
