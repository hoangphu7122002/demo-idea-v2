from fastapi import APIRouter, HTTPException

from app.ai.release_check import CheckUnavailable
from app.api.deps import SessionDep
from app.checks import service
from app.checks.schemas import CheckIn, CheckOut

router = APIRouter(prefix="/api/posts", tags=["checks"])


@router.post(
    "/{slug}/check",
    responses={
        404: {"description": "Post not found"},
        422: {"description": "Unknown release URL, or neither URL nor text given"},
        503: {"description": "Live check failed and no cached result exists"},
    },
)
async def check_post(slug: str, body: CheckIn, session: SessionDep) -> CheckOut:
    try:
        out = await service.run_check(session, slug, body.release_url, body.release_text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except CheckUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if out is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return out


@router.get("/{slug}/flags", responses={404: {"description": "Post not found"}})
async def latest_flags(slug: str, session: SessionDep) -> CheckOut | None:
    """Flags of the latest check, or null if the post was never checked."""
    exists, out = await service.latest_check(session, slug)
    if not exists:
        raise HTTPException(status_code=404, detail="Post not found")
    return out
