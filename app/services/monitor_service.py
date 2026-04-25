from time import time
from app.state.memory_store import monitors
from app.models.monitor import Monitor
from app.services.alert_service import AlertService

alert_service = AlertService()


class MonitorService:

    def create_monitor(self, payload):
        monitor = Monitor(
            id=payload.id,
            timeout=payload.timeout,
            alert_email=payload.alert_email,
            expires_at=time() + payload.timeout
        )

        monitors[payload.id] = monitor
        return {"message": "Monitor created", "id": payload.id}

    def heartbeat(self, monitor_id: str):
        if monitor_id not in monitors:
            return {"error": "Monitor not found"}

        monitor = monitors[monitor_id]

        if monitor.paused:
            monitor.paused = False

        monitor.expires_at = time() + monitor.timeout

        return {"message": "Heartbeat received"}

    def receive_heartbeat(self, monitor_id: str):
        if monitor_id not in monitors:
            return True

        result = self.heartbeat(monitor_id)
        return result.get("message") == "Heartbeat received"

    def pause_monitor(self, monitor_id: str):
        if monitor_id not in monitors:
            return {"error": "Monitor not found"}

        monitors[monitor_id].paused = True
        return {"message": "Monitor paused"}
