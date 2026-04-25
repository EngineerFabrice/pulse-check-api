from typing import List

from fastapi import APIRouter, HTTPException, status
from app.schemas.monitor_schema import MonitorCreate, MonitorResponse
from app.services.monitor_service import MonitorService

router = APIRouter()
service = MonitorService()


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_monitor(payload: MonitorCreate):
    result = service.create_monitor(payload)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=result["error"])
    return result


@router.post("/{monitor_id}/heartbeat", response_model=dict)
async def heartbeat(monitor_id: str):
    result = service.heartbeat(monitor_id)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])
    return result


@router.post("/{monitor_id}/pause", response_model=dict)
async def pause_monitor(monitor_id: str):
    result = service.pause_monitor(monitor_id)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])
    return result


@router.get("", response_model=List[MonitorResponse], summary="List all monitors")
async def list_monitors():
    return service.list_monitors()


@router.get("/{monitor_id}", response_model=MonitorResponse, summary="Get monitor status")
async def get_monitor(monitor_id: str):
    monitor = service.get_monitor(monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return monitor
