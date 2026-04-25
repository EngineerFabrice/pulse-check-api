from fastapi.testclient import TestClient

from app.main import app
from app.schemas.monitor_schema import MonitorCreate
from app.services.monitor_service import MonitorService
from app.state.memory_store import monitors

client = TestClient(app)


def test_create_monitor():
    monitors.clear()
    service = MonitorService()

    payload = MonitorCreate(
        id="solar-farm-1",
        timeout=60,
        alert_email="alerts@example.com"
    )

    monitor = service.create_monitor(payload)

    assert monitor["id"] == "solar-farm-1"
    assert monitor["message"] == "Monitor created"


def test_create_monitor_endpoint_returns_201():
    monitors.clear()
    response = client.post(
        "/monitors",
        json={
            "id": "device-api-1",
            "timeout": 60,
            "alert_email": "ops@example.com",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == "device-api-1"


def test_heartbeat_unknown_monitor_returns_404():
    monitors.clear()
    response = client.post("/monitors/unknown-device/heartbeat")

    assert response.status_code == 404
    assert response.json()["detail"] == "Monitor not found"


def test_pause_unknown_monitor_returns_404():
    monitors.clear()
    response = client.post("/monitors/unknown-device/pause")

    assert response.status_code == 404
    assert response.json()["detail"] == "Monitor not found"


def test_get_monitor_status_endpoint():
    monitors.clear()
    payload = MonitorCreate(
        id="device-status-1",
        timeout=45,
        alert_email="ops@example.com"
    )

    MonitorService().create_monitor(payload)

    response = client.get(f"/monitors/{payload.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == payload.id
    assert body["status"] == "active"
    assert body["paused"] is False


def test_list_monitors_endpoint():
    monitors.clear()

    MonitorService().create_monitor(
        MonitorCreate(id="device-list-1", timeout=30, alert_email="ops1@example.com")
    )
    MonitorService().create_monitor(
        MonitorCreate(id="device-list-2", timeout=30, alert_email="ops2@example.com")
    )

    response = client.get("/monitors")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert any(item["id"] == "device-list-1" for item in body)
    assert any(item["id"] == "device-list-2" for item in body)
