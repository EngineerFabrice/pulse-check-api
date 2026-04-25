import asyncio
import logging
from dataclasses import asdict
from time import time

from app.models.monitor import Monitor
from app.state.memory_store import monitors
from app.services.scheduler import monitor_scheduler

logger = logging.getLogger("pulse_check_api.monitor")


def _get_running_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None


class MonitorService:
    def create_monitor(self, payload):
        if monitors.exists(payload.id):
            logger.warning(
                "Monitor already exists",
                extra={"device_id": payload.id},
            )
            return {"error": "Monitor already exists"}

        monitor = Monitor(
            id=payload.id,
            timeout=payload.timeout,
            alert_email=payload.alert_email,
            expires_at=time() + payload.timeout,
        )

        monitors.set_monitor(monitor)
        logger.info(
            "Monitor created",
            extra={"device_id": payload.id, "timeout": payload.timeout},
        )

        loop = _get_running_loop()
        if loop:
            monitor_scheduler.schedule_monitor(payload.id)

        return {"message": "Monitor created", "id": payload.id}

    def get_monitor(self, monitor_id: str):
        monitor = monitors.get_monitor(monitor_id)
        if not monitor:
            return None
        return asdict(monitor)

    def list_monitors(self):
        return [asdict(monitor) for monitor in monitors.list_monitors()]

    def receive_heartbeat(self, monitor_id: str):
        monitor = monitors.get_monitor(monitor_id)
        if not monitor:
            logger.warning(
                "Heartbeat received for unknown monitor",
                extra={"device_id": monitor_id},
            )
            return True

        if monitor.paused:
            monitors.update_monitor(monitor_id, paused=False, status="active")

        expires_at = time() + monitor.timeout
        monitors.update_monitor(
            monitor_id,
            expires_at=expires_at,
            status="active",
        )

        logger.info(
            "Heartbeat received",
            extra={"device_id": monitor_id, "expires_at": expires_at},
        )

        loop = _get_running_loop()
        if loop:
            monitor_scheduler.schedule_monitor(monitor_id)

        return True

    def heartbeat(self, monitor_id: str):
        if not monitors.exists(monitor_id):
            return {"error": "Monitor not found"}

        self.receive_heartbeat(monitor_id)
        return {"message": "Heartbeat received"}

    def pause_monitor(self, monitor_id: str):
        monitor = monitors.get_monitor(monitor_id)
        if not monitor:
            logger.warning(
                "Pause requested for missing monitor",
                extra={"device_id": monitor_id},
            )
            return {"error": "Monitor not found"}

        monitors.update_monitor(monitor_id, paused=True, status="paused")
        logger.warning(
            "Monitor paused",
            extra={"device_id": monitor_id},
        )

        loop = _get_running_loop()
        if loop:
            monitor_scheduler.cancel_monitor(monitor_id)

        return {"message": "Monitor paused"}
