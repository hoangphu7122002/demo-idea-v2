from fastapi import APIRouter, Response
from sqlalchemy import text

from app.api.deps import SessionDep
from app.core.redis import get_redis

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(session: SessionDep, response: Response) -> dict[str, str]:
    checks: dict[str, str] = {}
    try:
        await session.execute(text("select 1"))
        checks["db"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["db"] = f"error: {type(exc).__name__}"
    redis = get_redis()
    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["redis"] = f"error: {type(exc).__name__}"
    finally:
        await redis.aclose()
    if any(v != "ok" for v in checks.values()):
        response.status_code = 503
    return checks
