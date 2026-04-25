from app.services.monitor_service import MonitorService

def test_heartbeat_update():
    service = MonitorService()

    result = service.receive_heartbeat("device_1")

    assert result is True