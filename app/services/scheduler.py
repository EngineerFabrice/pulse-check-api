import asyncio
import logging
from time import time

from app.services.alert_service import AlertService
from app.state.memory_store import monitors

logger = logging.getLogger("pulse_check_api.scheduler")
alert_service = AlertService()


def _get_running_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None


class MonitorScheduler:
    def __init__(self):
        self._tasks: dict[str, asyncio.Task] = {}
        self._lock = asyncio.Lock()

    async def _cancel_task(self, monitor_id: str) -> None:
        task = None
        async with self._lock:
            task = self._tasks.pop(monitor_id, None)

        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                logger.info(
                    "Cancelled existing expiration task",
                    extra={"device_id": monitor_id},
                )

    async def _run_expiration(self, monitor_id: str, delay: float) -> None:
        try:
            await asyncio.sleep(delay)

            monitor = monitors.get_monitor(monitor_id)
            if not monitor:
                return

            if monitor.paused or monitor.status == "down":
                return

            if time() < monitor.expires_at:
                return

            monitors.update_monitor(monitor_id, status="down")
            alert_service.trigger_alert(
                monitor_id,
                "timeout",
                monitor.alert_email,
            )
            logger.critical(
                "Monitor expired",
                extra={"device_id": monitor_id, "reason": "timeout"},
            )

        except asyncio.CancelledError:
            logger.info(
                "Expiration task canceled",
                extra={"device_id": monitor_id},
            )

    async def _schedule_task(self, monitor_id: str) -> None:
        await self._cancel_task(monitor_id)

        monitor = monitors.get_monitor(monitor_id)
        if not monitor or monitor.paused:
            return

        delay = max(0.0, monitor.expires_at - time())
        async with self._lock:
            task = asyncio.create_task(self._run_expiration(monitor_id, delay))
            self._tasks[monitor_id] = task

    def schedule_monitor(self, monitor_id: str) -> None:
        loop = _get_running_loop()
        if not loop:
            return

        loop.create_task(self._schedule_task(monitor_id))

    def cancel_monitor(self, monitor_id: str) -> None:
        loop = _get_running_loop()
        if not loop:
            return

        loop.create_task(self._cancel_task(monitor_id))


monitor_scheduler = MonitorScheduler()
