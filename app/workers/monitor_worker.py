import asyncio
from app.services.scheduler import monitor_loop


def start_worker():
    loop = asyncio.get_event_loop()
    loop.create_task(monitor_loop())