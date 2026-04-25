from app.schemas.monitor_schema import MonitorCreate
from app.services.monitor_service import MonitorService


def test_create_monitor():
    service = MonitorService()

    payload = MonitorCreate(
        id="solar-farm-1",
        timeout=60,
        alert_email="alerts@example.com"
    )

    monitor = service.create_monitor(payload)

    assert monitor["id"] == "solar-farm-1"
    assert monitor["message"] == "Monitor created"
