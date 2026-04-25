from datetime import datetime


class AlertService:

    def create_alert(self, monitor_id: str, message: str):
        alert = {
            "monitor_id": monitor_id,
            "message": message,
            "time": datetime.utcnow().isoformat()
        }

        print(alert)  # simulate webhook/email
        return alert

    def trigger_alert(self, monitor_id: str):
        alert = {
            "ALERT": f"Device {monitor_id} is down!",
            "time": datetime.utcnow().isoformat()
        }

        print(alert)  # simulate webhook/email
        return alert