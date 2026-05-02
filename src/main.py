import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ADD THIS

from src.api.routes import router
from src.config import settings
from src.metrics.tracker import tracker
from src.adaptive_thresholds import adaptive

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}


@app.get("/metrics")
def metrics():
    return tracker.get_stats()


@router.get("/thresholds")
async def get_thresholds():
    return adaptive.get_thresholds()
