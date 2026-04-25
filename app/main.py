from fastapi import FastAPI
from app.api.router import router
from app.core.logger import setup_logger

app = FastAPI(title="Pulse Check API", version="1.0.0")

setup_logger()

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Pulse Check API is running 🚀"}