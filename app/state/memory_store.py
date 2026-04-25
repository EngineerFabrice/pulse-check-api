import copy
import threading
from typing import Dict, List, Optional

from app.models.monitor import Monitor


class MonitorStore:
    """
    In-memory monitor store with lock-based protection.
    This is the primary state layer and can be replaced later with Redis.
    """

    def __init__(self):
        self._monitors: Dict[str, Monitor] = {}
        self._lock = threading.RLock()

    def set_monitor(self, monitor: Monitor) -> None:
        with self._lock:
            self._monitors[monitor.id] = monitor

    def get_monitor(self, monitor_id: str) -> Optional[Monitor]:
        with self._lock:
            monitor = self._monitors.get(monitor_id)
            return copy.copy(monitor) if monitor else None

    def update_monitor(self, monitor_id: str, **data) -> Optional[Monitor]:
        with self._lock:
            monitor = self._monitors.get(monitor_id)
            if not monitor:
                return None

            for key, value in data.items():
                if hasattr(monitor, key):
                    setattr(monitor, key, value)

            return copy.copy(monitor)

    def set_status(self, monitor_id: str, status: str) -> Optional[Monitor]:
        return self.update_monitor(monitor_id, status=status)

    def delete_monitor(self, monitor_id: str) -> None:
        with self._lock:
            if monitor_id in self._monitors:
                del self._monitors[monitor_id]

    def exists(self, monitor_id: str) -> bool:
        with self._lock:
            return monitor_id in self._monitors

    def list_monitors(self) -> List[Monitor]:
        with self._lock:
            return [copy.copy(monitor) for monitor in self._monitors.values()]

    def clear(self) -> None:
        with self._lock:
            self._monitors.clear()


monitors = MonitorStore()
