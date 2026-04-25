from pydantic import BaseModel


class MonitorCreate(BaseModel):
    id: str
    timeout: int
    alert_email: str


class MonitorResponse(BaseModel):
    id: str
    timeout: int
    alert_email: str
    expires_at: float
    status: str
    paused: bool