from app.services.alert_service import AlertService

def test_alert_creation():
    service = AlertService()

    result = service.create_alert(
        monitor_id="123",
        message="Device offline"
    )

    assert result is not None
    assert result["message"] == "Device offline"