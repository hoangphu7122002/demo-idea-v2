from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.db import SyncSessionLocal
from app.core.settings import get_settings
from app.seed import reseed

router = APIRouter(prefix="/api/demo", tags=["demo"])


class ResetOut(BaseModel):
    counts: dict[str, int]


@router.post("/reset")
def reset_demo() -> ResetOut:
    """Reseed demo data. 404 unless DEMO_MODE is on."""
    if not get_settings().demo_mode:
        raise HTTPException(status_code=404, detail="Not Found")
    with SyncSessionLocal() as session:
        return ResetOut(counts=reseed(session))
