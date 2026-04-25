from fastapi import APIRouter
from app.api.routes.monitors import router as monitor_router

router = APIRouter()

router.include_router(monitor_router, prefix="/monitors", tags=["Monitors"])