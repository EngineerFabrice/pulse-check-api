from fastapi import APIRouter
from app.schemas.monitor_schema import MonitorCreate
from app.services.monitor_service import MonitorService

router = APIRouter()
service = MonitorService()


@router.post("")
def create_monitor(payload: MonitorCreate):
    return service.create_monitor(payload)


@router.post("/{monitor_id}/heartbeat")
def heartbeat(monitor_id: str):
    return service.heartbeat(monitor_id)


@router.post("/{monitor_id}/pause")
def pause_monitor(monitor_id: str):
    return service.pause_monitor(monitor_id)
