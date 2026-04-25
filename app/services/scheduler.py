import asyncio
from app.state.memory_store import monitors
from app.services.alert_service import AlertService
from time import time

alert_service = AlertService()


async def monitor_loop():
    while True:
        now = time()

        for m_id, monitor in list(monitors.items()):
            if monitor.paused:
                continue

            if now > monitor.expires_at and monitor.status != "down":
                monitor.status = "down"
                alert_service.trigger_alert(m_id)

        await asyncio.sleep(1)