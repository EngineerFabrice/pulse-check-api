import json
import logging
from datetime import datetime

logger = logging.getLogger("pulse_check_api.alerts")


class AlertService:
    def create_alert(
        self,
        monitor_id: str,
        message: str,
        reason: str = "timeout",
    ):
        alert = {
            "ALERT": message,
            "time": datetime.utcnow().isoformat() + "Z",
            "device_id": monitor_id,
            "reason": reason,
        }

        logger.critical(json.dumps(alert))
        return {**alert, "message": message}

    def trigger_alert(
        self,
        monitor_id: str,
        reason: str = "timeout",
        alert_email: str | None = None,
    ):
        message = f"Device {monitor_id} is down!"
        return self.create_alert(monitor_id, message, reason)
