from datetime import datetime


class AlertService:

    def trigger_alert(self, monitor_id: str):
        alert = {
            "ALERT": f"Device {monitor_id} is down!",
            "time": datetime.utcnow().isoformat()
        }

        print(alert)  # simulate webhook/email
        return alert